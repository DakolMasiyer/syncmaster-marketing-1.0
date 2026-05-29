'use strict';

// Top header — sticky, breadcrumb on left, avatar on right
function Header({ crumb }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 30,
      height: 56, flexShrink: 0,
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 24px',
      background: 'rgba(15,15,26,.8)', backdropFilter: 'blur(12px)',
    }}>
      <h1 style={{ margin: 0, fontSize: 13, fontWeight: 900, letterSpacing: '-0.068em' }}>{crumb}</h1>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{
          width: 32, height: 32, borderRadius: '50%',
          background: 'rgba(255,255,255,.06)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 11, fontWeight: 700, color: 'var(--foreground)',
          border: '1px solid var(--border)'
        }}>GO</div>
      </div>
    </header>
  );
}

// Status badge — driven by BriefStatus
function StatusBadge({ status }) {
  const styles = {
    active: { bg: 'oklch(0.88 0.18 120)', fg: '#000', glow: '0 0 20px rgba(217,249,157,.3)' },
    draft:  { bg: 'var(--muted)', fg: 'var(--muted-foreground)', glow: 'none' },
    matched:{ bg: 'var(--accent)', fg: 'var(--accent-foreground)', glow: 'none' },
    closed: { bg: 'var(--card)', fg: 'var(--muted-foreground)', glow: 'none' },
  };
  const labels = { active: 'ACTIVE — CURATING', draft: 'DRAFT', matched: 'MATCHED', closed: 'CLOSED' };
  const s = styles[status] || styles.draft;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center',
      padding: '4px 12px', borderRadius: 9999,
      background: s.bg, color: s.fg,
      fontFamily: 'var(--font-mono)',
      fontSize: 10, fontWeight: 900,
      letterSpacing: '0.2em',
      boxShadow: s.glow,
      border: status === 'matched' || status === 'closed' || status === 'draft' ? '1px solid var(--border)' : 'none',
    }}>{labels[status]}</span>
  );
}

// Brief card — Top-Briefs carousel item
function BriefCard({ brief }) {
  const [hover, setHover] = React.useState(false);
  return (
    <a onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
       style={{
         display: 'flex', flexDirection: 'column', gap: 14,
         padding: 24, borderRadius: 24,
         background: 'var(--card)',
         border: `1px solid ${hover ? 'rgba(75,75,192,.4)' : 'var(--border)'}`,
         minWidth: 340, maxWidth: 340,
         boxShadow: hover ? '0 25px 50px -12px rgba(0,0,0,.5)' : '0 1px 3px rgba(0,0,0,.1)',
         transform: hover ? 'translateY(-6px)' : 'none',
         transition: 'all 300ms cubic-bezier(.4,0,.2,1)',
         cursor: 'pointer', textDecoration: 'none', color: 'inherit', flexShrink: 0,
       }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <StatusBadge status={brief.status} />
        {brief.deadline && (
          <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--muted-foreground)',
                         background: 'rgba(255,255,255,.04)', padding: '2px 8px',
                         borderRadius: 6, border: '1px solid var(--border)' }}>
            {brief.deadline}
          </span>
        )}
      </div>
      <h3 style={{ margin: 0, fontSize: 18, lineHeight: 1.25 }}>{brief.title}</h3>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{
          width: 24, height: 24, borderRadius: '50%',
          background: 'linear-gradient(135deg, rgba(75,75,192,.2), rgba(168,85,247,.2))',
          border: '1px solid rgba(75,75,192,.1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 11, fontWeight: 700,
        }}>{brief.producer.charAt(0)}</div>
        <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--muted-foreground)' }}>
          {brief.producer} <span style={{fontWeight:400, opacity:.6}}>at</span> {brief.company}
        </span>
      </div>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {brief.genres.map(g => (
          <span key={g} style={{
            padding: '4px 10px', borderRadius: 6,
            background: 'rgba(255,255,255,.04)', border: '1px solid var(--border)',
            color: '#4b4bc0', fontSize: 11, fontWeight: 700
          }}>{g}</span>
        ))}
      </div>
      <div style={{
        marginTop: 8, paddingTop: 18, borderTop: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div>
          <div className="label">BUDGET RANGE</div>
          <div style={{ fontSize: 14, fontWeight: 900, letterSpacing: '-0.04em', marginTop: 2 }}>{brief.budget}</div>
        </div>
        <div style={{
          width: 36, height: 36, borderRadius: '50%',
          background: hover ? '#4b4bc0' : 'rgba(75,75,192,.1)',
          color: hover ? '#fff' : '#4b4bc0',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          transition: 'all 300ms ease',
        }}>→</div>
      </div>
    </a>
  );
}

// Tool tile — homepage utility entrypoints
function ToolTile({ tool }) {
  const [hover, setHover] = React.useState(false);
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <a onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
       style={{
         display: 'flex', alignItems: 'center', gap: 24,
         padding: 24, borderRadius: 32,
         background: 'var(--card)', border: `1px solid ${hover ? 'rgba(75,75,192,.4)' : 'var(--border)'}`,
         transition: 'all 300ms cubic-bezier(.4,0,.2,1)',
         boxShadow: hover ? '0 25px 50px -12px rgba(0,0,0,.5)' : 'none',
         transform: hover ? 'translateY(-6px)' : 'none',
         cursor: 'pointer', textDecoration: 'none', color: 'inherit',
       }}>
      <div style={{
        width: 64, height: 64, flexShrink: 0, borderRadius: 16,
        background: hover ? '#4b4bc0' : tool.bg, color: hover ? '#fff' : tool.color,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        transition: 'all 300ms ease',
        transform: hover ? 'scale(1.1)' : 'none',
      }}>
        <i data-lucide={tool.icon} style={{ width: 28, height: 28 }}></i>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4, flex: 1 }}>
        <h3 style={{ margin: 0, fontSize: 18, lineHeight: 1.2 }}>{tool.label}</h3>
        <p style={{ margin: 0, fontSize: 13, fontWeight: 500, color: 'var(--muted-foreground)', letterSpacing: '-0.02em', opacity: .8, lineHeight: 1.35 }}>
          {tool.description}
        </p>
      </div>
      <i data-lucide="arrow-right" style={{
        width: 22, height: 22, color: hover ? '#4b4bc0' : 'var(--muted-foreground)',
        opacity: hover ? 1 : 0, transform: hover ? 'translateX(0)' : 'translateX(-12px)',
        transition: 'all 300ms ease',
      }}></i>
    </a>
  );
}

