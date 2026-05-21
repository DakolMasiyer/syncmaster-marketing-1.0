# SyncMaster Carousel 02 — Design System

> **Font family:** DM Sans · **Global line-height:** 1.224 · **Global tracking:** −68 (−0.068 em)

---

## 1. Design Tokens

```json
{
  "global": {
    "fontFamily": "DM Sans",
    "lineHeight": 1.224,
    "letterSpacing": "-0.068em",
    "letterSpacingRaw": -68
  },

  "color": {
    "brand": {
      "purple":    { "value": "#5252E0", "usage": "Brand primary. Brand-slide background." },
      "lime":      { "value": "#C9E834", "usage": "Accent. Accent text, CTA button, play circle, waveform bars." },
      "dark":      { "value": "#0A0A20", "usage": "Photo-slide background base." },
      "white":     { "value": "#FFFFFF", "usage": "Primary text on dark and purple surfaces." },
      "ink":       { "value": "#0D0D18", "usage": "Dark text on lime (CTA label, play icon)." }
    },
    "alpha": {
      "white-72": { "value": "rgba(255,255,255,0.72)", "on": "purple",   "usage": "Slide 10 sub-headline" },
      "white-52": { "value": "rgba(255,255,255,0.52)", "on": "purple",   "usage": "Eyebrow dim on brand slides" },
      "white-48": { "value": "rgba(255,255,255,0.48)", "on": "purple",   "usage": "Slide 10 bio caption" },
      "white-42": { "value": "rgba(255,255,255,0.42)", "on": "purple",   "usage": "Pill border on brand slides" },
      "white-38": { "value": "rgba(255,255,255,0.38)", "on": "purple",   "usage": "Source footnote" },
      "white-76": { "value": "rgba(255,255,255,0.76)", "on": "purple",   "usage": "Stat block label" },
      "white-75": { "value": "rgba(255,255,255,0.75)", "on": "dark",     "usage": "Body copy on photo slides" },
      "white-58": { "value": "rgba(255,255,255,0.58)", "on": "dark",     "usage": "Artist name in NowPlayingCard" },
      "white-55": { "value": "rgba(255,255,255,0.55)", "on": "dark",     "usage": "Pill border on photo slides" },
      "white-16": { "value": "rgba(255,255,255,0.16)", "on": "dark",     "usage": "NowPlayingCard border" },
      "white-11": { "value": "rgba(255,255,255,0.11)", "on": "purple",   "usage": "StatBlock border" },
      "white-09": { "value": "rgba(255,255,255,0.09)", "on": "dark",     "usage": "NowPlayingCard background" },
      "white-07": { "value": "rgba(255,255,255,0.07)", "on": "purple",   "usage": "StatBlock background" },
      "lime-55":  { "value": "rgba(201,232,52,0.55)",  "on": "purple",   "usage": "Glow orb inner stop" },
      "lime-18":  { "value": "rgba(201,232,52,0.18)",  "on": "purple",   "usage": "Glow orb mid stop" },
      "lime-44":  { "value": "rgba(201,232,52,0.44)",  "on": "any",      "usage": "CTA button drop shadow" },
      "dark-overlay": { "value": "linear-gradient(170deg, rgba(10,4,40,0.62) 0%, rgba(6,2,25,0.84) 100%)", "usage": "Photo-slide dark overlay" }
    }
  },

  "typography": {
    "fontFamily":    "DM Sans",
    "fallback":      "system-ui, sans-serif",
    "lineHeight":    1.224,
    "letterSpacing": "-0.068em",

    "scale": {
      "display-2xl": {
        "fontSize": "98px",  "fontWeight": 600,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Slide 1 opener headline"
      },
      "display-xl": {
        "fontSize": "96px",  "fontWeight": 600,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Slide 10 CTA headline (DISPLAY_XL base)"
      },
      "display-lg": {
        "fontSize": "84px",  "fontWeight": 600,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Primary headline on slides 2-7, 9 (DISPLAY_LG)"
      },
      "display-md": {
        "fontSize": "64px",  "fontWeight": 700,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Stat numbers (slide 8)"
      },
      "sub-display": {
        "fontSize": "46px",  "fontWeight": 500,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Slide 1 lime sub-headline"
      },
      "heading-lg": {
        "fontSize": "44px",  "fontWeight": 600,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Slide 9 lime callouts"
      },
      "heading-md": {
        "fontSize": "40px",  "fontWeight": 700,
        "lineHeight": 1.224, "letterSpacing": "0.02em",
        "usage": "CTA button label (slide 10). Positive tracking exception."
      },
      "heading-sm": {
        "fontSize": "38px",  "fontWeight": 500,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Slide 7 lime answer / slide 9 mid text"
      },
      "body-xl": {
        "fontSize": "36px",  "fontWeight": 600,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "Slide 8 section header"
      },
      "body-lg": {
        "fontSize": "34px",  "fontWeight": 400,
        "lineHeight": 1.4,   "letterSpacing": "-0.068em",
        "usage": "Body copy on photo slides (2-6)"
      },
      "body-md": {
        "fontSize": "30px",  "fontWeight": 600,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "NowPlayingCard track name"
      },
      "body-sm": {
        "fontSize": "26px",  "fontWeight": 400,
        "lineHeight": 1.35,  "letterSpacing": "-0.068em",
        "usage": "Slide 10 bio caption"
      },
      "label-lg": {
        "fontSize": "25px",  "fontWeight": 400,
        "lineHeight": 1.35,  "letterSpacing": "-0.068em",
        "usage": "StatBlock label text (slide 8)"
      },
      "label-md": {
        "fontSize": "22px",  "fontWeight": 500,
        "lineHeight": 1.224, "letterSpacing": "-0.068em",
        "usage": "NowPlayingCard artist name, pill base size"
      },
      "label-sm": {
        "fontSize": "18px",  "fontWeight": 400,
        "lineHeight": 1.4,   "letterSpacing": "-0.068em",
        "usage": "Slide 8 source footnote (italic)"
      },
      "wordmark": {
        "fontSize": "22px",  "fontWeight": 600,
        "lineHeight": 1,     "letterSpacing": "0.10em",
        "textTransform": "uppercase",
        "usage": "SYNCMASTER brand lockup. Positive tracking — fixed exception."
      },
      "eyebrow": {
        "fontSize": "22px",  "fontWeight": 500,
        "lineHeight": 1.224, "letterSpacing": "0.18em",
        "textTransform": "uppercase",
        "usage": "All-caps section label above headlines. Positive tracking — fixed exception."
      },
      "eyebrow-wide": {
        "fontSize": "22px",  "fontWeight": 500,
        "lineHeight": 1.224, "letterSpacing": "0.22em",
        "textTransform": "uppercase",
        "usage": "Slide 7 THE QUESTION eyebrow. Extra-wide version."
      },
      "pill": {
        "fontSize": "22px",  "fontWeight": 500,
        "lineHeight": 1,     "letterSpacing": "0.04em",
        "textTransform": "uppercase",
        "usage": "Pill labels (category + counter). Positive tracking — fixed exception."
      }
    }
  },

  "spacing": {
    "2":    "6px",
    "3":    "8px",
    "4":    "12px",
    "5":    "14px",
    "6":    "16px",
    "7":    "20px",
    "8":    "22px",
    "10":   "28px",
    "11":   "30px",
    "12":   "32px",
    "14":   "36px",
    "15":   "38px",
    "16":   "40px",
    "18":   "44px",
    "20":   "52px",
    "22":   "56px",
    "chrome-edge": "79px",
    "wordmark-top": "91px",
    "slide-pad-x": "95px",
    "stage-pad-y": "150px"
  },

  "radius": {
    "pill":       "9999px",
    "card":       "22px",
    "stat-block": "28px",
    "cta-button": "9999px",
    "bar":        "2px"
  },

  "shadow": {
    "cta": "0 14px 48px rgba(201,232,52,0.44)"
  },

  "layout": {
    "slide": {
      "width":       "1080px",
      "height":      "1350px",
      "aspectRatio": "4/5",
      "format":      "portrait",
      "padding-x":   "95px",
      "chrome-top":  "150px",
      "chrome-btm":  "150px",
      "stage-top":   "150px",
      "stage-btm":   "1200px"
    }
  }
}
```

