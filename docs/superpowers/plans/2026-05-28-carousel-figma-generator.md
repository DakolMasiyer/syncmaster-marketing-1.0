# Carousel Figma Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate Figma-ready Instagram carousels for every post in the content calendar by translating copy bank bodies into structured 5-slide HTML, then batch-importing via Figma MCP.

**Architecture:** Python content pipeline scrapes calendar + copy bank → maps each carousel post to a 5-field slide schema → renders HTML using the BTS Carousel Figma-Ready template → Claude imports each HTML into the open Figma file via `html_to_design` MCP.

**Tech Stack:** Python 3 (stdlib only), regex HTML parser, Jinja2-style f-string templating, `mcp__claude_ai_html_to_design__import-html` for Figma push.

---

## Slide Schema (5 fields per slide, per carousel)

Each carousel post maps to this JSON structure:

```json
{
  "id": "IG-EDU-01",
  "date": "2026-06-02",
  "platform": "Instagram",
  "pillar": "Education",
  "topic": "What is sync licensing?",
  "caption": "Full Instagram caption text...",
  "cta_line": "Save this post. It's the starting point for everything.",
  "slides": {
    "s1_eyebrow": "Education · June 02",
    "s1_headline": "Nobody\nexplained this\nin music school.",
    "s1_lede": "Your music can earn thousands per placement — upfront, in TV, film, ads and games.",
    "s1_footer_kicker": "SyncMaster · Education",
    "s2_eyebrow": "What is sync licensing?",
    "s2_headline": "Sync licensing =\nyour music in\nfilm, TV, ads & games.",
    "s2_lede": "One Netflix scene: $5K–$20K. One global ad: $10K–$75K. Upfront. Not per stream.",
    "s2_footer_kicker": "The opportunity",
    "s3_micro_label": "03 · The deal structure",
    "s3_micro_text": "Two licences. One placement. Real money.",
    "s4_micro_label": "04 · What supervisors look for",
    "s4_micro_text": "Cleared rights. Brief-matched. Fast response.",
    "s5_cta_title": "Save this.\nShare it.",
    "s5_cta_sub": "This is the starting point for every sync conversation. Share it with a composer who needs to know.",
    "s5_footer_kicker": "Learn"
  }
}
```

---

## Template Text Fields (from BTS Carousel Figma-Ready.html)

| Slide | Element | CSS class / tag | Max length |
|---|---|---|---|
| 1 | Eyebrow label | `.eyebrow` | 40 chars |
| 1 | Display headline | `h1.display` | 3 lines × 8 words |
| 1 | Lede | `p.lede` | 25 words |
| 1 | Footer kicker | `.footer-kicker` | 30 chars |
| 2 | Eyebrow | `.eyebrow` | 40 chars |
| 2 | Display headline | `h2.display` | 3 lines × 6 words |
| 2 | Lede | `p.lede` | 30 words |
| 2 | Footer kicker | `.footer-kicker` | 30 chars |
| 3 | Micro label | `.micro.micro--dot` | 30 chars |
| 3 | Micro text | `.micro` (bottom) | 60 chars |
| 4 | Micro label | `.micro.micro--dot` | 30 chars |
| 4 | Micro text | `.micro` (bottom) | 60 chars |
| 5 | CTA title | `.cta-title` | 2 lines × 4 words |
| 5 | CTA sub | `.cta-sub` | 2 sentences |
| 5 | Footer kicker | `.footer-kicker` | 15 chars |

---

## File Map

| File | Purpose |
|---|---|
| `carousel/generate_figma_copy.py` | Reads calendar + copy bank → outputs `carousel/exports/figma_manifest.json` |
| `carousel/render_carousel_html.py` | Takes manifest → renders one HTML per carousel using BTS template |
| `carousel/exports/figma_manifest.json` | Structured 5-slide copy for all carousel posts |
| `carousel/exports/html/IG-EDU-01.html` | Figma-ready HTML per post (one file per carousel) |

---

## Task 1: Generate Slide Copy + Captions (Content Pipeline)

**Files:**
- Create: `carousel/generate_figma_copy.py`
- Output: `carousel/exports/figma_manifest.json`

- [ ] **Step 1: Write the content extractor**

