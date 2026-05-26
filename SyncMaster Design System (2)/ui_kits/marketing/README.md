# Marketing UI Kit

Light-mode editorial public site — DM Sans black weight headlines, big radii, sectioned vertical rhythm with hairline separators. Direct port of `Syncmaster-Live/app/page.tsx`, `app/composers/page.tsx`, `app/supervisors/page.tsx`.

## Files

- `index.html` — three-page click-through (Home / For Composers / For Supervisors).
- `Components.jsx` — `MarketingNav`, `CTAButton`, `Capsule`, `FeatureCard`, `RoleCard`, `PlatformStrip`, `StepCard`, `Footer`.
- `Screens.jsx` — `Landing`, `ComposersPage`, `SupervisorsPage`.

## Pages recreated

1. **Landing** — hero with capsule label + italic-emphasis headline + platform strip + framed dashboard preview, three-feature grid, role-split, CTA banner.
2. **For Composers** — composer-direct hero, problem/solution two-column, four-step pipeline.
3. **For Supervisors** — supervisor-direct hero with embedded sample brief card, stats strip (24–48h / 3–5 / 100% / $0).

## Visual contracts

| Surface | Token |
|---|---|
| Background | `#ffffff` |
| Card | `#ffffff` (1px `#e5e5e5` border, no shadow at rest) |
| Section break | `border-top: 1px solid #e5e5e5` between every section |
| Headings | weight 900 · −0.04em / −0.068em · 1.05–1.2 lh |
| Hero CTA | H64 · `border-radius: 16` · weight 900 · `0 20px 40px -8px rgba(75,75,192,.4)` glow |
| Card radius | 32–40px (the largest in the system) |
| Italic emphasis | inline `<span style="font-style: italic; color: #4b4bc0">` on one word |
| Capsule | inline rounded-pill above section heading, color-keyed (purple / emerald / red) |

## Caveats / cut corners

- `/login`, `/signup`, `/brand`, `/terms`, `/privacy`, `/contact` links are non-functional anchors.
- The dashboard-preview screenshot embedded in the hero is the production PNG, not a live render.
- `For Supervisors` is original copy + layout I authored — the production site only stubs this page; I extended it into a full hero + stats strip following the same patterns.
