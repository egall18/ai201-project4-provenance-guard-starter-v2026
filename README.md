# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **The request arrives.** A writer sends `POST /submit` with
   `{"text": ..., "creator_id": ...}`. Flask hands the JSON to
   `app.py::submit`.
2. **The route checks it.** Missing, blank, too-short (under 5 words) or
   too-long (over 20,000 characters) text is refused with a `400` and logged
   as a rejection. Anything that passes gets a fresh `content_id` (a uuid).
3. **Signal one — `detector.model_signal`.** GPT-2, running locally, reads the
   first ~400 tokens and measures perplexity: how predictable the words are.
   That becomes `model_score`, 0–1, higher = more AI-like.
4. **Signal two — `stylometry.style_signal`.** Measures the shape of the text
   — sentence-length spread, vocabulary variety, punctuation — and turns it
   into `style_score`, 0–1, higher = more AI-like.
5. **`scoring.combine_signals`** merges the two into one score, returned as
   `confidence`.
6. **`scoring.score_to_label`** compares that score to the thresholds and
   returns a `guess` (`human` / `unsure` / `ai`) and the sentence the reader
   actually sees.
7. **`audit.log_decision`** writes all nine fields to `logs/audit.jsonl` with
   `status: "decided"`, and the response goes back to the writer — including
   the `content_id` they need if they want to appeal.

If the writer disagrees, `POST /appeal` with that `content_id` appends an
appeal to the log and moves the item to `under_review`.

### The false positive I designed around

A writer working in their second language submits a plain paragraph they
wrote themselves — short sentences, common words. I ran one like it through
signal one: perplexity **12.1**, `model_score` **0.890**. The detector's own
AI sample scored **0.886**. Signal one cannot tell them apart.

If their sentences are also fairly even, signal two leans AI too (say 0.7),
and a 50/50 average lands around 0.80 — over the 0.65 line, so they're told
their work looks AI-written. Their only recourse is `/appeal` with their
`content_id`, which moves the item to `under_review` for a person to look at.

What that means for scoring: **one signal at 0.89 should not be enough to
reach "AI" on its own.** That's the case Milestone 4's weights and Milestone
5's thresholds have to handle.

### The two endpoints

**`POST /submit`**

| In | Type | Rule |
|---|---|---|
| `text` | string | required; at least 5 words and at most 20,000 characters after trimming |
| `creator_id` | string | required; not blank |

| Out (`200`) | Type | Meaning |
|---|---|---|
| `content_id` | string | uuid for this submission — needed to appeal |
| `guess` | string | `"human"`, `"unsure"` or `"ai"` |
| `confidence` | float | the combined score: 0.0 = confidently human, 1.0 = confidently AI |
| `label` | string | the sentence shown to the writer |
| `model_score` | float | signal one, 0–1, higher = more AI-like |
| `style_score` | float | signal two, 0–1, higher = more AI-like |
| `status` | string | `"decided"` |

Errors: `400 {"error": "invalid_input", "message": ...}` for bad input;
`503 {"error": "detector_unavailable", ...}` if the model can't load;
`429` once rate limiting is on (unit 8).

**`POST /appeal`**

| In | Type | Rule |
|---|---|---|
| `content_id` | string | required; must match a submission in the log |
| `reasoning` | string | required; not blank |

| Out (`200`) | Type | Meaning |
|---|---|---|
| `content_id` | string | the item appealed |
| `status` | string | `"under_review"` |
| `message` | string | confirmation to the writer |

Errors: `400` for a missing or blank field; `404 {"error": "not_found"}` for
an unknown `content_id`; `409 {"error": "already_under_review"}` if that item
has already been appealed.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model. GPT-2
runs locally and computes perplexity over the first ~400 tokens; low
perplexity means "I could have guessed this". `detector.model_signal` squashes
that onto 0–1, higher = more AI-like.

**Why that might differ between human and AI writing:** A language model
writes by repeatedly picking a likely next word, so its output tends to be
text a model finds easy to predict. Human writing wanders more — odd word
choices, abrupt turns, the specific instead of the typical.

**What it can't see:** Authorship. It measures predictability, and plenty of
people write predictably: someone in their second language sticking to words
they're sure of, a younger writer, anyone writing plainly on purpose. My plain
human test paragraph scored 0.890, against 0.886 for an AI sample. It fails
the other way too — ornate prose full of rare words reads as human (my ornate
sample scored 0.229), so AI text prompted to use unusual vocabulary slips
through. And it only reads the first ~300 words.

### Signal two — the style signal

**What it measures:** The shape of the text without reading it — how much
sentence length varies, how varied the vocabulary is, and how much
punctuation is used.

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