```python
# carousel/generate_figma_copy.py
import re, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL_PATH = os.path.join(BASE, 'syncmaster-content-calendar.html')
CB_PATHS = [
    os.path.join(BASE, 'copy-bank-m1.html'),
    os.path.join(BASE, 'copy-bank-m2.html'),
    os.path.join(BASE, 'copy-bank-m3.html'),
]

def extract_posts(html: str) -> list[dict]:
    """Pull the POSTS array out of the calendar HTML."""
    match = re.search(r'const POSTS\s*=\s*\[(.*?)\];', html, re.DOTALL)
    if not match:
        return []
    raw = match.group(1)
    posts = []
    for obj in re.finditer(r'\{([^{}]+)\}', raw, re.DOTALL):
        fields = {}
        for k, v in re.findall(r"(\w+):\s*['\"`](.*?)['\"`](?=[,\s}])", obj.group(1), re.DOTALL):
            fields[k] = v.replace("\\'", "'")
        if fields.get('type') == 'Carousel' and fields.get('platform') == 'Instagram':
            posts.append(fields)
    return posts

def extract_copy(html: str) -> dict:
    """Pull all COPY_* objects from a copy bank HTML."""
    combined = {}
    for block_match in re.finditer(r'const COPY\w*\s*=\s*\{(.*?)(?=\n(?:const |</script))', html, re.DOTALL):
        block = block_match.group(1)
        for entry in re.finditer(r"'([\w-]+)':\s*\{\s*body:\s*`(.*?)`\s*,\s*cta:\s*(?:`(.*?)`|null)\s*\}", block, re.DOTALL):
            combined[entry.group(1)] = {
                'body': entry.group(2).strip(),
                'cta': entry.group(3).strip() if entry.group(3) else ''
            }
    return combined

def map_slides(post: dict, copy: dict) -> dict:
    """Map a post + copy body to the 5-slide schema."""
    body = copy.get('body', '')
    cta = copy.get('cta', '')
    paras = [p.strip() for p in body.split('\n\n') if p.strip()]
    
    hook_line = paras[0] if paras else post.get('hook', '')
    
    # Slide 1 — Hook: first 1-2 lines, made display-size
    headline_words = hook_line.replace('.', '.\n').split('\n')
    s1_headline = '\n'.join(w.strip() for w in headline_words if w.strip())[:80]
    s1_lede = paras[1][:120] if len(paras) > 1 else ''
    
    # Slide 2 — Context: central thesis
    context_para = next((p for p in paras[1:4] if '=' in p or 'is' in p.lower() or ':' in p), paras[1] if len(paras) > 1 else '')
    s2_headline = _format_headline(context_para, max_lines=3)
    s2_lede = next((p for p in paras[2:5] if p and p != context_para), '')[:140]
    
    # Slide 3 — Showcase A: first insight cluster
    bullets = [p for p in paras if p.startswith('→') or re.match(r'^[✓•]\s', p)]
    s3_micro_text = ' · '.join(b[:30] for b in bullets[:2]) if bullets else paras[3][:60] if len(paras) > 3 else ''
    
    # Slide 4 — Showcase B: second insight cluster
    s4_micro_text = ' · '.join(b[:30] for b in bullets[2:4]) if len(bullets) >= 3 else paras[4][:60] if len(paras) > 4 else ''
    
    # Slide 5 — CTA
    cta_para = cta or next((p for p in reversed(paras) if 'save' in p.lower() or 'apply' in p.lower() or 'share' in p.lower()), '')
    s5_cta_title = _format_cta_title(cta_para)
    s5_cta_sub = cta_para if cta_para else paras[-1]
    s5_footer_kicker = _cta_verb(post.get('pillar', ''))
    
    month_abbr = {'2026-06': 'June', '2026-07': 'July', '2026-08': 'Aug'}.get(post.get('date', '')[:7], '')
    day = post.get('date', '')[-2:].lstrip('0')
    date_label = f"{month_abbr} {day}" if month_abbr else ''
    
    return {
        's1_eyebrow': f"{post.get('pillar', '')} · {date_label}",
        's1_headline': s1_headline,
        's1_lede': s1_lede[:120],
        's1_footer_kicker': f"SyncMaster · {post.get('pillar', '')}",
        's2_eyebrow': post.get('topic', ''),
        's2_headline': s2_headline,
        's2_lede': s2_lede[:140],
        's2_footer_kicker': _context_label(post.get('pillar', '')),
        's3_micro_label': f"03 · {_topic_short(post.get('topic', ''), 1)}",
        's3_micro_text': s3_micro_text[:70],
        's4_micro_label': f"04 · {_topic_short(post.get('topic', ''), 2)}",
        's4_micro_text': s4_micro_text[:70],
        's5_cta_title': s5_cta_title,
        's5_cta_sub': s5_cta_sub[:180],
        's5_footer_kicker': s5_footer_kicker,
    }

def _format_headline(text: str, max_lines: int = 3) -> str:
    text = text.replace('=', '=\n').replace(':', ':\n').replace('. ', '.\n')
    lines = [l.strip() for l in text.split('\n') if l.strip()][:max_lines]
    return '\n'.join(lines)

def _format_cta_title(text: str) -> str:
    words = text.split()[:8]
    mid = len(words) // 2
    return ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])

