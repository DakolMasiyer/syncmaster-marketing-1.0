'use strict';

// Marketing nav — sticky, blurred backdrop, light-mode
function MarketingNav({ active = 'home', onNavigate }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  const link = (id, label) => (
    <a onClick={() => onNavigate && onNavigate(id)}
       style={{
         fontSize: 13, fontWeight: 700,
         color: active === id ? 'var(--foreground)' : 'var(--muted-foreground)',
         cursor: 'pointer',
         textDecoration: 'none',
       }}>{label}</a>
  );
  return (
    <nav style={{
      position: 'sticky', top: 0, zIndex: 50,
      borderBottom: '1px solid rgba(229,229,229,.5)',
      background: 'rgba(255,255,255,.8)',
      backdropFilter: 'blur(20px)',
      height: 80,
    }}>
      <div style={{
        maxWidth: 1440, margin: '0 auto', padding: '0 24px',
        height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <a onClick={() => onNavigate && onNavigate('home')} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
          <img src="../../assets/logos/syncmaster-wordmark.png" style={{ width: 160, height: 40, objectFit: 'contain' }} />
        </a>
        <div style={{ display: 'flex', alignItems: 'center', gap: 40 }}>
          {link('features', 'Features')}
          {link('solutions', 'Solutions')}
          {link('composers', 'For Composers')}
          {link('supervisors', 'For Supervisors')}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <a style={{ fontSize: 13, fontWeight: 700, cursor: 'pointer', color: '#111' }}>Login</a>
          <a style={{
            display: 'inline-flex', alignItems: 'center',
            height: 36, padding: '0 24px', borderRadius: 9999,
            background: '#fff', color: '#000', border: '1px solid rgba(0,0,0,.1)',
            fontWeight: 700, fontSize: 13, cursor: 'pointer',
            boxShadow: '0 1px 2px rgba(0,0,0,.05)',
          }}>Get early access</a>
        </div>
      </div>
    </nav>
  );
}

// Editorial CTA button — used at every section break
function CTAButton({ children, variant = 'primary', icon = 'arrow-right' }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  const primary = {
    background: '#4b4bc0', color: '#fff',
    boxShadow: '0 20px 40px -8px rgba(75,75,192,.4)',
    border: 'none',
  };
  const outline = {
    background: 'transparent', color: '#111',
    border: '1px solid #e5e5e5',
  };
  return (
    <a style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      height: 64, padding: '0 40px', borderRadius: 16,
      fontWeight: 900, fontSize: 18, letterSpacing: '-0.04em',
      cursor: 'pointer', textDecoration: 'none',
      ...(variant === 'primary' ? primary : outline),
    }}>
      {children}
      {icon && <i data-lucide={icon} style={{ width: 18, height: 18 }}></i>}
    </a>
  );
}

// Capsule tag — small pill above section headings
function Capsule({ icon, color = '#4b4bc0', children }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  const bg = color === '#4b4bc0' ? 'rgba(75,75,192,.1)' :
             color === '#10b981' ? 'rgba(16,185,129,.1)' :
             color === '#ef4444' ? 'rgba(239,68,68,.1)' : 'rgba(0,0,0,.05)';
  const border = color === '#4b4bc0' ? 'rgba(75,75,192,.2)' :
                 color === '#10b981' ? 'rgba(16,185,129,.2)' :
                 color === '#ef4444' ? 'rgba(239,68,68,.2)' : 'rgba(0,0,0,.1)';
  return (
    <div style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      padding: '6px 16px', borderRadius: 9999,
      background: bg, border: `1px solid ${border}`, color,
      fontSize: 11, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase',
      width: 'fit-content',
    }}>
      {icon && <i data-lucide={icon} style={{ width: 14, height: 14 }}></i>}
      {children}
    </div>
  );
}

// Feature card — used in the "Built for sync" grid
function FeatureCard({ icon, color, bg, title, description }) {
  const [hover, setHover] = React.useState(false);
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <div onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
         style={{
           display: 'flex', flexDirection: 'column', gap: 24,
           padding: 32, borderRadius: 40,
           background: '#fff',
           border: `1px solid ${hover ? color + '80' : '#e5e5e5'}`,
           transition: 'border-color 300ms ease',
         }}>
      <div style={{
        width: 56, height: 56, borderRadius: 16, background: bg,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        transform: hover ? 'scale(1.1)' : 'none', transition: 'transform 300ms ease',
      }}>
        <i data-lucide={icon} style={{ width: 28, height: 28, color }}></i>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <h3 style={{ margin: 0, color: '#111', fontSize: 24 }}>{title}</h3>
        <p style={{ margin: 0, color: '#666', fontSize: 15, lineHeight: 1.6, fontWeight: 500 }}>{description}</p>
      </div>
    </div>
  );
}

