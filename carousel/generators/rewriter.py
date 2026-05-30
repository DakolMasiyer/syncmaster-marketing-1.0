"""
LLM-backed copy rewriter for SyncMaster carousel beats.

Activated with --rewrite flag in batch_run.py. Requires ANTHROPIC_API_KEY.
Rewrites beats that STILL exceed their slot budget after deterministic trimming,
producing on-brand, hook-led, IG-trendy copy within the measured char limits.

Offline batch (no flag): this module is never imported.
"""
import json
import os

_BRAND_SYSTEM = """\
You rewrite Instagram carousel slide copy for SyncMaster — a sync licensing
infrastructure platform for independent African composers.

Brand voice:
- Direct and practical. No fluff. No hype. No academic tone.
- Specific over vague: real numbers, real timelines, named territories.
- Confident without bravado. African music is the asset, not the underdog.
- Never invent placements, client names, or metrics. Use what is given.
- One idea per slide. Hook-led. Short enough to read in 2 seconds.

Output ONLY a JSON object with the rewritten field(s). No explanation.
Example: {"headline": "One placement. One month of rent."}
"""


def _effective_max(budget: dict) -> int:
    """Capacity at floor font size (same formula as fitter._capacity)."""
    return int(budget["max_chars"] * budget["font_max"] / budget["font_min"])


def _build_prompt(beat: dict, field: str, text: str, max_chars: int) -> str:
    arch = beat.get("archetype", "context")
    stat_ctx = ""
    if beat.get("stat_number"):
        stat_ctx = f"\nSlide stat number: {beat['stat_number']}"
    return (
        f"Rewrite this {arch} slide {field} to be ≤{max_chars} chars.\n"
        f"Keep the core fact. Match brand voice.{stat_ctx}\n\n"
        f"ORIGINAL ({len(text)} chars):\n{text}\n\n"
        f'Return JSON: {{"{field}": "rewritten text"}}'
    )


def rewrite_beats(beats: list, budgets: dict, post: dict) -> list:
    """Rewrite any beat fields that still exceed their slot budget after fitting.

    Returns the same list (mutated in place) with over-budget fields replaced
    by LLM-generated IG-trendy copy. Skips CTA beats (fixed copy).
    """
    try:
        import anthropic
    except ImportError:
        print("  [rewrite] 'anthropic' package not installed — pip install anthropic")
        return beats

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  [rewrite] ANTHROPIC_API_KEY not set — skipping LLM rewrite")
        return beats

    client = anthropic.Anthropic(api_key=api_key)

    for beat in beats:
        arch = beat.get("archetype", "")
        if arch == "cta":
            continue  # CTA copy is brand-fixed

        slot_budgets = budgets.get(arch, {})
        fit_warnings = beat.get("fit_warnings", [])
        if not fit_warnings:
            continue

        for field in ("headline", "body"):
            value = beat.get(field, "")
            budget = slot_budgets.get(field)
            if not value or not budget:
                continue
            max_cap = _effective_max(budget)
            if len(value) <= max_cap:
                continue

            prompt = _build_prompt(beat, field, value, max_cap)
            try:
                msg = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=300,
                    system=_BRAND_SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                result = json.loads(msg.content[0].text)
                if field in result and isinstance(result[field], str):
                    rewritten = result[field].strip()
                    if rewritten and len(rewritten) <= max_cap:
                        before = len(value)
                        beat[field] = rewritten
                        print(
                            f"  [rewrite] {beat.get('slide',0):02d} "
                            f"{arch}.{field}: {before}→{len(rewritten)} chars"
                        )
            except Exception as exc:
                print(f"  [rewrite] {arch}.{field} failed: {exc}")

    return beats
