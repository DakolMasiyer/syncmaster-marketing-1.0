# PLAN: Phase 2 — Playbooks Page

## Status
**Date:** 2026-05-19 (refined after second main pull)
**Branch:** main — confirmed up to date with origin (985c3ae)
**Objective:** Complete 3 missing outreach sequences and build `playbooks.html` as a live siteNav page.

---

## Verified Site State

| URL | File | Nav pattern | Content state |
|---|---|---|---|
| `/` | `index.html` | siteNav | Live |
| `/content-pillars.html` | `content-pillars.html` | siteNav | Live |
| `/content-calendar.html` | `content-calendar.html` | siteNav | Live (legacy — used as Copy Bank M1 reference) |
| `/syncmaster-content-calendar.html` | `syncmaster-content-calendar.html` | **None (standalone)** | Live — kanban, all 5 fixes applied |
| `/copy-bank-m2.html` | `copy-bank-m2.html` | Own mini-nav | Live — **39 posts, full copy written** |
| `/copy-bank-m3.html` | `copy-bank-m3.html` | Own mini-nav | Live — **40 posts, full copy written** |

**siteNav active links:** Strategy Deck · Content Pillars · Content Calendar
**siteNav SOON slots:** Outreach System · **Playbooks** · Measurement · Growth Loops
**Copy Bank removed from siteNav** (commit `1738e44`) — lives in its own cluster now.

---

## What's Fully Done

| Deliverable | File | State |
|---|---|---|
| Month 1 content (42 posts + copy) | `syncmaster-content-calendar.html` | ✅ Complete |
| Month 2 copy bank (39 posts + full copy) | `copy-bank-m2.html` | ✅ Complete |
| Month 3 copy bank (40 posts + full copy) | `copy-bank-m3.html` | ✅ Complete |
| Composer cold outreach sequence | `playbook-composer-sequence.md` | ✅ Complete |
| Producer cold outreach sequence | `playbook-producer-sequence.md` | ✅ Complete |
| Objection handling guide | `objection-handling-guide.md` | ✅ Complete |
| Persona cards | `persona-cards.md` | ✅ Complete |
| Strategy deck | `SyncMaster Deck.html` | ✅ Complete |
| Content pillars guide | `content-pillars.html` | ✅ Complete |

---

## What's Missing — Phase 2 Scope

### Sequence 3 — Composer Onboarding (post-acceptance nurture)
**Gap:** `playbook-composer-sequence.md` ends: "If enrolled → Onboard into composer nurture track." That track is unwritten.
**File:** `playbook-composer-onboarding.md`
**Format:** 4-touch email sequence
**Cadence:** Day 0 (accepted) → Day 2 → Day 5 → Day 10
**Arc:** Acceptance welcome → Metadata & ISRC walkthrough → Stems & rights docs → "You're live" activation
**Persona:** Tunde
**Accent colour:** `--coral`

### Sequence 4 — Producer Post-Demo
**Gap:** `playbook-producer-sequence.md` ends at "Demo booked" with no follow-through.
**File:** `playbook-producer-post-demo.md`
**Format:** 2-touch LinkedIn + email
**Cadence:** Day 1 (post-demo recap) → Day 5 (first brief invitation)
**Arc:** Recap what was shown → Invite first live brief → Establish working relationship
**Persona:** Amara
**Accent colour:** `--purple`

### Sequence 5 — Monthly Newsletter Template
**Gap:** Composer cold sequence ends: "If no reply after Email 3 → add to monthly newsletter list." No template exists.
**File:** `playbook-newsletter-monthly.md`
**Format:** Parameterised monthly digest template
**Structure:** 1 placement story (Proof pillar) · 1 education tip (Education pillar) · 1 CTA (application)
**Persona:** Cold/warm Tunde list
**Accent colour:** `--teal`

---

## HTML Build Plan — `playbooks.html`

### Design pattern
Follow **`content-pillars.html`** — scrollable reference doc with siteNav.
- NOT the copy-bank pattern (standalone, own header, own mini-nav)
- NOT the deck pattern (full-screen scroll-snap, topbar/sidenav/bottombar)
- Copy button pattern: borrow `cb-copy-btn` from `copy-bank-m2.html`

### Page layout