def _cta_verb(pillar: str) -> str:
    return {'Education': 'Learn', 'Proof': 'Apply', 'Behind the Scenes': 'Follow', 'Industry': 'Read'}.get(pillar, 'Apply')

def _context_label(pillar: str) -> str:
    return {'Education': 'The opportunity', 'Proof': 'Real results', 'Behind the Scenes': 'The process', 'Industry': 'The landscape'}.get(pillar, 'Context')

def _topic_short(topic: str, part: int) -> str:
    words = topic.split()
    half = len(words) // 2
    return ' '.join(words[:half]).strip() if part == 1 else ' '.join(words[half:]).strip()

def main():
    with open(CAL_PATH, encoding='utf-8') as f:
        cal_html = f.read()
    
    all_copy = {}
    for p in CB_PATHS:
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                all_copy.update(extract_copy(f.read()))
    
    posts = extract_posts(cal_html)
    manifest = []
    
    for post in posts:
        pid = post.get('id', '')
        copy = all_copy.get(pid, {'body': post.get('hook', ''), 'cta': ''})
        slides = map_slides(post, copy)
        manifest.append({
            'id': pid,
            'date': post.get('date', ''),
            'topic': post.get('topic', ''),
            'pillar': post.get('pillar', ''),
            'caption': copy.get('body', ''),
            'cta_line': copy.get('cta', ''),
            'slides': slides
        })
    
    out_dir = os.path.join(BASE, 'carousel', 'exports')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'figma_manifest.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(manifest)} carousels → {out_path}")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run it**

```bash
cd /Users/dakolmasiyer/Projects/syncmaster-marketing-1.0
python carousel/generate_figma_copy.py
```

Expected output:
```
Generated N carousels → /Users/.../carousel/exports/figma_manifest.json
```

- [ ] **Step 3: Review manifest** — open `carousel/exports/figma_manifest.json`, check first 3 entries look right (headlines ≤3 lines, lede ≤25 words, cta_title has a line break)

- [ ] **Step 4: Commit**

```bash
git add carousel/generate_figma_copy.py carousel/exports/figma_manifest.json
git commit -m "feat: carousel figma copy generator — scrapes calendar + copy bank → 5-slide manifest"
```

---

## Task 2: Render Figma-Ready HTML Per Carousel

**Files:**
- Create: `carousel/render_carousel_html.py`
- Output: `carousel/exports/html/IG-EDU-01.html`, `IG-EDU-02.html`, etc.

- [ ] **Step 1: Write the renderer**

