# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. At most 2 of 10 pieces I wrote myself are labelled high-confidence AI

I submit 10 pieces of my own writing. At most 2 come back with
`guess: "ai"`. An `unsure` label does not count against this — only the
high-confidence AI label does. This must hold in all three trials.

**Why this target:** On a writing site, wrongly calling someone's real work AI
costs them far more than letting some AI text through. My first number was 3
of 10, but that meant almost a third of honest writers accused, which I
couldn't defend after reading what one of them would write to me.

---

## 2. Every bad input gets a 400 and a log entry — none crash the service

Five malformed submissions: `text` missing, `text` blank (`""` or only
spaces), `text` under 5 words, `text` over 20,000 characters, and `text` that
isn't a string (`null`). All 5 of 5 return `400` with an `error` and a
`message`, none return `500`, and each one adds an entry with
`status: "rejected"` to the audit log. This must hold in all three trials.

**Why this target:** A 500 tells a real writer the site is broken instead of
telling them what to fix. And a rejected request that leaves no log entry
hides anyone probing the system with weird inputs — I'd never see it in
unit 8. Both the writer and I need to see what happened.

---

## 3. Every appeal is recorded, and appeals on unknown IDs are refused

10 appeals on real `content_id`s: all 10 of 10 return `200` with
`status: "under_review"`, and each adds an `appeal` entry to the audit log
for that `content_id`. 3 appeals on made-up `content_id`s: all 3 of 3 return
`404` and add no appeal entry. This must hold in all three trials.

**Why this target:** The appeal is the only thing a wrongly flagged writer can
do, so it has to work every single time — one silent failure leaves that
person with no recourse at all. And a mistyped ID has to fail loudly, or the
writer thinks they appealed when nothing happened.

---

## 4. Clearly-AI text scores at least 0.30 higher than clearly-human text

Five texts I'm confident are AI-generated and five I'm confident are
human-written. The average `confidence` of the AI five minus the average of
the human five is at least 0.30. This must hold in all three trials.

**Why this target:** If clearly-AI and clearly-human text score close
together, my signals aren't telling them apart and the labels are basically
guesses. 0.30 is also the width of my unsure band (0.35–0.65), so a smaller
gap means clear cases could both land in "unsure".

---

## 5. Every submission after the first answers within 3 seconds

After one warm-up submission (which loads the model — about 20 seconds on my
laptop), every `/submit` in the run returns within 3 seconds, measured from
request sent to response received. This must hold in all three trials.

**Why this target:** The model runs on my laptop's CPU, so timing moves with
text length and whatever else the machine is doing. I measured about 0.7 s
per submission at the longest text the model reads, and 3 seconds leaves room
for that variance while still being short enough that a writer won't give up
waiting. A model being reloaded on every request would take 20+ seconds and
miss this immediately.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 9 — capstone criteria

Written for the unit 9 extension — the English-word gate on `/submit`
(shape B) — **before** any unit 9 results exist. Criteria 1–3 are about the
extension; criterion 1 is the bad path. Every target has to hold in all
three trials.

An "English word" here means what `app.py::english_words` counts: a run of
the letters A–Z, with an apostrophe allowed inside (*didn't* is one word).

---

## 1. Every unreadable submission is refused, never labelled

I send 10 submissions that each contain fewer than 5 English words:
punctuation only, emoji only, Arabic, Chinese, Russian, Hindi, numbers only,
control characters, a 4-word English sentence, and English mixed with Arabic
where only 4 of the words are English. All **10 of 10** return `400` with
reason `too_few_english_words`, none comes back with a `guess` or `label`,
and each leaves a `rejected` entry with that reason in `logs/audit.jsonl`.

**Why this target:** One unreadable input getting a label is exactly the
unit 8 failure this extension exists to fix — MF04 called a line of
punctuation "written by a person". Allowing one miss in ten would allow the
bug I'm fixing.

---

## 2. No real English writing is refused by the gate

26 real English texts: all 13 pieces I wrote (the 10 from unit 8 and the 3 I
didn't use), 5 more short sentences I write for this test that sit right at
the line — 5 to 7 English words each — and the 8 human-written texts from
the unit 8 attack set (FP01–FP08, the shortest of which is 8 words).
**0 of 26** are refused — every one returns `200` with a label.

**Why this target:** The gate is new, so it's a new way to hurt a real
writer — refusing their honest writing instead of scoring it. Short, plain
writing like mine is the most at risk of being cut off by a word count,
which is why my own pieces are the core of the test set — and why five of
them sit just above the five-word line, where a miscount would show.

---

## 3. A refusal is answered without running the model

Every refusal from criterion 1's run — 10 per trial — has a `duration_ms`
**under 10** in its log entry.

**Why this target:** The fastest scored request I measured took 66 ms, so
anything under 10 ms means the refusal happened before the model ran. It is
also about 20 times the 0.5 ms I measured for a refusal in Milestone 3, so
ordinary laptop noise won't fail it — something actually doing work before
the gate would.

---

## 4. Every submission and appeal leaves exactly one record

A mixed run of **30 POST requests to `/submit` or `/appeal`** covering every
path — scored submissions, refusals, appeals, rate-limited submissions
(`429`) and one crash forced in signal one — produces exactly **30** new
lines in `logs/audit.jsonl`, one per request, and every one has
`timestamp`, `route`, `duration_ms`, and either the input fields (`input_chars`, `input_english_words`, `input_sha256`) or
`input_type`.

`GET` routes (`/ping`, `/health`, `/log`) don't write records and aren't
counted.

**Why this target:** A request that leaves no record is one I can never
diagnose — an attack that shows up only as an absence looks like a quiet
afternoon. Every kind of request has to be in the run, including the crash,
which left nothing at all before this unit.

---

## 5. A typical submission costs under 0.35 CPU-seconds

After one warm-up submission, my 10 pieces from unit 8 are submitted one at
a time. The mean `cpu_ms` of those 10 decisions, read from the log, is
**under 350**.

**Why this target:** I measured a mean of 0.27 CPU-seconds in Milestone 3,
with the gate and the new logging already in place. 0.35 is about 1.3 times
that — tight enough that any real added cost, like the model being reloaded
or logging that re-reads the whole file, would miss it, and loose enough to
absorb ordinary variation on a laptop.