```
[siteNav — fixed 36px, "Playbooks" active]

Hero
├── Eyebrow: "OUTREACH SYSTEM"
├── Title: "Playbooks"
└── Subtitle: two-persona funnel overview + colour key

Funnel map (visual)
├── Left rail — Composer journey: Cold → Applied → Onboarding → Active → Newsletter
└── Right rail — Producer journey: Cold → Demo → Active Brief

── COMPOSER TRACK ─────────────────────────────── (Gold accent)

Section 1 — Composer Cold Outreach
├── Trigger: LinkedIn/email/event
├── Timeline strip: Day 0 · Day 3 · Day 7
├── Email 1 card (expandable): subject lines A/B + body + alignment note
├── Email 2 card
└── Email 3 card + "next steps after sequence" block

Section 2 — Composer Onboarding
├── Trigger: "Application accepted" condition
├── Timeline strip: Day 0 · Day 2 · Day 5 · Day 10
├── Email 1–4 cards (same pattern)
└── "Composer goes live" outcome block

Section 3 — Monthly Newsletter
├── Send cadence: monthly, to cold/warm list
└── Template card with [MONTH], [PLACEMENT_STORY], [TIP] tokens

── PRODUCER TRACK ────────────────────────────── (Teal accent)

Section 4 — Producer Cold Outreach
├── Trigger: LinkedIn connection accepted
├── Timeline strip: Day 0 · Day 3 · Day 7
└── LinkedIn message cards 1–3

Section 5 — Producer Post-Demo
├── Trigger: "Demo attended" condition
├── Timeline strip: Day 1 · Day 5
└── Message + email cards + "active brief relationship" outcome block
```

### Component spec
| Element | Pattern |
|---|---|
| Section headers | `Syne 800`, eyebrow + large title, accent left-rule |
| Message cards | `--surface` bg, `--border` outline, accent left-border (4px) |
| Expandable body | `<details>/<summary>` — no JS dependency |
| Copy button | `cb-copy-btn` class from copy-bank-m2.html |
| Timeline strip | Inline flex dots + labels, accent colour per track |
| Trigger badge | Small pill showing the condition that fires the sequence |
| Metrics row | Open rate / reply rate / conversion targets per sequence |
| Grain overlay | Fixed, z-index 9999 (standard across all pages) |

---

## Nav Update — 3 Files

`playbooks.html` must be added to the siteNav in every file that carries it:

| File | Current stub to replace |
|---|---|
| `index.html` | line ~1955 |
| `content-pillars.html` | line ~641 |
| `content-calendar.html` | same pattern |

Replace in all 3:
```html
<!-- Before -->
<span class="snav-item snav-soon">Playbooks <span class="snav-badge">SOON</span></span>

<!-- After -->
<a href="/playbooks.html" class="snav-item" data-page="playbooks">Playbooks</a>
```

Also add `playbooks.html` to the active-page detection block in each file's JS (`data-page="playbooks"` check).

`playbooks.html` itself also needs the full siteNav block with `data-page="playbooks"` as the active item.

---

## Constraints & Flags

| # | Constraint | Impact |
|---|---|---|
| 1 | `syncmaster-content-calendar.html` has no siteNav | Known gap — not blocking Phase 2 |
| 2 | Copy banks use standalone mini-nav, not siteNav | Playbooks does NOT join the copy-bank cluster |
| 3 | "Outreach System SOON" remains a separate slot | Leave it — it's a future operational tool, not these docs |
| 4 | `codex/implement-content-calendar-system` unmerged | Has `calendar.ts`, `content-os.js`, tests — Content OS work, no conflict with Phase 2 |
| 5 | copy-bank-m2/m3 "0 posted" counter is localStorage tracking | Content IS written — counters reset per browser, not a bug |
| 6 | `SyncMaster Deck.html` has no siteNav | Standalone presentation — no nav update needed |

---

## Execution Order

1. Write `playbook-composer-onboarding.md`
2. Write `playbook-producer-post-demo.md`
3. Write `playbook-newsletter-monthly.md`
4. Build `playbooks.html` using `content-pillars.html` as structural base
5. Update siteNav span → `<a>` link in `index.html`, `content-pillars.html`, `content-calendar.html`
6. Add `playbooks.html` to the active-page JS in each of those 3 files
7. Push to main → verify live at `/playbooks.html`