**What it can't see:** Meaning. Anything that changes the shape without
changing the substance moves it: adding typos, chopping sentences up, pasting
in a quotation. That's cheap to do on purpose — my lightly-edited AI sample
(contractions, one short "Honestly?") already has more spread than the human
bike story. It also can't judge very short text: in a single short sentence
no word repeats, so vocabulary variety maxes out and an 8-word sentence scores
0.83, AI-like. I use a 50-word moving average to stop length alone looking
like a signal, but under 50 words there's nothing to average over.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals equally. But an "AI" label needs both
signals to agree: if either one is below 0.5, the score is capped just under
the AI line, so the most it can say is "unsure". One signal on its own can
never accuse anyone. It's one-sided on purpose — disagreement can still end
in a confident "human".

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`,
`AGREEMENT_FLOOR = 0.5`, cap = `AI_THRESHOLD - 0.01` = 0.64. All in
`config.py`.

Inside signal two, each measure is mapped onto 0–1 and the three are averaged:

| Measure | Maps to 0.0 (human) | Maps to 1.0 (AI) |
|---|---|---|
| sentence-length spread (stdev ÷ mean) | 0.65 or more | 0.15 or less |
| type-token ratio (50-word moving average) | 0.75 or less | 0.95 or more |
| punctuation per word (everything but full stops) | 0.02 or less | 0.10 or more |

I picked the direction of each from data, not assumption. Vocabulary variety
came out **backwards** from what I expected: the AI texts scored 0.86–0.92,
the human ones 0.78–0.83. Generated text reaches for varied, formal words;
plain human writers repeat common ones.

**Calibration run** (both signals printed separately, as the brief asks):

| Input | model | style | combined |
|---|---|---|---|
| clearly AI | 0.867 | 0.919 | 0.893 |
| clearly human | 0.394 | 0.258 | 0.326 |
| formal human (Lincoln, 2nd Inaugural) | 0.600 | 0.353 | 0.477 |
| lightly-edited AI | 0.505 | 0.551 | 0.528 |
| plain human | 0.884 | 0.417 | 0.640 (capped) |

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A plain, human-style paragraph about a weekend hike — short sentences, common
words. Signal one scored it **0.884** (very AI-like: it's predictable). Signal
two scored it **0.417** (human-leaning: low punctuation, repeated everyday
words). A plain average gives **0.651**, which is just over the 0.65 AI line —
a false accusation. Under my rule, the style score is below 0.5, so the score
is capped at **0.64** and the writer gets "unsure" instead. The same thing
happens to the second-language paragraph from Milestone 1 (0.890 / 0.356).



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 up to and including 0.35 | We think this was probably written by a person. |
| unsure | above 0.35 and below 0.65 | We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review. |
| high-confidence AI | 0.65 up to 1.00 | This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person most likely to see this label is a plain or second-language writer
who wrote every word — my agreement rule sends them here on purpose instead of
to "AI". So I wrote it for them: no guess about them, no score, nothing they
have to defend, and a way to get a person to look if they want one.

My first version ended "This is not an accusation." Reading it back as the
writer, that line made it sound like one — nobody says that unless they're
thinking it — and it didn't tell them what they could do. I swapped it for the
review option.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence has transformed numerous industries in recent years. It offers significant benefits, including increased efficiency, improved accuracy, and enhanced decision-making capabilities. However, it is important to consider the ethical implications of these technologies. By addressing these challenges, organizations can ensure that AI is used responsibly and effectively.", "creator_id": "erik"}'
```

```json
{
  "confidence": 0.8926,
  "content_id": "1c53a5e0-0b5d-49a8-863c-06a39c5508a3",
  "guess": "ai",
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "model_score": 0.8665,
  "status": "decided",
  "style_score": 0.9187
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "1c53a5e0-0b5d-49a8-863c-06a39c5508a3", "reasoning": "I wrote this myself for my ethics class. I tend to write formally when it is for school."}'
```

```json
{
  "content_id": "1c53a5e0-0b5d-49a8-863c-06a39c5508a3",
  "message": "Thanks — your appeal is in. A person will review this piece.",
  "status": "under_review"
}
```

**What the log shows afterwards**

<!-- limit=6 rather than 3 so the original decision is in view: the run also
     produced a human and an unsure submission, and two refused appeals. -->

```bash
$ curl "http://127.0.0.1:5000/log?limit=6"
```

```json
{
  "count": 6,
  "entries": [
    {
      "combined_score": 0.8926,
      "content_id": "1c53a5e0-0b5d-49a8-863c-06a39c5508a3",
      "creator_id": "erik",
      "guess": "ai",
      "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
      "model_score": 0.8665,
      "status": "decided",
      "style_score": 0.9187,
      "timestamp": "2026-10-29T01:05:58+00:00"
    },
    {
      "combined_score": 0.326,
      "content_id": "a72be3ff-dfcc-4dc8-b01d-45cf2e5cf4b4",
      "creator_id": "erik",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3943,
      "status": "decided",
      "style_score": 0.2578,
      "timestamp": "2026-10-29T01:05:58+00:00"
    },
    {
      "combined_score": 0.64,
      "content_id": "5f934ed6-09a1-4221-872e-81db8f6568c0",
      "creator_id": "erik",
      "guess": "unsure",
      "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
      "model_score": 0.884,
      "status": "decided",
      "style_score": 0.4172,
      "timestamp": "2026-10-29T01:05:58+00:00"
    },
    {
      "content_id": "1c53a5e0-0b5d-49a8-863c-06a39c5508a3",
      "creator_id": "erik",
      "event": "appeal",
      "reasoning": "I wrote this myself for my ethics class. I tend to write formally when it is for school.",
      "status": "under_review",
      "timestamp": "2026-10-29T01:05:58+00:00"
    },
    {
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "appeal_not_found",
      "requested_content_id": "not-a-real-id",
      "status": "rejected",
      "timestamp": "2026-10-29T01:05:58+00:00"
    },
    {
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "appeal_missing_reasoning",
      "status": "rejected",
      "timestamp": "2026-10-29T01:05:58+00:00"
    }
  ]
}
```

The original decision is untouched; the appeal sits after it with
`status: "under_review"`. A second appeal on the same id returned `409`, an
appeal on `not-a-real-id` returned `404`, and one with no reasoning returned
`400` — the last two are the rejection entries at the bottom.

**A bad input, refused and logged**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "too short here", "creator_id": "eval_short"}'
```

```json
{"error": "invalid_input", "message": "text needs at least 5 words to judge.", "reason": "text_too_short"}
```

```json
{"creator_id": "eval_short", "event": "rejected", "reason": "text_too_short", "status": "rejected", "timestamp": "2026-10-29T00:48:39+00:00"}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
