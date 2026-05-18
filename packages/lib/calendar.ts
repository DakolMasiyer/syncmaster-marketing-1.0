export type Platform = "linkedin" | "instagram" | "tiktok" | "youtube" | "newsletter";
export type ContentType = "repurposed" | "standalone";

export type CalendarItem = {
  id: string;
  sourceContentId?: string;
  repurposedContentId?: string;
  standaloneContentId?: string;
  contentType: ContentType;
  platform: Platform;
  title: string;
  content: string;
  caption?: string;
  publishDate: string;
  publishTime?: string;
  status: "scheduled" | "posted" | "draft" | "failed";
  tags: string[];
  automationLink?: string;
  createdAt: string;
  updatedAt: string;
};

const scheduleMap: Record<Platform, number> = {
  linkedin: 2,
  instagram: 3,
  tiktok: 4,
  youtube: 5,
  newsletter: 0,
};

const uid = (prefix = "id") => `${prefix}_${Math.random().toString(36).slice(2, 10)}`;

export function assignDate(weekStartISO: string, dayIndex: number): string {
  const start = new Date(weekStartISO);
  const d = new Date(start);
  d.setUTCDate(start.getUTCDate() + dayIndex);
  return d.toISOString();
}

export function getNextAvailableWeek(existing: CalendarItem[], weekStartISO: string): string {
  const hasConflict = (startISO: string) => {
    const weeklySlots = new Set(Object.values(scheduleMap).map((d) => assignDate(startISO, d).slice(0, 10)));
    return existing.some((i) => weeklySlots.has(i.publishDate.slice(0, 10)));
  };

  let cursor = new Date(weekStartISO);
  while (hasConflict(cursor.toISOString())) {
    cursor.setUTCDate(cursor.getUTCDate() + 7);
  }
  return cursor.toISOString();
}

export function autoSchedule(repItems: Array<Partial<CalendarItem> & { platform: Platform; title: string; content: string }>, weekStartISO: string, existing: CalendarItem[] = []): CalendarItem[] {
  const week = getNextAvailableWeek(existing, weekStartISO);
  const occupied = new Set(existing.map((i) => i.publishDate.slice(0, 10) + i.platform));

  return repItems.map((item) => {
    let targetDate = assignDate(week, scheduleMap[item.platform]);
    let dateObj = new Date(targetDate);

    while (occupied.has(targetDate.slice(0, 10) + item.platform)) {
      dateObj.setUTCDate(dateObj.getUTCDate() + 7);
      targetDate = dateObj.toISOString();
    }
    occupied.add(targetDate.slice(0, 10) + item.platform);

    const now = new Date().toISOString();
    return {
      id: item.id ?? uid("cal"),
      sourceContentId: item.sourceContentId,
      repurposedContentId: item.repurposedContentId,
      standaloneContentId: item.standaloneContentId,
      contentType: item.contentType ?? "repurposed",
      platform: item.platform,
      title: item.title,
      content: item.content,
      caption: item.caption,
      publishDate: targetDate,
      publishTime: item.publishTime,
      status: "scheduled",
      tags: item.tags ?? [],
      automationLink: item.automationLink,
      createdAt: item.createdAt ?? now,
      updatedAt: now,
    };
  });
}

export function createStandaloneCalendarItem(input: {
  title: string;
  content: string;
  platform: Platform;
  publishDate: string;
  tags?: string[];
  caption?: string;
}): CalendarItem {
  const now = new Date().toISOString();
  return {
    id: uid("cal"),
    standaloneContentId: uid("standalone"),
    contentType: "standalone",
    platform: input.platform,
    title: input.title,
    content: input.content,
    caption: input.caption,
    publishDate: new Date(input.publishDate).toISOString(),
    status: "scheduled",
    tags: input.tags ?? [],
    createdAt: now,
    updatedAt: now,
  };
}

export async function triggerAutomation(calendarItemId: string, webhookUrl?: string): Promise<{ ok: boolean; status: number; calendarItemId: string }> {
  if (!webhookUrl) return { ok: false, status: 0, calendarItemId };
  const res = await fetch(webhookUrl, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ calendarItemId }),
  });
  return { ok: res.ok, status: res.status, calendarItemId };
}
