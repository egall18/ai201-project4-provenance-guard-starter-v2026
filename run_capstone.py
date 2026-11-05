#!/usr/bin/env python3
"""
Run the five unit 9 capstone criteria (criteria.md, "Unit 9") three times.

    gunicorn app:app --bind 127.0.0.1:5000 --workers 1 --timeout 120   # one terminal
    python run_capstone.py --label before                               # another

Like run_eval.py, this does the sending and the recording and reports the
number each criterion asks for. The verdict is mine to write.

Criterion 4 needs one crash. The running service has no crash switch — I
didn't add a test hook to production code — so that one request goes through
Flask's test client in this process, with signal one made to raise. It writes
to the same logs/audit.jsonl as everything else.

Writes results/capstone_<date>_<label>.md.
"""

import argparse
import csv
import datetime as dt
import json
import statistics
import sys
from pathlib import Path

import config

ROOT = Path(__file__).parent
URL = f"http://{config.HOST}:{config.PORT}"


# ── Inputs ───────────────────────────────────────────────────────────────────

# Criterion 1: fewer than 5 English words each, in the order criteria.md names them.
UNREADABLE = {
    "punctuation": "!!! ??? ... ,,, ;;; --- ((( )))",
    "emoji": "🙂🙃😀😃😄 😁😆😅😂🤣 🙂🙃😀😃😄 😁😆😅😂🤣 🙂🙃",
    "arabic": "هذا نص باللغة العربية لاختبار كيفية تعامل النظام مع النصوص",
    "chinese": "这是一段用中文写的文字，用来测试系统如何处理非拉丁字母的文本。",
    "russian": "Это текст на русском языке, чтобы проверить, как система обрабатывает кириллицу.",
    "hindi": "यह हिंदी में लिखा गया एक वाक्य है जो सिस्टम की जाँच करता है।",
    "numbers": "12 345 6789 10 11 12 13 14 15 16",
    "control": "\x00\x01\x02 \x03\x04 \x05\x06 \x07\x08 \x0e\x0f \x10\x11",
    "four_english_words": "I like long walks.",
    "english_plus_arabic": "My favorite word is هذا نص باللغة العربية جميل جدا",
}


def my_pieces():
    """My ten unit 8 pieces, exactly as typed."""
    return [p.read_text(encoding="utf-8").strip()
            for p in sorted((ROOT / "my_writing").glob("*.txt"))]


