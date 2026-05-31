# Blog Farm SEO — Prompts & Instructions
Generated: 2026-05-31

---

## PROMPT 1 — Take to Claude Web (Strategy + Architecture)

Paste this into a new Claude.ai conversation:

---

**PASTE START**

I'm building a blog farm SEO strategy for **SyncMaster** (syncmaster.io), a sync licensing infrastructure platform that connects African composers to global film/TV/ad music supervisors.

Here is the full product context — read this before answering anything:

[PASTE CONTENTS OF notebooklm-upload-bundle.md HERE]

---

My blog strategy:
- Posts go live immediately (for Google indexing) but show the social announcement date as the "published" date visible to readers
- We will eventually have a NotebookLM notebook loaded with all the above context that generates briefs, which I then expand in Claude Code into full posts
- Posts live at syncmaster.io/blog (Next.js app)

I need you to do three things:

**1. TOPIC CLUSTER MAP**
Build a full topic cluster architecture for the SyncMaster blog. For each cluster, give me:
- 1 pillar page title + target keyword
- 4–6 supporting post titles + long-tail keywords
- Internal linking logic (which supporting posts link to the pillar, which link to each other)
- Search intent for each post (informational / commercial / navigational)

Target at least 4 clusters:
- Sync licensing fundamentals (composer-facing)
- Music supervisor workflow & African music (supervisor-facing)  
- African music infrastructure & market (culture/industry)
- SyncMaster proof & process (brand/BTS)

**2. KEYWORD PRIORITY LIST**
For each cluster, rank the 3 most valuable keywords by:
- Estimated monthly search volume (use your knowledge — be honest about uncertainty)
- Keyword difficulty (low / medium / high)
- Which persona it targets (Tunde / Amara / Nollywood / industry observer)
- Recommended post format (long-form guide / case study / listicle / explainer / opinion)

**3. PUBLISHING SEQUENCE**
Give me a 12-week publishing sequence — which posts to publish in which order, and why (SEO dependency, internal linking readiness, social calendar alignment).

Important constraints:
- SyncMaster brand voice: direct, specific, confident — no hype, no charity framing for African music
- No invented metrics — mark any placeholders clearly
- The blog supports social proof on Instagram/LinkedIn, so posts should be expandable into carousels or threads

**PASTE END**

---

## PROMPT 2 — NotebookLM Setup Instructions

### Step 1: Create the notebook
1. Go to notebooklm.google.com
2. Create a new notebook: **"SyncMaster Blog Brain"**

### Step 2: Upload sources (in this order)
Upload all of these — each as a separate source so NotebookLM can cite them individually:

| File | Why |
|---|---|
| `notebooklm-upload-bundle.md` | Full product context, personas, voice, proof points |
| `syncmaster-content-calendar.html` | 122 posts — shows what themes are already planned |
| `copy-bank-m1.html` | Month 1 post copy — shows voice and framing patterns |
| `copy-bank-m2.html` | Month 2 post copy |
| `copy-bank-m3.html` | Month 3 post copy |
| `content-pillars.html` | Pillar strategy and content architecture |
| `objection-handling-guide.md` | The real objections to address in educational posts |
| `playbook-composer-onboarding.md` | Composer journey — informs educational blog arc |
| `playbook-producer-post-demo.md` | Supervisor side — informs supervisor-facing posts |

### Step 3: Add a note inside the notebook

After uploading, click "+ New Note" and paste this as your standing instruction:

---

**SyncMaster Blog Brain — Standing Instructions**

This notebook is the knowledge base for SyncMaster's blog content pipeline.

When I ask you to generate a blog brief or outline, follow these rules:

1. **Voice**: Direct, practical, specific, confident. No hype. No fluff. Numbers and timelines > adjectives.
2. **Framing**: African music is infrastructure and asset — never an underdog or charity story. SyncMaster is the infrastructure, not a music library or label.
3. **No invented metrics**: If I don't have a specific number, write [PLACEHOLDER: X] — never make up figures.
4. **Persona targeting**: Every post brief should specify which persona it primarily serves (Tunde / Amara / Nollywood / industry observer).
5. **SEO intent**: Every brief should include the primary keyword and search intent (informational / commercial / navigational).
6. **Blog-to-social bridge**: Every post should end with a note on which social format it can become (carousel / thread / single).
7. **Internal linking**: Suggest 2–3 other posts in the cluster this should link to.

---

### Step 4: The brief generation query (use this every time you want a new post)

When you're ready to generate a brief for a specific post, query NotebookLM with:

```
Generate a blog post brief for: [POST TITLE]
Target keyword: [KEYWORD]
Persona: [Tunde / Amara / Nollywood / industry]
Cluster: [cluster name]

Include:
- Working title (SEO-optimised H1)
- Meta description (155 chars max)
- Search intent
- Outline (H2s and H3s)
- Key proof points to include (from the sources)
- Suggested internal links
- Social format bridge (carousel / thread / single)
- Word count target
```

---

## PROMPT 3 — Back to Claude Code (Pipeline Build)

Once you have the cluster map from Claude Web and have set up NotebookLM, come back here and say:

> "I have the cluster map. Build me a blog post generation pipeline."

Claude Code will then:
1. Build a `blog/` directory structure in this repo
2. Create a `blog_generator.py` that takes a NotebookLM-style brief JSON and outputs a full `.md` post file with YAML frontmatter (title, slug, publishDate, socialDate, keyword, cluster, persona, wordCount)
3. Wire it into the existing `batch_run.py` content pipeline so blog posts sit alongside the carousel exports

---

## Quick Reference: Post Date Strategy

| Field | Value | Purpose |
|---|---|---|
| `publishDate` | Immediate (today or past) | Google indexes from this date |
| `socialDate` | Future (day you announce on IG/LinkedIn) | What readers see as "published" |
| `status` | `live` / `draft` / `scheduled` | Pipeline state |

The Next.js blog template should render `socialDate` as the visible date but use `publishDate` for the sitemap and canonical URL — this is standard and clean for SEO.
