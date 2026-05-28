# SyncMaster Design System

> **SyncMaster** is the infrastructure layer between African composers and the global sync licensing market. Composers manage their EPK, catalog, and brief invitations from a curated dashboard. Music supervisors and producers post briefs and receive a vetted shortlist of rights-cleared matches within 24–48 hours.

This folder is the canonical design system: typography, color, components, voice, and UI kits — extracted from the production `Syncmaster-Live` codebase (Next.js 16 + Tailwind v4 + shadcn/ui, Phase E2 baseline) and the supplied logo assets.

---

## Sources

| Source | Path | Notes |
|---|---|---|
| Production codebase | `Syncmaster-Live/` (mounted) | Next.js 16 App Router. Tokens in `app/globals.css`, scale in `tailwind.config.ts`. |
| Logo (icon) | `uploads/Syncdark.png` → `assets/logos/Icon . Mark only.png` | Acid-lime circle with purple "S" mark. |
| Logo (wordmark, light bg) | `uploads/syncmasterwhite.png` → `assets/logos/Primary Horizontal Logo.png` | Full lockup, purple type on white/light backgrounds. |
| Logo (wordmark, dark bg) | — → `assets/logos/Primary Horizontal Logo - p.png` | Full lockup, white type on dark/purple backgrounds. |
| Reference URL | `https://syncmaster-live.vercel.app` | Production deploy referenced in `app/layout.tsx`. |

---

## Index — what lives where

```
README.md                       This file
SKILL.md                        Agent Skill manifest (Claude Code-compatible)
colors_and_type.css             All design tokens — color, type, radii, spacing, shadow
fonts/                          (Linked from Google Fonts — see Type Substitutions below)
assets/
  logos/                          Icon . Mark only, Primary Horizontal Logo, Primary Horizontal Logo - p, Stacked Logo - p, Stacked Logo - w
  platforms/                      Netflix, Hulu, Prime Video, Disney, HBO, Paramount, EA, NBA2K
  screens/                        dashboard-preview, dashboard-banner, syncscreen
preview/                        Cards that populate the Design System tab
  type-*.html                     Type scale & specimen cards
  color-*.html                    Palette + semantic + status cards
  spacing-*.html, radius-*.html   Tokens
  shadow-*.html                   Elevation
  comp-*.html                     Buttons, badges, inputs, cards, banners
  brand-*.html                    Logo cards, platforms strip
ui_kits/
  marketing/                      Public site — landing, /composers, /supervisors
    index.html, *.jsx
  dashboard/                      Product app — dashboard, briefs, tracks
    index.html, *.jsx
```

---

## Product context

SyncMaster has **two surfaces**:

1. **Marketing site** (`syncmaster-live.vercel.app`) — light mode, big editorial type, hero with platform-logo strip, role-split pages for Composers and Supervisors.
2. **Dashboard product** (`/dashboard/*`) — dark mode, purple sidebar rail, mono labels, card-list-detail flows for Briefs, Tracks, Composers, Producers, Placements, EPK, Campaigns, Radio Directory.

Three roles inside the product:
- **Composer** — uploads catalog, manages EPK, receives brief invites, submits tracks.
- **Producer** (music supervisor) — posts briefs, receives 3–5 curated matches.
- **Admin** — operates the platform: vets composers, curates matches, manages placements.

The product wedge is "**human curation + rights clarity**" — explicitly *not* an open directory.

---

## Content fundamentals

**Voice.** Confident, direct, practical. Operator's voice — not marketing copywriter. Reads like a developer-tool product page that happens to be about music. Show the data, show the process, no fluff.

**Casing & punctuation.**
- Headings & section titles: **Sentence case**. Never Title Case.
- Mono labels & micro-metadata: **ALL CAPS with wide letterspacing** (`PROJECT BRIEF / SCOPE`, `ESTIMATED BUDGET`, `DEADLINE:`, `SONIC DIRECTION`).
- Em dashes for compression: `African Composers — Global Briefs.` `3–5 curated matches — not 500 unvetted submissions.`
- En dashes for ranges: `$5,000 – $20,000`, `24–48h turnaround`.
- Trailing periods on hero headlines: yes (`Your music, placed in film, TV, games and ads worldwide.`).

