# SyncMaster Marketing Agent Instructions

These instructions are shared workspace rules for AI agents. Keep model-specific behavior in `CLAUDE.md`, `GEMINI.md`, or local tool config files.

## Workspace Purpose

This workspace is for SyncMaster marketing assets, social content, sales enablement, and lightweight HTML tooling.

Primary outputs include:

- Social media carousels and visual assets
- Content calendars and pillar planning
- Sales playbooks and outreach systems
- Copy banks, persona docs, and objection handling
- Static HTML prototypes and content tools

## Source of Truth

Use `.agents/product-marketing.md` as the primary source for SyncMaster positioning, ICP, brand voice, personas, content pillars, and proof points.

Current durable positioning:

- SyncMaster bridges African composers and global sync licensing.
- It is infrastructure, not a generic music library or label.
- Core value to composers: legally clean, professionally submitted, brief-matched opportunities.
- Core value to supervisors: curated, rights-cleared African tracks delivered quickly.
- Voice is direct, practical, specific, and confident without hype.

## Brand Defaults

- Purple: `#5252E0`
- Lime: `#C9E834`
- Dark: `#0A0A20`
- Preferred font: DM Sans when available

Design should feel sharp, modern, and practical. Avoid generic creator-economy visuals, vague music-industry language, and decorative layouts that reduce readability.

## Workflow Rules

- Before writing copy or assets, check the relevant positioning in `.agents/product-marketing.md`.
- For carousels and social graphics, verify mobile readability and avoid cramped text.
- For batch content, keep variants separated by persona or channel.
- For sales enablement, write separately for composers, music supervisors, production companies, and Nollywood when relevant.
- Prefer finished artifacts as files when the user asks for assets, decks, HTML pages, or playbooks.
- Do not introduce secrets, platform tokens, or real private contact data into generated content.

## Key Paths

```text
.agents/product-marketing.md          positioning, ICP, voice, proof points
carousel/                             carousel/content generation logic
Uploads/                              user-provided source assets
content-calendar.html                 content calendar artifact
content-pillars.html                  content pillar artifact
playbooks.html                        playbook artifact
outreach-system.html                  outreach artifact
copy-bank-*.html                      copy bank artifacts
playbook-*.md                         persona or channel-specific playbooks
persona-cards.md                      persona reference
objection-handling-guide.md           sales objections reference
SESSION-PROGRESS.md                   latest workspace progress notes
figma-handoff/                        static Figma-ready HTML/CSS handoff package
figma-handoff/Figma_Master_Handoff.html master handoff portal
```

## Content Quality Bar

- Be specific: use numbers, timelines, territories, and concrete workflows when known.
- Prefer operational proof over broad claims.
- Explain sync infrastructure plainly.
- Never position African music as a charity or underdog story; position it as an asset that needs better infrastructure.
- Do not invent placements, client names, or metrics. If proof is unknown, ask or mark it as a placeholder.

## Verification

For HTML/CSS/JS artifacts:

- Open or inspect the changed file when practical.
- Check mobile readability for carousel and social assets.
- Confirm links, navigation, and visible text do not overlap.

For markdown playbooks or copy banks:

- Check that the output matches the intended persona, channel, and funnel stage.
- Keep claims aligned with `.agents/product-marketing.md`.
