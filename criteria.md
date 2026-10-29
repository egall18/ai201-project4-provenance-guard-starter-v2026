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
