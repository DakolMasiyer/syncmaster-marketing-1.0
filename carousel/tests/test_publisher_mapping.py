import pytest
import figma_publisher as fp

def test_context_beat_keeps_number_and_body():
    beat = {"archetype": "context", "slide": 2, "counter": "02 / 05",
            "eyebrow": "Education · 2/5", "stat_number": "$5,000",
            "body": "The market rate for one sync placement.",
            "fonts": {"stat_number": 320, "body": 60}}
    sec = fp.section_for_archetype("context", "dark")
    ops = fp.build_text_ops_v2(beat, sec, "dark")
    placed = {o["find_by_name"]: o["set_text"] for o in ops}
    assert placed["stat_number"] == "$5,000"      # number kept
    assert "market rate" in placed["body"]         # body kept (was dropped before)

def test_no_field_silently_dropped():
    beat = {"archetype": "proof", "slide": 4, "counter": "04 / 05",
            "eyebrow": "Proof", "headline": "The work, in numbers.",
            "stats": [{"label": "PLACED", "value": "$148k"}], "fonts": {"headline": 176}}
    sec = fp.section_for_archetype("proof", "dark")
    ops = fp.build_text_ops_v2(beat, sec, "dark")
    names = {o["find_by_name"] for o in ops}
    assert "headline" in names
    assert "stat_placed_value" in names

def test_validate_raises_on_unmapped_field():
    beat = {"archetype": "hook", "slide": 1, "counter": "01 / 05",
            "headline": "Hi", "bogus_field": "oops", "fonts": {}}
    sec = fp.section_for_archetype("hook", "dark")
    with pytest.raises(ValueError):
        fp.validate_ops(beat, sec, "dark", strict_fields={"bogus_field"})

def test_font_size_emitted():
    beat = {"archetype": "hook", "slide": 1, "counter": "01 / 05",
            "eyebrow": "Education", "headline": "Placed worldwide.",
            "body": "African composers. Global screens.", "fonts": {"headline": 280, "body": 60}}
    sec = fp.section_for_archetype("hook", "dark")
    ops = fp.build_text_ops_v2(beat, sec, "dark")
    head = next(o for o in ops if o["find_by_name"] == "headline")
    assert head["set_font_size"] == 280


def test_empty_stat_number_blanks_placeholder_dark():
    beat = {"archetype": "context", "slide": 2, "counter": "02 / 05", "eyebrow": "E",
            "stat_number": "", "body": "Just prose, no number.", "fonts": {"body": 60}}
    sec = fp.section_for_archetype("context", "dark")
    ops = fp.build_text_ops_v2(beat, sec, "dark")
    placed = {o["find_by_name"]: o["set_text"] for o in ops}
    assert "stat_number" in placed                  # a blanking op was emitted
    assert placed["stat_number"].strip() == ""      # blanked, not left as template "500"

def test_empty_stat_number_blanks_placeholder_light():
    beat = {"archetype": "context", "slide": 2, "counter": "02 / 05", "eyebrow": "E",
            "stat_number": "", "body": "Just prose.", "fonts": {"body": 60}}
    sec = fp.section_for_archetype("context", "light")
    ops = fp.build_text_ops_v2(beat, sec, "light")
    placed = {o["find_by_name"]: o["set_text"] for o in ops}
    assert placed.get("stat_number", "x").strip() == ""
    assert placed.get("type_overlay", "x").strip() == ""   # ghost digit blanked too

def test_populated_stat_number_not_blanked():
    beat = {"archetype": "context", "slide": 2, "counter": "02 / 05", "eyebrow": "E",
            "stat_number": "$5,000", "body": "Market rate.", "fonts": {"stat_number": 320, "body": 60}}
    sec = fp.section_for_archetype("context", "dark")
    ops = fp.build_text_ops_v2(beat, sec, "dark")
    placed = {o["find_by_name"]: o["set_text"] for o in ops}
    assert placed["stat_number"] == "$5,000"        # real number kept, no blank override

def test_empty_proof_stat_value_not_emitted():
    beat = {"archetype": "proof", "slide": 4, "counter": "04 / 05", "eyebrow": "Proof",
            "headline": "The work.", "stats": [{"label": "PLACED", "value": ""}], "fonts": {}}
    sec = fp.section_for_archetype("proof", "dark")
    ops = fp.build_text_ops_v2(beat, sec, "dark")
    placed = {o["find_by_name"]: o["set_text"] for o in ops}
    assert placed.get("stat_placed_label") == "PLACED"
    assert "stat_placed_value" not in placed        # empty value skipped
