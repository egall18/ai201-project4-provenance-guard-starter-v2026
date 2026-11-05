"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

from pathlib import Path

_HERE = Path(__file__).parent


def _my_writing() -> list[str]:
    """
    Criterion 1's inputs: my own writing, one piece per file in my_writing/.
    An empty file comes back as a placeholder so validate() refuses to run it.
    """
    pieces = []
    for path in sorted((_HERE / "my_writing").glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        pieces.append(text or f"REPLACE ME — {path.name} is empty")
    return pieces


# Clearly AI: written by Claude (claude-opus-5-5) on request, in its ordinary
# style, for criterion 4. Not edited.
CLEARLY_AI = [
    "Regular exercise offers numerous benefits for both physical and mental health. It strengthens the cardiovascular system, improves muscle tone, and helps maintain a healthy weight. In addition, physical activity releases endorphins, which can reduce stress and improve overall mood. By incorporating even a small amount of exercise into their daily routine, individuals can significantly enhance their quality of life and reduce the risk of chronic disease.",
    "Remote work has fundamentally changed the way many organizations operate. While it offers employees greater flexibility and eliminates long commutes, it also presents unique challenges, such as maintaining clear communication and fostering a strong team culture. To succeed in a remote environment, companies should invest in reliable collaboration tools, establish clear expectations, and prioritize regular check-ins to ensure that every team member feels connected and supported.",
    "Reading is one of the most valuable habits a person can develop. It expands vocabulary, improves concentration, and exposes readers to new ideas and perspectives. Furthermore, reading fiction has been shown to increase empathy by allowing readers to experience the world through the eyes of different characters. Whether through books, articles, or essays, making time to read each day can lead to lasting personal and intellectual growth.",
    "Climate change is one of the most pressing challenges facing the world today. Rising global temperatures contribute to more frequent extreme weather events, rising sea levels, and disruptions to ecosystems. Addressing this issue requires a combination of individual action and large-scale policy changes, including a transition to renewable energy sources. By working together, governments, businesses, and communities can help build a more sustainable future for generations to come.",
    "Effective communication is essential in both personal and professional settings. It involves not only expressing ideas clearly but also listening actively and responding thoughtfully. Strong communication skills can help prevent misunderstandings, build trust, and strengthen relationships. Additionally, being aware of nonverbal cues, such as body language and tone of voice, can further improve how messages are received. Ultimately, investing in communication skills benefits every area of life.",
]

# Clearly human: public-domain prose, copied verbatim from Project Gutenberg
# (mid-book passages, not the famous openings). Famous books, so gpt2 may
# have seen them in training — if they read as AI, that's a finding.
CLEARLY_HUMAN = [
    # Mark Twain, The Adventures of Tom Sawyer (Gutenberg #74)
    "At school the children made so much of him and of Joe, and delivered such eloquent admiration from their eyes, that the two heroes were not long in becoming insufferably “stuck-up.” They began to tell their adventures to hungry listeners—but they only began; it was not a thing likely to have an end, with imaginations like theirs to furnish material. And finally, when they got out their pipes and went serenely puffing around, the very summit of glory was reached.",
    # Jane Austen, Pride and Prejudice (Gutenberg #1342)
    "At length the chaise arrived, the trunks were fastened on, the parcels placed within, and it was pronounced to be ready. After an affectionate parting between the friends, Elizabeth was attended to the carriage by Mr. Collins; and as they walked down the garden, he was commissioning her with his best respects to all her family, not forgetting his thanks for the kindness he had received at Longbourn in the winter, and his compliments to Mr. and Mrs. Gardiner, though unknown. He then handed her in, Maria followed, and the door was on the point of being closed, when he suddenly reminded them, with some consternation, that they had hitherto forgotten to leave any message for the ladies of Rosings.",
    # Herman Melville, Moby Dick (Gutenberg #2701)
    "In the first place, you are struck by the general contrast between these heads. Both are massive enough in all conscience; but there is a certain mathematical symmetry in the Sperm Whale’s which the Right Whale’s sadly lacks. There is more character in the Sperm Whale’s head. As you behold it, you involuntarily yield the immense superiority to him, in point of pervading dignity. In the present instance, too, this dignity is heightened by the pepper and salt colour of his head at the summit, giving token of advanced age and large experience. In short, he is what the fishermen technically call a “grey-headed whale.”",
    # Charles Dickens, A Tale of Two Cities (Gutenberg #98)
    "Through gloomy vaults where the light of day had never shone, past hideous doors of dark dens and cages, down cavernous flights of steps, and again up steep rugged ascents of stone and brick, more like dry waterfalls than staircases, Defarge, the turnkey, and Jacques Three, linked hand and arm, went with all the speed they could make. Here and there, especially at first, the inundation started on them and swept by; but when they had done descending, and were winding and climbing up a tower, they were alone. Hemmed in here by the massive thickness of walls and arches, the storm within the fortress and without was only audible to them in a dull, subdued way, as if the noise out of which they had come had almost destroyed their sense of hearing.",
    # Jack London, The Call of the Wild (Gutenberg #215)
    "And through it all Buck staggered along at the head of the team as in a nightmare. He pulled when he could; when he could no longer pull, he fell down and remained down till blows from whip or club drove him to his feet again. All the stiffness and gloss had gone out of his beautiful furry coat. The hair hung down, limp and draggled, or matted with dried blood where Hal’s club had bruised him. His muscles had wasted away to knotty strings, and the flesh pads had disappeared, so that each rib and every bone in his frame were outlined cleanly through the loose hide that was wrinkled in folds of emptiness. It was heartbreaking, only Buck’s heart was unbreakable. The man in the red sweater had proved that.",
]


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Pass: at most 2 of 10 come back guess "ai", in every trial.
        "texts": _my_writing(),
    },
    {
        "name": "bad input",
        "criterion": 2,
        # Pass: 5 of 5 return 400, none 500, each leaves a "rejected" log entry.
        "bodies": [
            {"creator_id": "eval_bad_missing"},                    # no text field
            {"text": "   ", "creator_id": "eval_bad_blank"},       # only spaces
            {"text": "too short here", "creator_id": "eval_bad_short"},
            {"text": "word " * 4001, "creator_id": "eval_bad_huge"},  # 20,005 chars
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },
    {
        "name": "appeal path",
        "criterion": 3,
        # Pass: 10 of 10 real appeals -> 200, under_review, logged once;
        #       3 of 3 fake ids -> 404, no appeal entry.
        "appeals": {
            "texts": CLEARLY_AI + CLEARLY_HUMAN,
            "fake_ids": ["not-a-real-id", "00000000-0000-0000-0000-000000000000",
                         "83a28f49-2177-4e07-9739-0b151e4301e2"],  # one char off a real id
        },
    },
    {
        "name": "clearly AI",
        "criterion": 4,
        # Pass (with "clearly human"): mean confidence here minus mean there >= 0.30.
        "texts": CLEARLY_AI,
    },
    {
        "name": "clearly human",
        "criterion": 4,
        "texts": CLEARLY_HUMAN,
    },
    {
        "name": "speed",
        "criterion": 5,
        # Pass: every submission returns within 3 s (after the warm-up). Lengths
        # from minimum to just under the 20,000-character cap.
        "texts": [
            "The bus was late again today.",
            CLEARLY_AI[0],
            " ".join(CLEARLY_HUMAN),
            " ".join(CLEARLY_HUMAN * 6),
            " ".join(CLEARLY_HUMAN * 6 + CLEARLY_AI * 3)[:19_900],
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        # Added: an appeal scenario carries its own texts and fake ids.
        appeals = scenario.get("appeals")
        if appeals:
            if not appeals.get("texts") or not appeals.get("fake_ids"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}') needs appeals.texts "
                    f"and appeals.fake_ids"
                )
            continue

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
