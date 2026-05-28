'use strict';
// SyncMaster Dashboard — Sidebar component
// Mirrors Syncmaster-Live/components/dashboard/Sidebar.tsx — purple rail, white-fill active nav.

const NAV_GROUPS = {
  Workspace: [
    { label: 'Dashboard', icon: 'layout-dashboard' },
    { label: 'Catalog', icon: 'layers' },
    { label: 'Briefs', icon: 'briefcase' },
    { label: 'Placements', icon: 'trending-up' },
  ],
  Distribution: [
    { label: 'Pages (EPK)', icon: 'monitor-play' },
    { label: 'Campaigns', icon: 'mail' },
    { label: 'Radio Directory', icon: 'radio' },
  ],
  Network: [
    { label: 'Composers', icon: 'users' },
    { label: 'Producers', icon: 'headphones' },
  ],
};

function NavLink({ icon, label, active, onClick }) {
  const base = {
    width: '100%', display: 'flex', alignItems: 'center', gap: 12,
    padding: '10px 16px', borderRadius: 12,
    fontSize: 13, fontWeight: 900, letterSpacing: '-0.04em',
    transition: 'all 200ms cubic-bezier(.4,0,.2,1)',
    cursor: 'pointer', textDecoration: 'none',
  };
  const activeStyle = {
    ...base,
    background: '#fff', color: '#4b4bc0',
    boxShadow: '0 8px 24px rgba(0,0,0,.2)',
    transform: 'scale(1.02)',
    borderRight: '4px solid rgba(75,75,192,.2)',
  };
  const idleStyle = {
    ...base,
    color: 'rgba(255,255,255,.7)',
    background: 'transparent',
  };
  const [hover, setHover] = React.useState(false);
  return (
    <a onClick={onClick}
       onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
       style={active ? activeStyle : {
         ...idleStyle,
         color: hover ? '#fff' : 'rgba(255,255,255,.7)',
         background: hover ? 'rgba(255,255,255,.05)' : 'transparent',
         transform: hover ? 'translateX(4px)' : 'none',
       }}>
      <i data-lucide={icon} style={{width: 16, height: 16, flexShrink: 0}}></i>
      {label}
    </a>
  );
}

function NavGroupHeader({ title }) {
  return (
    <div style={{
      padding: '0 16px 8px',
      fontSize: 10,
      fontWeight: 900,
      color: 'rgba(255,255,255,.4)',
      letterSpacing: '0.05em',
      display: 'flex', alignItems: 'center', gap: 8,
    }}>
      <span style={{width: 8, height: 1, background: 'rgba(255,255,255,.2)'}}></span>
      {title}
    </div>
  );
}

function Sidebar({ active, onNavigate }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <aside style={{
      width: 256, minWidth: 256,
      position: 'fixed', top: 0, left: 0, bottom: 0,
      background: '#4b4bc0',
      borderRight: '1px solid rgba(255,255,255,.1)',
      display: 'flex', flexDirection: 'column',
      zIndex: 40,
    }}>
      <div style={{ height: 80, padding: '0 32px', display: 'flex', alignItems: 'center' }}>
        {/* Syncdark.png — designed for dark/purple backgrounds; white text + acid icon */}
        <img src="../../assets/logos/Icon . Mark only.svg" style={{height: 44, width: 'auto', opacity: .95 }} />
      </div>

      <nav style={{ flex: 1, padding: 16, paddingTop: 24, display: 'flex', flexDirection: 'column', gap: 0, overflowY: 'hidden' }}>
        {Object.entries(NAV_GROUPS).map(([group, items]) => (
          <div key={group} style={{ marginBottom: 28 }}>
            <NavGroupHeader title={group} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {items.map(it => (
                <NavLink key={it.label} icon={it.icon} label={it.label}
                         active={active === it.label} onClick={() => onNavigate && onNavigate(it.label)} />
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div style={{ padding: 16 }}>
        <div style={{
          padding: 16, borderRadius: 24,
          background: 'rgba(255,255,255,.05)',
          border: '1px solid rgba(255,255,255,.1)',
          backdropFilter: 'blur(12px)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
            <div style={{
              width: 40, height: 40, borderRadius: 14,
              background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 900, color: '#4b4bc0', letterSpacing: '-0.04em',
            }}>G</div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 900, color: '#fff', letterSpacing: '-0.04em' }}>Godliverse</div>
              <div style={{ fontSize: 10, fontWeight: 700, color: 'rgba(255,255,255,.5)', marginTop: 2 }}>Admin access</div>
            </div>
          </div>
          <button style={{
            all: 'unset', cursor: 'pointer', width: '100%', textAlign: 'center',
            padding: '10px 0', borderRadius: 16,
            color: 'rgba(255,255,255,.6)', fontSize: 12, fontWeight: 900,
            border: '1px solid transparent', boxSizing: 'border-box',
          }}>↳ Sign out</button>
        </div>
      </div>
    </aside>
  );
}

Object.assign(window, { Sidebar });
