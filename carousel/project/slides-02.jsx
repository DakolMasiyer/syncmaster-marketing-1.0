// slides-02.jsx — SyncMaster Carousel 02 — "Did You Catch This?"
// 10 slides. SyncMaster native brand: purple #5252E0 + lime #C9E834.
// Slides 1, 7–10: BrandSlideFrame (purple bg, glow motif).
// Slides 2–6:     PhotoSlideFrame (full-bleed blurred image-slot + frosted card).
//
// Slide registry:
//   1. Opener    — "Your favourite songs have been on the world's biggest stages."
//   2. One Dance — Drake ft. Wizkid · NBA Playoffs 2016
//   3. Location  — Burna Boy · Netflix Top Boy Season 1
//   4. Free Mind — Tems · Spider-Man: Across the Spider-Verse
//   5. Peru      — Fireboy DML · UEFA Champions League
//   6. Wakanda   — Various · Black Panther: Wakanda Forever · Disney+
//   7. The Turn  — "So what actually happened when those songs played?"
//   8. The Stats — 812% streams / $5k–$500k fees / $178M royalties
//   9. The Gap   — "African composers make the music the world wants."
//  10. CTA       — "That's the gap we're closing."

const BRAND_PURPLE = '#5252E0';
const BRAND_LIME   = '#C9E834';

// ── Glow orb — radial lime bloom from the SyncMaster brand screenshots ────
function GlowOrb({ top = '40%', left = '50%', size = 480, opacity = 0.3 }) {
  return (
    <div
      style={{
        position: 'absolute',
        top,
        left,
        transform: 'translate(-50%, -50%)',
        width: size,
        height: size,
        borderRadius: '50%',
        background: `radial-gradient(circle, ${BRAND_LIME}55 0%, ${BRAND_LIME}18 45%, transparent 70%)`,
        opacity,
        pointerEvents: 'none',
        zIndex: 0,
      }}
    />
  );
}

// ── BrandSlideFrame — pure purple brand slides ────────────────────────────
function BrandSlideFrame({
  children,
  num,
  total = 10,
  category = 'DID YOU CATCH THIS?',
  showSwipe = true,
  centerWordmark = false,
  filledPills = false,
  showGlow = true,
  glowTop = '40%',
  glowSize = 480,
  glowOpacity = 0.3,
  accent = BRAND_LIME,
}) {
  const cssVars = {
    '--pill-stroke': 'rgba(255,255,255,0.42)',
    '--bg': BRAND_PURPLE,
    '--ink': '#FFFFFF',
    '--accent': accent,
  };
  return (
    <div
      style={{
        ...cssVars,
        position: 'relative',
        width: SLIDE_W,
        height: SLIDE_H,
        background: BRAND_PURPLE,
        color: '#FFFFFF',
        fontFamily: '"Space Grotesk", sans-serif',
        overflow: 'hidden',
      }}
    >
      {showGlow && <GlowOrb top={glowTop} size={glowSize} opacity={glowOpacity} />}

      {/* Wordmark */}
      <div
        style={{
          position: 'absolute',
          top: 91,
          left: centerWordmark ? '50%' : 95,
          transform: centerWordmark ? 'translateX(-50%)' : 'none',
          fontSize: 22,
          fontWeight: 600,
          letterSpacing: '0.10em',
          textTransform: 'uppercase',
          lineHeight: 1,
          zIndex: 2,
        }}
      >
        SYNCMASTER
      </div>

      {showSwipe && (
        <div style={{ position: 'absolute', top: 79, right: 79, zIndex: 2 }}>
          <SwipePill filled={filledPills} />
        </div>
      )}

      <div style={{ position: 'absolute', bottom: 79, left: 79, zIndex: 2 }}>
        <Pill filled={filledPills}>{category}</Pill>
      </div>

      <div style={{ position: 'absolute', bottom: 79, right: 79, zIndex: 2 }}>
        <Pill filled={filledPills}>
          {String(num).padStart(2, '0')} / {String(total).padStart(2, '0')}
        </Pill>
      </div>

      {/* Main stage */}
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 0,
          right: 0,
          bottom: 150,
          padding: '0 95px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          zIndex: 1,
        }}
      >
        {children}
      </div>
    </div>
  );
}

