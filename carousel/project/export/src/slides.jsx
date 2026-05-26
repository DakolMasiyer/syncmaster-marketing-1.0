// slides.jsx — Nine carousel slides for SyncMaster Carousel 01.
// Content sourced from the user's brief; visual system from the Linkedist audit.
//
// Slide registry:
//   1. Hook        — "You scored 4 Nollywood films. None of them pay you again."
//   2. Walk-in     — "A producer called you on a Tuesday."
//   3. Deal        — 12 cues / 3 weeks / ₦180,000 — full buyout
//   4. Release     — "The film hit Netflix. Then YouTube. Then a hotel lobby in Accra."
//   5. Silence     — "Your phone never rang again."
//   6. Reframe     — "This isn't a talent problem. / It's a rights problem."
//   7. Mechanism   — 2×2 grid: structured briefs / rights kept clean / curated / paid on placement
//   8. Promise     — "You scored it once. / Now it should pay you forever."
//   9. CTA         — JOIN THE WAITLIST

// Shared accent-emphasis span (for slide 6's "rights" and slide 8's payoff line)
function Accent({ children }) {
  return <span style={{ color: 'var(--accent)' }}>{children}</span>;
}

// ── Slide 1 — Hook ────────────────────────────────────────────────────────
function Slide1(props) {
  return (
    <SlideFrame {...props} num={1} category="THE COMPOSER PROBLEM">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 48 }}>
        <h1 style={{ ...DISPLAY_XL, textAlign: 'left' }}>
          You scored <span style={{ color: 'var(--accent)' }}>4 Nollywood films.</span>
          <br />None of them pay you again.
        </h1>
        <image-slot
          id="syncmaster-slide1-photo"
          shape="rounded"
          radius="40"
          placeholder="Drop a greyscale Lagos / film-set photo"
          style={{
            width: '100%',
            height: 360,
            filter: 'grayscale(1) contrast(0.95)',
            display: 'block',
          }}
        />
      </div>
    </SlideFrame>
  );
}

// ── Slide 2 — The walk-in ─────────────────────────────────────────────────
function Slide2(props) {
  return (
    <SlideFrame {...props} num={2} category="THE COMPOSER PROBLEM">
      <div style={{ textAlign: 'center' }}>
        <div style={EYEBROW}>SCENE ONE</div>
        <h1 style={{ ...DISPLAY_XL, textAlign: 'center' }}>
          A producer called you on a Tuesday.
        </h1>
      </div>
    </SlideFrame>
  );
}

// ── Slide 3 — The deal ────────────────────────────────────────────────────
function Slide3(props) {
  const rowLabel = {
    fontSize: 28,
    fontWeight: 400,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    opacity: 0.5,
  };
  const rowVal = {
    fontSize: 72,
    fontWeight: 600,
    letterSpacing: '-0.02em',
    lineHeight: 1,
  };
  const divider = {
    height: 1.5,
    background: 'currentColor',
    opacity: 0.1,
  };
  return (
    <SlideFrame {...props} num={3} category="THE COMPOSER PROBLEM">
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 32 }}>
        <div
          style={{
            background: 'var(--card)',
            border: '1.5px solid var(--card-border)',
            borderRadius: 40,
            padding: '64px 64px 56px',
            width: 740,
            boxShadow: '0 4px 24px rgba(0,0,0,0.04), 0 1px 0 rgba(0,0,0,0.02)',
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
              <span style={rowLabel}>Cues</span>
              <span style={rowVal}>12</span>
            </div>
            <div style={divider} />
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
              <span style={rowLabel}>Timeline</span>
              <span style={rowVal}>3 weeks</span>
            </div>
            <div style={divider} />
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 8, marginTop: 8 }}>
              <span style={rowLabel}>Fee</span>
              <span
                style={{
                  fontSize: 124,
                  fontWeight: 700,
                  letterSpacing: '-0.04em',
                  lineHeight: 1,
                  alignSelf: 'center',
                }}
              >
                ₦180,000
              </span>
              <span
                style={{
                  alignSelf: 'center',
                  fontSize: 26,
                  fontWeight: 500,
                  letterSpacing: '0.06em',
                  textTransform: 'uppercase',
                  opacity: 0.55,
                  marginTop: 4,
                }}
              >
                — full buyout —
              </span>
            </div>
          </div>
        </div>
        <div style={{ ...CAPTION, fontSize: 26, fontStyle: 'italic' }}>
          Signed on WhatsApp. No contract you kept.
        </div>
      </div>
    </SlideFrame>
  );
}