**Pronouns.** Direct second-person *you* for the composer-facing copy ("Your talent belongs on the world stage."). First-person plural *we* for the platform's own actions ("We vet you once, then match you to briefs.").

**Numbers as proof.** Brief copy leans on concrete counts: *3–5 matches, not 500*. *24–48h turnaround*. *Apply once. Lifetime access*. Anti-vagueness — pair every claim with a number or a contrast.

**No marketing fluff list:**
- No "revolutionize" / "unleash" / "transform" / "powerful" / "seamless" / "best-in-class".
- No exclamation points.
- No emoji in product or marketing. (None appear in the codebase.)

**Yes list:**
- Italic *emphasis* used sparingly on a single word in a headline (`Your music, placed in *film, TV, games and ads* worldwide.`).
- Contrasting two-sentence cadence: short claim, then qualification (`Apply once. Get verified once. Then sit back and let the briefs come to you.`).
- Concrete platforms named in body copy (`from Netflix to Nollywood`).

**Sample copy (verbatim from the product):**
- Hero: *"Your music, placed in film, TV, games and ads worldwide."*
- Subhead: *"SyncMaster connects vetted African composers with briefs from production houses worldwide. Human curation. Rights clarity. 3–5 curated matches — not 500 unvetted submissions."*
- For Composers tagline: *"Your talent belongs on the world stage."*
- For Supervisors: *"Post a brief and receive 3–5 hand-curated African tracks within days. Vetted. Rights-cleared. No directories. No noise."*
- Status copy: `Active — Curating composers`, `Draft — Pending review`, `Matched — Intro made`.
- Empty state: *"No active briefs yet. Check back soon — new opportunities are added regularly."*

---

## Visual foundations

### Colors

- **Primary brand:** `#4b4bc0` SyncMaster Purple. Used for sidebar fill (light mode), primary buttons, links, focus rings, active states.
- **Highlight accent:** `oklch(0.88 0.18 120)` acid lime — used **exclusively** for the `Active` status badge and selection-state shimmer. Never used as primary action color.
- **Dark canvas:** `#0f0f1a` background, `#16162a` card. The product app's default.
- **Light canvas:** `#ffffff` background, also `#ffffff` cards (separation by 1px border, not by fill).
- **Foreground:** `#f9f9f9` dark / `#111111` light.
- **Borders:** `rgba(255,255,255,0.08)` (dark) / `#e5e5e5` (light). Hairline-first.
- **Status palette:** green `#22c55e` success, amber `#f59e0b` warning, blue `#3b82f6` info, red `#ef4444` destructive.

### Type

- **All UI:** DM Sans, weights 300/400/500/700/900.
- **Body weight is 500.** Not 400 — this is intentional. The product reads more confident at 500.
- **Headings:** weight **900** ("black"), letterspacing **−0.068em**, line-height **1.2**. This is the signature treatment — every `h1–h6` carries it.
- **Display:** weight 300, letterspacing −0.04em, line-height 0.95. Used for brief titles and editorial moments — very different vibe from the headings; light + airy, where headings are dense + cropped.
- **Mono:** Geist Mono, used for labels (`.label`/`.label-strong`), data (BPM, durations, money), and any technical metadata. Labels are 10–11px, all-caps, letterspacing 0.1–0.25em.

### Spacing & radii

- 4px base unit. Tailwind scale 1=4, 2=8, 3=12, 4=16, 5=20, 6=24, 8=32, 10=40, 12=48, 16=64, 20=80.
- Base radius **6px** (`--radius: 0.375rem`). Scale 2/4/6/8/12/16. The product itself **frequently uses larger radii** for hero/feature cards: `rounded-3xl` (32px), `rounded-[2rem]` (32px), `rounded-[2.5rem]` (40px). The base is 6 but the marketing surface lives at 24–40.