// ── PhotoSlideFrame — blurred full-bleed image-slot slides ────────────────
function PhotoSlideFrame({
  children,
  num,
  total = 10,
  category = 'DID YOU CATCH THIS?',
  showSwipe = true,
  filledPills = false,
  bgSlotId,
  bgPlaceholder,
  accent = BRAND_LIME,
}) {
  const cssVars = {
    '--pill-stroke': 'rgba(255,255,255,0.55)',
    '--bg': '#0A0A20',
    '--ink': '#FFFFFF',
    '--accent': accent,
  };
  return (
    <div
      style={{
        ...cssVars,
        position: 'relative',
        width: SLIDE_W,
        height: SLIDE_H,
        background: '#0A0A20',
        color: '#FFFFFF',
        fontFamily: '"Space Grotesk", sans-serif',
        overflow: 'hidden',
      }}
    >
      {/* Full-bleed background image — blurred + darkened */}
      <image-slot
        id={bgSlotId}
        placeholder={bgPlaceholder}
        style={{
          position: 'absolute',
          top: '0',
          left: '0',
          width: '100%',
          height: '100%',
          display: 'block',
          filter: 'blur(20px) brightness(0.28) saturate(0.65)',
          zIndex: '0',
        }}
      />

      {/* Dark purple gradient overlay */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(170deg, rgba(10,4,40,0.62) 0%, rgba(6,2,25,0.84) 100%)',
          zIndex: 1,
        }}
      />

      {/* Wordmark */}
      <div
        style={{
          position: 'absolute',
          top: 91,
          left: 95,
          fontSize: 22,
          fontWeight: 600,
          letterSpacing: '0.10em',
          textTransform: 'uppercase',
          lineHeight: 1,
          zIndex: 3,
        }}
      >
        SYNCMASTER
      </div>

      {showSwipe && (
        <div style={{ position: 'absolute', top: 79, right: 79, zIndex: 3 }}>
          <SwipePill filled={filledPills} />
        </div>
      )}

      <div style={{ position: 'absolute', bottom: 79, left: 79, zIndex: 3 }}>
        <Pill filled={filledPills}>{category}</Pill>
      </div>

      <div style={{ position: 'absolute', bottom: 79, right: 79, zIndex: 3 }}>
        <Pill filled={filledPills}>
          {String(num).padStart(2, '0')} / {String(total).padStart(2, '0')}
        </Pill>
      </div>

      {/* Content */}
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 0,
          right: 0,
          bottom: 150,
          padding: '0 95px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          zIndex: 2,
        }}
      >
        {children}
      </div>
    </div>
  );
}

// ── NowPlayingCard — frosted glass music player pill ──────────────────────
function NowPlayingCard({ track, artist }) {
  const bars = [12, 20, 8, 22, 14, 18, 10];
  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 22,
        background: 'rgba(255,255,255,0.09)',
        backdropFilter: 'blur(28px)',
        WebkitBackdropFilter: 'blur(28px)',
        border: '1px solid rgba(255,255,255,0.16)',
        borderRadius: 22,
        padding: '20px 32px',
        maxWidth: 740,
      }}
    >
      {/* Lime play button */}
      <div
        style={{
          width: 56,
          height: 56,
          borderRadius: '50%',
          background: BRAND_LIME,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}
      >
        <svg width="20" height="20" viewBox="0 0 20 20" fill="#0D0D18">
          <path d="M6 3.8L16 10L6 16.2V3.8Z" />
        </svg>
      </div>

      {/* Track info */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            fontSize: 30,
            fontWeight: 600,
            lineHeight: 1.15,
            letterSpacing: '-0.01em',
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
          }}
        >
          {track}
        </div>
        <div style={{ fontSize: 22, opacity: 0.58, marginTop: 6, letterSpacing: '0.01em' }}>
          {artist}
        </div>
      </div>

      {/* Static waveform bars */}
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: 4,
          height: 26,
          flexShrink: 0,
        }}
      >
        {bars.map((h, i) => (
          <div
            key={i}
            style={{
              width: 3,
              height: h,
              background: BRAND_LIME,
              borderRadius: 2,
              opacity: 0.82,
            }}
          />
        ))}
      </div>
    </div>
  );
}

