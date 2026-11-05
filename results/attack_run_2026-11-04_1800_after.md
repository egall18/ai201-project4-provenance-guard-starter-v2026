# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 18:00
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `52273bfb-4e88-4450-8581-20ddfeb40750` | unsure | 0.434 || BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b28c2536-a133-4460-9f91-28e7555d1cf9` | unsure | 0.445 || BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `7a2aac44-28bd-43f0-b297-7aa215afeaae` | ai | 0.660 || HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `0d30e30f-aa6b-4af9-b6ab-57dfd71607cc` | ai | 0.654 || HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d04be4cb-6a64-45de-96e7-88991414bc4f` | human | 0.337 || BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c94550bc-5884-4438-85ea-2041baf629d2` | unsure | 0.395 || BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `9ddc774e-438f-4d92-97ab-f54c838cad77` | ai | 0.623 || HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `5cf00cf3-3c49-4f81-8e93-b79f27442d10` | unsure | 0.412 || BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `0ad4d12d-8df6-4247-b149-14d5537c25d2` | ai | 0.618 || HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `1271feac-a05c-431c-91bb-fb64fe7d3c13` | unsure | 0.575 || BROKE |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `150d3d71-e839-46a7-9a44-de1b3eeebc62` | unsure | 0.420 || HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `e85c3392-49e8-41f4-88dd-3f493aa1fae8` | unsure | 0.522 || HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `80e7f063-802f-4216-8d2f-922743ece68d` | unsure | 0.568 || HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `da469010-37f7-4c83-8ea0-0e0fd580f12a` | unsure | 0.570 || HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `25ed1099-0297-460f-91a9-db7ccda54db3` | unsure | 0.542 || HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `6a846475-62c0-4cc0-ae3f-d69b62b99b9f` | unsure | 0.489 || HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b67d1fe0-56b0-4a07-91f3-6ecd4d561b83` | unsure | 0.470 || HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `a446507b-91d6-47af-a89e-c35d2405c605` | unsure | 0.400 || HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `b39f92f5-2fc9-474a-bca5-2caec6518b50` | unsure | 0.384 || BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f694c67b-0b85-4138-a8ad-75d992c2692f` | human | 0.320 || BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ef923144-ae75-426a-a889-a26263a73503` | ai | 0.616 || HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b71f3017-c3a1-49d0-9a61-b795174adbdf` | unsure | 0.548 || HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `e4b94958-61f9-4091-9a4a-8125c7936a48` | ai | 0.713 || HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `bfeddb3f-1920-4032-96b9-5cacc2e84782` | unsure | 0.400 || HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — || HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — || HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — || HELD |
| MF04 | malformed | text is only punctuation | 200 | `ef071565-3f79-46cc-a7af-1bc08f2e1849` | human | 0.172 || BROKE |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — || HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — || HELD |
| MF07 | malformed | text is right-to-left script | 200 | `b2955932-f8ef-46d1-91ec-021d90d75208` | unsure | 0.536 || BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — || HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — || HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — || HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — || HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — || HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — || HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — || HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — || HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — || HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — || HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — || HELD — 429 again (address limit, same as before); route unchanged since the 400 re-send |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — || HELD — 429 again (same cause); route unchanged since the 400 re-send |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — || HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2d35c998-bd25-4727-9982-3d378cfd92e4` | human | 0.264 || HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `812ee3df-2f58-49f1-bf75-d942477bc90b` | human | 0.264 || HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `24e78c82-897f-4084-be0a-e6c53559ba15` | human | 0.264 || HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d1f1f14a-6be5-4c77-879c-43fae883adcf` | human | 0.264 || HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `65b06bdd-3ff4-453e-a336-b1ef36e74f1b` | human | 0.264 || HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "52273bfb-4e88-4450-8581-20ddfeb40750",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4345,
  "model_score": 0.1635,
  "style_score": 0.7056,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "b28c2536-a133-4460-9f91-28e7555d1cf9",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4445,
  "model_score": 0.5943,
  "style_score": 0.2947,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "7a2aac44-28bd-43f0-b297-7aa215afeaae",
  "creator_id": "attacker_EV03",
  "guess": "ai",
  "confidence": 0.6602,
  "model_score": 0.6662,
  "style_score": 0.6542,
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "0d30e30f-aa6b-4af9-b6ab-57dfd71607cc",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6542,
  "model_score": 0.6114,
  "style_score": 0.6969,
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "d04be4cb-6a64-45de-96e7-88991414bc4f",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3372,
  "model_score": 0.3212,
  "style_score": 0.3532,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c94550bc-5884-4438-85ea-2041baf629d2",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.395,
  "model_score": 0.5727,
  "style_score": 0.2172,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "9ddc774e-438f-4d92-97ab-f54c838cad77",
  "creator_id": "attacker_EV07",
  "guess": "ai",
  "confidence": 0.6226,
  "model_score": 0.5862,
  "style_score": 0.659,
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "5cf00cf3-3c49-4f81-8e93-b79f27442d10",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4116,
  "model_score": 0.2452,
  "style_score": 0.5781,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "0ad4d12d-8df6-4247-b149-14d5537c25d2",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.6182,
  "model_score": 0.7042,
  "style_score": 0.5323,
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "1271feac-a05c-431c-91bb-fb64fe7d3c13",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.5749,
  "model_score": 0.9792,
  "style_score": 0.1707,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "150d3d71-e839-46a7-9a44-de1b3eeebc62",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4199,
  "model_score": 0.6175,
  "style_score": 0.2222,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "e85c3392-49e8-41f4-88dd-3f493aa1fae8",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5222,
  "model_score": 0.7387,
  "style_score": 0.3058,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "80e7f063-802f-4216-8d2f-922743ece68d",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5676,
  "model_score": 0.8051,
  "style_score": 0.3302,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "da469010-37f7-4c83-8ea0-0e0fd580f12a",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5701,
  "model_score": 0.8329,
  "style_score": 0.3074,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "25ed1099-0297-460f-91a9-db7ccda54db3",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.5425,
  "model_score": 0.8005,
  "style_score": 0.2846,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "6a846475-62c0-4cc0-ae3f-d69b62b99b9f",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.4893,
  "model_score": 0.8814,
  "style_score": 0.0972,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "b67d1fe0-56b0-4a07-91f3-6ecd4d561b83",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4698,
  "model_score": 0.8816,
  "style_score": 0.0579,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "a446507b-91d6-47af-a89e-c35d2405c605",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4002,
  "model_score": 0.3223,
  "style_score": 0.478,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "b39f92f5-2fc9-474a-bca5-2caec6518b50",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.384,
  "model_score": 0.4625,
  "style_score": 0.3055,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "f694c67b-0b85-4138-a8ad-75d992c2692f",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3197,
  "model_score": 0.2044,
  "style_score": 0.435,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "ef923144-ae75-426a-a889-a26263a73503",
  "creator_id": "attacker_PI03",
  "guess": "ai",
  "confidence": 0.6158,
  "model_score": 0.5943,
  "style_score": 0.6372,
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "b71f3017-c3a1-49d0-9a61-b795174adbdf",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5476,
  "model_score": 0.4998,
  "style_score": 0.5955,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "e4b94958-61f9-4091-9a4a-8125c7936a48",
  "creator_id": "attacker_PI05",
  "guess": "ai",
  "confidence": 0.7129,
  "model_score": 0.6401,
  "style_score": 0.7857,
  "label": "This looks like it was likely written with AI. Our checks can be wrong. If you wrote this yourself, you can ask a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "bfeddb3f-1920-4032-96b9-5cacc2e84782",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.3995,
  "model_score": 0.5583,
  "style_score": 0.2406,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "ef071565-3f79-46cc-a7af-1bc08f2e1849",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.1722,
  "model_score": 0.0112,
  "style_score": 0.3333,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "b2955932-f8ef-46d1-91ec-021d90d75208",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.5365,
  "model_score": 0.9064,
  "style_score": 0.1667,
  "label": "We couldn't tell whether this was written by a person or with AI help, so we're not making a call either way. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "2d35c998-bd25-4727-9982-3d378cfd92e4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "812ee3df-2f58-49f1-bf75-d942477bc90b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "24e78c82-897f-4084-be0a-e6c53559ba15",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "d1f1f14a-6be5-4c77-879c-43fae883adcf",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "65b06bdd-3ff4-453e-a336-b1ef36e74f1b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