### Backgrounds

- **No image backgrounds** as primary surface. The hero on the landing page uses a `blur(120px)` purple glow at low opacity — that's the only "decorative" treatment, and even it is subtle.
- **No repeating patterns, no textures, no grain, no hand-drawn illustration.** The aesthetic is editorial-software-minimal.
- Dashboard hero uses a flat purple (`#4b4bc0`) panel with white absolute-positioned blur orbs at `blur-[120px]` for depth — never gradients.

### Borders, shadows, separation

- **Borders before shadows.** Cards are `border border-border` (1px). Shadow is added on hover only — `hover:shadow-2xl hover:-translate-y-2`.
- Active brief detail uses a **left border accent**: `border-l-4 border-l-acid-lime` on the Budget card. This is one of the few places color leaves the badge.
- Sidebar nav active state: white fill + purple text + `scale-[1.02]` + `border-r-4 border-primary/20`. Plus icon scales 110% on active.
- Elevation shadows exist but are Spotify-style heavy (used for music-player panels): `0 8px 24px rgba(0,0,0,0.40)` etc.

### Hover & press states

- **Cards** on hover: `hover:border-primary/40 hover:shadow-2xl hover:-translate-y-2` and inner icon-pill `group-hover:bg-primary group-hover:text-white group-hover:scale-110`.
- **Buttons (default)** on hover: subtle background lift (`hover:bg-white/90` on white-on-purple; `hover:bg-primary/90` on purple-on-white).
- **Nav links** on hover: `hover:text-foreground hover:bg-white/5 hover:translate-x-1` — slight rightward nudge.
- **Press** (`active:`): all buttons drop 1px (`active:not-aria-[haspopup]:translate-y-px`). No color change.

### Animation

- Generic durations: 150ms / 200ms / 300ms (`--transition-fast/base/slow`).
- Pages use Tailwind's `animate-in fade-in slide-in-from-bottom-{2,4,6,8,10} duration-{500,700,1000}` for staggered hero entrance.
- Loading: `animate-pulse` (2s, ease-in-out infinite).
- **No bounces. No elastic. No spring.** Easings are `ease-in-out` (`cubic-bezier(0.4,0,0.2,1)`) — Material-ish, not playful.

### Layout

- Marketing: `max-w-screen-2xl` with `px-6`. 20-section vertical rhythm with `border-t border-border` separators between sections.
- Dashboard: fixed 64px header + 256px (16rem) sidebar on `lg:`, `p-4 md:p-6` content. Music player docks bottom.
- Mobile breakpoints: 375 / 640 / 768 / 1024 / 1280 / 1400.

### Transparency & blur

- Sticky navs and headers: `bg-background/80 backdrop-blur-xl`. Always paired with a `border-b border-border/50`.
- Sidebar user card: `bg-white/5 border border-white/10 backdrop-blur-md`.
- Used sparingly — only for floating chrome.

### Imagery

- Product screenshots embedded in the marketing hero, framed by a fake macOS browser chrome (`rounded-[2.5rem] border bg-card` with three small grey circles top-left).
- Platform logos shown in `opacity-60 grayscale hover:grayscale-0 transition-all duration-500` strip — they pop on hover.

### Iconography

See `assets/` and the **Iconography** section below.

---

## Iconography