---

## 2. Typography Scale

| Token | Size | Weight | Line-ht | Tracking | Usage |
|---|---|---|---|---|---|
| `display-2xl` | 98 px | 600 | **1.224** | **−0.068 em** | Slide 1 opener |
| `display-xl`  | 96 px | 600 | **1.224** | **−0.068 em** | Slide 10 CTA headline |
| `display-lg`  | 84 px | 600 | **1.224** | **−0.068 em** | Primary headline, slides 2–7, 9 |
| `display-md`  | 64 px | 700 | **1.224** | **−0.068 em** | Stat numbers (slide 8) |
| `sub-display` | 46 px | 500 | **1.224** | **−0.068 em** | Slide 1 lime sub-line |
| `heading-lg`  | 44 px | 600 | **1.224** | **−0.068 em** | Slide 9 lime callouts |
| `heading-md`  | 40 px | 700 | **1.224** | +0.02 em ⚠ | CTA button label |
| `heading-sm`  | 38 px | 500 | **1.224** | **−0.068 em** | Slide 7 lime line, slide 9 |
| `body-xl`     | 36 px | 600 | **1.224** | **−0.068 em** | Slide 8 section header |
| `body-lg`     | 34 px | 400 | 1.4       | **−0.068 em** | Body copy, photo slides 2–6 |
| `body-md`     | 30 px | 600 | **1.224** | **−0.068 em** | NowPlayingCard track name |
| `body-sm`     | 26 px | 400 | 1.35      | **−0.068 em** | Slide 10 bio caption |
| `label-lg`    | 25 px | 400 | 1.35      | **−0.068 em** | StatBlock label |
| `label-md`    | 22 px | 500 | **1.224** | **−0.068 em** | Artist name, pill base |
| `label-sm`    | 18 px | 400 | 1.4       | **−0.068 em** | Source footnote (italic) |
| `wordmark`    | 22 px | 600 | 1         | +0.10 em ⚠  | SYNCMASTER lockup, uppercase |
| `eyebrow`     | 22 px | 500 | **1.224** | +0.18 em ⚠  | Section label, uppercase |
| `eyebrow-wide`| 22 px | 500 | **1.224** | +0.22 em ⚠  | Slide 7 THE QUESTION |
| `pill`        | 22 px | 500 | 1         | +0.04 em ⚠  | Pill labels, uppercase |

