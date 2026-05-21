"""
Slide 2 — Placed Brief Card
Dark canvas, green left border accent, placed status badge, deal banner.
All elements are native pptx shapes/text — fully editable in Canva.
"""

from pptx.enum.text import PP_ALIGN

from builders.tokens import (
    W, H, e, pt,
    CARD_L, CARD_T, CARD_W, CARD_H, CARD_R,
    IX, IY, IW, C2X, CW2,
    BG, SURFACE, BORDER, TEXT, MUTED, ACCENT, ACCENT_LT, ACCENT_DK,
    PLACED_BD, PLACED_BG,
    DM_SERIF, DM_SANS,
    FOOTER_Y,
)
from builders.primitives import (
    solid_bg, add_rect, add_oval,
    tb, tb2, pill, divider,
    meta_row, cta_strip, branding_footer,
)

# Left accent is 4px wide, overlaid on the card's left edge
_ACCENT_W = 4
# Content x shifts right to clear the accent bar
_CX = IX + _ACCENT_W   # = 128

# ── Y-coordinates (absolute canvas px) ───────────────────────────────────
_Y = {}
def _layout():
    y = IY   # 124

    _Y['eyebrow'] = y;           y += 18 + 16     # 158
    _Y['platform']= y;           y += 26 + 18     # 202
    _Y['div1']    = y;           y += 1  + 24     # 227
    _Y['title']   = y;           y += 80 + 14     # 321
    _Y['sub']     = y;           y += 26 + 14     # 361
    _Y['badge']   = y;           y += 38 + 26     # 425
    _Y['div2']    = y;           y += 1  + 26     # 452
    _Y['meta1']   = y;           y += 76 + 14     # 542
    _Y['meta2']   = y;           y += 76 + 14     # 632
    _Y['meta3']   = y;           y += 76 + 22     # 730
    _Y['div3']    = y;           y += 1  + 22     # 753
    _Y['banner']  = y;           y += 80 + 22     # 855
    _Y['div4']    = y;           y += 1  + 26     # 882
    _Y['cta']     = y                             # 882

_layout()


