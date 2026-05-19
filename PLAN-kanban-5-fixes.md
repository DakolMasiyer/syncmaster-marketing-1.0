# PLAN: Kanban Calendar — 5 Missing Fixes

## Status
All 5 fixes are CONFIRMED MISSING from the feature branch `claude/syncmaster-content-calendar-XXeSQ`.
Verified by direct code inspection on 2026-05-19. Safe to implement — no double work.

## File to Edit
`/home/user/syncmaster-marketing-1.0/syncmaster-content-calendar.html`

---

## Fix 1 — Pillar label on chips
**Confirmed missing:** `lbl.textContent = post.type` (line ~1660), no `PILLAR_ABBR` constant exists.

Add after the `PILLAR_CLASS` constant (~line 1541):
```js
const PILLAR_ABBR = {
  'Education':'Edu','Proof':'Proof','Behind the Scenes':'BTS','Culture':'Culture','Industry':'Ind'
};
```

Change `buildChip` label line (~line 1660):
```js
lbl.textContent = post.type + ' · ' + (PILLAR_ABBR[post.pillar] || post.pillar);
```

---

## Fix 2a — Simplify status to 3 stages (To Do / In Progress / Done)
**Confirmed missing:** Modal still has 5 options (idea/draft/designed/scheduled/posted).

Replace modal `<select>` options (lines 237–242):
```html
<option value="todo">○ To Do</option>
<option value="inprogress">◐ In Progress</option>
<option value="done">● Done</option>
```

Replace status select CSS (lines 133–137):
```css
.status-select[data-status="todo"]       { color: var(--muted); }
.status-select[data-status="inprogress"] { color: var(--gold);   border-color: rgba(242,201,76,0.3); }
.status-select[data-status="done"]       { color: var(--green);  border-color: rgba(76,175,128,0.3); }
```

Update `loadState()` to bump key to `syncmaster_cal_v3` and migrate v2 values:
```js
const STORAGE_KEY = 'syncmaster_cal_v3';
// After loading, migrate old values:
const V2_MAP = { idea:'todo', draft:'todo', designed:'inprogress', scheduled:'inprogress', posted:'done' };
Object.keys(state.statuses).forEach(id => {
  if (V2_MAP[state.statuses[id]]) state.statuses[id] = V2_MAP[state.statuses[id]];
});
```

Update `updateProgress()` to count `done` instead of `posted`.
Update `openModal()` default status fallback to `'todo'`.

---

## Fix 2b — Status left-border on chips
**Confirmed missing:** No `btn.dataset.status` in `buildChip`, no `.post-chip[data-status]` CSS.

In `buildChip`, add before `return btn`:
```js
btn.dataset.status = state.statuses[post.id] || 'todo';
```

Add to `.post-chip` CSS rule (~line 74): `border-left: 2px solid transparent;`

Add after `.post-chip` rule:
```css
.post-chip[data-status="todo"]       { border-left-color: var(--muted); }
.post-chip[data-status="inprogress"] { border-left-color: var(--gold); }
.post-chip[data-status="done"]       { border-left-color: var(--green); opacity: 0.7; }
```

---

## Fix 3 — Content Pillars Guide milestone card
**Confirmed missing:** No `MILESTONE-CPG` in POSTS array.

Add to start of POSTS array (before Jun 1 block):
```js
{ id:'MILESTONE-CPG', date:'2026-05-31', platform:'Blog', pillar:'Behind the Scenes',
  type:'Article', topic:'Content Pillars Guide published',
  persona:'Both', hook:'Month 1 planning foundation — content pillars, platform strategy, and copy bank.' },
```

Add to COPY object:
```js
'MILESTONE-CPG': { body: `Content Pillars Guide published at syncmaster.io/content-pillars.\n\nCovers: 5 content pillars, platform channel strategy, persona profiles (Tunde & Amara), and the Month 1 copy bank.\n\nThis document is the planning foundation for all Month 1 content.`, cta: null },
```

In `loadState()`, after `POSTS.forEach` defaults, force status to done:
```js
state.statuses['MILESTONE-CPG'] = 'done';
```

---

## Fix 4 — Month 2 July 2026 posts + Copy Bank
**Confirmed missing:** POSTS array ends at 2026-06-30, no July posts exist.

Append 39 posts to POSTS array after the Jun 30 entry. July 1 = Wednesday.