// ── SVG icons for Slide 8 stats (hand-drawn feel, stroked) ───────────────
const ICON_S = 'rgba(255,255,255,0.88)';
const StatIcons = {
  trending: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke={ICON_S} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 36 L15 22 L23 28 L35 12 L43 12" />
      <path d="M35 12 L43 12 L43 20" />
      <path d="M5 44 L43 44" strokeOpacity="0.2" />
    </svg>
  ),
  receipt: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke={ICON_S} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 5 L37 5 L37 44 L33 41 L29 44 L25 41 L21 44 L17 41 L13 44 L11 41 Z" />
      <path d="M23 14 L23 32 M25 14 C28 14 30 15.5 30 18.5 C30 21.5 28 23 25 23 L23 23" />
      <path d="M17 29 L31 29" />
    </svg>
  ),
  globe: (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke={ICON_S} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="24" cy="24" r="18" />
      <path d="M6 24 H42" />
      <path d="M24 6 C17 12 17 36 24 42 C31 36 31 12 24 6" />
      <path d="M8.5 16 C13 18.5 20 19.5 24 19.5 C28 19.5 35 18.5 39.5 16" />
      <path d="M8.5 32 C13 29.5 20 28.5 24 28.5 C28 28.5 35 29.5 39.5 32" />
    </svg>
  ),
};

// ── StatBlock for Slide 8 ─────────────────────────────────────────────────
function StatBlock({ icon, stat, label }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 36,
        padding: '30px 40px',
        background: 'rgba(255,255,255,0.07)',
        border: '1px solid rgba(255,255,255,0.11)',
        borderRadius: 28,
      }}
    >
      <div style={{ flexShrink: 0 }}>{icon}</div>
      <div>
        <div
          style={{
            fontSize: 64,
            fontWeight: 700,
            letterSpacing: '-0.04em',
            lineHeight: 1,
            color: BRAND_LIME,
          }}
        >
          {stat}
        </div>
        <div
          style={{
            fontSize: 25,
            lineHeight: 1.35,
            opacity: 0.76,
            marginTop: 8,
          }}
        >
          {label}
        </div>
      </div>
    </div>
  );
}

// ── Eyebrow style for dark slides ─────────────────────────────────────────
const EYEBROW_DARK = {
  fontSize: 22,
  fontWeight: 500,
  letterSpacing: '0.18em',
  textTransform: 'uppercase',
  marginBottom: 0,
  color: 'rgba(255,255,255,0.52)',
  fontFamily: '"Space Grotesk", sans-serif',
};

// ─────────────────────────────────────────────────────────────────────────────
// SLIDES
// ─────────────────────────────────────────────────────────────────────────────

// ── Slide 1 — Series Opener ───────────────────────────────────────────────
function Slide1(props) {
  return (
    <BrandSlideFrame
      {...props}
      num={1}
      category="DID YOU CATCH THIS?"
      glowTop="48%"
      glowSize={580}
      glowOpacity={0.28}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 40 }}>
        <h1
          style={{
            ...DISPLAY_XL,
            fontSize: 98,
            lineHeight: 1.02,
            color: '#FFFFFF',
            textAlign: 'left',
            margin: 0,
          }}
        >
          Your favourite songs have been on the world's biggest stages.
        </h1>
        <div
          style={{
            fontSize: 46,
            fontWeight: 500,
            letterSpacing: '-0.015em',
            lineHeight: 1.1,
            color: BRAND_LIME,
          }}
        >
          Did you catch them?
        </div>
      </div>
    </BrandSlideFrame>
  );
}

// ── Slide 2 — One Dance ───────────────────────────────────────────────────
function Slide2(props) {
  return (
    <PhotoSlideFrame
      {...props}
      num={2}
      bgSlotId="s02-nba"
      bgPlaceholder="Drop an NBA court / arena photo here"
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 56 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <NowPlayingCard track="One Dance" artist="Drake ft. Wizkid & Kyla" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={EYEBROW_DARK}>Did you catch it at the…</div>
          <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
            NBA Playoffs. 2016.
          </h1>
          <p style={{ fontSize: 34, lineHeight: 1.4, margin: '12px 0 0', color: 'rgba(255,255,255,0.75)' }}>
            That wasn't radio.{' '}
            <span style={{ color: BRAND_LIME, fontStyle: 'italic' }}>That was a sync deal.</span>
          </p>
        </div>
      </div>
    </PhotoSlideFrame>
  );
}

