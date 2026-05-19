# PLAN: Phase 2 Next Steps — Skills-Informed Execution

## Status
**Date:** 2026-05-19
**Completed:** `playbook-composer-onboarding.md` ✅
**Remaining:** 2 sequences + 1 copy pass + HTML build

---

## Why the Skills Matter Here

All 4 relevant skills (`cold-email`, `emails`, `sales-enablement`, `copywriting`) check for
`.agents/product-marketing.md` before asking questions. That file already exists and contains:
- Full Tunde + Amara persona profiles
- Positioning, proof points, and brand voice
- Platform strategy and content pillars

This means each skill loads with full SyncMaster context automatically — no re-briefing needed.
The skills add structure and best-practice guardrails on top of the existing source material.

---

## Step 2 — Write `playbook-producer-post-demo.md`

**Skill to invoke:** `cold-email`
**Why cold-email, not emails:** This is a 2-touch follow-up sequence after a warm event (demo).
The tone is peer-to-peer, short, low-friction — exactly what cold-email optimises for.
The `emails` skill is better suited for longer nurture sequences with more automation logic.

**What cold-email adds here:**
- Interest-based CTA structure ("Worth running a brief through us?" beats "Book a follow-up call")
- "Peer not vendor" framing — Amara is a professional, not a warm lead to be nurtured
- Ruthless brevity: post-demo messages should be shorter than the cold sequence, not longer
- Personalization that connects to what was shown in the demo, not generic follow-up copy

**Inputs already available (no questions needed):**
- Amara persona: `persona-cards.md` + `.agents/product-marketing.md`
- Proof points: Month 2 metrics (31h brief-to-delivery, 5h rights, 0 rights issues)
- Demo content: producer sequence Message 3 shows exact workflow that was demonstrated
- Objections to address post-demo: "I already have go-to sources" + "Is quality really there?"

**Sequence spec:**
| Touch | Day | Channel | Goal |
|---|---|---|---|
| 1 | Day 1 | LinkedIn message | Demo recap + one concrete takeaway they can use now |
| 2 | Day 5 | Email | First live brief invitation — low-barrier, specific ask |

**Trigger:** Demo attended (Amara booked and showed up to the 15-min demo)
**Outcome:** Amara sends first brief through SyncMaster, or opts into trial basis

---

## Step 3 — Write `playbook-newsletter-monthly.md`

**Skill to invoke:** `emails`
**Why emails:** This is a lifecycle/nurture asset — a parameterised template for a monthly
digest sent to a cold-to-warm Tunde list. The `emails` skill is built for this: sequence
structure, one-email-one-job principle, segmentation logic, and re-engagement mechanics.

**What emails adds here:**
- "One email, one job" discipline — prevents the newsletter from trying to do too much
- Value-before-ask structure — proof story first, education tip second, CTA last
- Personalisation token patterns for a parameterised template
- Re-engagement variant: a separate version for composers who've been on the list 3+ months
  without clicking anything

**Inputs already available:**
- Tunde persona: `persona-cards.md` + `.agents/product-marketing.md`
- Proof content: the Proof pillar posts in copy-bank-m2/m3 are ready-made newsletter proof stories
- Education content: Education pillar posts are ready-made tips
- Trigger: "no reply after Email 3 in cold sequence → add to monthly newsletter list"

**Template spec:**
```
Subject: [MONTH] update — [ONE_LINE_PROOF_HOOK]

Section 1 — Proof story (150 words max)
  "[COMPOSER_NAME] went from [BEFORE] to [PLACEMENT_RESULT] in [TIMEFRAME]."
  What they fixed. What happened next.

Section 2 — Education tip (100 words max)
  One actionable thing: a metadata fix, a rights step, a brief-prep task.
  Takes under 30 minutes to implement.

Section 3 — CTA (1 sentence)
  "Applications for [MONTH+1] are open — [link]."
  OR re-engagement variant: "Still interested? Here's what's changed since you signed up."

Footer — Unsubscribe + "Why you're getting this" (compliance)
```

**Deliverable:** One master template + one re-engagement variant for 3-month cold subscribers

---

## Step 4 — Copywriting Pass (all 5 sequences)

**Skill to invoke:** `copywriting`
**When:** After both sequences are written, before HTML build
**Scope:** All 5 playbook MD files — tighten body copy before it's committed to HTML

**What copywriting adds here:**
- Specificity audit: flag any vague claims ("we move fast" → "31 hours brief-to-delivery")
- Customer language check: confirm Tunde and Amara's own words are reflected, not marketing-speak
- CTA clarity: every email ends with one action — verify none have multiple asks
- First-line audit: each email's opening line is the most important — the skill will pressure-test them

**Note:** The composer onboarding sequence (`playbook-composer-onboarding.md`) was written
without this pass. Include it in Step 4 scope even though it's already "done."

---

## Step 5 — Build `playbooks.html`

**Skill to invoke:** `sales-enablement`
**Why sales-enablement:** The playbooks page is sales collateral — it needs to be scannable,
situation-specific, and tied to business outcomes. Sales-enablement is built for exactly
this: reps need to find information in 3 seconds, and the page must work as a reference
during actual outreach, not just as a document to read once.

**What sales-enablement adds here:**
- Scannable-over-comprehensive principle → drives the expandable card pattern (overview visible,
  full body hidden behind `<details>`) rather than walls of text
- "Situation-specific" principle → the funnel map and trigger badges become load-bearing,
  not decorative — they tell a rep exactly which sequence applies to their situation
- Objection card component pattern → the objection-handling-guide content gets its own
  scannable format: Objection → Why they say it → Response → Proof → Question
- Outcome blocks → each sequence ends with a clear "what success looks like" block,
  not just a metrics table

**Template base:** `content-pillars.html` (structure), `copy-bank-m2.html` (copy button component)
**Accent colours:** Gold (Composer cold) · Coral (Composer onboarding) · Teal (Newsletter) ·
                    Purple (Producer cold) · Mid/grey (Producer post-demo)

---

## Execution Order (revised)

| Step | Action | Skill | Output |
|---|---|---|---|
| ✅ 1 | Write composer onboarding sequence | — (source material sufficient) | `playbook-composer-onboarding.md` |
| 2 | Write producer post-demo sequence | `cold-email` | `playbook-producer-post-demo.md` |
| 3 | Write monthly newsletter template | `emails` | `playbook-newsletter-monthly.md` |
| 4 | Copywriting pass — all 5 sequences | `copywriting` | Updated MD files |
| 5 | Build `playbooks.html` | `sales-enablement` | `playbooks.html` |
| 6 | Update siteNav in 3 files | — | `index.html`, `content-pillars.html`, `content-calendar.html` |
| 7 | Push to main + verify live | — | Live at `/playbooks.html` |

---

## What to Skip

- `copy-editing` skill — overlaps with `copywriting` pass in Step 4; one pass is enough
- `onboarding` skill — this is an email sequence, not in-app onboarding; `emails` is correct
- `product-marketing` skill — `.agents/product-marketing.md` already exists; no rebuild needed
- `social` skill — not relevant to playbooks (content calendar work is separate)
