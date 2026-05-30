from generators.fitter import fit, FitResult

BODY = {"layer": "body", "kind": "text", "max_lines": 2, "max_chars": 110, "font_max": 60, "font_min": 48}
HEAD = {"layer": "headline", "kind": "text", "max_lines": 2, "max_chars": 30, "font_max": 220, "font_min": 140}

def test_short_text_fits_at_max_font():
    r = fit("Open briefs every Tuesday.", HEAD)
    assert r.fits is True
    assert r.font_size == 220
    assert r.warning is None

def test_overflow_steps_font_down_but_keeps_words():
    long = "x" * 130  # 130 chars, budget 110
    r = fit(long, BODY)
    assert r.text == long                 # words never cut
    assert r.font_size < 60               # shrunk
    assert r.font_size >= 48              # not below floor

def test_unfittable_warns_at_floor():
    huge = "y" * 400
    r = fit(huge, BODY)
    assert r.font_size == 48              # pinned at floor
    assert r.fits is False
    assert "exceeds" in r.warning.lower()

def test_whitespace_is_normalized():
    r = fit("  hello   world  ", HEAD)
    assert r.text == "hello world"
