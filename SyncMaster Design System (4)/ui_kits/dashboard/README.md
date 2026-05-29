# Dashboard UI Kit

Dark editorial product app — purple navigation rail, mono labels, brief cards, AI score bars, waveform-equipped music player. Direct port of `Syncmaster-Live/components/dashboard/*` and `app/(dashboard)/dashboard/*`.

## Files

- `index.html` — the full interactive shell. Click any sidebar item to navigate; click a row on the Briefs list to open the detail view.
- `Sidebar.jsx` — purple rail, grouped nav (Workspace / Distribution / Network), white-fill active state, user pod with sign-out.
- `Components.jsx` — `Header`, `StatusBadge`, `BriefCard`, `ToolTile`, `Waveform`, `MusicPlayer`, `ScoreBar`, `Banner`.
- `Screens.jsx` — `DashboardHome`, `BriefsList`, `BriefDetail`, `CatalogPage`, plus `SCREEN_DATA` fixtures.

## Pages recreated

1. **Dashboard home** — welcome greeting, purple hero banner with rotated screenshot, Top Briefs carousel, Tools grid.
2. **Briefs list** — dense list pattern with status pill + mono "DUE" label, genre chips, mono budget.
3. **Brief detail** — italic uppercase display title, two-column body / metadata, acid-lime-bordered budget card, AI suggested composers with score bars.
4. **Catalog** — tracks table with BPM / key / AI-match score columns, search bar, play affordance that triggers the dockable music player.

## Visual contracts

| Surface | Token |
|---|---|
| Background | `#0f0f1a` |
| Card | `#16162a` (1px border, no shadow at rest) |
| Sidebar | `#4b4bc0` flat fill |
| Active nav | white fill + purple text + `scale(1.02)` + `border-r-4 border-primary/20` |
| Headings | weight 900 · −0.068em · 1.2 lh |
| Mono labels | Geist Mono · 10–11px · ALL CAPS · 0.25em / 0.1em tracking |
| Active status | `oklch(0.88 0.18 120)` acid lime + `0 0 20px rgba(217,249,157,.3)` glow |

## Caveats / cut corners

- Navigation is one-level — clicking unimplemented nav items lands on the Dashboard.
- Audio is muted; the player dock appears when you click a track row in Catalog but doesn't actually play.
- Score-bar percentages are hard-coded; the real product runs them through the AI matcher in `agents/composer-matcher.ts`.
- The brief deadline labels read as static dates instead of relative ("2 days").
