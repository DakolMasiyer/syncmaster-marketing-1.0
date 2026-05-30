# Carousel & Single Text-Placement Fix — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the batch content pipeline place the right copy in the right slot, in the right amount, by constraining the generator to the template's real archetypes, budgeting every text box from measured Figma geometry, and validating that no copy is ever silently dropped.

**Architecture:** The Figma carousel template is a fixed 5-beat story (HOOK → CONTEXT → SHOWCASE → PROOF → CTA), non-autolayout, with absolutely-positioned text boxes at fixed font sizes. The current generator emits 8–10 free-form text slides that don't map to those beats, so a stringly-typed mapping layer silently drops mismatches. We (1) encode each slot's measured budget as data, (2) rewrite the carousel generator to emit exactly the template's beats (5, stretch to 7) with one idea per beat, (3) add a pure `fitter` that font-shrinks within bounds and warns at the floor, (4) fix the publisher's role→section→layer mapping to real layer names with a fail-loud validator, and (5) make the single generator template-aware. IG-trendy copy rewriting (LLM/copywriting) is layered in Phase 2; singles in Phase 3.

**Tech Stack:** Python 3, python-pptx (existing), figma-mcp-go (Claude-driven render), pytest (new dev dep). No new runtime network deps. Unsplash stays disabled (`ENABLE_UNSPLASH = False`).

**Source-of-truth note:** All budgets in this plan were measured live from the Figma file "SyncMaster Design System & Brand Guidelines", page "Templates", on 2026-05-30. Dark template `196:2855` and light `144:63` are structurally identical, so one carousel budget table covers both.

---

## File Structure

