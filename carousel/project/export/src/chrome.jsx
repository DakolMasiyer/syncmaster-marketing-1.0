// chrome.jsx — Shared slide chrome: theme tokens, dot grid, pills, slide frame.
// Tokens trace to the Linkedist audit (warm off-white, dot grid, outlined pills, blue accent).
// Slides are 1080×1350 portrait 4:5.

const SLIDE_W = 1080;
const SLIDE_H = 1350;

function DotGrid({ show = true }) {
  if (!show) return null;
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage:
          'radial-gradient(circle, var(--grid) 1.5px, transparent 1.6px)',
        backgroundSize: '35px 35px',
        backgroundPosition: '0 0',
        pointerEvents: 'none',
      }}
    />
  );
}

// Outlined or filled pill; uppercase, letter-spaced, Space Grotesk.
function Pill({ children, filled = false, size = 'md', style = {} }) {
  const px = size === 'lg' ? 28 : 24;
  const py = size === 'lg' ? 12 : 10;
  const fs = size === 'lg' ? 24 : 22;
  return (
    <div
      style={{
        border: filled ? 'none' : '2px solid var(--pill-stroke)',
        background: filled ? 'var(--pill-stroke)' : 'transparent',
        color: filled ? 'var(--bg)' : 'var(--ink)',
        borderRadius: 9999,
        padding: `${py}px ${px}px`,
        fontSize: fs,
        fontWeight: 500,
        letterSpacing: '0.04em',
        textTransform: 'uppercase',
        lineHeight: 1,
        whiteSpace: 'nowrap',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 10,
        fontFamily: '"Space Grotesk", sans-serif',
        ...style,
      }}
    >
      {children}
    </div>
  );
}

function SwipePill({ filled = false }) {
  return (
    <div
      style={{
        border: filled ? 'none' : '2px solid var(--pill-stroke)',
        background: filled ? 'var(--pill-stroke)' : 'transparent',
        color: filled ? 'var(--bg)' : 'var(--ink)',
        borderRadius: 9999,
        width: 88,
        height: 44,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <svg width="32" height="14" viewBox="0 0 32 14" fill="none"
        stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M2 7 H28 M22 1.5 L28 7 L22 12.5" />
      </svg>
    </div>
  );
}

// Theme tokens. mode is a tweak: paper (warm off-white) | pure (paper white) | dark.
function themeVars(mode, accent) {
  const base = {
    paper: { bg: '#F9F9F9', ink: '#000000', pill: '#0A0A0A', grid: '#E6E6E6', card: '#FFFFFF', cardBorder: 'rgba(0,0,0,0.05)' },
    pure:  { bg: '#FFFFFF', ink: '#000000', pill: '#0A0A0A', grid: '#E8E8E8', card: '#FAFAF7', cardBorder: 'rgba(0,0,0,0.06)' },
    dark:  { bg: '#0E0E10', ink: '#F4F2EC', pill: '#F4F2EC', grid: 'rgba(244,242,236,0.08)', card: '#16161A', cardBorder: 'rgba(255,255,255,0.08)' },
  }[mode] || { bg: '#F9F9F9', ink: '#000', pill: '#0A0A0A', grid: '#E6E6E6', card: '#FFFFFF', cardBorder: 'rgba(0,0,0,0.05)' };
  return {
    '--bg': base.bg,
    '--ink': base.ink,
    '--pill-stroke': base.pill,
    '--grid': base.grid,
    '--accent': accent,
    '--card': base.card,
    '--card-border': base.cardBorder,
  };
}

// SlideFrame — page chrome wrapper. Children render in the main stage.
function SlideFrame({
  children,
  num,
  total = 9,
  category = 'THE COMPOSER PROBLEM',
  showSwipe = true,
  centerWordmark = false,
  filledPills = false,
  showGrid = true,
  mode = 'paper',
  accent = '#3661FE',
  pad = true,
}) {
  return (
    <div
      style={{
        ...themeVars(mode, accent),
        position: 'relative',
        width: SLIDE_W,
        height: SLIDE_H,
        background: 'var(--bg)',
        color: 'var(--ink)',
        fontFamily: '"Space Grotesk", sans-serif',
        overflow: 'hidden',
      }}
    >
      <DotGrid show={showGrid} />

      {/* Top-left wordmark */}
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

      {/* Top-right swipe pill */}
      {showSwipe && (
        <div style={{ position: 'absolute', top: 79, right: 79, zIndex: 2 }}>
          <SwipePill filled={filledPills} />
        </div>
      )}

      {/* Bottom-left category */}
      <div style={{ position: 'absolute', bottom: 79, left: 79, zIndex: 2 }}>
        <Pill filled={filledPills}>{category}</Pill>
      </div>

      {/* Bottom-right counter */}
      <div style={{ position: 'absolute', bottom: 79, right: 79, zIndex: 2 }}>
        <Pill filled={filledPills}>
          {String(num).padStart(2, '0')} / {String(total).padStart(2, '0')}
        </Pill>
      </div>

      {/* Main stage 150–1200, optional inner padding */}
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 0,
          right: 0,
          bottom: 150,
          padding: pad ? '0 95px' : 0,
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

// Shared type ramps. Display headlines are tight, geometric, big.
const DISPLAY_XL = {
  fontFamily: '"Space Grotesk", sans-serif',
  fontSize: 96,
  lineHeight: 1.02,
  letterSpacing: '-0.025em',
  fontWeight: 600,
  textWrap: 'balance',
  margin: 0,
};
const DISPLAY_LG = { ...DISPLAY_XL, fontSize: 84 };
const DISPLAY_MD = { ...DISPLAY_XL, fontSize: 64, fontWeight: 500 };
const EYEBROW = {
  fontSize: 22,
  fontWeight: 500,
  letterSpacing: '0.18em',
  textTransform: 'uppercase',
  marginBottom: 28,
  opacity: 0.6,
  fontFamily: '"Space Grotesk", sans-serif',
};
const CAPTION = {
  fontSize: 28,
  fontWeight: 400,
  lineHeight: 1.35,
  opacity: 0.65,
  fontFamily: '"Space Grotesk", sans-serif',
  textAlign: 'center',
};

Object.assign(window, {
  SLIDE_W, SLIDE_H, DotGrid, Pill, SwipePill, SlideFrame,
  DISPLAY_XL, DISPLAY_LG, DISPLAY_MD, EYEBROW, CAPTION,
});
