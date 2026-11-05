#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeals"):
                results = run_appeal_trial(requests, args, scenario["appeals"], trial)
                trials.append(results)
                print(f"  trial {trial}: "
                      f"{', '.join(str(r.get('appeal_status')) for r in results)}")
                continue

            results = []
            for i, body in enumerate(bodies_for(scenario), 1):
                preview = describe(body)
                try:
                    response = requests.post(f"{args.url}/submit", json=body,
                                             timeout=args.timeout)
                    payload = response.json() if response.content else {}
                    results.append({
                        "status": response.status_code,
                        "guess": payload.get("guess"),
                        "confidence": payload.get("confidence"),
                        "model_score": payload.get("model_score"),
                        "style_score": payload.get("style_score"),
                        "label": payload.get("label"),
                        "seconds": round(response.elapsed.total_seconds(), 3),
                        "logged": latest_log_entry(requests, args),
                        "sent": preview,
                    })
                except Exception as exc:  # noqa: BLE001
                    results.append({"status": None, "error": f"{type(exc).__name__}: {exc}",
                                    "sent": preview})

            trials.append(results)
            guesses = [r.get("guess") or str(r.get("status")) for r in results]
            print(f"  trial {trial}: {', '.join(guesses)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def latest_log_entry(requests, args):
    """
    The newest audit entry, cut down to what a criterion checks — whether this
    request left a trace, and what kind. Added for criterion 2 ("each one adds
    a rejected entry"), which the response alone can't show.
    """
    entries = requests.get(f"{args.url}/log?limit=1", timeout=args.timeout).json()["entries"]
    if not entries:
        return None
    e = entries[0]
    return {k: e.get(k) for k in ("creator_id", "status", "reason", "content_id") if e.get(k)}


def run_appeal_trial(requests, args, spec, trial):
    """
    One trial of the appeal criterion. Added — run_eval only sent text before.

    Submits each of spec["texts"] under a creator_id unique to this trial (so
    trials don't collide with each other's appeals), appeals it, and checks
    the log for the appeal entry. Then appeals each of spec["fake_ids"] and
    checks no appeal entry was written for it.
    """
    results = []
    for i, text in enumerate(spec["texts"], 1):
        creator = f"eval_appeal_t{trial}_{i}"
        try:
            sub = requests.post(f"{args.url}/submit", timeout=args.timeout,
                                json={"text": text, "creator_id": creator})
            content_id = sub.json().get("content_id")
            ap = requests.post(f"{args.url}/appeal", timeout=args.timeout,
                               json={"content_id": content_id,
                                     "reasoning": "I wrote this myself."})
            log = requests.get(f"{args.url}/log", timeout=args.timeout).json()["entries"]
            appeal_entries = [e for e in log
                              if e.get("content_id") == content_id and e.get("event") == "appeal"]
            results.append({
                "kind": "real",
                "content_id": content_id,
                "submit_status": sub.status_code,
                "appeal_status": ap.status_code,
                "status_returned": ap.json().get("status"),
                "appeal_logged": len(appeal_entries) == 1,
            })
        except Exception as exc:  # noqa: BLE001
            results.append({"kind": "real", "appeal_status": None,
                            "error": f"{type(exc).__name__}: {exc}"})

    for fake in spec["fake_ids"]:
        try:
            ap = requests.post(f"{args.url}/appeal", timeout=args.timeout,
                               json={"content_id": fake, "reasoning": "typo test"})
            log = requests.get(f"{args.url}/log", timeout=args.timeout).json()["entries"]
            results.append({
                "kind": "fake",
                "content_id": fake,
                "appeal_status": ap.status_code,
                "appeal_logged": any(e.get("content_id") == fake and e.get("event") == "appeal"
                                     for e in log),
            })
        except Exception as exc:  # noqa: BLE001
            results.append({"kind": "fake", "appeal_status": None,
                            "error": f"{type(exc).__name__}: {exc}"})
    return results


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