> ⚠ **Positive tracking exceptions** — wordmark, eyebrow, pill, and CTA button keep their original positive tracking. All other tokens inherit the global **−68 / −0.068 em** default.

---

## 3. Colour Palette

### Brand

| Swatch | Token | Hex | Usage |
|---|---|---|---|
| 🟣 | `brand.purple` | `#5252E0` | Brand-slide backgrounds |
| 🟡 | `brand.lime`   | `#C9E834` | Accent, CTA, play button, bars |
| 🌑 | `brand.dark`   | `#0A0A20` | Photo-slide base background |
| ⬜ | `brand.white`  | `#FFFFFF` | Primary text on purple / dark |
| ⬛ | `brand.ink`    | `#0D0D18` | Text on lime surfaces |

### Alpha Tokens (purple surface)

| Token | Value | Usage |
|---|---|---|
| `alpha.white-72` | `rgba(255,255,255,0.72)` | Slide 10 sub-headline |
| `alpha.white-52` | `rgba(255,255,255,0.52)` | Eyebrow on brand slides |
| `alpha.white-48` | `rgba(255,255,255,0.48)` | Slide 10 caption |
| `alpha.white-42` | `rgba(255,255,255,0.42)` | Pill border (brand slides) |
| `alpha.white-38` | `rgba(255,255,255,0.38)` | Source footnote |
| `alpha.white-76` | `rgba(255,255,255,0.76)` | StatBlock label text |
| `alpha.white-07` | `rgba(255,255,255,0.07)` | StatBlock fill |
| `alpha.white-11` | `rgba(255,255,255,0.11)` | StatBlock border |

### Alpha Tokens (dark surface)

| Token | Value | Usage |
|---|---|---|
| `alpha.white-75` | `rgba(255,255,255,0.75)` | Body copy, photo slides |
| `alpha.white-58` | `rgba(255,255,255,0.58)` | Artist name in NowPlayingCard |
| `alpha.white-55` | `rgba(255,255,255,0.55)` | Pill border (photo slides) |
| `alpha.white-16` | `rgba(255,255,255,0.16)` | NowPlayingCard border |
| `alpha.white-09` | `rgba(255,255,255,0.09)` | NowPlayingCard fill |

---

## 4. Spacing Scale

