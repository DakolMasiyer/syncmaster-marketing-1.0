# Monthly Newsletter Template (Tunde — Cold/Warm List)

## Overview
Parameterised monthly digest sent to composers who completed the cold outreach sequence
without applying. One email per month. One job: keep the relationship warm and convert
at the moment they're ready.

**Trigger condition:** Composer received cold outreach Email 3 with no application. Added
to newsletter list. Receives this on the 1st of each month thereafter.
**Entry point:** Tunde knows what sync is, knows what SyncMaster does, has seen payment
numbers. He hasn't taken the step. Either the timing wasn't right, or trust isn't there yet.
**List segmentation:** Two versions — Standard (< 90 days on list, or recent open/click)
and Re-engagement (90+ days, no open or click in 60+ days).

---

## Sequence Overview

```
Sequence Name:   SyncMaster Monthly Digest
Trigger:         No application after cold sequence Email 3
Goal:            Application submitted (or list health maintained)
Length:          Ongoing monthly — no fixed endpoint
Timing:          1st of each month, send at 9am local time (B2B rule: avoid weekends)
Exit Conditions: Composer applies → exits to onboarding sequence
                 Composer unsubscribes → removed immediately
                 Re-engagement Version B sent twice with no open → suppress from list
```

---

## Version A — Standard Monthly

**Audience:** Composers < 90 days on list, OR recent open/click in last 60 days
**Tone:** Behind the Scenes (honest, operational) + Proof (specific, credible)
**Length target:** 200–280 words

---

### Email A: Standard Monthly Digest

```
Send:    1st of [MONTH], 9am local
Subject: [MONTH_SHORT]: [ONE_LINE_PROOF_HOOK]
Preview: [EDUCATION_TIP_TEASE] — and applications for [NEXT_MONTH] are open.
```

**Subject line examples (fill [MONTH_SHORT] and [ONE_LINE_PROOF_HOOK]):**

| Month | Hook | Full subject |
|---|---|---|
| July | 2 placements confirmed | "Jul: 2 placements confirmed" |
| August | fastest placement yet — 11 hours | "Aug: fastest placement yet — 11 hours" |
| September | 3 new markets, 1 brief waiting | "Sep: 3 new markets, 1 brief waiting" |

Rule: subject line is the proof number. Preview text is the education tip tease + CTA hint.
40–55 characters. No punctuation tricks. Reads like an internal update.

---

**Body template:**

```
[MONTH] update.

[PLACEMENT_STORY — 100 words max]

[COMPOSER_FIRST_NAME] had [CATALOGUE_STATE_BEFORE — e.g. "no ISRC codes on half his
catalogue and stems only for 3 tracks"]. He went through onboarding in [DAYS] days.
[WEEKS] weeks later, his track was shortlisted for [BRIEF_DESCRIPTION — e.g. "a
45-second open for a global NGO campaign"]. It placed. [PLACEMENT_FEE_RANGE or
"Upfront fee, plus performance royalties every time the content airs."]

What he fixed before he was eligible: [2–3 BULLET POINTS from his onboarding — e.g.
ISRC registration, cleared a sample, packaged stems for 8 tracks]

This month's tip: [EDUCATION_TIP — 80 words max]

[ONE_ACTIONABLE_STEP. Something that takes under 30 minutes. Directly addresses one
of the 6 sync-ready checklist items from Email 3. e.g.:

"Check your distributor dashboard right now — if any track shows 'ISRC pending' or
blank, email them today to assign codes. Takes 5 minutes to request. Takes 48 hours
to receive. Do it before you need it."]

Applications for [NEXT_MONTH] are open.
→ [APPLICATION_LINK]

[SIGN_OFF]
SyncMaster

---
You're getting this because you asked about sync licensing.
[Unsubscribe] · [Update preferences]
```

---

### Content token guide

| Token | What to fill | Source |
|---|---|---|
| `[MONTH]` | Full month name (e.g. "July 2026") | Calendar |
| `[MONTH_SHORT]` | Abbreviated (e.g. "Jul") | Calendar |
| `[NEXT_MONTH]` | Following month name | Calendar |
| `[PLACEMENT_STORY]` | One real composer placement that month | Proof pillar content — pull from copy-bank-m2/m3 IG-PROOF posts |
| `[COMPOSER_FIRST_NAME]` | First name only — no surname | Active composer roster |
| `[CATALOGUE_STATE_BEFORE]` | Their specific onboarding gap | Onboarding records |
| `[DAYS]` | Their actual onboarding duration | Onboarding records |
| `[WEEKS]` | Time from go-live to brief match | Brief records |
| `[BRIEF_DESCRIPTION]` | The actual brief type | Brief log |
| `[PLACEMENT_FEE_RANGE]` | Directional only — not exact if confidential | Approved disclosure |
| `[EDUCATION_TIP]` | One actionable step from Education pillar | copy-bank-m2/m3 Education posts |
| `[APPLICATION_LINK]` | Live application form URL | syncmaster.io |

