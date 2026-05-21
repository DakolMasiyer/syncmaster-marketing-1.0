"""
Slide 1 — Live Brief Card
Dark canvas, single card, green accents.
All elements are native pptx shapes/text — fully editable in Canva.
"""

from pptx.enum.text import PP_ALIGN

from builders.tokens import (
    W, H, e, pt,
    CARD_L, CARD_T, CARD_W, CARD_H, CARD_R,
    IX, IY, IW, C2X,
    BG, SURFACE, BORDER, TEXT, MUTED, HINT, ACCENT, ACCENT_LT,
    NETFLIX_RED, DM_SERIF, DM_SANS,
    FOOTER_Y,
)
from builders.primitives import (
    solid_bg, add_rect, add_oval,
    tb, tb2, pill, divider,
    meta_row, genre_tag, slot_dots, cta_strip, branding_footer,
)

# ── Y-coordinates (absolute canvas px) ───────────────────────────────────
_Y = {}
def _layout():
    y = IY   # 124

    _Y['eyebrow'] = y;           y += 18 + 18     # 160
    _Y['badge']   = y;           y += 44 + 18     # 222
    _Y['div1']    = y;           y += 1  + 24     # 247
    _Y['title']   = y;           y += 80 + 14     # 341
    _Y['sub']     = y;           y += 26 + 22     # 389
    _Y['div2']    = y;           y += 1  + 24     # 414
    _Y['meta1']   = y;           y += 68 + 14     # 496
    _Y['meta2']   = y;           y += 68 + 14     # 578
    _Y['meta3']   = y;           y += 68 + 22     # 668
    _Y['div3']    = y;           y += 1  + 22     # 691
    _Y['tags']    = y;           y += 44 + 22     # 757
    _Y['div4']    = y;           y += 1  + 22     # 780
    _Y['slots']   = y;           y += 44 + 26     # 850
    _Y['div5']    = y;           y += 1  + 26     # 877
    _Y['cta']     = y                             # 877

_layout()


def build_live_brief(prs, blank, data: dict):
    """
    Add one 'Live Brief' slide to prs.
    data keys: title, subtitle, platform_name, budget, usage, exclusivity,
               track_length, stems, rights, slots_filled, slots_total,
               deadline, cta_headline, cta_subtext, cta_button
    """
    s = prs.slides.add_slide(blank)

    # ── Canvas background ──────────────────────────────────────────────
    solid_bg(s, BG)

    # ── Card shell ────────────────────────────────────────────────────
    add_rect(s, CARD_L, CARD_T, CARD_W, CARD_H,
             fill=SURFACE, border=BORDER, bpt=1.0, radius_px=CARD_R)

    # ── Eyebrow ───────────────────────────────────────────────────────
    tb(s, 'BRIEF · OPEN FOR SUBMISSIONS',
       IX, _Y['eyebrow'], IW, 18,
       11, MUTED, font=DM_SANS)

    # ── Platform badge (Netflix N circle + name) ──────────────────────
    badge_y = _Y['badge']
    circle_size = 28
    add_oval(s, IX, badge_y + 6, circle_size, circle_size, fill=NETFLIX_RED)
    tb(s, 'N', IX + 7, badge_y + 8, circle_size - 8, circle_size - 8,
       14, ACCENT_LT, bold=True, align=PP_ALIGN.CENTER)
    tb(s, data.get('platform_name', 'Netflix Original Series'),
       IX + circle_size + 12, badge_y + 9, IW - circle_size - 12, 24,
       13, TEXT, font=DM_SANS)

    # ── Divider 1 ─────────────────────────────────────────────────────
    divider(s, _Y['div1'], CARD_L, CARD_W)

    # ── Title ─────────────────────────────────────────────────────────
    tb(s, data.get('title', 'Afrobeat score for premium TV drama'),
       IX, _Y['title'], IW, 80,
       28, TEXT, bold=False, font=DM_SERIF)

    # ── Subtitle ──────────────────────────────────────────────────────
    tb(s, data.get('subtitle', 'Post-production · Global rights · Instrumental'),
       IX, _Y['sub'], IW, 26,
       14, MUTED, font=DM_SANS)

    # ── Divider 2 ─────────────────────────────────────────────────────
    divider(s, _Y['div2'], CARD_L, CARD_W)

    # ── Meta grid (3 rows × 2 cols) ───────────────────────────────────
    meta_row(s, _Y['meta1'],
             'Budget',       data.get('budget', '$2,500 – $5,000'),
             'Usage',        data.get('usage', 'Global · 3 years'),
             left_accent=True)

    meta_row(s, _Y['meta2'],
             'Exclusivity',  data.get('exclusivity', 'Non-exclusive'),
             'Track length', data.get('track_length', '60 – 120 sec'))

    meta_row(s, _Y['meta3'],
             'Stems',        data.get('stems', 'Required'),
             'Rights',       data.get('rights', 'One-stop preferred'))

    # ── Divider 3 ─────────────────────────────────────────────────────
    divider(s, _Y['div3'], CARD_L, CARD_W)

    # ── Genre tags ────────────────────────────────────────────────────
    tags = data.get('genres', ['Afrobeats', 'Emotional', 'Mid-tempo', 'Instrumental'])
    tx = IX
    for tag in tags:
        tx = genre_tag(s, tag, tx, _Y['tags']) + 10

    # ── Divider 4 ─────────────────────────────────────────────────────
    divider(s, _Y['div4'], CARD_L, CARD_W)

    # ── Slot indicator + deadline pill ───────────────────────────────
    slot_dots(
        s,
        total    = data.get('slots_total', 5),
        filled   = data.get('slots_filled', 2),
        x        = IX,
        y        = _Y['slots'],
        label    = f"{data.get('slots_filled', 2)} of {data.get('slots_total', 5)} slots filled",
        deadline_text = data.get('deadline', '9 days left'),
    )

    # ── Divider 5 ─────────────────────────────────────────────────────
    divider(s, _Y['div5'], CARD_L, CARD_W)

    # ── CTA strip ────────────────────────────────────────────────────
    cta_strip(
        s,
        y          = _Y['cta'],
        headline   = data.get('cta_headline', 'One placement pays more than 6 months of streaming.'),
        subtext    = data.get('cta_subtext', 'Vetted composers only. Up to 3 tracks. We make the intro.'),
        btn_label  = data.get('cta_button', 'Submit a track →'),
    )

    # ── Footer branding ───────────────────────────────────────────────
    branding_footer(s)

    return s