| Token | Value | Where used |
|---|---|---|
| `spacing.6`           | 6 px  | Waveform bar gap |
| `spacing.12`          | 12 px | Body paragraph margin |
| `spacing.16`          | 16 px | Eyebrow → headline gap |
| `spacing.22`          | 22 px | Play icon → text gap in NowPlayingCard |
| `spacing.32`          | 32 px | NowPlayingCard inner padding-x |
| `spacing.40`          | 40 px | Slide 1 content gap, StatBlock icon-to-text gap |
| `spacing.44`          | 44 px | Slide 7 content gap |
| `spacing.52`          | 52 px | Slide 9/10 content gap |
| `spacing.56`          | 56 px | Card → headline gap (photo slides) |
| `spacing.chrome-edge` | 79 px | Pills from slide edge (all sides) |
| `spacing.wordmark-top`| 91 px | Wordmark top offset |
| `spacing.slide-pad-x` | 95 px | Slide horizontal content padding |
| `spacing.stage-pad-y` | 150 px| Safe zone from top/bottom (chrome avoidance) |

---

## 5. Components

### Pill (outlined label)

```json
{
  "component": "Pill",
  "variants": {
    "md": {
      "paddingX": "24px", "paddingY": "10px",
      "fontSize": "22px", "fontWeight": 500,
      "letterSpacing": "0.04em", "textTransform": "uppercase",
      "borderRadius": "9999px", "borderWidth": "2px",
      "borderColor-brand": "rgba(255,255,255,0.42)",
      "borderColor-photo": "rgba(255,255,255,0.55)",
      "color": "#FFFFFF",
      "background": "transparent"
    },
    "lg": {
      "paddingX": "28px", "paddingY": "12px",
      "fontSize": "24px"
    }
  }
}
```

### SwipePill (arrow pill, top-right chrome)

```json
{
  "component": "SwipePill",
  "width": "88px",
  "height": "44px",
  "borderRadius": "9999px",
  "borderWidth": "2px",
  "borderColor-brand": "rgba(255,255,255,0.42)",
  "borderColor-photo": "rgba(255,255,255,0.55)",
  "background": "transparent",
  "icon": "→ arrow (SVG stroke, 32×14 px viewBox)"
}
```

### NowPlayingCard (photo slides 2–6)

```json
{
  "component": "NowPlayingCard",
  "maxWidth": "740px",
  "paddingX": "32px",
  "paddingY": "20px",
  "gap": "22px",
  "borderRadius": "22px",
  "background": "rgba(255,255,255,0.09)",
  "backdropFilter": "blur(28px)",
  "border": "1px solid rgba(255,255,255,0.16)",

  "playCircle": {
    "size": "56px",
    "borderRadius": "50%",
    "background": "#C9E834",
    "iconColor": "#0D0D18"
  },

  "trackName": {
    "fontSize": "30px", "fontWeight": 600,
    "lineHeight": 1.224, "letterSpacing": "-0.068em",
    "color": "#FFFFFF"
  },
  "artistName": {
    "fontSize": "22px", "fontWeight": 400,
    "lineHeight": 1.224, "letterSpacing": "-0.068em",
    "color": "rgba(255,255,255,0.58)",
    "marginTop": "6px"
  },

  "waveformBars": {
    "count": 7,
    "heights": [12, 20, 8, 22, 14, 18, 10],
    "width": "3px",
    "gap": "4px",
    "container": "26px",
    "color": "#C9E834",
    "borderRadius": "2px",
    "opacity": 0.82
  }
}
```

### StatBlock (slide 8)

```json
{
  "component": "StatBlock",
  "paddingX": "40px",
  "paddingY": "30px",
  "gap": "36px",
  "borderRadius": "28px",
  "background": "rgba(255,255,255,0.07)",
  "border": "1px solid rgba(255,255,255,0.11)",

  "icon": {
    "size": "48px",
    "stroke": "rgba(255,255,255,0.88)",
    "strokeWidth": "2.2px",
    "lineCap": "round"
  },
  "stat": {
    "fontSize": "64px", "fontWeight": 700,
    "lineHeight": 1.224, "letterSpacing": "-0.068em",
    "color": "#C9E834"
  },
  "label": {
    "fontSize": "25px", "fontWeight": 400,
    "lineHeight": 1.35, "letterSpacing": "-0.068em",
    "color": "rgba(255,255,255,0.76)",
    "marginTop": "8px"
  }
}
```

### GlowOrb (brand slides)

