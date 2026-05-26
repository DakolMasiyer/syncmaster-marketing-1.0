import os
import re
import shutil
import subprocess
import time

# Paths
source_dir = r"C:\Users\infon\Downloads\SyncMaster_DS3_Extract"
workspace_dir = r"c:\Users\infon\Documents\Claude Code\Projects\syncmaster-marketing-1.0"
output_dir = os.path.join(workspace_dir, "figma-handoff")
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print(f"Source Directory: {source_dir}")
print(f"Output Directory: {output_dir}")

# Create output directories
os.makedirs(output_dir, exist_ok=True)
dest_assets = os.path.join(output_dir, "assets")

# 1. Copy Assets Directory
if os.path.exists(os.path.join(source_dir, "assets")):
    print("Copying assets directory...")
    shutil.copytree(os.path.join(source_dir, "assets"), dest_assets, dirs_exist_ok=True)
else:
    print("WARNING: Source assets directory not found!")

# Read colors_and_type.css
with open(os.path.join(source_dir, "colors_and_type.css"), "r", encoding="utf-8") as f:
    css_content = f.read()

# Make sure @import is at the very top of inlined CSS
css_cleaned = css_content
import_match = re.search(r'@import url\([^)]+\);', css_content)
if import_match:
    import_stmt = import_match.group(0)
    # Remove the import statement from its original position and prepended to the top
    css_cleaned = import_stmt + "\n" + css_content.replace(import_stmt, "")

def clean_html_source(html, title_comment="Figma-Ready"):
    # Replace relative asset paths to point to the local assets folder
    html = html.replace('../../assets/', 'assets/')
    html = html.replace('../assets/', 'assets/')
    
    # Remove script tags loading React, Babel, Tailwind, Lucide
    html = re.sub(r'<script\s+src="https://unpkg\.com/react@[^>]+></script>', '', html)
    html = re.sub(r'<script\s+src="https://unpkg\.com/react-dom@[^>]+></script>', '', html)
    html = re.sub(r'<script\s+src="https://unpkg\.com/@babel/[^>]+></script>', '', html)
    html = re.sub(r'<script\s+src="https://unpkg\.com/lucide@[^>]+></script>', '', html)
    html = re.sub(r'<script\s+src="https://cdn\.tailwindcss\.com"></script>', '', html)
    
    # Remove Babel babel scripts
    html = re.sub(r'<script\s+type="text/babel".*?</script>', '', html, flags=re.DOTALL)
    
    # Prepend figma-ready comment
    comment = f"<!-- Figma-Ready: {title_comment} -->\n"
    if not html.startswith("<!--"):
        html = comment + html
    return html

# Helper to run headless Chrome and dump DOM
def run_headless_chrome(file_path):
    print(f"Running headless Chrome for: {os.path.basename(file_path)}...")
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--dump-dom",
        "--virtual-time-budget=6000",
        f"file:///{file_path}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return result.stdout

# -------------------------------------------------------------
# TASK 1: BTS Instagram Carousel
# -------------------------------------------------------------
print("\n--- Compiling Task 1: BTS Carousel ---")
bts_source_path = os.path.join(source_dir, "BTS-Figma-Import.html")
with open(bts_source_path, "r", encoding="utf-8") as f:
    bts_html = f.read()

# Move fonts link to @import inside <style>
bts_html = re.sub(r'<link rel="preconnect"[^>]*>', '', bts_html)
bts_html = re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^>]*" rel="stylesheet">', '', bts_html)

# Add @import inside <style>
fonts_import = '@import url("https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700;9..40,900&family=Geist+Mono:wght@400;500;600;700&display=swap");\n'
bts_html = bts_html.replace("<style>", f"<style>\n{fonts_import}")
bts_html = clean_html_source(bts_html, "BTS Carousel (5 slides × 1080x1350px)")

with open(os.path.join(output_dir, "bts_carousel_figma_ready.html"), "w", encoding="utf-8") as f:
    f.write(bts_html)
print("Saved bts_carousel_figma_ready.html")