// ── Slide 3 — Location ────────────────────────────────────────────────────
function Slide3(props) {
  return (
    <PhotoSlideFrame
      {...props}
      num={3}
      bgSlotId="s03-topboy"
      bgPlaceholder="Drop a Top Boy still or dark London street photo here"
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 56 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <NowPlayingCard track="Location" artist="Burna Boy" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={EYEBROW_DARK}>Did you catch it on…</div>
          <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
            Netflix. Top Boy. Season 1.
          </h1>
          <p style={{ fontSize: 34, lineHeight: 1.4, margin: '12px 0 0', color: 'rgba(255,255,255,0.75)' }}>
            Lagos sound. London screen.{' '}
            <span style={{ color: BRAND_LIME, fontStyle: 'italic' }}>That was a sync deal.</span>
          </p>
        </div>
      </div>
    </PhotoSlideFrame>
  );
}

// ── Slide 4 — Free Mind ───────────────────────────────────────────────────
function Slide4(props) {
  return (
    <PhotoSlideFrame
      {...props}
      num={4}
      bgSlotId="s04-spiderman"
      bgPlaceholder="Drop a Spider-Man: Across the Spider-Verse still or poster here"
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 56 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <NowPlayingCard track="Free Mind" artist="Tems" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={EYEBROW_DARK}>Did you catch it in…</div>
          <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
            Spider-Man: Across the Spider-Verse.
          </h1>
          <p style={{ fontSize: 34, lineHeight: 1.4, margin: '12px 0 0', color: 'rgba(255,255,255,0.75)' }}>
            End credits. Everyone Shazamed it.{' '}
            <span style={{ color: BRAND_LIME, fontStyle: 'italic' }}>That was a sync deal.</span>
          </p>
        </div>
      </div>
    </PhotoSlideFrame>
  );
}

// ── Slide 5 — Peru ───────────────────────────────────────────────────────
function Slide5(props) {
  return (
    <PhotoSlideFrame
      {...props}
      num={5}
      bgSlotId="s05-ucl"
      bgPlaceholder="Drop a UEFA Champions League broadcast graphic or stadium photo here"
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 56 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <NowPlayingCard track="Peru" artist="Fireboy DML" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={EYEBROW_DARK}>Did you catch it at the…</div>
          <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
            UEFA Champions League. 180 countries watching.
          </h1>
          <p style={{ fontSize: 34, lineHeight: 1.4, margin: '12px 0 0', color: 'rgba(255,255,255,0.75)' }}>
            One track. One deal.{' '}
            <span style={{ color: BRAND_LIME, fontStyle: 'italic' }}>One billion impressions.</span>
          </p>
        </div>
      </div>
    </PhotoSlideFrame>
  );
}

// ── Slide 6 — Wakanda Forever ─────────────────────────────────────────────
function Slide6(props) {
  return (
    <PhotoSlideFrame
      {...props}
      num={6}
      bgSlotId="s06-wakanda"
      bgPlaceholder="Drop a Black Panther: Wakanda Forever poster or still here"
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 56 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <NowPlayingCard track="Wakanda Forever OST" artist="Various African Artists" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={EYEBROW_DARK}>Did you catch it in…</div>
          <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
            Black Panther: Wakanda Forever. Disney+.
          </h1>
          <p style={{ fontSize: 34, lineHeight: 1.4, margin: '12px 0 0', color: 'rgba(255,255,255,0.75)' }}>
            The whole film was the brief.{' '}
            <span style={{ color: BRAND_LIME, fontStyle: 'italic' }}>That was a sync deal.</span>
          </p>
        </div>
      </div>
    </PhotoSlideFrame>
  );
}

// ── Slide 7 — The Turn ────────────────────────────────────────────────────
function Slide7(props) {
  return (
    <BrandSlideFrame
      {...props}
      num={7}
      category="THE TURN"
      showGlow={true}
      glowTop="58%"
      glowSize={420}
      glowOpacity={0.22}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 44 }}>
        <div style={{ ...EYEBROW_DARK, letterSpacing: '0.22em' }}>THE QUESTION</div>
        <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
          So what actually happened when those songs played?
        </h1>
        <div
          style={{
            fontSize: 38,
            fontWeight: 500,
            lineHeight: 1.25,
            letterSpacing: '-0.01em',
            color: BRAND_LIME,
          }}
        >
          This is what a sync deal does.
        </div>
      </div>
    </BrandSlideFrame>
  );
}

