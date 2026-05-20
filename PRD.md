# SyncMaster Platform — Product Requirements Document

**Version:** 1.0  
**Date:** 2026-05-20  
**Status:** Draft — Pre-Build  
**Audience:** Engineering, Design, Product

---

## 1. Executive Summary

SyncMaster is a sync licensing infrastructure platform connecting African composers to global music supervisors. The current system operates as a static HTML Marketing OS (7 pages, no backend). This PRD specifies the full platform build: a web application with a composer-facing portal, a supervisor-facing brief system, and an admin dashboard — all backed by a database.

**Business goal:** Become the default pipeline for African music in global film, TV, advertising, and games productions within 24 months of platform launch.

**Why build now:** The manual workflow (static HTML, spreadsheet tracking, manual email sequences) has proven the model. Month 2 metrics — 9 composers vetted, 5+ briefs, 2 placements, 31h average brief-to-delivery — justify productising the workflow before volume makes it unmanageable.

---

## 2. Problem Statement

The current operation runs on manual tooling:
- Composer applications arrive via form link — tracked in a spreadsheet
- Brief matching is done manually by email
- Supervisor contacts managed in a static HTML page with no real data
- Email sequences sent manually (no automation)
- Placement tracking has no database

This works at 9 composers and 5 briefs per month. It does not work at 50 composers and 20 briefs per month.

**The platform must automate or systematise:**
1. Composer intake, vetting, and onboarding
2. Supervisor brief intake and catalogue matching
3. Outreach sequence delivery (composer cold, onboarding, producer cold, post-demo, newsletter)
4. Placement tracking and reporting
5. Payments and contract management

---

## 3. Users

### 3.1 Composer (Tunde)
- Independent African musician with professional-quality catalogue
- Has never placed a sync or doesn't know how
- Needs: application portal, onboarding checklist, catalogue submission, brief notification, placement history, payment record
- Device: Mobile-first (most African composers work from phones)
- Auth: Email + Google OAuth

### 3.2 Music Supervisor / Producer (Amara)
- Professional at a streaming platform, ad agency, or production company
- Needs: brief submission form, curated track delivery (max 5 options), rights documentation download, composer contact relay, invoice/licensing support
- Device: Desktop-primary
- Auth: Invite-only (no public signup)

### 3.3 Nollywood Producer (Tertiary)
- Nigerian film director or production company
- Needs: brief form + licensing workflow similar to Amara, but simpler
- Device: Mobile + desktop
- Auth: Self-register with approval gate

### 3.4 SyncMaster Admin
- Internal team member running the platform
- Needs: full CRM visibility (composers + supervisors), brief management, curation interface, sequence triggering, placement logging, payment processing
- Device: Desktop
- Auth: Admin role (internal only)

---

## 4. Core Modules

### 4.1 Composer Portal

**Purpose:** End-to-end journey from application to active placement.

#### Application Flow
- Public landing page with social proof (placements, proof points)
- Application form: name, location, genre, DAW, sample tracks (upload or link), rights confirmation checkbox
- Post-submission: automated acknowledgement email, entry into vetting queue

**Fields:**
```
composer_id (uuid)
name (string)
email (string)
location (string)          # country + city
genre_tags (string[])
daw (string)
social_links (json)        # instagram, spotify, soundcloud, etc.
sample_tracks (url[])
rights_confirmed (bool)
status (enum): applied | vetting | active | placed | alumni | rejected
applied_at (timestamp)
vetted_at (timestamp)
activated_at (timestamp)
```

#### Vetting Module (Admin-side)
- Admin review queue: composer details, sample tracks, rights status
- Vetting checklist: rights confirmed | master ownership clear | no sample issues | metadata standard | stems available
- Status transition triggers onboarding email sequence automatically

#### Onboarding Checklist (Composer-facing)
4-step activation checklist shown after acceptance:
1. **Metadata** — complete ISRC, BPM, key, instrumentation, mood, genre tags for each track
2. **Stems** — upload stems package (full mix + no-vocal + instrumental) per track
3. **Rights docs** — upload rights confirmation document or complete rights wizard
4. **Sample tracks** — confirm 3–5 priority tracks for brief matching

Each step: status badge (incomplete / in progress / complete), help link, admin review trigger on completion.

#### Catalogue
- Track list with metadata completeness score per track
- Bulk ISRC import
- Stems upload per track
- "Brief match history" — which briefs your tracks were submitted to (anonymised until placement)
- Placement history with fee + production name (post-placement)

---

### 4.2 Brief Management System

**Purpose:** Receive briefs from supervisors, match to catalogue, deliver curated options.

#### Brief Intake (Supervisor-facing)
- Brief submission form (accessible to approved supervisors only)
- Fields:

