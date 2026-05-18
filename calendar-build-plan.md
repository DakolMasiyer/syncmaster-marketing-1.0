# Content Calendar — Build Plan & Gap Analysis

## Current State

The existing codebase is a **static HTML marketing website** (4 HTML files, no framework, no backend, localStorage only). The `content-calendar.html` is a read-only grid showing 44 pre-written content pieces across 8 tabs, with a basic status tracker (Not Used / Drafted / Posted). No interactive application logic exists.

---

## Gap Analysis: Module by Module

### 4.1 Content Bank (Ideas Layer) — 0% built

| Requirement | Status |
|---|---|
| CRUD for content ideas | Missing |
| Fields: id, title, description, themeTags[], funnelStage (awareness/engagement/conversion/retention), platformPotential[], status (idea/selected/archived), createdAt | Missing |
| Tag filtering | Missing |
| Search by title and tags | Missing |
| "Select idea → create source content" action | Missing |

---

### 4.2 Source Content Module — 0% built

| Requirement | Status |
|---|---|
| Long-form content creation (blog, podcast_script, video_script) | Missing |
| Fields: id, ideaId (optional FK), title, format, body (markdown), keyPoints[], hook, status (draft/in_review/published) | Missing |
| Markdown editor | Missing |
| Link to content idea | Missing |
| Save drafts / Publish toggle | Missing |
| "Generate repurposed content" button | Missing |

---

### 4.3 Repurposing Engine — ~5% built

| Requirement | Status |
|---|---|
| Auto-generate platform variations (LinkedIn, Instagram, TikTok, YouTube Shorts, Newsletter) | Missing |
| Fields: id, sourceContentId, platform, format, content, hook, cta, status | Missing |
| Editable outputs | Missing |
| Copy-to-clipboard | Partial (copy button on static cards only) |
| Regenerate variations button | Missing |

---

### 4.4 Content Calendar Module — ~10% built

| Requirement | Status |
|---|---|
| CalendarItem data model with full field set | Missing — only static DOM nodes |
| repurposedContentId, standaloneContentId, sourceContentId linkage | Missing |
| contentType: "repurposed" \| "standalone" | Missing |
| publishDate (ISO), publishTime, automationLink, createdAt, updatedAt | Missing |
| Weekly calendar view (day-by-day, platform labels) | Partial — static grid, no real date logic |
| Monthly calendar view | Missing |
| Drag and drop rescheduling | Missing |
| Auto-scheduling engine (autoSchedule()) | Missing |
| Conflict handling (move to next available day → next week) | Missing |
| packages/lib/calendar.ts logic file | Missing entirely |
| Editable fields: publishDate, platform, content, caption, tags | Missing |
| Per-item actions: copy content, copy caption, open source, open repurposed, send to automation | Missing |
| "Detached state" when linked content is removed | Missing |

---

### 4.5 Standalone Content Module — 0% built

| Requirement | Status |
|---|---|
| Quick post creation UI | Missing |
| Direct calendar insertion | Missing |
| Fields: id, title, content, platform, tags[], publishDate, status | Missing |
| Independent of source/repurposed content | N/A |

---

### Section 5 — Calendar Logic (packages/lib/calendar.ts) — 0% built

| Requirement | Status |
|---|---|
| autoSchedule(repItems, week) function | Missing |
| scheduleMap: linkedin→tuesday, instagram→wednesday, tiktok→thursday, youtube→friday, newsletter→sunday | Missing |
| assignDate(week, day) helper | Missing |
| getNextAvailableWeek() | Missing |
| createStandaloneCalendarItem() | Missing |
| triggerAutomation(calendarItemId) webhook | Missing |
| Conflict resolution logic | Missing |
| Dual stream separation (repurposed vs standalone) | Missing |

---

## Completion Summary

| Module | Completion |
|---|---|
| Content Bank (Ideas) | 0% |
| Source Content Module | 0% |
| Repurposing Engine | ~5% |
| Content Calendar Module | ~10% |
| Standalone Content Module | 0% |
| Calendar Logic (lib/calendar.ts) | 0% |

---

## Recommended Build Order

1. **CalendarItem data model + `packages/lib/calendar.ts`** — core types, `autoSchedule()`, `createStandaloneCalendarItem()`, conflict resolution, `triggerAutomation()`
2. **Content Bank** — CRUD for ideas, tag filtering, search, funnel stage
3. **Source Content Module** — markdown editor, draft/publish flow, link to idea
4. **Repurposing Engine** — platform variation generation, editable outputs, regenerate
5. **Calendar UI** — weekly/monthly views, drag-and-drop, per-item actions, edit modal
6. **Standalone Content Module** — quick post creation, direct calendar insertion

---

## Key Data Models (from spec)

```ts
type CalendarItem = {
  id: string;
  sourceContentId?: string;
  repurposedContentId?: string;
  standaloneContentId?: string;
  contentType: "repurposed" | "standalone";
  platform: "linkedin" | "instagram" | "tiktok" | "youtube" | "newsletter";
  title: string;
  content: string;
  caption?: string;
  publishDate: string; // ISO format
  publishTime?: string;
  status: "scheduled" | "posted" | "draft" | "failed";
  tags: string[];
  automationLink?: string;
  createdAt: string;
  updatedAt: string;
};
```

```ts
// packages/lib/calendar.ts
export function autoSchedule(repItems, week) {
  const scheduleMap = {
    linkedin: "tuesday",
    instagram: "wednesday",
    tiktok: "thursday",
    youtube: "friday",
    newsletter: "sunday",
  };

  return repItems.map((item) => ({
    ...item,
    publishDate: assignDate(week, scheduleMap[item.platform]),
    status: "scheduled",
  }));
}
```

## Weekly Default Distribution

| Day | Content Type |
|---|---|
| Monday | Source Content (optional publish) |
| Tuesday | LinkedIn insight post |
| Wednesday | Instagram content |
| Thursday | TikTok short form |
| Friday | YouTube content |
| Sunday | Newsletter / recap |

Manual override always allowed.