def build_placed_brief(prs, blank, data: dict):
    """
    Add one 'Placed Brief' slide to prs.
    data keys: title, subtitle, platform_name, sync_fee, commission,
               placed_date, composer, track_name, usage,
               banner_status, cta_headline, cta_subtext, cta_button
    """
    s = prs.slides.add_slide(blank)

    # ── Canvas background ──────────────────────────────────────────────
    solid_bg(s, BG)

    # ── Card shell ────────────────────────────────────────────────────
    add_rect(s, CARD_L, CARD_T, CARD_W, CARD_H,
             fill=SURFACE, border=BORDER, bpt=1.0, radius_px=CARD_R)

    # ── Left border accent (4px green bar) ────────────────────────────
    add_rect(s, CARD_L, CARD_T, _ACCENT_W, CARD_H, fill=PLACED_BD)

    # ── Eyebrow (green) ───────────────────────────────────────────────
    tb(s, 'BRIEF · PLACED',
       _CX, _Y['eyebrow'], IW - _ACCENT_W, 18,
       11, ACCENT, font=DM_SANS)

    # ── Platform name ─────────────────────────────────────────────────
    tb(s, data.get('platform_name', 'Nike West Africa · Brand Campaign'),
       _CX, _Y['platform'], IW - _ACCENT_W, 26,
       14, TEXT, font=DM_SANS)

    # ── Divider 1 ─────────────────────────────────────────────────────
    divider(s, _Y['div1'], CARD_L + _ACCENT_W, CARD_W - _ACCENT_W)

    # ── Title ─────────────────────────────────────────────────────────
    tb(s, data.get('title', 'Amapiano · 30-sec ad placement'),
       _CX, _Y['title'], IW - _ACCENT_W, 80,
       28, TEXT, font=DM_SERIF)

    # ── Subtitle ──────────────────────────────────────────────────────
    tb(s, data.get('subtitle', 'Regional · West Africa · 1 year'),
       _CX, _Y['sub'], IW - _ACCENT_W, 26,
       14, MUTED, font=DM_SANS)

    # ── "✓ Placed" status badge ───────────────────────────────────────
    badge_text = '✓  Placed'
    badge_w    = 100
    badge_h    = 34
    pill(s, _CX, _Y['badge'], badge_w, badge_h,
         badge_text, None, ACCENT_LT, size=12, fill=ACCENT_DK)

    # ── Divider 2 ─────────────────────────────────────────────────────
    divider(s, _Y['div2'], CARD_L + _ACCENT_W, CARD_W - _ACCENT_W)

    # ── Meta grid (3 rows × 2 cols) ───────────────────────────────────
    # Row 1: Sync fee (DM Serif Display 24px, accent) | Commission (muted)
    fee_y     = _Y['meta1']
    lbl_h, val_h = 16, 36

    # Sync fee — larger value using DM Serif Display
    tb(s, 'SYNC FEE', _CX, fee_y, CW2, lbl_h, 10, MUTED, font=DM_SANS)
    tb(s, data.get('sync_fee', '$3,200'),
       _CX, fee_y + lbl_h + 6, CW2, val_h,
       24, ACCENT, font=DM_SERIF)

    tb(s, 'COMMISSION', C2X, fee_y, CW2, lbl_h, 10, MUTED, font=DM_SANS)
    tb(s, data.get('commission', '$480  (15%)'),
       C2X, fee_y + lbl_h + 6, CW2, val_h,
       14, MUTED, font=DM_SANS)

    # Row 2: Placed date | Composer
    meta_row(s, _Y['meta2'],
             'Placed',    data.get('placed_date', 'Apr 14 2026'),
             'Composer',  data.get('composer', 'Tunde A.'))

    # Row 3: Track | Usage
    meta_row(s, _Y['meta3'],
             'Track',  data.get('track_name', 'Lagos Summer v3'),
             'Usage',  data.get('usage', 'West Africa · 1 yr'))

    # ── Divider 3 ─────────────────────────────────────────────────────
    divider(s, _Y['div3'], CARD_L + _ACCENT_W, CARD_W - _ACCENT_W)

    # ── Placed banner (full card width, green tint) ───────────────────
    banner_y = _Y['banner']
    banner_h = 72
    # Green-tint background rect (full card width, no side padding)
    add_rect(s, CARD_L + _ACCENT_W, banner_y,
             CARD_W - _ACCENT_W, banner_h,
             fill=PLACED_BG, border=None)
    # Top-edge accent line
    add_rect(s, CARD_L + _ACCENT_W, banner_y,
             CARD_W - _ACCENT_W, 1, fill=PLACED_BD)

    # Banner status text (left)
    tb(s, data.get('banner_status', 'Deal closed  ·  Intro sent  ·  Invoice issued'),
       _CX, banner_y + 22, IW - 160, 28,
       12, MUTED, font=DM_SANS)

    # Banner amount (right, DM Serif Display, accent)
    amount_w = 120
    amount_x = CARD_L + CARD_W - CARD_R - amount_w
    tb(s, data.get('sync_fee', '$3,200'),
       amount_x, banner_y + 18, amount_w, 36,
       20, ACCENT, font=DM_SERIF, align=PP_ALIGN.RIGHT)

    # ── Divider 4 ─────────────────────────────────────────────────────
    divider(s, _Y['div4'], CARD_L + _ACCENT_W, CARD_W - _ACCENT_W)

    # ── CTA strip ────────────────────────────────────────────────────
    cta_strip(
        s,
        y         = _Y['cta'],
        headline  = data.get('cta_headline',
                             'Your sound is in demand. The world just doesn\'t know where to find you.'),
        subtext   = data.get('cta_subtext',
                             'Apply to join SyncMaster. Vetted composers only.'),
        btn_label = data.get('cta_button', 'Apply now →'),
    )

    # ── Footer branding ───────────────────────────────────────────────
    branding_footer(s)

    return s
