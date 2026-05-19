# Graph Report - .  (2026-05-19)

## Corpus Check
- 7 files · ~50,668 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 19 nodes · 14 edges · 10 communities detected
- Extraction: 50% EXTRACTED · 50% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]

## God Nodes (most connected - your core abstractions)
1. `Content Calendar Module` - 5 edges
2. `Source Content Module` - 3 edges
3. `Repurposing Engine` - 3 edges
4. `Calendar Logic (packages/lib/calendar.ts)` - 3 edges
5. `CalendarItem data model` - 3 edges
6. `Content Bank (Ideas Layer)` - 2 edges
7. `Standalone Content Module` - 2 edges
8. `Core types and scheduling logic must be built first as they form the foundation for the calendar.` - 2 edges
9. `The Content Bank provides the ideas that feed into the source content and repurposing engines.` - 1 edges
10. `The Source Content Module creates the long-form content that is then repurposed.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Source Content Module` --shares_data_with--> `Repurposing Engine`  [INFERRED]
  calendar-build-plan.md → calendar-build-plan.md  _Bridges community 0 → community 3_
- `Repurposing Engine` --shares_data_with--> `Content Calendar Module`  [INFERRED]
  calendar-build-plan.md → calendar-build-plan.md  _Bridges community 3 → community 1_
- `Calendar Logic (packages/lib/calendar.ts)` --shares_data_with--> `Content Calendar Module`  [INFERRED]
  calendar-build-plan.md → calendar-build-plan.md  _Bridges community 1 → community 2_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.5
Nodes (4): Content Bank (Ideas Layer), The Content Bank provides the ideas that feed into the source content and repurposing engines., The Source Content Module creates the long-form content that is then repurposed., Source Content Module

### Community 1 - "Community 1"
Cohesion: 0.5
Nodes (4): Content Calendar Module, The Calendar UI allows users to interact with the scheduled content and make adjustments., The Standalone Content Module allows for quick posts that are not tied to the idea bank., Standalone Content Module

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (3): CalendarItem data model, Calendar Logic (packages/lib/calendar.ts), Core types and scheduling logic must be built first as they form the foundation for the calendar.

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (2): The Repurposing Engine generates platform-specific variations from the source content., Repurposing Engine

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (1): Content Calendar

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (1): Build Plan

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (1): Gap Analysis

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (1): autoSchedule function

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): scheduleMap

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): Weekly Default Distribution

## Knowledge Gaps
- **11 isolated node(s):** `Content Calendar`, `Build Plan`, `Gap Analysis`, `autoSchedule function`, `scheduleMap` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 3`** (2 nodes): `The Repurposing Engine generates platform-specific variations from the source content.`, `Repurposing Engine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (1 nodes): `Content Calendar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (1 nodes): `Build Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (1 nodes): `Gap Analysis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (1 nodes): `autoSchedule function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (1 nodes): `scheduleMap`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `Weekly Default Distribution`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Content Calendar Module` connect `Community 1` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.307) - this node is a cross-community bridge._
- **Why does `Repurposing Engine` connect `Community 3` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Why does `Source Content Module` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Content Calendar Module` (e.g. with `Repurposing Engine` and `Standalone Content Module`) actually correct?**
  _`Content Calendar Module` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Source Content Module` (e.g. with `Content Bank (Ideas Layer)` and `Repurposing Engine`) actually correct?**
  _`Source Content Module` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Repurposing Engine` (e.g. with `Source Content Module` and `Content Calendar Module`) actually correct?**
  _`Repurposing Engine` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Calendar Logic (packages/lib/calendar.ts)` (e.g. with `Content Calendar Module` and `CalendarItem data model`) actually correct?**
  _`Calendar Logic (packages/lib/calendar.ts)` has 2 INFERRED edges - model-reasoned connections that need verification._