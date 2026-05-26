# syncmaster-marketing-1.0 — Claude Project Config

## Project
SyncMaster marketing site and carousel content tool (`/carousel`).
Focus: content production, brand assets, and marketing execution.

## Cross-Project Architecture
This workspace (`syncmaster-marketing-1.0`) is the **marketing layer** for the main platform.
- **Production Codebase:** `Syncmaster-Live` is the source of truth for the product application (Next.js/Supabase).
- **Design System:** Design tokens, UI kits, and `carousel_templates.html` are extracted from the `Syncmaster-Live` codebase to maintain 1:1 visual parity across projects.
- **Agents:** Never invent new positioning; always pull from `.agents/product-marketing.md`.

## Brand Tokens
Purple `#5252E0` · Lime `#C9E834` · Dark `#0A0A20` · Font: DM Sans

---

## Skill Routing — Use These Automatically

### Content Creation
- Copy, captions, post text → `/copywriting`, `/copy-editing`
- Social posts (LinkedIn, Instagram, Twitter/X) → `/social`, `/copywriting`
- Ad creative, sponsored content → `/ad-creative`, `/ckmbanner-design`
- Email campaigns → `/emails`
- Content calendar, strategy, pillar planning → `/content-strategy`
- Video scripts or short-form video → `/video`
- Image brief or visual direction → `/image`

### Brand & Design
- SyncMaster visual identity → `/ckmbrand`, `/ckmslides`
- Banner, ad, or promotional design → `/ckmbanner-design`
- Slide decks or carousel posts → `/ckmslides`, `/pptx`
- UI design or frontend build → `/frontend-design`, `/ui-ux-pro-max`
- UI audit or accessibility/UX review → `/web-design-guidelines`

### Marketing & Growth
- SEO → `/ai-seo`, `/seo-audit`, `/programmatic-seo`
- Analytics, reporting → `/analytics`, `/ab-testing`
- CRO → `/cro`
- Launch planning → `/launch`
- Product marketing → `/product-marketing`
- Competitor analysis → `/competitors`, `/competitor-profiling`
- Customer/market research → `/customer-research`, `/marketing-psychology`
- Lead magnets → `/lead-magnets`
- Referrals → `/referrals`

### Behaviour
- When I describe a content task, identify the format (carousel, post, email, ad) and route to the right skill before writing anything.
- For batch content (multiple posts, carousels, assets at once) → `/dispatching-parallel-agents`.
- Research before creation: run research skill first, summarise findings, then write.
- Apply SyncMaster brand tokens to all UI and visual work.

## Workflow & Mistake Avoidance
- **Save files directly:** When generating configuration files, code snippets, tokens (like JSON), or scripts, ALWAYS save them directly to the filesystem using the `write_to_file` tool. Do not just embed them in markdown guides or ask the user to copy-paste.
- **Do the heavy lifting:** If a task requires creating an asset or boilerplate, execute the creation on the user's behalf instead of providing instructions on how they should do it themselves.