```json
{
  "component": "GlowOrb",
  "shape": "radial-gradient ellipse",
  "gradient": "radial-gradient(circle, rgba(201,232,52,0.55) 0%, rgba(201,232,52,0.18) 45%, transparent 70%)",
  "instances": {
    "slide-01": { "size": "580px", "centerX": "50%", "centerY": "48%", "opacity": 0.28 },
    "slide-07": { "size": "420px", "centerX": "50%", "centerY": "58%", "opacity": 0.22 },
    "slide-08": { "size": "360px", "centerX": "50%", "centerY": "12%", "opacity": 0.20 },
    "slide-10": { "size": "640px", "centerX": "50%", "centerY": "46%", "opacity": 0.34 }
  }
}
```

---

## 6. Slide Layout Grid

```
┌─────────────────────────────────────────────┐  ← 1080 px wide
│  79          WORDMARK            SwipePill  │  ← top: 91 px (wordmark) / 79 px (pill)
│  ───────────────────────────────────────── │  ← stage top: 150 px
│                                             │
│  ◄── padding: 95 px ──────────────────────► │
│                                             │
│             CONTENT STAGE                  │
│          (vertically centred)               │
│                                             │
│  ◄── padding: 95 px ──────────────────────► │
│  ───────────────────────────────────────── │  ← stage bottom: 1200 px
│  CategoryPill              CounterPill  79  │  ← bottom: 79 px from edge
└─────────────────────────────────────────────┘  ← 1350 px tall
```

---

## 7. Per-Slide Content Map

| Slide | Frame | Background | Headline token | Key copy |
|---|---|---|---|---|
| 01 | Brand | `#5252E0` + glow (580 px, 48%) | `display-2xl` 98 px | "Your favourite songs have been on the world's biggest stages." |
| 02 | Photo | `#0A0A20` + image | `display-lg` 84 px | "NBA Playoffs. 2016." |
| 03 | Photo | `#0A0A20` + image | `display-lg` 84 px | "Netflix. Top Boy. Season 1." |
| 04 | Photo | `#0A0A20` + image | `display-lg` 84 px | "Spider-Man: Across the Spider-Verse." |
| 05 | Photo | `#0A0A20` + image | `display-lg` 84 px | "UEFA Champions League. 180 countries watching." |
| 06 | Photo | `#0A0A20` + image | `display-lg` 84 px | "Black Panther: Wakanda Forever. Disney+." |
| 07 | Brand | `#5252E0` + glow (420 px, 58%) | `display-lg` 84 px | "So what actually happened when those songs played?" |
| 08 | Brand | `#5252E0` + glow (360 px, 12%) | `display-md` 64 px (stats) | 812% / $5k–$500k / $178M |
| 09 | Brand | `#5252E0` (no glow) | `display-lg` 84 px | "African composers make the music the world wants." |
| 10 | Brand | `#5252E0` + glow (640 px, 46%) | `display-xl` 96 px | "That's the gap we're closing." |

---

## 8. Google Fonts Import

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400;1,9..40,500;1,9..40,600&display=swap');
```

```css
:root {
  --font-family:     "DM Sans", system-ui, sans-serif;
  --line-height:     1.224;
  --letter-spacing:  -0.068em;  /* −68 tracking */

  /* Brand */
  --brand-purple:    #5252E0;
  --brand-lime:      #C9E834;
  --brand-dark:      #0A0A20;
  --brand-white:     #FFFFFF;
  --brand-ink:       #0D0D18;

  /* Slide dimensions */
  --slide-w:         1080px;
  --slide-h:         1350px;
  --slide-pad-x:     95px;
  --stage-pad-y:     150px;
  --chrome-edge:     79px;
}

