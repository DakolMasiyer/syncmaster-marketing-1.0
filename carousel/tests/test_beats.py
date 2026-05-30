from generators.beats import build

POST = {"pillar": "Education", "persona": "Tunde", "topic": "Sync pay"}

def test_always_starts_hook_ends_cta():
    body = "A composer earned more from one placement.\n\nThe market is real.\n\nApply now."
    beats = build(POST, body)
    assert beats[0]["archetype"] == "hook"
    assert beats[-1]["archetype"] == "cta"

def test_never_exceeds_seven_slides():
    body = "\n\n".join(f"Paragraph number {i} with some real content here." for i in range(15))
    beats = build(POST, body)
    assert len(beats) <= 7

def test_number_paragraph_becomes_context_with_stat():
    body = "Hook line here.\n\n$5,000 per sync placement is the market rate today.\n\nApply."
    beats = build(POST, body)
    contexts = [b for b in beats if b["archetype"] == "context" and b.get("stat_number")]
    assert any(b["stat_number"].startswith("$5") for b in contexts)

def test_stat_grid_paragraph_becomes_proof():
    body = ("Hook.\n\nPLACED: $148k\nROSTER: 42\nTURNAROUND: 37h\n\nApply.")
    beats = build(POST, body)
    proof = [b for b in beats if b["archetype"] == "proof"]
    assert proof and len(proof[0]["stats"]) >= 2

def test_every_beat_has_archetype_and_eyebrow():
    beats = build(POST, "Hook.\n\nBody one.\n\nBody two.")
    for b in beats:
        assert b["archetype"] in {"hook", "context", "showcase", "proof", "cta"}
        assert b.get("eyebrow")