// ── Slide 4 — The release ─────────────────────────────────────────────────
function Slide4(props) {
  return (
    <SlideFrame {...props} num={4} category="THE COMPOSER PROBLEM">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 48 }}>
        <h1 style={{ ...DISPLAY_LG, textAlign: 'left' }}>
          The film hit Netflix.
          <br />Then YouTube.
          <br />Then a hotel lobby in Accra.
        </h1>
        <image-slot
          id="syncmaster-slide4-photo"
          shape="rounded"
          radius="40"
          placeholder="Drop a greyscale street / cinema / TV photo"
          style={{
            width: '100%',
            height: 320,
            filter: 'grayscale(1) contrast(0.95)',
            display: 'block',
          }}
        />
      </div>
    </SlideFrame>
  );
}

// ── Slide 5 — The silence ─────────────────────────────────────────────────
function Slide5(props) {
  return (
    <SlideFrame {...props} num={5} category="THE COMPOSER PROBLEM">
      <h1 style={{ ...DISPLAY_XL, textAlign: 'center' }}>
        Your phone never rang again.
      </h1>
    </SlideFrame>
  );
}

// ── Slide 6 — The reframe ─────────────────────────────────────────────────
function Slide6(props) {
  return (
    <SlideFrame {...props} num={6} category="THE TURN">
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ ...DISPLAY_XL, marginBottom: 24 }}>
          This isn't a talent problem.
        </h1>
        <h1 style={{ ...DISPLAY_XL }}>
          It's a <Accent>rights</Accent> problem.
        </h1>
      </div>
    </SlideFrame>
  );
}

// ── Slide 7 — The mechanism (2×2 grid with hand-drawn icons) ──────────────
function MechCard({ title, caption, icon }) {
  return (
    <div
      style={{
        background: 'var(--card)',
        border: '1.5px solid var(--card-border)',
        borderRadius: 32,
        padding: '36px 32px 32px',
        display: 'flex',
        flexDirection: 'column',
        gap: 14,
        boxShadow: '0 4px 24px rgba(0,0,0,0.04)',
      }}
    >
      <div style={{ height: 56, width: 56, display: 'flex', alignItems: 'center', justifyContent: 'flex-start' }}>
        {icon}
      </div>
      <div style={{ fontSize: 30, fontWeight: 600, letterSpacing: '-0.02em', lineHeight: 1.1 }}>{title}</div>
      <div style={{ fontSize: 20, lineHeight: 1.35, opacity: 0.7 }}>{caption}</div>
    </div>
  );
}

// Hand-drawn-feel SVG glyphs. Stroked, slightly wonky, no fills.
const ICON_STROKE = 'var(--ink)';
const Icon = {
  brief: (
    <svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke={ICON_STROKE} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 9 C10.5 8 11 7 12 7 L34 7 C35 7 35.5 8 35.5 8.5 L36 41 C36 42 35 43 34 42.7 L11.5 42 C10.5 41.7 10 41 10 40 Z" />
      <path d="M16 16 L29 16.2" />
      <path d="M16 23 L31 23.4" />
      <path d="M16 30 L25 30" />
      <circle cx="40" cy="38" r="4" />
      <path d="M43 41 L46 44.5" />
    </svg>
  ),
  rights: (
    <svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke={ICON_STROKE} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M26 5 C19 8 14 9 9 9 C8.5 22 11 36 26 46 C41 36 43.5 22 43 9 C38 9 33 8 26 5 Z" />
      <path d="M18 24 L24 30 L34 18" />
    </svg>
  ),
  curated: (
    <svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke={ICON_STROKE} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="13" r="3" />
      <circle cx="22" cy="13" r="3" />
      <circle cx="32" cy="13" r="3" />
      <circle cx="42" cy="13" r="3" />
      <circle cx="12" cy="26" r="3" />
      <path d="M22 23 L32 29" />
      <path d="M32 23 L22 29" />
      <circle cx="32" cy="26" r="3" />
      <path d="M27 39 L27 47" />
      <path d="M22 44 L27 47 L32 44" />
      <text x="6" y="48" fontSize="9" fontFamily="Space Grotesk" stroke="none" fill={ICON_STROKE} fontWeight="600">5</text>
    </svg>
  ),
  paid: (
    <svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke={ICON_STROKE} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="18" cy="22" r="11" />
      <path d="M14 22 L22 22 M14 18 L24 18 M16 26 C18 28 21 27 22 25 C23 23 21 22 18 21 C15 20 13 19 14 17 C15 15 18 14 20 16" />
      <path d="M32 30 L40 30 L40 38 L32 38 Z" />
      <path d="M34 30 L34 27 C34 25 36 24 38 24 C40 24 42 25 42 27 L42 30" />
      <path d="M36 34 L36 35" />
    </svg>
  ),
};