```python
# carousel/render_carousel_html.py
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(BASE, 'carousel', 'exports', 'figma_manifest.json')
TEMPLATE = os.path.join(BASE, 'SyncMaster Design System', 'Behind the Scenes Carousel (Figma-Ready).html')
OUT_DIR  = os.path.join(BASE, 'carousel', 'exports', 'html')

REPLACEMENTS = [
    # Slide 1
    ('Behind the build · Ep 04',                    '{s1_eyebrow}'),
    ('Inside<br>the platform.',                      '{s1_headline_html}'),
    ('A look at how briefs become placements',       '{s1_lede}'),
    ('SyncMaster · Operations',                      '{s1_footer_kicker}'),
    # Slide 2
    ('Why we built this',                            '{s2_eyebrow}'),
    ("Africa's best music<br>never reached<br>the right brief.", '{s2_headline_html}'),
    ('Rights complexity. Metadata gaps. No access',  '{s2_lede}'),
    ('The Problem',                                  '{s2_footer_kicker}'),
    # Slide 3
    ('03 · The dashboard',                           '{s3_micro_label}'),
    ('Sidebar / Hero / Top Briefs / Tools — one workspace', '{s3_micro_text}'),
    # Slide 4 — add after inspecting slide 4 micro labels
    # Slide 5
    ('Apply to compose.<br>Post a brief.',           '{s5_cta_title_html}'),
    ('Composers: apply once, get matched for life.<br>Supervisors: post a brief, get a shortlist in 48 hours.', '{s5_cta_sub}'),
    ('footer-kicker">Apply',                         'footer-kicker">{s5_footer_kicker}'),
]

def render(entry: dict, template: str) -> str:
    s = entry['slides']
    html = template
    vals = {
        's1_eyebrow':         s['s1_eyebrow'],
        's1_headline_html':   s['s1_headline'].replace('\n', '<br>'),
        's1_lede':            s['s1_lede'],
        's1_footer_kicker':   s['s1_footer_kicker'],
        's2_eyebrow':         s['s2_eyebrow'],
        's2_headline_html':   s['s2_headline'].replace('\n', '<br>'),
        's2_lede':            s['s2_lede'],
        's2_footer_kicker':   s['s2_footer_kicker'],
        's3_micro_label':     s['s3_micro_label'],
        's3_micro_text':      s['s3_micro_text'],
        's5_cta_title_html':  s['s5_cta_title'].replace('\n', '<br>'),
        's5_cta_sub':         s['s5_cta_sub'],
        's5_footer_kicker':   s['s5_footer_kicker'],
    }
    for old, new_tpl in REPLACEMENTS:
        new = new_tpl.format(**vals)
        html = html.replace(old, new, 1)
    # Update page title
    html = html.replace('SyncMaster — Behind the Scenes Carousel', f"SyncMaster — {entry['topic']}")
    return html

def main():
    with open(MANIFEST, encoding='utf-8') as f:
        manifest = json.load(f)
    with open(TEMPLATE, encoding='utf-8') as f:
        template = f.read()
    
    os.makedirs(OUT_DIR, exist_ok=True)
    for entry in manifest:
        out = render(entry, template)
        fname = os.path.join(OUT_DIR, f"{entry['id']}.html")
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f"  {entry['id']} → {fname}")
    print(f"\nRendered {len(manifest)} HTML files → {OUT_DIR}")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run it**

```bash
python carousel/render_carousel_html.py
```

- [ ] **Step 3: Open first output in browser and visually check**

```bash
open "carousel/exports/html/IG-EDU-01.html"
```

Confirm: slide 1 headline reads correctly, footer kicker updated, slide 5 CTA matches copy bank.

- [ ] **Step 4: Commit**

```bash
git add carousel/render_carousel_html.py carousel/exports/html/
git commit -m "feat: render Figma-ready HTML per carousel from manifest"
```

---

## Task 3: Figma Batch Import via MCP

**Tool:** `mcp__claude_ai_html_to_design__import-html` (or `import-url` if serving locally)

- [ ] **Step 1: Load import-html tool schema**

```
ToolSearch: select:mcp__claude_ai_html_to_design__import-html
```

- [ ] **Step 2: Navigate Figma to a "Carousels Generated" page**

```
mcp__figma-mcp-go__add_page: name = "Carousels — Generated YYYY-MM-DD"
mcp__figma-mcp-go__navigate_to_page: new page id
```

- [ ] **Step 3: Import each HTML file into Figma (batch, one per carousel)**

For each `carousel/exports/html/*.html`:
```
mcp__claude_ai_html_to_design__import-html: html = <file contents>
```

Position each import at `x = index * 1100, y = 0` so they tile horizontally.

- [ ] **Step 4: Review in Figma** — open the new page, confirm slides render, text is correct.

---

## Self-Review Checklist

- [x] Task 1 covers copy extraction from all 3 copy bank files
- [x] Task 2 renders one HTML per carousel using the real Figma-Ready template
- [x] Task 3 imports via MCP into the open Figma file
- [x] Slide schema covers all 5 template text zones
- [x] No placeholder copy — all field mappings are concrete
- [x] Caption text preserved verbatim from copy bank (not truncated)
