"""Phase 2 tests: hook trimming, eyebrow truncation, overflow distribution, parse_stats fixes."""
from generators.beats import build, _parse_stats, _trim_hook, _eyebrow, _is_droppable, _compact_num

POST = {"pillar": "Education", "persona": "Tunde", "topic": "Sync pay"}
POST_LONG_TOPIC = {"pillar": "Education", "persona": "Tunde",
                   "topic": "What sync placements actually pay and how to get in"}


# ── Eyebrow ───────────────────────────────────────────────────────────────────

def test_eyebrow_hook_short_fits():
    assert len(_eyebrow(POST, "hook", 1, 7)) <= 48


def test_eyebrow_hook_long_topic_truncated():
    result = _eyebrow(POST_LONG_TOPIC, "hook", 1, 7)
    assert len(result) <= 48


def test_eyebrow_middle_always_fits():
    # Middle eyebrow is "Pillar · N/T" — never long
    result = _eyebrow(POST_LONG_TOPIC, "context", 3, 7)
    assert len(result) <= 48


# ── Hook headline trimming ────────────────────────────────────────────────────

def test_trim_hook_short_unchanged():
    short = "One doc. More money."
    assert _trim_hook(short) == short


def test_trim_hook_multiline_takes_first_line():
    text = "Nobody explained this in music school.\nAnd it's worth more than anything they did teach you. ↓"
    result = _trim_hook(text)
    assert "\n" not in result
    assert len(result) <= 57
    assert "Nobody explained" in result


def test_trim_hook_long_single_line_truncates():
    text = "A South African composer just earned more from one Showmax documentary than from 6 months of streaming royalties."
    result = _trim_hook(text)
    assert len(result) <= 57


def test_trim_hook_finds_clause_boundary():
    # 64 chars total — over budget. Should clip at ". " before hitting the limit.
    text = "This is not exceptional. This is the real market rate today."
    assert len(text) > 57
    result = _trim_hook(text)
    assert len(result) <= 57
    assert result == "This is not exceptional."


def test_trim_hook_never_empty():
    result = _trim_hook("x" * 100)
    assert len(result) > 0


# ── Droppable paragraph filtering ────────────────────────────────────────────

def test_hashtag_para_is_droppable():
    assert _is_droppable("#SyncLicensing #AfricanComposers #MusicBusiness #FilmMusic #SyncMaster")


def test_regular_para_not_droppable():
    assert not _is_droppable("The market exists. The demand is real.")


def test_filler_save_this_is_droppable():
    assert _is_droppable("Save this. Share it with a composer who needs to know.")


def test_mixed_content_not_droppable():
    assert not _is_droppable("Sync licensing = your music in film, TV, ads & games.")


# ── Overflow distribution ─────────────────────────────────────────────────────

def test_no_single_context_body_exceeds_budget():
    """After build(), every context beat body must be ≤165 chars (budget at font_max)."""
    # Simulate a post with 10 meaty paragraphs
    long_body = "\n\n".join([
        "Hook line — the short punchy opener.",
        "Sync licensing = your music in film, TV, ads & games.",
        "One Netflix scene: $5,000–$20,000. One global ad campaign: $10,000–$75,000. Upfront. Not per stream.",
        "Here's the full breakdown — swipe through all slides:",
        "→ What sync licensing actually is → Who's involved and what they each do → What placements actually pay with real numbers → The two licences in every single deal → What music supervisors actually look for",
        "This is the foundation. Everything else builds on it.",
        "The market exists. The demand is real. What's missing is the infrastructure.",
        "Composers: you already have the talent. You need the access.",
        "Supervisors: 48h turnaround, rights-cleared, brief-matched.",
        "#SyncLicensing #AfricanComposers #MusicBusiness",
        "Save this. Share it with a composer who needs to know.",
    ])
    beats = build(POST, long_body)
    for b in beats:
        if b["archetype"] == "context":
            body = b.get("body", "")
            assert len(body) <= 165, (
                f"slide {b['slide']} context.body is {len(body)} chars (budget 165): {body!r}"
            )


def test_build_filters_hashtag_paragraphs():
    """Hashtag paragraphs must not appear as beat bodies."""
    body = "Hook.\n\nReal content here.\n\n#Hash #Tags #Everywhere\n\nMore content."
    beats = build(POST, body)
    for b in beats:
        body_text = b.get("body", "") + b.get("headline", "")
        assert "#" not in body_text or not body_text.startswith("#"), (
            f"Hashtag content leaked into beat body: {body_text!r}"
        )


def test_build_filters_save_this_paragraphs():
    """'Save this.' filler paragraphs must not become body content."""
    body = "Hook.\n\nReal content.\n\nSave this. Share it with a composer who needs to know."
    beats = build(POST, body)
    for b in beats:
        body_text = b.get("body", "")
        assert "Save this" not in body_text


# ── Parse stats ────────────────────────────────────────────────────────────────

def test_parse_stats_strips_arrow_prefix():
    para = "→ UPFRONT SYNC FEE: $5,000\n→ PUBLISHER SHARE: $2,000"
    stats = _parse_stats(para)
    assert stats
    for st in stats:
        assert not st["label"].startswith("→")


def test_parse_stats_extracts_first_number_not_range():
    para = "UPFRONT SYNC: $800–$1,200\nPUBLISHER SHARE: $2,000–$8,000"
    stats = _parse_stats(para)
    assert stats
    for st in stats:
        assert "–" not in st["value"], f"Range leaked into value: {st['value']!r}"
        assert len(st["value"]) <= 6


def test_parse_stats_label_max_11_chars():
    para = "VERY LONG LABEL NAME HERE: $5,000\nANOTHER LONG LABEL: $2,000"
    stats = _parse_stats(para)
    for st in stats:
        assert len(st["label"]) <= 11


def test_parse_stats_returns_up_to_three():
    para = "A: $1,000\nB: $2,000\nC: $3,000\nD: $4,000"
    stats = _parse_stats(para)
    assert len(stats) <= 3


# ── Number compaction ─────────────────────────────────────────────────────────

def test_compact_num_short_unchanged():
    assert _compact_num("$5,000") == "$5,000"   # 6 chars — fits as-is


def test_compact_num_large_converts_to_k():
    assert _compact_num("$10,000") == "$10k"    # 7 chars → 4 chars


def test_compact_num_millions():
    assert _compact_num("$1,500,000") == "$1.5m"


def test_compact_num_max_chars_respected():
    result = _compact_num("$10,000,000", max_chars=6)
    assert len(result) <= 6


def test_parse_stats_no_truncated_values():
    """Proof stats must not produce garbled values like '$10,00'."""
    para = (
        "ONE NETFLIX SCENE: $10,000–$20,000\n"
        "GLOBAL AD CAMPAIGN: $75,000\n"
        "STREAMING MONTH: $0.003"
    )
    stats = _parse_stats(para)
    for st in stats:
        assert not st["value"].endswith(","), f"Truncated value: {st['value']!r}"
        assert len(st["value"]) <= 6