// ── Slide 8 — The Stats ───────────────────────────────────────────────────
function Slide8(props) {
  return (
    <BrandSlideFrame
      {...props}
      num={8}
      category="SYNC DATA"
      showGlow={true}
      glowTop="12%"
      glowSize={360}
      glowOpacity={0.2}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div
          style={{
            fontSize: 36,
            fontWeight: 600,
            letterSpacing: '-0.015em',
            lineHeight: 1.2,
            marginBottom: 10,
            color: '#FFFFFF',
          }}
        >
          One placement changes the trajectory of a career.
        </div>

        <StatBlock
          icon={StatIcons.trending}
          stat="812%"
          label="Streams jump the week a track airs on a major TV show"
        />
        <StatBlock
          icon={StatIcons.receipt}
          stat="$5k – $500k"
          label="Sync fees per placement depending on project and territory"
        />
        <StatBlock
          icon={StatIcons.globe}
          stat="$178M"
          label="US sync royalties in H1 2022 alone — up 30% year on year"
        />

        <div
          style={{
            fontSize: 18,
            opacity: 0.38,
            marginTop: 2,
            lineHeight: 1.4,
            fontStyle: 'italic',
          }}
        >
          Sources: Blakmarigold / industry data · Trolley sync royalty report
        </div>
      </div>
    </BrandSlideFrame>
  );
}

// ── Slide 9 — The Gap ─────────────────────────────────────────────────────
function Slide9(props) {
  return (
    <BrandSlideFrame
      {...props}
      num={9}
      category="THE GAP"
      showGlow={false}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 52 }}>
        <h1 style={{ ...DISPLAY_LG, color: '#FFFFFF', margin: 0 }}>
          African composers make the music the world wants.
        </h1>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <p style={{ fontSize: 38, fontWeight: 500, lineHeight: 1.3, margin: 0, opacity: 0.88 }}>
            But most never see a sync deal.
          </p>
          <p style={{ fontSize: 30, lineHeight: 1.45, margin: 0, opacity: 0.55 }}>
            No agent. No publisher. No pathway in.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <p
            style={{
              fontSize: 44,
              fontWeight: 600,
              letterSpacing: '-0.02em',
              lineHeight: 1.15,
              margin: 0,
              color: BRAND_LIME,
            }}
          >
            The music is world-class.
          </p>
          <p
            style={{
              fontSize: 44,
              fontWeight: 600,
              letterSpacing: '-0.02em',
              lineHeight: 1.15,
              margin: 0,
              color: BRAND_LIME,
            }}
          >
            The infrastructure isn't. Yet.
          </p>
        </div>
      </div>
    </BrandSlideFrame>
  );
}

// ── Slide 10 — CTA ───────────────────────────────────────────────────────
function Slide10(props) {
  return (
    <BrandSlideFrame
      {...props}
      num={10}
      category="JOIN NOW"
      showSwipe={false}
      centerWordmark={true}
      glowTop="46%"
      glowSize={640}
      glowOpacity={0.34}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 52,
          textAlign: 'center',
        }}
      >
        <div>
          <h1 style={{ ...DISPLAY_XL, color: '#FFFFFF', margin: 0 }}>
            That's the gap we're closing.
          </h1>
          <p
            style={{
              fontSize: 34,
              fontWeight: 400,
              lineHeight: 1.35,
              color: 'rgba(255,255,255,0.72)',
              maxWidth: 800,
              margin: '28px auto 0',
            }}
          >
            SyncMaster connects African composers to global sync briefs — curated, vetted, rights-ready.
          </p>
        </div>

        {/* CTA button */}
        <div
          style={{
            background: BRAND_LIME,
            color: '#0D0D18',
            borderRadius: 9999,
            padding: '32px 60px',
            fontSize: 40,
            fontWeight: 700,
            letterSpacing: '0.02em',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 18,
            boxShadow: `0 14px 48px ${BRAND_LIME}44`,
          }}
        >
          Apply as a composer
          <span style={{ fontSize: 40, lineHeight: 1 }}>→</span>
        </div>

        <div
          style={{
            fontSize: 26,
            fontWeight: 400,
            lineHeight: 1.35,
            color: 'rgba(255,255,255,0.48)',
            fontFamily: '"Space Grotesk", sans-serif',
          }}
        >
          Link in bio · Takes 60 seconds
        </div>
      </div>
    </BrandSlideFrame>
  );
}

Object.assign(window, {
  Slide1, Slide2, Slide3, Slide4, Slide5,
  Slide6, Slide7, Slide8, Slide9, Slide10,
});