```
brief_id (uuid)
supervisor_id (FK)
production_title (string)
production_type (enum): film | tv | ad | game | podcast | other
genre_requirements (string[])
mood_tags (string[])
tempo (string)            # slow / mid / uptempo / any
duration_seconds (int)
vocal (enum): vocal | instrumental | either
budget_range (enum): under_1k | 1k_5k | 5k_20k | 20k_plus | undisclosed
deadline (timestamp)
notes (text)
status (enum): received | in_curation | delivered | placed | closed
received_at (timestamp)
delivered_at (timestamp)
```

#### Curation Interface (Admin-facing)
- Brief arrives → admin notified
- Catalogue search: filter by mood, genre, tempo, vocal/instrumental, rights status
- Select up to 5 tracks → "Curate brief" action
- Per-track: preview, metadata card, stems download, rights doc status
- Send curated pack to supervisor (email delivery + download portal link)

#### Brief Response Portal (Supervisor-facing)
- Unique link per brief delivery
- 5 tracks: listen, download stems, download rights doc, flag preference
- Selection → triggers placement workflow
- Reject all → reopen curation or close brief

**Target SLA:** Brief received → curated pack delivered in ≤48 hours.

---

### 4.3 Content Calendar & Repurposing Engine

**Purpose:** Automate the content workflow from idea to scheduled post across 5 platforms.

#### Content Bank (Ideas Layer)
```
idea_id (uuid)
title (string)
description (text)
theme_tags (string[])
funnel_stage (enum): awareness | engagement | conversion | retention
platform_potential (enum[]): linkedin | instagram | tiktok | youtube | newsletter
status (enum): idea | selected | archived
created_at (timestamp)
```

#### Source Content Module
```
source_id (uuid)
idea_id (uuid, nullable FK)
title (string)
format (enum): blog | podcast_script | video_script
body (markdown text)
key_points (string[])
hook (string)
status (enum): draft | in_review | published
created_at (timestamp)
```

#### Repurposing Engine
- Input: published Source Content
- Output: platform-specific variations (LinkedIn post, Instagram caption, TikTok script, YouTube short, newsletter snippet)
- Each variation: editable before scheduling, copy-to-clipboard, regenerate button
- AI-assisted generation (Claude API) with brand voice guardrails from `.agents/product-marketing.md`

```
repurposed_id (uuid)
source_id (FK)
platform (enum): linkedin | instagram | tiktok | youtube | newsletter
format (string)
content (text)
hook (string)
cta (string)
status (enum): draft | approved | scheduled | posted
created_at (timestamp)
```

#### Content Calendar Module
```
calendar_item_id (uuid)
source_content_id (uuid, nullable)
repurposed_content_id (uuid, nullable)
standalone_content_id (uuid, nullable)
content_type (enum): repurposed | standalone
platform (enum): linkedin | instagram | tiktok | youtube | newsletter
title (string)
content (text)
caption (string, nullable)
publish_date (date ISO)
publish_time (time, nullable)
status (enum): scheduled | posted | draft | failed
tags (string[])
automation_link (url, nullable)
created_at (timestamp)
updated_at (timestamp)
```

**Auto-scheduling defaults:**

| Day | Platform |
|---|---|
| Monday | Source content (optional) |
| Tuesday | LinkedIn |
| Wednesday | Instagram |
| Thursday | TikTok |
| Friday | YouTube |
| Sunday | Newsletter |

Manual override always available. Conflict resolution: push to next available same-day slot → next week.

---

### 4.4 Outreach Automation

**Purpose:** Replace manual email sequences with triggered, tracked sequences.

#### Sequences

| Sequence | Trigger | Touches | Channel |
|---|---|---|---|
| Composer cold outreach | Manual list import or new contact flag | 3 over 7 days | Email |
| Composer onboarding | `composer.status → active` | 4 over 10 days | Email |
| Monthly newsletter | `no_reply_after_cold_sequence_3` OR manual add | 1x/month | Email |
| Producer cold outreach | LinkedIn connection accepted (manual trigger) | 3 over 7 days | LinkedIn / Email |
| Producer post-demo | `demo_attended = true` | 2 over 5 days | LinkedIn + Email |

**Sequence engine requirements:**
- Per-sequence: open rate, reply rate, click rate, unsubscribe rate
- Per-touch: sent timestamp, opened, clicked, replied
- Manual override: pause, skip touch, mark replied
- Unsubscribe handling: instant suppression, GDPR-compliant
- Template variables: `{{first_name}}`, `{{placement_story}}`, `{{month}}`, `{{tip}}`

---

### 4.5 CRM

**Purpose:** Single source of truth for all composer and supervisor contacts.

#### Composer CRM
- All fields from composer portal (§4.1)
- Activity log: emails sent/opened, briefs matched, tracks pitched, placements, payments
- Stage view: pipeline stages Applied → Vetting → Active → Brief-Matched → Placed → Alumni
- Bulk actions: advance stage, send sequence touch, export