**Library: [lucide-react](https://lucide.dev/)** (loaded directly via the codebase, ~1.5px stroke, rounded line joins, 24×24 default). Heavily used — every nav link, every feature card, every status indicator. Common icons referenced in the source:

`LayoutDashboard, Layers, Briefcase, TrendingUp, Users, Headphones, FileText, CheckSquare, Mail, MonitorPlay, Radio, Music2, Sparkles, Search, Building2, ClipboardList, Settings, LogOut, Menu, X, ArrowRight, ArrowDownToLine, Calendar, DollarSign, Clock, Shield, Globe, Globe2, Mic2, Film, Zap, CheckCircle2, Send, BarChart3, Play, Pause, Plus, MoreHorizontal, Edit3, Trash2, Share2, Download, Upload, Loader2, GripVertical, ChevronRight, ChevronDown, ListPlus`

For the design system we load Lucide from a CDN inside HTML cards:

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
<script>lucide.createIcons();</script>
```

Or in JSX:
```js
const ICONS_CDN = "https://unpkg.com/lucide@latest";
// Use <i data-lucide="briefcase"></i> + lucide.createIcons()
```

**Emoji.** Not used — none appear in the codebase or marketing copy. Do not introduce them.

**Unicode characters as glyphs.** Em-dash (`—`), en-dash (`–`), and the bullet `·` are used liberally as punctuation/separators. The brief detail uses `•` between metadata, and `·` between producer name and company.

**Brand mark.**
- `assets/logos/Icon . Mark only.png` (also `.svg`) — acid-lime circle with stylised purple "S/∞" knot. Use at small sizes, favicons, monograms. Works on any background.
- `assets/logos/Primary Horizontal Logo.png` (also `.svg`) — full horizontal lockup, purple wordmark. Use in nav and footer on light/white backgrounds.
- `assets/logos/Primary Horizontal Logo - p.png` (also `.svg`) — full horizontal lockup, white wordmark. Use in nav and footer on dark (#0f0f1a, #16162a) or purple (#4b4bc0) backgrounds.

**Platform logos** (`assets/platforms/`) — Netflix, Hulu, Prime Video, Disney, HBO, Paramount, EA, NBA 2K. Real third-party trademarks; only shown as the "discover opportunities across" strip on the marketing hero, always in `grayscale` with `opacity-60`.

---

## Type substitutions

- **DM Sans** — pulled from Google Fonts via `next/font/google` in the codebase. The design system also loads it from Google Fonts in `colors_and_type.css`. ✅ No substitution.
- **Geist Mono** — same, loaded from Google Fonts. ✅ No substitution.

> If the user wants self-hosted font files, drop the TTFs into `fonts/` and switch the `@import` in `colors_and_type.css` to a `@font-face` block. Flagged: **no font files are bundled in this design system today**; everything is CDN-served from Google Fonts.

---

## UI kits

- **`ui_kits/marketing/`** — Light-mode public site. Hero, platform strip, role-split cards, big editorial type, big radii (32–40px), CTA banner with primary-tint background.
- **`ui_kits/dashboard/`** — Dark-mode product app. Purple sidebar rail (light-mode in the original, but reads stronger in our dark editorial direction), mono labels, brief cards, score-bar, waveform, music-player dock.

Each kit has a `README.md`, a static `index.html` demonstrating an interactive screen, and a set of `.jsx` component recreations.

---

## How to use this design system

1. Drop `colors_and_type.css` into any HTML / Next / React project and the tokens are available as CSS custom properties.
2. Apply `.dark` to `<html>` or `<body>` to flip to the dark editorial default.
3. Use the `.label`, `.label-strong`, `.mono`, `.display`, `.hairline` utility classes for the signature editorial moments.
4. Reach for **Lucide** for icons (CDN link above).
5. Keep headings on the signature **`font-weight: 900; letter-spacing: -0.068em; line-height: 1.2`** treatment — that's the SyncMaster type voice.

---

## Caveats / things to verify

- Production uses `next/font` for DM Sans and Geist; this kit loads both from public Google Fonts CSS for portability. **Sub-pixel hinting may differ.**
- A few additional logos (Spotify, Apple Music) referenced in the codebase aren't on the marketing hero; only the eight platform logos imported above are in `assets/platforms/`.
- Dashboard previews (`dashboard-preview.png`, `syncscreen.png`) are PNG screenshots from the live product. Treat as snapshots, not source-of-truth components.