// Role split — Composers / Supervisors callout cards
function RoleCard({ icon, color, bg, title, description, cta = 'Learn more', onClick }) {
  const [hover, setHover] = React.useState(false);
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <a onClick={onClick}
       onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
       style={{
         display: 'flex', flexDirection: 'column', gap: 24,
         padding: 40, borderRadius: 40,
         background: '#fff',
         border: `1px solid ${hover ? color + '80' : '#e5e5e5'}`,
         boxShadow: hover ? '0 25px 50px -12px rgba(0,0,0,.1)' : 'none',
         transition: 'all 300ms ease',
         cursor: 'pointer', textDecoration: 'none', color: 'inherit',
       }}>
      <div style={{
        width: 64, height: 64, borderRadius: 16, background: bg,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        transform: hover ? 'scale(1.1)' : 'none', transition: 'transform 300ms ease',
      }}>
        <i data-lucide={icon} style={{ width: 32, height: 32, color }}></i>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <h3 style={{ margin: 0, color: '#111', fontSize: 24 }}>{title}</h3>
        <p style={{ margin: 0, color: '#666', fontSize: 16, lineHeight: 1.6, fontWeight: 500 }}>{description}</p>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, color, fontWeight: 700, fontSize: 13, marginTop: 'auto', paddingTop: 8 }}>
        {cta}
        <i data-lucide="arrow-right" style={{ width: 14, height: 14, transform: hover ? 'translateX(4px)' : 'none', transition: 'transform 200ms ease' }}></i>
      </div>
    </a>
  );
}

// Platform strip — Netflix / Hulu / Disney etc grayscale row
function PlatformStrip() {
  const logos = [
    ['Netflix.png',     32],
    ['Hulu.webp',       24],
    ['PrimeVideo.png',  28],
    ['Disney.png',      40],
    ['HBO.svg',         24],
    ['Paramount.svg',   28],
    ['EA.png',          32],
    ['NBA2K.png',       32],
  ];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 32 }}>
      <p style={{
        margin: 0, fontSize: 13, fontWeight: 700,
        color: '#666', letterSpacing: '0.18em', textTransform: 'uppercase'
      }}>Discover opportunities across</p>
      <div style={{
        display: 'flex', gap: 48, alignItems: 'center', flexWrap: 'wrap',
        justifyContent: 'center', filter: 'grayscale(1)', opacity: 0.6,
      }}>
        {logos.map(([src, h]) => (
          <img key={src} src={`../../assets/platforms/${src}`} style={{ height: h, width: 'auto' }} />
        ))}
      </div>
    </div>
  );
}

// Step card — used in "How it works" composer flow
function StepCard({ number, title, description }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', gap: 14,
      padding: 32, borderRadius: 32, background: '#fff', border: '1px solid #e5e5e5',
    }}>
      <span style={{
        fontSize: 48, fontWeight: 900, color: 'rgba(75,75,192,.2)',
        lineHeight: 1, letterSpacing: '-0.068em',
      }}>{number}</span>
      <h3 style={{ margin: 0, color: '#111', fontSize: 20 }}>{title}</h3>
      <p style={{ margin: 0, color: '#666', fontSize: 14, lineHeight: 1.6, fontWeight: 500 }}>{description}</p>
    </div>
  );
}

// Footer
function Footer() {
  return (
    <footer style={{
      borderTop: '1px solid #e5e5e5',
      padding: '80px 0', background: '#fff',
    }}>
      <div style={{
        maxWidth: 1440, margin: '0 auto', padding: '0 24px',
        display: 'flex', flexDirection: 'row', flexWrap: 'wrap',
        justifyContent: 'space-between', alignItems: 'center', gap: 40,
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <img src="../../assets/logos/syncmaster-wordmark.png" style={{ width: 128, height: 32, objectFit: 'contain' }} />
          <p style={{ margin: 0, fontSize: 13, color: '#666', fontWeight: 500 }}>© 2026 SyncMaster Operations. All rights reserved.</p>
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 32, fontSize: 13, fontWeight: 700, color: '#666' }}>
          <a style={{cursor:'pointer'}}>For Composers</a>
          <a style={{cursor:'pointer'}}>For Supervisors</a>
          <a style={{cursor:'pointer'}}>Brand Assets</a>
          <a style={{cursor:'pointer'}}>Terms</a>
          <a style={{cursor:'pointer'}}>Privacy</a>
          <a style={{cursor:'pointer'}}>Contact</a>
        </div>
      </div>
    </footer>
  );
}

Object.assign(window, { MarketingNav, CTAButton, Capsule, FeatureCard, RoleCard, PlatformStrip, StepCard, Footer });