| ID | Date | Platform | Type | Pillar | Topic |
|---|---|---|---|---|---|
| IG-M2-EDU-01 | Jul 1 | Instagram | Carousel | Education | The sync deal checklist — what to negotiate |
| IG-M2-EDU-02 | Jul 2 | Instagram | Carousel | Education | Publishing rights: what composers give up without knowing |
| TW-M2-SOLO-01 | Jul 3 | Twitter/X | Tweet | Industry | The sync rights every African composer must understand |
| IG-M2-PROOF-01 | Jul 4 | Instagram | Single | Proof | Composer 2 placement confirmed |
| YT-M2-01 | Jul 5 | YouTube | Video | Education | Sync deal negotiation walkthrough |
| BLOG-M2-01 | Jul 6 | Blog | Blog | Education | Advanced sync licensing: how to negotiate your first deal |
| LI-M2-01 | Jul 6 | LinkedIn | Article | Education | What composers get wrong about sync deal terms |
| TW-M2-01 | Jul 6 | Twitter/X | Thread | Education | Sync deal terms explained for independent composers |
| IG-M2-EDU-03 | Jul 7 | Instagram | Carousel | Education | How to build a sync-ready catalogue from scratch |
| TW-M2-SOLO-02 | Jul 8 | Twitter/X | Tweet | Education | The 3 documents every sync-ready composer needs |
| IG-M2-EDU-04 | Jul 9 | Instagram | Carousel | Education | What "one-stop" really means — and how to get there |
| IG-M2-PROOF-02 | Jul 10 | Instagram | Single | Proof | Brief received: this is what it looked like |
| TW-M2-SOLO-03 | Jul 11 | Twitter/X | Tweet | Culture | African composers are winning sync placements. Here's how they did it |
| IG-M2-BTS-01 | Jul 12 | Instagram | Single | Behind the Scenes | Week 2 of Month 2 — behind the scenes |
| BLOG-M2-02 | Jul 13 | Blog | Blog | Proof | Month 2: briefs, pitches, and placements so far |
| LI-M2-02 | Jul 13 | LinkedIn | Article | Proof | What Month 2 is teaching us about the sync market |
| TW-M2-02 | Jul 13 | Twitter/X | Thread | Proof | Month 2 update — here's what's happened so far |
| IG-M2-EDU-05 | Jul 14 | Instagram | Carousel | Education | PRO registration: which societies African composers should join |
| TW-M2-SOLO-04 | Jul 15 | Twitter/X | Tweet | Education | Your PRO registration determines whether you get paid from placements |
| IG-M2-EDU-06 | Jul 16 | Instagram | Carousel | Education | Metadata deep dive — every tag that matters |
| IG-M2-PROOF-03 | Jul 17 | Instagram | Single | Proof | Month 2 placement update |
| TW-M2-SOLO-05 | Jul 18 | Twitter/X | Tweet | Industry | The sync market is moving faster than most composers realise |
| IG-M2-BTS-02 | Jul 19 | Instagram | Single | Behind the Scenes | What a brief response week looks like inside SyncMaster |
| BLOG-M2-03 | Jul 20 | Blog | Blog | Culture | The African composer's playbook for international sync |
| LI-M2-03 | Jul 20 | LinkedIn | Article | Culture | Why African music is becoming the default sound of global campaigns |
| TW-M2-03 | Jul 20 | Twitter/X | Thread | Culture | African music is shaping global culture — and the money is following |
| IG-M2-EDU-07 | Jul 21 | Instagram | Carousel | Education | The composer audit: 6 things to fix before you pitch |
| TW-M2-SOLO-06 | Jul 22 | Twitter/X | Tweet | Education | Fix these 6 things before you send your next supervisor pitch |
| IG-M2-EDU-08 | Jul 23 | Instagram | Carousel | Education | What great stems look like — the technical spec |
| IG-M2-PROOF-04 | Jul 24 | Instagram | Single | Proof | Placement story — from brief to signed |
| TW-M2-SOLO-07 | Jul 25 | Twitter/X | Tweet | Culture | The African composers changing what global film sounds like |
| IG-M2-BTS-03 | Jul 26 | Instagram | Single | Behind the Scenes | Week 4 of Month 2 — where we are |
| BLOG-M2-04 | Jul 27 | Blog | Blog | Behind the Scenes | Month 2 mid-point: what we built and what's coming |
| LI-M2-04 | Jul 27 | LinkedIn | Article | Behind the Scenes | Building SyncMaster Month 2: what's changed |
| TW-M2-04 | Jul 27 | Twitter/X | Thread | Behind the Scenes | Mid-Month 2 update — the full breakdown |
| YT-M2-02 | Jul 28 | YouTube | Video | Education | Composer audit walkthrough — is your catalogue sync-ready? |
| TW-M2-SOLO-08 | Jul 29 | Twitter/X | Tweet | Industry | Month 2 numbers update |
| IG-M2-PROOF-05 | Jul 30 | Instagram | Single | Proof | Month 2 placement summary |
| IG-M2-WRAP | Jul 31 | Instagram | Single | Behind the Scenes | Month 2 complete. Month 3 incoming. |

**Carousel run check:** Jul 1–2 = 2 in a row (Tweet on Jul 3 breaks it). Jul 7, 9 = separated by Tweet. Jul 14, 16 = separated by Tweet. Jul 21, 23 = separated by Tweet. All clear — no run > 2.

Add COPY stubs for all 39 July posts. Format:
```js
'BLOG-M2-01': { body: `[Month 2 Blog — Advanced sync licensing: how to negotiate your first deal\n\n→ Publish at syncmaster.io/blog]`, cta: null },
'IG-M2-EDU-01': { body: `The sync deal checklist.\n\nMost composers accept the first offer. Here's what to push back on — and why. ↓\n\n[Full carousel copy — Month 2]`, cta: 'Save this before your next deal conversation.' },
```
Same stub pattern for all 39 IDs.

---

## Fix 5 — Break 4-consecutive-carousel run on Jun 11
**Confirmed missing:** `IG-EDU-04` at line 1460 still has `type:'Carousel'`.

Change to:
```js
type:'Single'
```

Result: Jun 9 Carousel → Jun 10 Carousel → Jun 11 **Single** → Jun 12 Carousel. No run > 2.

---

## Verification Checklist
1. June 2026 chips show `Type · Pillar` (e.g. "Carousel · Edu")
2. Chips have coloured left border: grey=To Do, gold=In Progress, green=Done
3. Status dropdown shows 3 options only: To Do / In Progress / Done
4. Status change → chip border updates immediately
5. Navigate to May 2026 → MILESTONE-CPG card appears with green Done border
6. Navigate to July 2026 → full 31-day July grid renders
7. Jun 9–12: Carousel, Carousel, **Single**, Carousel
8. July: no carousel run longer than 2 consecutive days
9. localStorage key = `syncmaster_cal_v3`