# -------------------------------------------------------------
# TASK 2: Instagram Carousel Templates
# -------------------------------------------------------------
print("\n--- Compiling Task 2: Carousel Templates ---")
tmpl_source_path = os.path.join(source_dir, "carousel_templates.html")
with open(tmpl_source_path, "r", encoding="utf-8") as f:
    tmpl_html = f.read()

# Replace css link with inlined stylesheet
tmpl_html = re.sub(r'<link rel="stylesheet" href="colors_and_type.css">', f"<style>\n{css_cleaned}\n</style>", tmpl_html)
tmpl_html = clean_html_source(tmpl_html, "Carousel Templates (5 templates × 1080x1350px)")

with open(os.path.join(output_dir, "carousel_templates_figma_ready.html"), "w", encoding="utf-8") as f:
    f.write(tmpl_html)
print("Saved carousel_templates_figma_ready.html")

# -------------------------------------------------------------
# TASK 3: Design System Spec (React/Babel/Tailwind CDN)
# -------------------------------------------------------------
print("\n--- Compiling Task 3: Design System Spec ---")
ds_source_path = os.path.join(source_dir, "design_system.html")

# Render it via Chrome
ds_rendered = run_headless_chrome(ds_source_path)

# Replace css link with inlined stylesheet
ds_rendered = re.sub(r'<link rel="stylesheet" href="colors_and_type.css">', f"<style>\n{css_cleaned}\n</style>", ds_rendered)
ds_rendered = clean_html_source(ds_rendered, "Static pre-render of SyncMaster Design System. No JS required.")

# Save
with open(os.path.join(output_dir, "design_system_figma_ready.html"), "w", encoding="utf-8") as f:
    f.write(ds_rendered)
print("Saved design_system_figma_ready.html")

# -------------------------------------------------------------
# TASK 4: Brand Guidelines (Tailwind CDN)
# -------------------------------------------------------------
print("\n--- Compiling Task 4: Brand Guidelines ---")
brand_source_path = os.path.join(source_dir, "brand_guidelines.html")

# Render it via Chrome
brand_rendered = run_headless_chrome(brand_source_path)

# Replace css link with inlined stylesheet
brand_rendered = re.sub(r'<link rel="stylesheet" href="colors_and_type.css">', f"<style>\n{css_cleaned}\n</style>", brand_rendered)
brand_rendered = clean_html_source(brand_rendered, "SyncMaster Brand Guidelines v1.0. No JS required.")

with open(os.path.join(output_dir, "brand_guidelines_figma_ready.html"), "w", encoding="utf-8") as f:
    f.write(brand_rendered)
print("Saved brand_guidelines_figma_ready.html")

# -------------------------------------------------------------
# TASK 5: UI Kits (Pre-rendering 7 screens side-by-side)
# -------------------------------------------------------------
print("\n--- Compiling Task 5: UI Kits ---")

# Let's read the JSX scripts for dashboard and marketing
with open(os.path.join(source_dir, r"ui_kits\dashboard\Sidebar.jsx"), "r", encoding="utf-8") as f:
    db_sidebar_jsx = f.read()

with open(os.path.join(source_dir, r"ui_kits\dashboard\Components.jsx"), "r", encoding="utf-8") as f:
    db_comp_jsx = f.read()

with open(os.path.join(source_dir, r"ui_kits\dashboard\Screens.jsx"), "r", encoding="utf-8") as f:
    db_screens_jsx = f.read()

with open(os.path.join(source_dir, r"ui_kits\marketing\Components.jsx"), "r", encoding="utf-8") as f:
    mkt_comp_jsx = f.read()

with open(os.path.join(source_dir, r"ui_kits\marketing\Screens.jsx"), "r", encoding="utf-8") as f:
    mkt_screens_jsx = f.read()