#### Supervisor CRM
```
supervisor_id (uuid)
name (string)
company (string)
role (string)
location (string)
email (string)
linkedin_url (url)
relationship_stage (enum): cold | contacted | demo_booked | demo_attended | active | repeat
briefs_submitted (int)
placements_made (int)
last_contact_at (timestamp)
notes (text)
```

- Activity log: outreach sequence status, briefs submitted, tracks accepted, placements
- Relationship stage progression with timestamps

---

### 4.6 Placement & Payment Tracking

**Purpose:** Log every placement, manage licensing, and process payments.

```
placement_id (uuid)
brief_id (FK)
composer_id (FK)
supervisor_id (FK)
track_id (FK)
production_title (string)
production_type (enum)
license_type (enum): sync | master | sync_and_master
fee_gross (decimal)
syncmaster_commission (decimal)       # configurable %, default 20%
composer_payout (decimal)
currency (string)
status (enum): negotiating | confirmed | invoiced | paid | disputed
licensed_at (timestamp)
paid_at (timestamp)
contract_url (url)
notes (text)
```

**Payment workflow:**
1. Placement confirmed → contract generated
2. Invoice sent to supervisor/production company
3. Payment received → composer payout triggered
4. PRO royalties: log registration, track performance royalty income separately

---

### 4.7 Admin Dashboard

**Purpose:** Operational control centre for the SyncMaster team.

**KPI Strip (real-time):**
- Composers in pipeline (by stage)
- Active briefs (received / in curation / delivered)
- Placements this month
- Revenue this month
- Average brief-to-delivery time

**Views:**
- Composer pipeline (kanban by stage)
- Brief log (table with filters: status, production type, deadline)
- Supervisor tracker (list view + detail)
- Sequence status (per-sequence health metrics)
- Placement log (table with revenue summary)
- Payment queue (outstanding payouts)

---

## 5. Technical Architecture

### Stack Recommendation

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | Next.js (App Router) | SSR for SEO on public pages, React for admin SPA |
| Styling | Tailwind CSS + existing CSS variables | Preserve existing design system |
| Backend | Next.js API routes + tRPC | Type-safe API, minimal surface area |
| Database | PostgreSQL (Supabase) | Relational data, auth included, row-level security |
| Auth | Supabase Auth | Email + OAuth, role-based access (composer / supervisor / admin) |
| File storage | Supabase Storage | Track files, stems, rights docs, contracts |
| Email | Resend | Transactional email, sequence delivery |
| AI (repurposing) | Claude API (claude-sonnet-4-6) | Brand-voice-aware content generation |
| Deployment | Vercel | Existing deploy target, zero-config |
| Payments | Stripe | International payments, SyncMaster commission split |

### Data Architecture — Key Relationships

```
Composer ──────────────────── Tracks (1:many)
    │                              │
    │                         BriefMatch (many:many via Brief)
    │                              │
Placement ◄──────────── Brief ────┤
    │                    │
Supervisor ─────────────┘
    │
OutreachContact ──── SequenceEnrollment ──── TouchLog
```

### Row-Level Security (Supabase)
- Composer: read/write own record + tracks only
- Supervisor: read own briefs + delivered curated packs only
- Admin: full access all tables

---

## 6. Build Phases

### Phase 1 — Foundation (Weeks 1–4)
**Goal:** Database up, auth working, composer application flow live

| Task | Priority |
|---|---|
| Supabase project setup — tables, RLS policies | P0 |
| Auth: email + Google OAuth, role assignment | P0 |
| Composer application form (public) | P0 |
| Composer onboarding checklist (authenticated) | P0 |
| Admin vetting queue (basic list + status toggle) | P0 |
| Triggered onboarding email sequence (Resend) | P0 |
| Track + metadata upload UI | P1 |
| Stems upload per track | P1 |

### Phase 2 — Brief System (Weeks 5–8)
**Goal:** End-to-end brief → curation → delivery working

| Task | Priority |
|---|---|
| Supervisor invite + auth | P0 |
| Brief submission form | P0 |
| Admin curation interface (search catalogue, select 5) | P0 |
| Brief delivery portal (supervisor-facing) | P0 |
| Brief status tracking | P0 |
| SLA timer + admin alert at 36h | P1 |
| Track preview player | P1 |
| Rights doc download | P1 |

### Phase 3 — CRM + Outreach (Weeks 9–12)
**Goal:** Manual sequences replaced with triggered automation

| Task | Priority |
|---|---|
| Composer CRM (stage view + activity log) | P0 |
| Supervisor CRM (contact list + detail) | P0 |
| Sequence engine: enrollment, touches, tracking | P0 |
| All 5 sequences live in Resend | P0 |
| Unsubscribe handling | P0 |
| Sequence analytics dashboard | P1 |