body {
  font-family:    var(--font-family);
  line-height:    var(--line-height);
  letter-spacing: var(--letter-spacing);
}
```

---

*Design system derived from `slides-02.jsx` + `chrome.jsx` · Font updated to DM Sans · Line-height 1.224 · Tracking −68*

---

## 9. Platform UI Tokens — Brief Cards

> Dark editorial. "Spotify meets A&R portal." Applied to `slide-01-live-brief` and `slide-02-placed-brief`.

### 9.1 Colour Palette

| Token | Hex | Usage |
|---|---|---|
| `bg` | `#111110` | Canvas background |
| `surface` | `#1a1a18` | Card fill |
| `border` | `#2a2a27` | 1 px card border, tag outlines, dividers |
| `text` | `#f0efe8` | Primary text |
| `muted` | `#888780` | Labels, meta keys, secondary text |
| `hint` | `#55544f` | Lowest-emphasis text |
| `accent` | `#639922` | Live / placed / money — green |
| `accent-lt` | `#eaf3de` | Text on green filled surfaces |
| `accent-dk` | `#3b6d11` | Filled badge background |
| `placed-border` | `#4a7a20` | Left accent bar on placed card |
| `placed-bg` | `#1d2e16` | Placed banner fill (dark green tint) |
| `amber` | `#d97706` | Deadline pill text |
| `amber-bg` | `#3a2807` | Deadline pill fill |
| `netflix-red` | `#e50914` | Netflix platform badge circle |

### 9.2 Typography

| Role | Font | Size | Weight | Tracking | Usage |
|---|---|---|---|---|---|
| Headline | DM Serif Display | 28 px | 400 | −0.068 em | Card title |
| Stat number | DM Serif Display | 24 px | 400 | −0.068 em | Sync fee value (placed) |
| Banner amount | DM Serif Display | 20 px | 400 | −0.068 em | Deal amount in banner |
| CTA headline | DM Serif Display | 18 px | 400 | −0.068 em | CTA conversion line |
| Body / value | DM Sans | 14 px | 400 | −0.068 em | Meta values, subtitle |
| CTA button | DM Sans | 13 px | 700 | −0.068 em | Button label |
| Platform name | DM Sans | 13 px | 400 | −0.068 em | Badge text, platform line |
| Tag / label | DM Sans | 11 px | 400 | −0.068 em | Genre tags, meta keys, slot text |
| Eyebrow | DM Sans | 11 px | 400 | −0.068 em | "BRIEF · OPEN" — uppercase |

Global line-height: **1.224** (from §2)

### 9.3 Card Geometry

```json
{
  "card": {
    "left":         "80px",
    "top":          "80px",
    "width":        "920px",
    "height":       "1150px",
    "radius":       "12px",
    "paddingX":     "44px",
    "paddingY":     "44px",
    "border":       "1px solid #2a2a27"
  },
  "leftAccent": {
    "width":        "4px",
    "fill":         "#4a7a20",
    "appliedTo":    "placed-brief only"
  },
  "footer": {
    "y":            "1266px",
    "dot":          "10px circle #639922",
    "wordmark":     "DM Sans 13px #f0efe8",
    "url":          "DM Sans 12px #888780 right-aligned"
  }
}
```

### 9.4 Components

#### Live Brief Card — element stack (top → bottom)
```
Eyebrow      "BRIEF · OPEN FOR SUBMISSIONS"  11px muted uppercase
Badge        Platform circle + name           13px
────────────────────────────────────────────── 1px divider
Title        Brief headline                   28px DM Serif Display
Subtitle     Tags line                        14px muted
────────────────────────────────────────────── 1px divider
Meta grid    3 rows × 2 cols (label 11px / value 14px)
             Budget value → accent green
────────────────────────────────────────────── 1px divider
Genre tags   Pills: border #2a2a27 / text muted / radius 100px
────────────────────────────────────────────── 1px divider
Slot dots    5 ovals (2 filled accent, 3 surface+border) + deadline pill
────────────────────────────────────────────── 1px divider
CTA strip    Headline 18px DM Serif + subtext 12px + button
```

#### Placed Brief Card — differences from Live Brief
```
Left border  4px rect #4a7a20 full card height
Eyebrow      "BRIEF · PLACED" in accent green
Status badge "✓ Placed" filled pill (accent-dk bg, accent-lt text)
Meta R1 val  Sync fee: DM Serif Display 24px accent green
Placed banner Full-width green-tint strip (placed-bg fill, placed-border top line)
              Left: status text (muted 12px) | Right: amount (DM Serif 20px accent)
```

### 9.5 Python token file
`builders/tokens.py` — single source of truth, consumed by all slide builders.
No hex values appear in any slide file — only token names.

### 9.6 Output files
| File | Slides | Shapes | Images |
|---|---|---|---|
| `exports/slide-01-live-brief.pptx` | 1 | 42 | 0 |
| `exports/slide-02-placed-brief.pptx` | 1 | 34 | 0 |

Both are 1080 × 1350 px, fully editable in Canva. Zero embedded screenshots.