# Let's create the temporary HTML that bundles React, Babel, and all components
# to display them in a side-by-side layout. Use string replacements to avoid formatting problems.
ui_kits_temp_content = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SyncMaster — UI Kits Handoff Spec</title>
  <link rel="stylesheet" href="colors_and_type.css">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    html, body { margin: 0; padding: 0; background: #09090e; color: #f9f9f9; }
    .scrollbar-hide::-webkit-scrollbar { display: none; }
    .scrollbar-hide { scrollbar-width: none; -ms-overflow-style: none; }
  </style>
</head>
<body>
<div id="root"></div>

<script src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>

<script type="text/babel">
// --- Dashboard Sidebar ---
__DB_SIDEBAR_JSX__

// --- Dashboard Components ---
__DB_COMP_JSX__

// --- Dashboard Screens ---
__DB_SCREENS_JSX__

// --- Marketing Components ---
__MKT_COMP_JSX__

// --- Marketing Screens ---
__MKT_SCREENS_JSX__

// --- Master Grid App ---
function App() {
  React.useEffect(() => {
    const id = setInterval(() => window.lucide && window.lucide.createIcons(), 500);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ background: '#09090e', color: '#f9f9f9', padding: '48px', fontFamily: 'var(--font-sans)', boxSizing: 'border-box' }}>
      <header style={{ marginBottom: '48px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '24px', maxWidth: 1440, marginInline: 'auto' }}>
        <h1 style={{ margin: 0, fontSize: 36, fontWeight: 900, letterSpacing: '-0.04em', color: '#f9f9f9' }}>SyncMaster · UI Kits Spec</h1>
        <p style={{ margin: '8px 0 0', fontSize: 14, color: 'rgba(255,255,255,0.6)', fontWeight: 500 }}>Static Figma-Ready pre-render of all 7 core marketing and product screens.</p>
      </header>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 80 }}>
        {/* MARKETING SECTION */}
        <div style={{ maxWidth: 1440, marginInline: 'auto', width: '100%' }}>
          <h2 style={{ fontSize: 24, fontWeight: 900, letterSpacing: '-0.03em', marginBottom: '24px', color: '#C9E834' }}>01 · Marketing Screens (Light Mode)</h2>
          <div style={{ display: 'flex', gap: 48, overflowX: 'auto', paddingBottom: '24px' }}>
            
            {/* Screen 1: Landing */}
            <div style={{ width: 1440, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#fff', color: '#111' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Marketing — Landing (Home)</div>
              <div style={{ background: '#fff', color: '#111', position: 'relative' }}>
                <MarketingNav active="home" />
                <main style={{ minHeight: 900 }}><Landing /></main>
                <Footer />
              </div>
            </div>

            {/* Screen 2: Composers */}
            <div style={{ width: 1440, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#fff', color: '#111' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Marketing — For Composers</div>
              <div style={{ background: '#fff', color: '#111', position: 'relative' }}>
                <MarketingNav active="composers" />
                <main style={{ minHeight: 900 }}><ComposersPage /></main>
                <Footer />
              </div>
            </div>

            {/* Screen 3: Supervisors */}
            <div style={{ width: 1440, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#fff', color: '#111' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Marketing — For Supervisors</div>
              <div style={{ background: '#fff', color: '#111', position: 'relative' }}>
                <MarketingNav active="supervisors" />
                <main style={{ minHeight: 900 }}><SupervisorsPage /></main>
                <Footer />
              </div>
            </div>

          </div>
        </div>

        {/* DASHBOARD SECTION */}
        <div style={{ maxWidth: 1440, marginInline: 'auto', width: '100%' }}>
          <h2 style={{ fontSize: 24, fontWeight: 900, letterSpacing: '-0.03em', marginBottom: '24px', color: '#5252E0' }}>02 · Dashboard Screens (Dark Mode)</h2>
          <div style={{ display: 'flex', gap: 48, overflowX: 'auto', paddingBottom: '24px' }}>

            {/* Screen 4: Dashboard Home */}
            <div className="dark" style={{ width: 1440, minHeight: 1000, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#0f0f1a' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Dashboard — Home</div>
              <div style={{ display: 'flex', minHeight: 944, background: 'var(--background)' }}>
                <Sidebar active="Dashboard" />
                <div style={{ flex: 1, marginLeft: 256, display: 'flex', flexDirection: 'column' }}>
                  <Header crumb="Dashboard" />
                  <main style={{ flex: 1, padding: '16px 24px 96px' }}><DashboardHome /></main>
                </div>
              </div>
            </div>

            {/* Screen 5: Briefs List */}
            <div className="dark" style={{ width: 1440, minHeight: 1000, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#0f0f1a' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Dashboard — Briefs List</div>
              <div style={{ display: 'flex', minHeight: 944, background: 'var(--background)' }}>
                <Sidebar active="Briefs" />
                <div style={{ flex: 1, marginLeft: 256, display: 'flex', flexDirection: 'column' }}>
                  <Header crumb="Briefs" />
                  <main style={{ flex: 1, padding: '16px 24px 96px' }}><BriefsList /></main>
                </div>
              </div>
            </div>

            {/* Screen 6: Brief Detail */}
            <div className="dark" style={{ width: 1440, minHeight: 1000, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#0f0f1a' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Dashboard — Brief Detail</div>
              <div style={{ display: 'flex', minHeight: 944, background: 'var(--background)' }}>
                <Sidebar active="Briefs" />
                <div style={{ flex: 1, marginLeft: 256, display: 'flex', flexDirection: 'column' }}>
                  <Header crumb="Briefs / Lagos crime thriller" />
                  <main style={{ flex: 1, padding: '16px 24px 96px' }}><BriefDetail /></main>
                </div>
              </div>
            </div>

            {/* Screen 7: Catalog */}
            <div className="dark" style={{ width: 1440, minHeight: 1000, flexShrink: 0, border: '1px solid rgba(255,255,255,0.1)', borderRadius: 24, overflow: 'hidden', background: '#0f0f1a' }}>
              <div style={{ background: '#1a1a24', color: '#fff', padding: '16px 24px', fontWeight: 'bold' }}>Dashboard — Catalog</div>
              <div style={{ display: 'flex', minHeight: 944, background: 'var(--background)' }}>
                <Sidebar active="Catalog" />
                <div style={{ flex: 1, marginLeft: 256, display: 'flex', flexDirection: 'column' }}>
                  <Header crumb="Catalog" />
                  <main style={{ flex: 1, padding: '16px 24px 96px' }}><CatalogPage /></main>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
"""

ui_kits_temp_content = ui_kits_temp_content.replace("__DB_SIDEBAR_JSX__", db_sidebar_jsx)
ui_kits_temp_content = ui_kits_temp_content.replace("__DB_COMP_JSX__", db_comp_jsx)
ui_kits_temp_content = ui_kits_temp_content.replace("__DB_SCREENS_JSX__", db_screens_jsx)
ui_kits_temp_content = ui_kits_temp_content.replace("__MKT_COMP_JSX__", mkt_comp_jsx)
ui_kits_temp_content = ui_kits_temp_content.replace("__MKT_SCREENS_JSX__", mkt_screens_jsx)

# Save temporary html file in source directory so that it can resolve colors_and_type.css relatively
temp_html_path = os.path.join(source_dir, "ui_kits_temp.html")
with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(ui_kits_temp_content)

# Render UI Kits via Chrome
ui_kits_rendered = run_headless_chrome(temp_html_path)

# Clean up temporary HTML file
if os.path.exists(temp_html_path):
    os.remove(temp_html_path)

# In-line colors_and_type.css in UI Kits output
ui_kits_rendered = re.sub(r'<link rel="stylesheet" href="colors_and_type.css">', f"<style>\n{css_cleaned}\n</style>", ui_kits_rendered)
ui_kits_rendered = clean_html_source(ui_kits_rendered, "UI Kits Spec Grid (7 Screens). No JS required.")

# Save output
with open(os.path.join(output_dir, "ui_kits_figma_ready.html"), "w", encoding="utf-8") as f:
    f.write(ui_kits_rendered)
print("Saved ui_kits_figma_ready.html")

# -------------------------------------------------------------
# TASK 6: Figma Master Handoff Portal
# -------------------------------------------------------------
print("\n--- Creating Task 6: Handoff Master Portal ---")
portal_html = f"""<!-- Figma-Ready: SyncMaster Figma Handoff Portal. Use html.to.design to import assets. -->
<!doctype html>
<html lang="en" class="dark">
<head>
  <meta charset="utf-8">
  <title>SyncMaster — Figma Handoff Portal</title>
  <meta name="viewport" content="width=1440">
  <style>
    {css_cleaned}
    
    html, body {{ margin: 0; padding: 0; background: var(--sm-ink); color: var(--sm-fg-dark); font-family: var(--font-sans); }}
    .portal-container {{ width: 1440px; margin: 0 auto; padding: 64px 96px; box-sizing: border-box; }}
    
    .portal-header {{
      display: flex; align-items: center; justify-content: space-between;
      padding-bottom: 32px; border-bottom: 1px solid var(--border); margin-bottom: 64px;
    }}
    .portal-title {{ font-size: 56px; font-weight: 900; letter-spacing: -0.068em; line-height: 1.05; margin: 0; }}
    .portal-subtitle {{ font-size: 18px; color: var(--muted-foreground); font-weight: 500; margin-top: 12px; }}
    
    .grid-cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; margin-bottom: 64px; }}
    .handoff-card {{
      background: var(--sm-ink-raised); border: 1px solid var(--border); border-radius: 24px;
      padding: 32px; display: flex; flex-direction: column; gap: 24px;
      text-decoration: none; color: inherit; transition: all 300ms cubic-bezier(.4,0,.2,1);
    }}
    .handoff-card:hover {{
      border-color: rgba(75,75,192,0.4);
      transform: translateY(-4px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }}
    .handoff-card__icon {{
      width: 48px; height: 48px; border-radius: 12px; background: rgba(75,75,192,0.1);
      color: var(--primary); display: flex; items-center; justify-content: center;
      display: flex; align-items: center;
    }}
    .handoff-card__title {{ font-size: 24px; font-weight: 900; letter-spacing: -0.04em; margin: 0; }}
    .handoff-card__desc {{ font-size: 14px; color: var(--muted-foreground); line-height: 1.5; font-weight: 500; margin: 0; }}
    .handoff-card__meta {{
      font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.15em;
      text-transform: uppercase; color: var(--sm-acid); font-weight: 700; margin-top: auto;
    }}
    
    .instruction-block {{
      background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 24px;
      padding: 40px; margin-bottom: 64px;
    }}
    .instruction-title {{ font-size: 28px; font-weight: 900; letter-spacing: -0.04em; margin: 0 0 24px; }}
    .instruction-list {{ display: flex; flex-direction: column; gap: 16px; margin: 0; padding: 0; list-style: none; }}
    .instruction-item {{ display: flex; gap: 16px; font-size: 15px; line-height: 1.6; font-weight: 500; }}
    .instruction-num {{
      font-family: var(--font-mono); font-size: 12px; font-weight: 900;
      color: var(--sm-acid); width: 24px; height: 24px; border-radius: 6px;
      background: rgba(201,232,52,0.1); display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; margin-top: 2px;
    }}
    
    .footer-bar {{
      display: flex; align-items: center; justify-content: space-between;
      padding-top: 32px; border-top: 1px solid var(--border);
      font-family: var(--font-mono); font-size: 11px; color: var(--muted-foreground);
      letter-spacing: 0.1em; text-transform: uppercase;
    }}
  </style>
</head>
<body>

<div class="portal-container">
  <header class="portal-header">
    <div>
      <h1 class="portal-title">SyncMaster</h1>
      <p class="portal-subtitle">Figma Handoff Spec &amp; Pre-rendered Assets</p>
    </div>
    <span class="mono-tag" style="font-size: 11px; letter-spacing: 0.25em;">V1.0 · FIGMA COMPILATION</span>
  </header>

  <div class="grid-cards">
    <!-- Card 1 -->
    <a href="bts_carousel_figma_ready.html" class="handoff-card">
      <div class="handoff-card__icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37zM17.5 6.5h.01"/></svg>
      </div>
      <div>
        <h3 class="handoff-card__title">BTS Instagram Carousel</h3>
        <p class="handoff-card__desc" style="margin-top: 8px;">Behind-the-scenes slides optimized for instagram sharing. 5 frames horizontally aligned.</p>
      </div>
      <div class="handoff-card__meta">5 frames · 1080×1350px</div>
    </a>

    <!-- Card 2 -->
    <a href="carousel_templates_figma_ready.html" class="handoff-card">
      <div class="handoff-card__icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-10 9 10 9 10-9-10-9Z"/><path d="m2 17 10 9 10-9"/><path d="m2 12 10 9 10-9"/></svg>
      </div>
      <div>
        <h3 class="handoff-card__title">Carousel Templates</h3>
        <p class="handoff-card__desc" style="margin-top: 8px;">5 fully inlined and static Instagram carousel template slides showing positioning and brand taglines.</p>
      </div>
      <div class="handoff-card__meta">5 frames · 5400×1350px</div>
    </a>

    <!-- Card 3 -->
    <a href="design_system_figma_ready.html" class="handoff-card">
      <div class="handoff-card__icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18M3 9h18M9 15h12M3 15h6"/></svg>
      </div>
      <div>
        <h3 class="handoff-card__title">Design System Spec</h3>
        <p class="handoff-card__desc" style="margin-top: 8px;">Pre-rendered design tokens, buttons, inputs, badges, alerts, score bars, and navigation cards.</p>
      </div>
      <div class="handoff-card__meta">8 sections · 1440px wide</div>
    </a>

    <!-- Card 4 -->
    <a href="brand_guidelines_figma_ready.html" class="handoff-card">
      <div class="handoff-card__icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg>
      </div>
      <div>
        <h3 class="handoff-card__title">Brand Guidelines</h3>
        <p class="handoff-card__desc" style="margin-top: 8px;">Static spec sheets outlining Brand story, identity lockups, typography, voice guidelines, and iconography.</p>
      </div>
      <div class="handoff-card__meta">8 pages · 1440px wide</div>
    </a>

    <!-- Card 5 -->
    <a href="ui_kits_figma_ready.html" class="handoff-card" style="grid-column: span 2;">
      <div class="handoff-card__icon">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="10" rx="1"/><rect width="7" height="5" x="3" y="14" rx="1"/></svg>
      </div>
      <div>
        <h3 class="handoff-card__title">UI Kits Handoff Spec</h3>
        <p class="handoff-card__desc" style="margin-top: 8px;">A side-by-side spec grid containing all 7 marketing and product interface views: Landing page, Composer application, Supervisor briefs, Admin dashboard home, briefs list, details panel, and track catalog.</p>
      </div>
      <div class="handoff-card__meta">7 viewports · side-by-side grid</div>
    </a>
  </div>

  <section class="instruction-block">
    <h2 class="instruction-title">Figma Import Instructions</h2>
    <ul class="instruction-list">
      <li class="instruction-item">
        <span class="instruction-num">1</span>
        <div>
          <strong>Open Handoff portal or target file in your web browser.</strong><br>
          We recommend using Google Chrome. Right-click any of the cards above to open the compiled HTML specification page.
        </div>
      </li>
      <li class="instruction-item">
        <span class="instruction-num">2</span>
        <div>
          <strong>Run the html.to.design plugin in Figma.</strong><br>
          In Figma, open a new or existing design file, search for the plugin <code>html.to.design</code>, and open it.
        </div>
      </li>
      <li class="instruction-item">
        <span class="instruction-num">3</span>
        <div>
          <strong>Input the local URL or drag the HTML file.</strong><br>
          Copy the browser's URL (e.g. <code>file:///C:/Users/.../figma-handoff/ui_kits_figma_ready.html</code>) and paste it into the plugin's URL field, or upload the HTML file directly. Set the viewport width matching the target metadata (e.g., 1440px for UI Kits and Design System, 1080px for carousels).
        </div>
      </li>
      <li class="instruction-item">
        <span class="instruction-num">4</span>
        <div>
          <strong>Import and customize!</strong><br>
          Click <strong>Import</strong>. The plugin translates all HTML elements, fonts, colors, and layout nodes into fully-editable, pixel-perfect Figma layers automatically.
        </div>
      </li>
    </ul>
  </section>

  <footer class="footer-bar">
    <span>SYNCMASTER FIGMA HANDOFF SPEC v1.0</span>
    <span>CONFIDENTIAL · INTERNAL DESIGN &amp; DEVELOPMENT USE</span>
  </footer>
</div>

</body>
</html>
"""

with open(os.path.join(output_dir, "Figma_Master_Handoff.html"), "w", encoding="utf-8") as f:
    f.write(portal_html)
print("Saved Figma_Master_Handoff.html")

print("\nAll tasks compiled successfully!")