function Slide7(props) {
  return (
    <SlideFrame {...props} num={7} category="WHAT WE DO">
      <div style={{ display: 'flex', flexDirection: 'column', gap: 40 }}>
        <h1 style={{ ...DISPLAY_MD, textAlign: 'left' }}>
          What SyncMaster does:
        </h1>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gridTemplateRows: '1fr 1fr',
            gap: 24,
          }}
        >
          <MechCard
            icon={Icon.brief}
            title="Structured briefs"
            caption="Producers post real opportunities. You see them first."
          />
          <MechCard
            icon={Icon.rights}
            title="Rights kept clean"
            caption="Sync licences, not buyouts. You keep the publishing."
          />
          <MechCard
            icon={Icon.curated}
            title="Curated, not flooded"
            caption="5 composers submit per brief. Not 500."
          />
          <MechCard
            icon={Icon.paid}
            title="Paid on placement"
            caption="When your cue is used, you get paid. Every time."
          />
        </div>
      </div>
    </SlideFrame>
  );
}

// ── Slide 8 — The promise ─────────────────────────────────────────────────
function Slide8(props) {
  return (
    <SlideFrame {...props} num={8} category="THE TURN">
      <div style={{ textAlign: 'center' }}>
        <div
          style={{
            fontSize: 220,
            fontWeight: 700,
            lineHeight: 0.7,
            color: 'var(--accent)',
            marginBottom: 24,
            fontFamily: '"Space Grotesk", serif',
          }}
        >
          &rdquo;
        </div>
        <h1 style={{ ...DISPLAY_XL, marginBottom: 16 }}>
          You scored it once.
        </h1>
        <h1 style={{ ...DISPLAY_XL, color: 'var(--accent)' }}>
          Now it should pay you forever.
        </h1>
      </div>
    </SlideFrame>
  );
}

// ── Slide 9 — CTA ─────────────────────────────────────────────────────────
function Slide9(props) {
  return (
    <SlideFrame
      {...props}
      num={9}
      category="JOIN NOW"
      showSwipe={false}
      centerWordmark={true}
    >
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 56, textAlign: 'center' }}>
        <div>
          <h1 style={{ ...DISPLAY_XL, marginBottom: 28 }}>
            SyncMaster is live.
          </h1>
          <div
            style={{
              fontSize: 36,
              fontWeight: 400,
              lineHeight: 1.3,
              opacity: 0.7,
              maxWidth: 760,
              margin: '0 auto',
            }}
          >
            We're onboarding Nigerian composers right now.
          </div>
        </div>
        <div
          style={{
            background: 'var(--accent)',
            color: '#fff',
            borderRadius: 9999,
            padding: '32px 56px',
            fontSize: 44,
            fontWeight: 600,
            letterSpacing: '0.04em',
            textTransform: 'uppercase',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 20,
            boxShadow: '0 10px 30px rgba(54,97,254,0.25)',
          }}
        >
          Join the waitlist
          <span style={{ fontSize: 44, lineHeight: 1 }}>→</span>
        </div>
        <div style={{ ...CAPTION, fontSize: 24 }}>
          Link in bio. Takes 60 seconds.
        </div>
      </div>
    </SlideFrame>
  );
}

Object.assign(window, {
  Slide1, Slide2, Slide3, Slide4, Slide5, Slide6, Slide7, Slide8, Slide9,
});
