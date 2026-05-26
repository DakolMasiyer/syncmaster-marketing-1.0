"""
SyncMaster Design Agent — generate_slides.py
Entry point. Builds both brief cards as editable PPTX files.
Run from project root: python scripts/generate_slides.py
"""

import sys, os

# Ensure project root is on the path so builders.* imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pptx import Presentation
from builders.tokens import e, W, H
from builders.slide_live_brief   import build_live_brief
from builders.slide_placed_brief import build_placed_brief

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS = os.path.join(ROOT, 'exports')
os.makedirs(EXPORTS, exist_ok=True)


def make_prs():
    prs = Presentation()
    prs.slide_width  = e(W)
    prs.slide_height = e(H)
    return prs


def generate_slide(slide_type: str, output_path: str, data: dict) -> None:
    blank = None

    if slide_type == 'live-brief':
        prs   = make_prs()
        blank = prs.slide_layouts[6]
        build_live_brief(prs, blank, data)

    elif slide_type == 'placed-brief':
        prs   = make_prs()
        blank = prs.slide_layouts[6]
        build_placed_brief(prs, blank, data)

    else:
        raise ValueError(f"Unknown slideType: {slide_type!r}")

    prs.save(output_path)
    kb = os.path.getsize(output_path) // 1024
    print(f"Slide exported -> {output_path}  ({kb} KB)")


if __name__ == '__main__':

    # ── Slide 1 — Live Brief ──────────────────────────────────────────
    generate_slide(
        slide_type  = 'live-brief',
        output_path = os.path.join(EXPORTS, 'slide-01-live-brief.pptx'),
        data = {
            'platform_name':  'Netflix Original Series',
            'title':          'Afrobeat score for premium TV drama',
            'subtitle':       'Post-production · Global rights · Instrumental',
            'budget':         '$2,500 – $5,000',
            'usage':          'Global · 3 years',
            'exclusivity':    'Non-exclusive',
            'track_length':   '60 – 120 sec',
            'stems':          'Required',
            'rights':         'One-stop preferred',
            'genres':         ['Afrobeats', 'Emotional', 'Mid-tempo', 'Instrumental'],
            'slots_filled':   2,
            'slots_total':    5,
            'deadline':       '9 days left',
            'cta_headline':   'One placement pays more than 6 months of streaming.',
            'cta_subtext':    'Vetted composers only. Up to 3 tracks. We make the intro.',
            'cta_button':     'Submit a track →',
        },
    )

    # ── Slide 2 — Placed Brief ────────────────────────────────────────
    generate_slide(
        slide_type  = 'placed-brief',
        output_path = os.path.join(EXPORTS, 'slide-02-placed-brief.pptx'),
        data = {
            'platform_name':  'Nike West Africa · Brand Campaign',
            'title':          'Amapiano · 30-sec ad placement',
            'subtitle':       'Regional · West Africa · 1 year',
            'sync_fee':       '$3,200',
            'commission':     '$480  (15%)',
            'placed_date':    'Apr 14 2026',
            'composer':       'Tunde A.',
            'track_name':     'Lagos Summer v3',
            'usage':          'West Africa · 1 yr',
            'banner_status':  'Deal closed  ·  Intro sent  ·  Invoice issued',
            'cta_headline':   "Your sound is in demand. The world just doesn't know where to find you.",
            'cta_subtext':    'Apply to join SyncMaster. Vetted composers only.',
            'cta_button':     'Apply now →',
        },
    )
