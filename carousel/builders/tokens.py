"""
SyncMaster Platform UI — Design Tokens
Mirrors DESIGN_SYSTEM.md § 9.
Single source of truth — no hex values anywhere else.
"""

from pptx.util import Pt
from pptx.dml.color import RGBColor

# ── Canvas ────────────────────────────────────────────────────────────────
W = 1080
H = 1350

# ── px → EMU (96 dpi) and px → Pt ────────────────────────────────────────
def e(n): return int(n * 9525)
def pt(n): return Pt(n * 0.75)

# ── Typography ────────────────────────────────────────────────────────────
DM_SERIF = "DM Serif Display"   # headlines, numbers
DM_SANS  = "DM Sans"            # labels, meta, CTA
LINE_HEIGHT = 1.224
TRACKING    = -0.068             # em  (−68 tracking units)

# ── Colours ───────────────────────────────────────────────────────────────
BG          = RGBColor(0x11, 0x11, 0x10)   # canvas background
SURFACE     = RGBColor(0x1A, 0x1A, 0x18)   # card fill
BORDER      = RGBColor(0x2A, 0x2A, 0x27)   # 1px borders, tag outlines
TEXT        = RGBColor(0xF0, 0xEF, 0xE8)   # primary text
MUTED       = RGBColor(0x88, 0x87, 0x80)   # labels, meta keys, secondary text
HINT        = RGBColor(0x55, 0x54, 0x4F)   # lowest-emphasis text
ACCENT      = RGBColor(0x63, 0x99, 0x22)   # live / placed / money
ACCENT_LT   = RGBColor(0xEA, 0xF3, 0xDE)   # accent on dark (text on green fill)
ACCENT_DK   = RGBColor(0x3B, 0x6D, 0x11)   # filled badge bg
PLACED_BD   = RGBColor(0x4A, 0x7A, 0x20)   # placed card left border
PLACED_BG   = RGBColor(0x1D, 0x2E, 0x16)   # placed banner fill (dark green tint)
AMBER       = RGBColor(0xD9, 0x77, 0x06)   # deadline pill text
AMBER_BG    = RGBColor(0x3A, 0x28, 0x07)   # deadline pill fill
NETFLIX_RED = RGBColor(0xE5, 0x09, 0x14)   # Netflix N circle

# ── Card geometry ─────────────────────────────────────────────────────────
CARD_L  = 80    # card left
CARD_T  = 80    # card top
CARD_W  = 920   # card width
CARD_H  = 1150  # card height
CARD_R  = 12    # corner radius px
CARD_B  = CARD_T + CARD_H   # card bottom  (= 1230)
CARD_PX = 44    # inner padding x
CARD_PY = 44    # inner padding y

# Inner content box
IX  = CARD_L + CARD_PX          # 124
IY  = CARD_T + CARD_PY          # 124
IW  = CARD_W - 2 * CARD_PX      # 832
C2X = IX + IW // 2              # col-2 x (= 540)
CW2 = IW // 2                   # half-width per column (= 416)

# ── Footer ────────────────────────────────────────────────────────────────
FOOTER_Y = 1266   # bottom branding strip y