def real_english():
    """Criterion 2: my 13 pieces, my 5 short sentences, and FP01–FP08."""
    texts = {f"mine_{i:02d}": t for i, t in enumerate(my_pieces(), 1)}
    for p in sorted((ROOT / "my_writing" / "unit9").glob("*.txt")):
        texts[p.stem] = p.read_text(encoding="utf-8").strip()
    with open(ROOT / "attack_set" / "attacks.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["family"] == "false_positive":
                texts[row["id"]] = row["text"]
    return texts


# ── Helpers ──────────────────────────────────────────────────────────────────

def log_lines():
    path = config.AUDIT_LOG
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def entry_for(log, creator_id):
    return next((json.loads(l) for l in reversed(log)
                 if json.loads(l).get("creator_id") == creator_id), None)


def submit(requests, text, creator):
    r = requests.post(f"{URL}/submit", json={"text": text, "creator_id": creator}, timeout=120)
    return r.status_code, r.json()


# ── The five criteria ────────────────────────────────────────────────────────

def criteria_1_and_3(requests, trial):
    """10 unreadable inputs: status, reason, no label, logged — and how long."""
    rows = []
    for name, text in UNREADABLE.items():
        creator = f"cap_t{trial}_c1_{name}"
        status, body = submit(requests, text, creator)
        logged = entry_for(log_lines(), creator) or {}
        rows.append({
            "input": name,
            "status": status,
            "reason": body.get("reason"),
            "got_label": "label" in body or "guess" in body,
            "logged_reason": logged.get("reason"),
            "duration_ms": logged.get("duration_ms"),
        })
    refused = sum(r["status"] == 400 and r["reason"] == "too_few_english_words"
                  and not r["got_label"] and r["logged_reason"] == "too_few_english_words"
                  for r in rows)
    fast = sum((r["duration_ms"] or 1e9) < 10 for r in rows)
    return ({"refused": refused, "of": len(rows), "rows": rows},
            {"under_10ms": fast, "of": len(rows),
             "max_ms": max(r["duration_ms"] or 0 for r in rows),
             "durations_ms": [r["duration_ms"] for r in rows]})


def criterion_2(requests, trial):
    """Real English writing: none refused."""
    rows = []
    for name, text in real_english().items():
        status, body = submit(requests, text, f"cap_t{trial}_c2_{name}")
        rows.append({"input": name, "words": len(text.split()), "status": status,
                     "guess": body.get("guess"), "reason": body.get("reason")})
    refused = sum(r["status"] != 200 for r in rows)
    return {"refused": refused, "of": len(rows), "rows": rows}


def criterion_4(requests, trial):
    """30 POSTs across every path → exactly 30 new log lines, all with the fields."""
    import app as service
    import detector

    before = len(log_lines())
    sent = []
    content_ids = []
    for i in range(6):
        status, body = submit(requests, my_pieces()[i], f"cap_t{trial}_c4_scored_{i}")
        sent.append(("scored", status)); content_ids.append(body.get("content_id"))
    for i in range(9):
        status, _ = submit(requests, "I went for a long walk by the river today.",
                           f"cap_t{trial}_c4_flood")
        sent.append(("flood", status))
    for name in list(UNREADABLE)[:8]:
        status, _ = submit(requests, UNREADABLE[name], f"cap_t{trial}_c4_refused_{name}")
        sent.append(("refused", status))
    for cid in content_ids[:5]:
        r = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": "I wrote this."}, timeout=30)
        sent.append(("appeal", r.status_code))
    r = requests.post(f"{URL}/appeal", json={"content_id": f"not-a-real-id-{trial}", "reasoning": "typo"}, timeout=30)
    sent.append(("appeal_fake", r.status_code))

    real = detector.model_signal
    detector.model_signal = lambda text: (_ for _ in ()).throw(RuntimeError("forced crash for criterion 4"))
    try:
        with service.app.test_client() as client:
            r = client.post("/submit", json={"text": "This request is forced to crash in signal one.",
                                             "creator_id": f"cap_t{trial}_c4_crash"})
            sent.append(("crash", r.status_code))
    finally:
        detector.model_signal = real

    new = [json.loads(l) for l in log_lines()[before:]]
    has_fields = [all(k in e for k in ("timestamp", "route", "duration_ms"))
                  and (("input_sha256" in e and "input_chars" in e and "input_english_words" in e)
                       or "input_type" in e)
                  for e in new]
    return {"requests": len(sent), "new_log_lines": len(new), "with_all_fields": sum(has_fields),
            "statuses": [f"{kind}:{status}" for kind, status in sent],
            "sample_entries": new[:2] + new[-2:]}


def criterion_5(requests, trial):
    """Mean cpu_ms of my 10 pieces, after a warm-up."""
    submit(requests, "This is a warm-up request before measuring cost.", f"cap_t{trial}_c5_warmup")
    cpu = []
    for i, text in enumerate(my_pieces(), 1):
        creator = f"cap_t{trial}_c5_{i:02d}"
        submit(requests, text, creator)
        cpu.append(entry_for(log_lines(), creator)["cpu_ms"])
    return {"mean_cpu_ms": round(statistics.mean(cpu), 1), "max_cpu_ms": max(cpu), "cpu_ms": cpu}


# ── Run and report ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", default="")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    import requests
    try:
        requests.get(f"{URL}/health", timeout=5)
    except Exception:  # noqa: BLE001
        sys.exit(f"Nothing answering at {URL}. Start it with the command in RUNNING.md.")

    if len(real_english()) != 26:
        sys.exit(f"Criterion 2 needs 26 texts; found {len(real_english())}. "
                 f"Are my_writing/unit9/ files in place?")

    trials = []
    for t in range(1, args.trials + 1):
        c1, c3 = criteria_1_and_3(requests, t)
        c2 = criterion_2(requests, t)
        c4 = criterion_4(requests, t)
        c5 = criterion_5(requests, t)
        trials.append({"1": c1, "2": c2, "3": c3, "4": c4, "5": c5})
        print(f"trial {t}: C1 {c1['refused']}/{c1['of']} refused | C2 {c2['refused']}/{c2['of']} refused | "
              f"C3 {c3['under_10ms']}/{c3['of']} under 10 ms (max {c3['max_ms']}) | "
              f"C4 {c4['new_log_lines']} lines for {c4['requests']} requests, {c4['with_all_fields']} complete | "
              f"C5 mean {c5['mean_cpu_ms']} cpu_ms")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"capstone_{stamp}{'_' + args.label if args.label else ''}.md"
    lines = [f"# Capstone run{' — ' + args.label if args.label else ''}", "",
             "- Produced by: `run_capstone.py::main` against `app.py::submit` / `app.py::appeal`",
             f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for n in "12345":
        lines += [f"## Criterion {n}", ""]
        for t, trial in enumerate(trials, 1):
            lines += [f"**Trial {t}**", "", "```json", json.dumps(trial[n], indent=2, ensure_ascii=False), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
