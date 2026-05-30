"""
Pure text fitter for SyncMaster slots.

Given a string and a slot budget (from slot_budgets.json), decide the largest
font size in [font_min, font_max] at which the text fits the box's character
budget. Never cuts words — if it cannot fit even at font_min, it pins to
font_min and reports fits=False with a warning for manual review.

The char budget (max_chars) is the TOTAL allowance measured at font_max. When
the font shrinks, proportionally more characters fit, so the effective capacity
scales by (font_max / font).
"""
from dataclasses import dataclass
import re
from typing import Optional


@dataclass
class FitResult:
    text: str
    font_size: int
    fits: bool
    warning: Optional[str] = None


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