- `carousel/slot_budgets.json` — **NEW.** Data: per archetype, per slot → `{layer, kind, max_lines, max_chars, font_max, font_min}`. Single source of truth for budgets. No magic numbers in code.
- `carousel/generators/beats.py` — **NEW.** Pure. Converts raw body copy → an ordered list of beat dicts matching the template's available sections (hook, context, showcase, proof, cta). Caps at the 7-slide stretch limit. One idea per beat.
- `carousel/generators/fitter.py` — **NEW.** Pure. `fit(text, budget) -> FitResult{text, font_size, fits, warning}`. Deterministic: normalize whitespace → measure lines/chars → step font down within `[font_min, font_max]` → if still over at floor, set `fits=False` + warning. Does **not** rewrite words (that's Phase 2).
- `carousel/generators/carousel_copy.py` — **MODIFY.** Replace `_build_slides` internals to call `beats.build()` then `fitter.fit()` per slot; emit `font_size` per text field.
- `carousel/generators/single_copy.py` — **MODIFY (Phase 3).** Produce fields for the *selected* single template's slot set; fit each.
- `carousel/figma_publisher.py` — **MODIFY.** Fix `section_for_role` (stat→context, not proof), fix layer-name maps to real Figma names, compute counters after final slide count, emit `font_size` in text_ops, add `validate_ops()` that raises if a beat field has no destination layer.
- `carousel/tests/` — **NEW.** `test_fitter.py`, `test_beats.py`, `test_publisher_mapping.py`.
- `carousel/requirements-dev.txt` — **NEW.** `pytest>=8.0`.

---

### Task 0: Test harness setup

**Files:**
- Create: `carousel/requirements-dev.txt`
- Create: `carousel/tests/__init__.py`
- Create: `carousel/conftest.py`

- [ ] **Step 1: Add dev deps**

Create `carousel/requirements-dev.txt`:
```
pytest>=8.0
```

- [ ] **Step 2: Make tests a package and put carousel/ on sys.path**

Create `carousel/tests/__init__.py` (empty file).

Create `carousel/conftest.py`:
```python
import sys
from pathlib import Path

# Allow `from generators...` and `import figma_publisher` from tests.
sys.path.insert(0, str(Path(__file__).resolve().parent))
```

- [ ] **Step 3: Install and verify**

Run: `cd carousel && pip install -r requirements-dev.txt && python -m pytest --version`
Expected: prints a pytest version, exit 0.

- [ ] **Step 4: Commit**

```bash
git add carousel/requirements-dev.txt carousel/tests/__init__.py carousel/conftest.py
git commit -m "test: add pytest harness for carousel pipeline"
```

---

### Task 1: Encode measured slot budgets as data

**Files:**
- Create: `carousel/slot_budgets.json`
- Test: `carousel/tests/test_budgets.py`

- [ ] **Step 1: Write the failing test**

Create `carousel/tests/test_budgets.py`:
```python
import json
from pathlib import Path

BUDGETS = json.loads((Path(__file__).resolve().parent.parent / "slot_budgets.json").read_text())

def test_carousel_archetypes_present():
    arch = BUDGETS["carousel"]
    assert set(arch) >= {"hook", "context", "showcase", "proof", "cta"}

def test_every_slot_has_required_keys():
    required = {"layer", "kind", "max_lines", "max_chars", "font_max", "font_min"}
    for archetype, slots in BUDGETS["carousel"].items():
        for slot_name, spec in slots.items():
            assert required <= set(spec), f"{archetype}.{slot_name} missing {required - set(spec)}"
            assert spec["font_min"] <= spec["font_max"]
            assert spec["kind"] in ("text", "number")

def test_hook_headline_budget_matches_measurement():
    h = BUDGETS["carousel"]["hook"]["headline"]
    assert h["layer"] == "headline"
    assert h["font_max"] == 320
    assert h["max_lines"] == 3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd carousel && python -m pytest tests/test_budgets.py -v`
Expected: FAIL — `slot_budgets.json` does not exist (FileNotFoundError at import).

- [ ] **Step 3: Create the budgets file (measured 2026-05-30)**

Create `carousel/slot_budgets.json`:
```json
{
  "_meta": {
    "measured_from": "SyncMaster Design System & Brand Guidelines / Templates",
    "measured_on": "2026-05-30",
    "note": "Dark (196:2855) and light (144:63) carousels are structurally identical; budgets apply to both. char/line limits derived from placeholder copy that fits the box at font_max."
  },
  "carousel": {
    "hook": {
      "eyebrow":  { "layer": "top_eyebrow",   "kind": "text",   "max_lines": 1, "max_chars": 48,  "font_max": 44,  "font_min": 44 },
      "headline": { "layer": "headline",       "kind": "text",   "max_lines": 3, "max_chars": 36,  "font_max": 320, "font_min": 200 },
      "body":     { "layer": "body",           "kind": "text",   "max_lines": 2, "max_chars": 110, "font_max": 60,  "font_min": 48 }
    },
    "context": {
      "eyebrow":     { "layer": "section_eyebrow", "kind": "text",   "max_lines": 1, "max_chars": 40,  "font_max": 44,  "font_min": 44 },
      "stat_number": { "layer": "stat_number",     "kind": "number", "max_lines": 1, "max_chars": 6,   "font_max": 320, "font_min": 180 },
      "body":        { "layer": "body",            "kind": "text",   "max_lines": 3, "max_chars": 165, "font_max": 60,  "font_min": 48 }
    },
    "showcase": {
      "eyebrow":     { "layer": "section_eyebrow", "kind": "text",   "max_lines": 1, "max_chars": 40,  "font_max": 44,  "font_min": 44 },
      "stat_number": { "layer": "stat_number",     "kind": "number", "max_lines": 1, "max_chars": 6,   "font_max": 320, "font_min": 180 },
      "body":        { "layer": "body",            "kind": "text",   "max_lines": 3, "max_chars": 165, "font_max": 60,  "font_min": 48 }
    },
    "proof": {
      "eyebrow":  { "layer": "section_eyebrow", "kind": "text",   "max_lines": 1, "max_chars": 40, "font_max": 44,  "font_min": 44 },
      "headline": { "layer": "headline",        "kind": "text",   "max_lines": 1, "max_chars": 24, "font_max": 176, "font_min": 120 },
      "stat_label": { "layer": "stat_*_label",  "kind": "text",   "max_lines": 1, "max_chars": 11, "font_max": 28,  "font_min": 28 },
      "stat_value": { "layer": "stat_*_value",  "kind": "number", "max_lines": 1, "max_chars": 6,  "font_max": 176, "font_min": 120 }
    },
    "cta": {
      "eyebrow":  { "layer": "section_eyebrow", "kind": "text", "max_lines": 1, "max_chars": 40,  "font_max": 44,  "font_min": 44 },
      "headline": { "layer": "headline",        "kind": "text", "max_lines": 2, "max_chars": 30,  "font_max": 220, "font_min": 140 },
      "body":     { "layer": "body",            "kind": "text", "max_lines": 2, "max_chars": 115, "font_max": 60,  "font_min": 48 },
      "cta_text": { "layer": "cta_text",        "kind": "text", "max_lines": 1, "max_chars": 14,  "font_max": 64,  "font_min": 52 }
    }
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd carousel && python -m pytest tests/test_budgets.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add carousel/slot_budgets.json carousel/tests/test_budgets.py
git commit -m "feat: encode measured Figma slot budgets as data"
```

---

### Task 2: Pure text fitter (font-shrink within bounds, warn at floor)

**Files:**
- Create: `carousel/generators/fitter.py`
- Test: `carousel/tests/test_fitter.py`

- [ ] **Step 1: Write the failing test**

Create `carousel/tests/test_fitter.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd carousel && python -m pytest tests/test_fitter.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'generators.fitter'`.

- [ ] **Step 3: Implement the fitter**

Create `carousel/generators/fitter.py`:
```python
"""
Pure text fitter for SyncMaster slots.

Given a string and a slot budget (from slot_budgets.json), decide the largest
font size in [font_min, font_max] at which the text fits the box's char/line
budget. Never cuts words — if it cannot fit even at font_min, it pins to
font_min and reports fits=False with a warning for manual review.

The char budget is measured at font_max. When the font shrinks, proportionally
more characters fit, so the effective char allowance scales by (font_max/font).
"""
from dataclasses import dataclass
import re


@dataclass
class FitResult:
    text: str
    font_size: int
    fits: bool
    warning: str | None = None


def _normalize(text: str) -> str:
    # Collapse runs of spaces/tabs but preserve intentional newlines.
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines).strip()


def _capacity(budget: dict, font: int) -> int:
    """Effective TOTAL character capacity at a given font size.

    `max_chars` is the total budget across all lines, measured at font_max.
    A smaller font fits proportionally more characters, so capacity scales by
    (font_max / font). `max_lines` is informational here (not multiplied in).
    """
    return int(budget["max_chars"] * budget["font_max"] / font)


def fit(text: str, budget: dict) -> FitResult:
    text = _normalize(text)
    length = len(text.replace("\n", ""))

    font_max, font_min = budget["font_max"], budget["font_min"]
    # Try sizes from max down to min in 4px steps.
    for font in range(font_max, font_min - 1, -4):
        if length <= _capacity(budget, font):
            return FitResult(text=text, font_size=font, fits=True, warning=None)

    cap = _capacity(budget, font_min)
    return FitResult(
        text=text,
        font_size=font_min,
        fits=False,
        warning=f"copy ({length} chars) exceeds slot budget ({cap} at {font_min}px) — needs a rewrite",
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd carousel && python -m pytest tests/test_fitter.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add carousel/generators/fitter.py carousel/tests/test_fitter.py
git commit -m "feat: add pure text fitter with font-shrink and floor warning"
```

---

### Task 3: Beat builder — constrain copy to the template's archetypes

**Files:**
- Create: `carousel/generators/beats.py`
- Test: `carousel/tests/test_beats.py`

**Design:** A deck is always `hook` + middle beats + `cta`. Middle beats are chosen from the source paragraphs, each classified into exactly one archetype:
- paragraph with a leading short number/currency + unit → `context` (number hero + body)
- paragraph with ≥2 stat lines → `proof` (grid)
- everything else → `context` with `stat_number` omitted (body-only context)
- `showcase` is reserved for product slides (Phase 3); not emitted from text.

Cap middle beats so total ≤ 7 (IG-trendy). Excess paragraphs are merged into the nearest kept beat's body. This replaces the old free-form `body`/`list` roles entirely.

- [ ] **Step 1: Write the failing test**

Create `carousel/tests/test_beats.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd carousel && python -m pytest tests/test_beats.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'generators.beats'`.

- [ ] **Step 3: Implement the beat builder**

Create `carousel/generators/beats.py`:
```python
"""
Beat builder — maps raw body copy onto the carousel template's fixed archetypes.

The template supports exactly these section archetypes:
  hook | context | showcase | proof | cta
A deck is always hook + (<=5 middle beats) + cta, total <= 7 slides (IG-trendy).
Each middle source paragraph is classified into exactly one archetype; excess
paragraphs beyond the cap are folded into the previous beat's body so no copy
is lost.
"""
import re

MAX_SLIDES = 7
FOOTER_NAME = "syncmaster.live"

_RE_STAT_LINE = re.compile(r"[\$€£]\s?[\d,]+|\b\d+%|\b\d+\s?(?:h|hrs|hours|days|k|m)\b", re.I)
_RE_LEAD_NUM = re.compile(r"^\s*([\$€£]?\d[\d,\.]*[kKmM%+]?)")  # \s* not [\s\W]* — \W would eat the leading $


def _eyebrow(post, archetype, idx, total):
    pillar = post.get("pillar", "SyncMaster")
    if archetype == "hook":
        topic = post.get("topic", "")
        return f"{pillar} · {topic}" if topic else pillar
    if archetype == "cta":
        return "Apply this week"
    return f"{pillar} · {idx}/{total}"


def _parse_stats(paragraph):
    stats = []
    for line in paragraph.splitlines():
        line = line.strip()
        if not _RE_STAT_LINE.search(line):
            continue
        m = re.match(r"(.+?)\s*[:\-—–]\s*(.+)", line)
        if m:
            stats.append({"label": m.group(1).strip().upper()[:11], "value": m.group(2).strip()[:6]})
    return stats[:3]


def _classify(paragraph):
    stat_lines = [l for l in paragraph.splitlines() if _RE_STAT_LINE.search(l)]
    if len(stat_lines) >= 2:
        return "proof"
    return "context"


def build(post, body):
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [""]

    beats = []
    # ── Hook ──────────────────────────────────────────────────────────────
    hook_para = paragraphs[0]
    beats.append({
        "archetype": "hook",
        "headline": hook_para,
        "body": "",
        "footer_name": FOOTER_NAME,
    })

    # ── Middle beats ──────────────────────────────────────────────────────
    middles = []
    for para in paragraphs[1:]:
        archetype = _classify(para)
        if archetype == "proof":
            middles.append({"archetype": "proof", "headline": "The work, in numbers.",
                            "stats": _parse_stats(para), "footer_name": FOOTER_NAME})
        else:
            lead = _RE_LEAD_NUM.match(para)
            stat_number = lead.group(1) if lead and len(lead.group(1)) <= 6 else ""
            body_text = para[lead.end():].strip() if stat_number else para
            middles.append({"archetype": "context", "stat_number": stat_number,
                            "headline": "", "body": body_text, "footer_name": FOOTER_NAME})

    # Cap middles so total (hook + middles + cta) <= MAX_SLIDES.
    max_middles = MAX_SLIDES - 2
    if len(middles) > max_middles:
        keep, overflow = middles[:max_middles], middles[max_middles:]
        for extra in overflow:
            extra_text = extra.get("body") or extra.get("headline") or ""
            tgt = keep[-1]
            tgt["body"] = (tgt.get("body", "") + " " + extra_text).strip()
        middles = keep
    beats.extend(middles)

    # ── CTA ───────────────────────────────────────────────────────────────
    persona = post.get("persona", "")
    beats.append({
        "archetype": "cta",
        "headline": "Open briefs. Every Tuesday.",
        "body": "Composers: apply once, get matched for life. Supervisors: shortlist in 48h.",
        "cta_text": "Apply now" if persona == "Tunde" else "Work with us",
        "footer_name": FOOTER_NAME,
    })

    # ── Stamp eyebrows + counters now that the count is final ─────────────
    total = len(beats)
    for n, beat in enumerate(beats, 1):
        beat["slide"] = n
        beat["eyebrow"] = _eyebrow(post, beat["archetype"], n, total)
        beat["counter"] = f"{n:02d} / {total:02d}"
    return beats
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd carousel && python -m pytest tests/test_beats.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add carousel/generators/beats.py carousel/tests/test_beats.py
git commit -m "feat: add beat builder constraining copy to template archetypes"
```

---

### Task 4: Wire beats + fitter into carousel_copy.generate

**Files:**
- Modify: `carousel/generators/carousel_copy.py`
- Test: `carousel/tests/test_carousel_copy.py`

- [ ] **Step 1: Write the failing test**

Create `carousel/tests/test_carousel_copy.py`:
```python
import json
from generators import carousel_copy

POST = {"id": "TEST-01", "type": "Carousel", "pillar": "Education", "persona": "Tunde",
        "platform": "Instagram", "topic": "Sync pay"}
COPY = {"body": "A composer earned $5,000 from one sync.\n\n$5,000 is the market rate.\n\nThe market is real.\n\nApply now.",
        "hook": "A composer earned $5,000 from one sync.", "cta": "Apply at syncmaster.io"}

def test_slides_capped_at_seven(tmp_path):
    out = carousel_copy.generate(POST, COPY, tmp_path)
    data = json.loads(out.read_text())
    assert data["slide_count"] <= 7
    assert data["slides"][0]["archetype"] == "hook"
    assert data["slides"][-1]["archetype"] == "cta"

def test_every_text_field_has_font_size(tmp_path):
    out = carousel_copy.generate(POST, COPY, tmp_path)
    data = json.loads(out.read_text())
    for s in data["slides"]:
        assert "fonts" in s            # {field: font_size}
        for field in ("headline", "body"):
            if s.get(field):
                assert field in s["fonts"]
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd carousel && python -m pytest tests/test_carousel_copy.py -v`
Expected: FAIL — slides use old roles, no `archetype`/`fonts` keys.

- [ ] **Step 3: Rewrite the slide-building core**

In `carousel/generators/carousel_copy.py`, replace the body of `_build_slides` (and its helpers `_split_headline_lede`, `_consolidate`, `_derive_eyebrow`, `_parse_stats`, `_is_thin`) with a call into the new modules, and add per-field fitting. Replace `_build_slides` with:

```python
import json
from generators import beats as _beats
from generators.fitter import fit as _fit

_BUDGETS = json.loads((Path(__file__).resolve().parent.parent / "slot_budgets.json").read_text())["carousel"]


def _fit_beat(beat):
    """Fit each text field of a beat to its slot budget; record font sizes."""
    arch = beat["archetype"]
    slot_budgets = _BUDGETS[arch]
    fonts = {}
    warnings_out = []
    for field in ("eyebrow", "headline", "body", "stat_number", "cta_text"):
        value = beat.get(field)
        if not value or field not in slot_budgets:
            continue
        res = _fit(str(value), slot_budgets[field])
        beat[field] = res.text
        fonts[field] = res.font_size
        if not res.fits:
            warnings_out.append(f"[{beat['slide']:02d} {arch}.{field}] {res.warning}")
    beat["fonts"] = fonts
    if warnings_out:
        beat["fit_warnings"] = warnings_out
    return beat


def _build_slides(post, body):
    built = _beats.build(post, body)
    return [_fit_beat(b) for b in built]
```

Keep the existing `generate()` function, but after `slides = _build_slides(post, body)`, collect and surface warnings:

```python
    slides = _build_slides(post, body)
    fit_warnings = [w for s in slides for w in s.get("fit_warnings", [])]
    if fit_warnings:
        print(f"  [fit]  {post['id']} — {len(fit_warnings)} slot(s) over budget:")
        for w in fit_warnings:
            print(f"         {w}")
```

And add `"fit_warnings": fit_warnings` to the `output` dict. Leave caption fields as-is (they read `slides[0]['headline']`, still valid).

- [ ] **Step 4: Run to verify it passes**

Run: `cd carousel && python -m pytest tests/test_carousel_copy.py -v`
Expected: 2 passed.

- [ ] **Step 5: Regression — regenerate month 1 and eyeball**

Run: `cd carousel && python batch_run.py --month 1 --type Carousel 2>&1 | tail -20`
Expected: all carousels regenerate; any over-budget slots print `[fit]` warnings. No exceptions.

- [ ] **Step 6: Commit**

```bash
git add carousel/generators/carousel_copy.py carousel/tests/test_carousel_copy.py
git commit -m "feat: carousel copy now emits fitted template-archetype beats"
```

---

### Task 5: Fix publisher role→section→layer mapping + fail-loud validation

**Files:**
- Modify: `carousel/figma_publisher.py`
- Test: `carousel/tests/test_publisher_mapping.py`

**Root-cause fixes:**
1. `section_for_role` must map archetype names, not the old roles: `context`/`stat`→CONTEXT section, `showcase`→SHOWCASE, `proof`→PROOF, `hook`→HOOK, `cta`→CTA.
2. `build_text_ops` must read the beat's `fonts` and emit `set_font_size` alongside `set_text`.
3. Counters come from `beat["counter"]` (already correct post-count), not recomputed against a stale total.
4. New `validate_ops(beat, layers)`: every non-empty text field in the beat must resolve to a layer in `layers`; if not, raise `ValueError` (fail loud — no more silent drops).

- [ ] **Step 1: Write the failing test**

Create `carousel/tests/test_publisher_mapping.py`:
```python
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
    # headline + at least one stat pair present
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd carousel && python -m pytest tests/test_publisher_mapping.py -v`
Expected: FAIL — `section_for_archetype` / `build_text_ops_v2` / `validate_ops` don't exist.

- [ ] **Step 3: Add the new mapping functions**

In `carousel/figma_publisher.py`, add archetype→section mapping and the v2 ops builder. Reuse the existing `DARK_SECTIONS`/`LIGHT_SECTIONS` and `*_LAYER_NAMES` dicts (their layer names already match the live Figma scan: hook→`headline`+`body`, context→`stat_number`+`body`, proof→`headline`+stat grid, cta→`headline`+`body`+`cta_text`).

```python
ARCHETYPE_SECTION = {
    "hook": "hook", "context": "body", "stat": "body",
    "showcase": "showcase", "proof": "proof", "cta": "cta",
}

def section_for_archetype(archetype: str, template: str) -> str:
    key = ARCHETYPE_SECTION.get(archetype, "body")
    return (DARK_SECTIONS if template == "dark" else LIGHT_SECTIONS)[key]

# Beat field -> semantic key understood by the section layer maps.
_FIELD_TO_KEY = {
    "eyebrow": ["eyebrow", "section_eyebrow", "top_eyebrow"],
    "headline": ["headline"],
    "body": ["body"],
    "stat_number": ["stat_number"],
    "cta_text": ["cta_text"],
    "counter": ["counter", "counter_main"],
    "footer_name": ["footer_domain"],
}

def build_text_ops_v2(beat: dict, section_id: str, template: str) -> list:
    layers = (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES).get(section_id, {})
    fonts = beat.get("fonts", {})
    ops = []

    def emit(field, value):
        if not value:
            return
        for key in _FIELD_TO_KEY.get(field, [field]):
            if key in layers:
                op = {"find_by_name": layers[key], "set_text": str(value).strip()}
                if field in fonts:
                    op["set_font_size"] = fonts[field]
                ops.append(op)
                return

    emit("counter", beat.get("counter"))
    emit("eyebrow", beat.get("eyebrow"))
    emit("headline", beat.get("headline"))
    emit("stat_number", beat.get("stat_number"))
    emit("body", beat.get("body"))
    emit("cta_text", beat.get("cta_text"))
    emit("footer_name", beat.get("footer_name"))

    # Proof stat grid
    for i, slot in enumerate(("placed", "roster", "turnaround")):
        if i < len(beat.get("stats", [])):
            st = beat["stats"][i]
            lbl = layers.get(f"stat_{slot}_label")
            val = layers.get(f"stat_{slot}_value")
            if lbl: ops.append({"find_by_name": lbl, "set_text": st.get("label", "")})
            if val: ops.append({"find_by_name": val, "set_text": st.get("value", "")})
    return ops

def validate_ops(beat: dict, section_id: str, template: str, strict_fields=None) -> None:
    """Raise if any populated content field has no destination layer in this section."""
    layers = (DARK_LAYER_NAMES if template == "dark" else LIGHT_LAYER_NAMES).get(section_id, {})
    check = strict_fields or {"headline", "body", "stat_number", "cta_text"}
    for field in check:
        if not beat.get(field):
            continue
        keys = _FIELD_TO_KEY.get(field, [field])
        if not any(k in layers for k in keys):
            raise ValueError(
                f"slide {beat.get('slide')} ({beat['archetype']}): field '{field}' "
                f"has copy but no layer in section {section_id} — would be dropped"
            )
```

- [ ] **Step 4: Run to verify it passes**

Run: `cd carousel && python -m pytest tests/test_publisher_mapping.py -v`
Expected: 4 passed.

- [ ] **Step 5: Switch the plan builder to v2 and validate**

In `build_publish_plan`, inside the carousel slide loop, replace the `section_for_role` + `build_text_ops` calls with:
```python
            arch = slide.get("archetype", slide.get("role", "context"))
            sec_id = section_for_archetype(arch, template)
            validate_ops(slide, sec_id, template)        # fail loud on drops
            text_ops = build_text_ops_v2(slide, sec_id, template)
```

- [ ] **Step 6: Regenerate + render-verify one deck in Figma**

Run: `cd carousel && python figma_publisher.py --plan --id IG-EDU-02 > /tmp/plan.json && python -c "import json;p=json.load(open('/tmp/plan.json'));s=p['posts'][0]['slides'];print('slides',len(s));[print(o['find_by_name'],'<-',o['set_text'][:40]) for sl in s for o in sl['text_ops']]"`
Expected: stat/context slides now show BOTH `stat_number` and `body` populated; no slide has only a counter. Then (Claude, via figma-mcp-go) clone IG-EDU-02 into a scratch page and visually confirm no overflow.

- [ ] **Step 7: Commit**

```bash
git add carousel/figma_publisher.py carousel/tests/test_publisher_mapping.py
git commit -m "fix: archetype-based slot mapping with fail-loud validation and font sizes"
```

---

### Task 6: Remove dead/legacy paths

**Files:**
- Modify: `carousel/figma_publisher.py`

- [ ] **Step 1: Point single dark fallback at the new template**

In `select_single_template`, change the dark fallback `return "198:3022"` → `return "238:3472"` and the light fallback `return "198:3023"` → `return "238:3505"`. (Legacy `198:*` frames stay defined for backward compat but are no longer selected.)

- [ ] **Step 2: Verify no single routes to a legacy template**

Run: `cd carousel && python -c "
import json; from pathlib import Path; import figma_publisher as fp
man=json.load(open('exports/manifest.json'))
singles=[p for p in man['posts'] if p.get('type')=='Single' and p.get('platform')=='Instagram']
fp.assign_templates(singles)
legacy=[p['post_id'] for p in singles if fp.select_single_template(p, fp.load_copy(Path('.'),p) or {}) in ('198:3022','198:3023')]
print('legacy routes:', legacy); assert not legacy"`
Expected: `legacy routes: []`, exit 0.

- [ ] **Step 3: Commit**

```bash
git add carousel/figma_publisher.py
git commit -m "fix: route single fallbacks to current 238 templates, retire legacy"
```

---

## Phase 2 (separate plan) — IG-trendy copy rewriting

Once placement is correct, add a copywriting pass (LLM via claude-api skill, using `.agents/product-marketing.md` voice) that rewrites each beat to its budget **before** the fitter runs — turning the deterministic trim into on-brand, hook-led, one-idea-per-slide copy. Gate behind a `--rewrite` flag so offline batch still works. This is where `superpowers` copywriting + frontend-design judgement live. Write as `docs/superpowers/plans/2026-XX-XX-ig-trendy-copy-rewrite.md`.

## Phase 3 (separate plan) — template-aware singles

Give each of the 6 single templates (`238:3472/3505/3535/3569/3601/3631`) its own slot budget block (measured: Stat Hero wants a number+caption+body; Split wants a left context column + headline + body; Minimal has no body). Make `single_copy.generate` produce the field set the *selected* template needs, fitted. Write as `docs/superpowers/plans/2026-XX-XX-template-aware-singles.md`.

---

## Self-Review

- **Spec coverage:** BUG 1 (stat content dropped) → Task 5 (context keeps stat_number+body, validate_ops). BUG 2 (headline in number layer) → Task 1+3 (hook uses `headline` layer; context number paragraphs only set `stat_number`, prose goes to `body`). BUG 3 (garbage stat parse) → Task 3 `_parse_stats`. BUG 4 (wrong counters) → Task 3 (counter stamped after final count). BUG 5 (showcase dead) → reserved for Phase 3 product slides, documented. BUG 6 (legacy single fallback) → Task 6. BUG 7 (no length budget) → Tasks 1, 2, 4. "IG-trendy" → Task 3 (≤7 slides) + Phase 2. Autolayout-absent / shrink-or-resize → Task 2 (font-shrink) + slot budgets. Singles → Phase 3. Unsplash off → already done (`ENABLE_UNSPLASH = False`).
- **Placeholders:** none — every code step has complete code.
- **Type consistency:** `fit()`/`FitResult` consistent across Tasks 2/4; `build()` beat dict keys (`archetype`, `stat_number`, `body`, `stats`, `fonts`, `counter`, `eyebrow`) consistent across Tasks 3/4/5; `section_for_archetype`/`build_text_ops_v2`/`validate_ops` consistent across Task 5/Task 6.

---

## Execution Handoff

Plan complete. Two execution options:
1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks.
2. **Inline Execution** — execute here with checkpoints.