**Content sourcing rule:** The Proof story and Education tip should come directly from
that month's content calendar posts (copy-bank-m2 or copy-bank-m3). Do not write fresh
copy from scratch — repurpose what was already published. The newsletter is a delivery
mechanism for content Tunde may have missed on social.

---

## Version B — Re-engagement Variant

**Audience:** Composers 90+ days on list with no open or click in 60+ days
**Trigger:** 90-day mark from list entry AND no open/click in 60 days
**Tone:** Direct, no pretence — acknowledges the gap, gives them an exit or a reason to stay
**Length target:** 120–160 words (shorter than standard — earn attention before giving content)
**Send:** Replace their next standard monthly with this. If no response, send Version B once
more 30 days later. If still no response: suppress from list (do not delete — retain for
manual re-activation if they reach out).

---

### Email B1: Re-engagement Check-in

```
Send:    Their next scheduled monthly send date
Subject: still interested in sync?
Preview: Here's what's changed in the last 3 months — and a quick way to tell us either way.
```

**Body:**

```
You signed up a few months ago. We haven't heard from you since.

That's fine — timing matters in this. But we want to make sure we're
sending you something worth opening.

Here's what's happened since you signed up:

→ [N] composers vetted and active in the catalogue
→ [N] placements confirmed across Months [X]–[Y]
→ Fastest brief-to-delivery: [N] hours
→ [N] music supervisors reached out via content alone

If sync is still on your radar: applications for [NEXT_MONTH] are open.
→ [APPLICATION_LINK]

If the timing isn't right, no problem — you can unsubscribe below and
we'll remove you cleanly. No hard feelings, no follow-up.

[SIGN_OFF]
SyncMaster

---
[Unsubscribe] · [Update preferences]
```

---

### Email B2: Last touch (30 days after B1, no open/click)

```
Send:    30 days after B1 if no open or click
Subject: last one from us
Preview: Unsubscribe below or reply to stay — either way, we'll respect it.
```

**Body:**

```
This is the last email we'll send unless you want to stay on the list.

If sync licensing is still something you're working toward:
→ [APPLICATION_LINK]

If not, unsubscribe below. We'll remove you immediately.

[SIGN_OFF]
SyncMaster

---
[Unsubscribe] · [Update preferences]
```

*After B2 with no action: suppress from automated sends. Tag as "dormant — manual only."
Re-activate only if they engage with organic content or reach out directly.*

---

## Metrics Plan

| Metric | Version A target | Version B target |
|---|---|---|
| Open rate | >42% (warm list, specific subject) | >25% (dormant list) |
| Click rate | >8% (application link) | >5% (any link) |
| Application conversion | >4% of opens | >2% of opens |
| Unsubscribe rate | <1% per send | <8% (acceptable — list cleaning) |
| List health (monthly) | Track open rate trend — if drops below 30%, review subject lines | Track suppression rate — target: clean 10–15% dormant per quarter |

---

## Implementation Notes

### Send day and time:
- 1st of month, Tuesday–Thursday only
- 9am in the composer's local timezone where known; default to Lagos time (WAT, UTC+1)
  for the African composer list
- Avoid: Mondays (inbox competition), Fridays (low engagement), weekends

### Personalisation minimum:
- `[First Name]` in opening line — not in subject line (cold-email rule: no names in subject)
- Proof story composer name: first name only, with their explicit consent to be named

### Repurposing rule:
The newsletter should never require fresh copy. Every month's Proof story and Education
tip already exists in the copy bank (copy-bank-m2.html, copy-bank-m3.html). The newsletter
editor's job each month: pick the strongest Proof post + one Education post → drop into
template → personalise tokens → send. Total prep time per month: under 30 minutes.

### List hygiene:
- Suppress after B2 with no action — do not delete, do not re-enter into automated sends
- Review suppressed list quarterly — manually re-activate if they engage with content elsewhere
- Hard bounces: remove immediately
- Soft bounces: retry twice, then suppress

### Tool recommendation (from emails skill):
- **Kit** (formerly ConvertKit) — best fit for a creator/independent composer audience,
  supports tagging, conditional sends, and the B1/B2 suppression logic natively
- **Mailchimp** — viable alternative if already in use; segments and automation handle
  the Version A/B split without custom code