// Waveform — used in the music-player dock
function Waveform({ progress = 30 }) {
  const bars = React.useMemo(() =>
    Array.from({length: 80}, (_, i) => 0.2 + Math.abs(Math.sin(i * 0.42 + Math.sin(i*0.13)*1.2)) * 0.8),
  []);
  const threshold = Math.floor(bars.length * progress / 100);
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 2, height: 32, flex: 1 }}>
      {bars.map((v, i) => (
        <div key={i} style={{
          width: 2, height: `${v*100}%`,
          background: i < threshold ? '#4b4bc0' : 'rgba(255,255,255,.35)',
        }}></div>
      ))}
    </div>
  );
}

// Music-player dock — appears at bottom of every dashboard page
function MusicPlayer({ track }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  if (!track) return null;
  return (
    <div style={{
      position: 'fixed', left: 256, right: 0, bottom: 0,
      height: 72, zIndex: 50,
      background: 'rgba(22,22,42,.95)',
      backdropFilter: 'blur(20px)',
      borderTop: '1px solid var(--border)',
      display: 'grid', gridTemplateColumns: '300px 1fr 200px', gap: 24,
      alignItems: 'center', padding: '0 24px',
      boxShadow: '0 -8px 24px rgba(0,0,0,.4)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
        <div style={{
          width: 44, height: 44, borderRadius: 8, flexShrink: 0,
          background: 'linear-gradient(135deg, #4b4bc0, #a855f7)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <i data-lucide="music-2" style={{width:18, height:18, color:'#fff'}}></i>
        </div>
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: 13, fontWeight: 900, letterSpacing: '-0.04em', overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{track.title}</div>
          <div style={{ fontSize: 11, color: 'var(--muted-foreground)', overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{track.artist} · {track.genre}</div>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
        <button style={{ all:'unset', cursor:'pointer', color: 'var(--muted-foreground)' }}>
          <i data-lucide="skip-back" style={{width:18, height:18}}></i>
        </button>
        <button style={{
          all:'unset', cursor:'pointer', width:36, height:36, borderRadius:'50%',
          background: '#fff', color: '#000',
          display:'flex', alignItems:'center', justifyContent:'center'
        }}>
          <i data-lucide="pause" style={{width:14, height:14, fill: '#000'}}></i>
        </button>
        <button style={{ all:'unset', cursor:'pointer', color: 'var(--muted-foreground)' }}>
          <i data-lucide="skip-forward" style={{width:18, height:18}}></i>
        </button>
        <Waveform progress={28} />
        <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--muted-foreground)' }}>1:02 / 3:24</div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 8 }}>
        <i data-lucide="heart" style={{width:18, height:18, color: 'var(--muted-foreground)'}}></i>
        <i data-lucide="list-plus" style={{width:18, height:18, color: 'var(--muted-foreground)'}}></i>
        <i data-lucide="volume-2" style={{width:18, height:18, color: 'var(--muted-foreground)'}}></i>
      </div>
    </div>
  );
}

// Score-bar — AI match fit
function ScoreBar({ score }) {
  const color = score >= 85 ? '#4b4bc0' : score >= 70 ? 'rgba(255,255,255,.6)' : 'rgba(255,255,255,.25)';
  const textColor = score >= 85 ? '#4b4bc0' : 'var(--muted-foreground)';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      <div style={{ flex: 1, height: 6, background: 'rgba(255,255,255,.06)', borderRadius: 9999, overflow: 'hidden' }}>
        <div style={{
          height: '100%', width: `${score}%`, background: color,
          boxShadow: score >= 85 ? '0 0 8px #4b4bc0' : 'none',
          transition: 'width 1000ms ease',
        }}></div>
      </div>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, fontWeight: 700, color: textColor, minWidth: 36, textAlign: 'right' }}>{score}%</span>
    </div>
  );
}

// Banner — left-border accent context msg
function Banner({ variant = 'default', children }) {
  const variants = {
    default: { bg: 'rgba(255,255,255,.03)', accent: '#4b4bc0', fg: 'var(--foreground)' },
    success: { bg: 'rgba(34,197,94,.08)', accent: '#22c55e', fg: '#22c55e' },
    warning: { bg: 'rgba(245,158,11,.08)', accent: '#f59e0b', fg: '#f59e0b' },
    error:   { bg: 'rgba(239,68,68,.08)', accent: '#ef4444', fg: '#ef4444' },
  };
  const v = variants[variant];
  return (
    <div style={{
      padding: '14px 18px', borderRadius: 12,
      background: v.bg, border: '1px solid var(--border)', borderLeft: `4px solid ${v.accent}`,
      color: v.fg, fontSize: 13, fontWeight: 500,
    }}>{children}</div>
  );
}

Object.assign(window, { Header, StatusBadge, BriefCard, ToolTile, Waveform, MusicPlayer, ScoreBar, Banner });