### Phase 4 — Placement + Payments (Weeks 13–16)
**Goal:** Placement confirmed → invoice sent → composer paid

| Task | Priority |
|---|---|
| Placement log | P0 |
| Contract generation (PDF) | P0 |
| Stripe Connect for composer payouts | P0 |
| Invoice generation | P0 |
| PRO royalty logging | P1 |
| Revenue dashboard | P1 |

### Phase 5 — Content OS (Weeks 17–20)
**Goal:** Content Bank, Repurposing Engine, and Calendar live

| Task | Priority |
|---|---|
| Content Bank CRUD | P0 |
| Source Content module (markdown editor) | P0 |
| Repurposing Engine (Claude API integration) | P0 |
| Calendar UI (weekly view + drag-and-drop) | P0 |
| Auto-scheduling logic | P0 |
| Standalone content (quick post) | P1 |
| Automation webhook (trigger external scheduler) | P1 |

### Phase 6 — Admin Dashboard + Measurement (Weeks 21–24)
**Goal:** Full operational visibility, KPI tracking live

| Task | Priority |
|---|---|
| Admin dashboard (all KPI strips) | P0 |
| Composer pipeline kanban | P0 |
| Brief log table | P0 |
| Sequence status overview | P0 |
| Measurement page (L4) — open rates, reply rates, application conversion, placement rate | P0 |
| Growth Loops page (L5) — referral mechanics, community flywheel | P1 |

---

## 7. Design System

Carry the existing design system into the platform build.

```css
--bg:       #0C0C10     /* Page background */
--gold:     #F2C94C     /* Composer primary / cold outreach accent */
--coral:    #F26B5E     /* Composer onboarding / urgent */
--teal:     #38D1B5     /* Newsletter / active status */
--purple:   #9B72F2     /* Producer cold / vetting stage */
--mid:      #C0C0D0     /* Producer post-demo / body text */
--green:    #4CAF80     /* Placed status */
--muted:    #787890     /* Secondary text */
```

**Typography:** Syne 800 (display/headings) · DM Sans 300/400/500 (body)

**Pipeline stage colours:**
- Applied: gold
- Vetting: purple
- Active: teal
- Brief-Matched: coral
- Placed: green
- Alumni: muted

**Status badge classes (carry forward from current HTML):**
`status--placed | status--pending | status--no-fit | status--active | status--cold | status--paused | status--repeat | status--scheduled`

---

## 8. Migration Plan

The current static HTML Marketing OS remains live during the build.

| Current asset | Migration action |
|---|---|
| `index.html` (Strategy Deck) | Keep as-is — reference, not data |
| `content-pillars.html` | Keep as-is — reference |
| `playbooks.html` | Keep as-is — reference |
| Outreach System data sections | Move to admin dashboard (Phase 3) |
| Content Calendar (static) | Replace with Content OS module (Phase 5) |
| Copy banks M1/M2/M3 | Archive — content migrated to Content Bank |
| Composer pipeline (HTML) | Replace with live CRM kanban (Phase 3) |
| Brief log (HTML) | Replace with brief management system (Phase 2) |

The static pages act as the working spec until each module goes live. No content is lost — it becomes seed data.

---

## 9. Success Metrics

| Metric | Month 3 baseline | Month 6 target | Month 12 target |
|---|---|---|---|
| Vetted composers | 9 | 25 | 50 |
| Briefs per month | 5 | 12 | 30+ |
| Average brief-to-delivery | 31h | 24h | ≤18h |
| Placement rate | ~40% | 50% | 60%+ |
| Composer application → active rate | TBD | 40% | 50% |
| Rights issues per placement | 0 | 0 | 0 |
| Monthly GMV (placement fees) | $0 tracked | $10K+ | $50K+ |
| Sequence open rate (cold) | Baseline | 35%+ | 40%+ |
| Sequence reply rate (cold) | Baseline | 12%+ | 15%+ |

---

## 10. Open Questions

1. **Payment split mechanics** — Is the default 20% SyncMaster commission confirmed? Any tier structure for top composers?
2. **Supervisor verification** — What's the verification process for invite-only supervisor access? Manual review or form-based?
3. **PRO registration** — Does SyncMaster assist with PRO registration (SAMRO, MCSK, PRS, ASCAP) as part of onboarding, or is this composer-managed?
4. **Brief exclusivity** — When a brief is in curation, is the catalogue locked from other brief matches, or can a track be in multiple active briefs simultaneously?
5. **Contract templates** — Are sync license + master use contracts being drafted independently, or will a legal template library be part of Phase 4?
6. **Mobile app** — Is a native mobile app in scope (Phase 2+) for composer notifications on brief matches?
7. **AI guardrails for repurposing** — What level of brand voice enforcement is required for Claude-generated content variations? Human review required before scheduling?
