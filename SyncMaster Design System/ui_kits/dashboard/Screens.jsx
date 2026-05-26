'use strict';

const SCREEN_DATA = {
  briefs: [
    { id:'b1', title:'Lagos crime thriller — main title cue', producer:'Aisha Olatunde', company:'Black River Pictures', genres:['Afrobeats','Cinematic','Tense'], budget:'$15,000 – $25,000', deadline:'Jun 14, 2026', status:'active' },
    { id:'b2', title:'Streaming docuseries — Lagos club scene', producer:'Marcus Chen', company:'Sunday Studio', genres:['Amapiano','Documentary','Modern'], budget:'$8,000 – $14,000', deadline:'Jun 22, 2026', status:'active' },
    { id:'b3', title:'Mobile RPG — boss battle theme', producer:'Yuki Tanaka', company:'Anthem Games', genres:['Orchestral','Percussive','Hybrid'], budget:'$20,000 – $35,000', deadline:'Jul 03, 2026', status:'active' },
    { id:'b4', title:'Telco brand spot — 60 second hero', producer:'Sophie Laurent', company:'Forge Creative', genres:['Highlife','Uplifting','Modern'], budget:'$30,000 – $50,000', deadline:'Jun 30, 2026', status:'matched' },
    { id:'b5', title:'Indie feature — closing credits', producer:'Tope Adebayo', company:'Sahara Films', genres:['Soukous','Acoustic','Warm'], budget:'$5,000 – $9,000', deadline:'Jul 18, 2026', status:'active' },
  ],
  tools: [
    { label:'AI Tagger', description:'Auto-tag tracks with smart AI engine', icon:'sparkles', color:'#6366f1', bg:'rgba(99,102,241,.1)' },
    { label:'Sound Radar', description:'Discover trending sync sounds', icon:'search', color:'#d946ef', bg:'rgba(217,70,239,.1)' },
    { label:'Agency Directory', description:'Connect with music supervisors', icon:'building-2', color:'#10b981', bg:'rgba(16,185,129,.1)' },
    { label:'Radio Directory', description:'Connect with college radio stations', icon:'radio', color:'#8b5cf6', bg:'rgba(139,92,246,.1)' },
    { label:'Submissions', description:'Manage track submissions', icon:'file-text', color:'#f97316', bg:'rgba(249,115,22,.1)' },
    { label:'Composers', description:'Manage composer applications', icon:'users', color:'#06b6d4', bg:'rgba(6,182,212,.1)' },
  ],
  tracks: [
    { id:'t1', title:'Lagos at Midnight', artist:'Aisha Olatunde', genre:'Afrobeats', duration:'3:24', bpm:118, key:'F#m', score:92 },
    { id:'t2', title:'Brass Sundown', artist:'Tope Adebayo', genre:'Highlife', duration:'2:48', bpm:96, key:'C', score:88 },
    { id:'t3', title:'Township Pulse', artist:'Nomzamo Khoza', genre:'Amapiano', duration:'4:02', bpm:112, key:'Am', score:76 },
    { id:'t4', title:'Ndani', artist:'Kwame Mensah', genre:'Soukous', duration:'3:11', bpm:128, key:'D', score:67 },
    { id:'t5', title:'Sahara Tape', artist:'Burna Idris', genre:'Afrofusion', duration:'5:24', bpm:88, key:'Gm', score:54 },
  ],
};

// ─────────────────────────────────────────────
// DASHBOARD HOME — the / route
// ─────────────────────────────────────────────
function DashboardHome() {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 40, paddingTop: 8, paddingBottom: 48, maxWidth: 1280, marginInline: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
        <h1 style={{ margin: 0, fontSize: 48, lineHeight: 1.1 }}>Welcome, Godliverse</h1>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '6px 14px 6px 6px',
          background: 'rgba(255,255,255,.04)',
          border: '1px solid var(--border)',
          borderRadius: 9999,
        }}>
          <div style={{ width: 32, height: 32, borderRadius: 8, background: 'oklch(0.88 0.18 120)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#000', fontWeight: 900, letterSpacing: '-0.04em'}}>A</div>
          <div className="label-strong" style={{ letterSpacing: '0.15em' }}>ADMIN</div>
        </div>
      </div>

      {/* Hero banner */}
      <section style={{
        position: 'relative', overflow: 'hidden',
        borderRadius: 40, background: '#4b4bc0',
        padding: '56px 64px',
        color: '#fff', border: '1px solid rgba(255,255,255,.1)',
        boxShadow: '0 25px 50px -12px rgba(0,0,0,.5)',
      }}>
        <div style={{ position:'absolute', top:-80, right:-80, width:384, height:384, borderRadius:'50%', background:'rgba(255,255,255,.1)', filter:'blur(120px)'}}></div>
        <div style={{ position:'absolute', bottom:-80, left:-80, width:384, height:384, borderRadius:'50%', background:'rgba(0,0,0,.3)', filter:'blur(120px)'}}></div>
        <div style={{ position: 'relative', display:'flex', alignItems:'center', justifyContent:'space-between', gap: 48 }}>
          <div style={{ display:'flex', flexDirection:'column', gap: 32, maxWidth: 640 }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <h2 style={{ margin: 0, fontSize: 60, color: '#fff', letterSpacing: '-0.068em', lineHeight: 1.1 }}>Your sync operations, simplified.</h2>
              <p style={{ margin: 0, fontSize: 20, color: 'rgba(255,255,255,.8)', fontWeight: 500, letterSpacing: '-0.04em', lineHeight: 1.4, maxWidth: 520 }}>
                Manage your music assets, track submissions, and connect with supervisors from one central hub.
              </p>
            </div>
            <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
              <button style={{
                all: 'unset', cursor: 'pointer', height: 64, padding: '0 40px',
                borderRadius: 16, background: '#fff', color: '#4b4bc0',
                fontWeight: 900, fontSize: 18, letterSpacing: '-0.04em',
                boxShadow: '0 12px 32px rgba(0,0,0,.2)',
              }}>Explore Briefs</button>
              <button style={{
                all: 'unset', cursor: 'pointer', height: 64, padding: '0 40px',
                borderRadius: 16, background: 'rgba(255,255,255,.05)',
                color: '#fff', fontWeight: 900, fontSize: 18, letterSpacing: '-0.04em',
                border: '1px solid rgba(255,255,255,.2)', backdropFilter: 'blur(8px)',
              }}>View Catalog</button>
            </div>
          </div>
          <div style={{ flexShrink: 0, position: 'relative' }}>
            <div style={{
              width: 420, height: 260, borderRadius: 40, overflow: 'hidden',
              border: '1px solid rgba(255,255,255,.2)',
              background: 'rgba(255,255,255,.05)', backdropFilter: 'blur(12px)',
              boxShadow: '0 25px 50px -12px rgba(0,0,0,.5)',
              transform: 'rotate(3deg)',
            }}>
              <img src="../../assets/screens/dashboard-preview.png" style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: .9 }} />
            </div>
          </div>
        </div>
      </section>

      {/* Top Briefs */}
      <section style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h2 style={{ margin: 0, fontSize: 32 }}>Top Briefs</h2>
            <p style={{ margin: '6px 0 0', fontSize: 13, color: 'var(--muted-foreground)', letterSpacing: '-0.02em' }}>Latest opportunities from producers</p>
          </div>
          <a style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 13, fontWeight: 700, color: '#4b4bc0', cursor: 'pointer' }}>
            View all <i data-lucide="arrow-right" style={{width:14,height:14}}></i>
          </a>
        </div>
        <div style={{ display: 'flex', gap: 20, overflowX: 'auto', paddingBottom: 12, scrollbarWidth: 'none' }} className="scrollbar-hide">
          {SCREEN_DATA.briefs.map(b => <BriefCard key={b.id} brief={b} />)}
        </div>
      </section>

      {/* Tools */}
      <section style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
        <div style={{ paddingBottom: 24, borderBottom: '1px solid rgba(255,255,255,.05)' }}>
          <h2 style={{ margin: 0, fontSize: 32 }}>Tools</h2>
          <p style={{ margin: '6px 0 0', fontSize: 13, color: 'var(--muted-foreground)', letterSpacing: '-0.02em' }}>Centralized utilities for your operations</p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: 24 }}>
          {SCREEN_DATA.tools.map(t => <ToolTile key={t.label} tool={t} />)}
        </div>
      </section>
    </div>
  );
}

// ─────────────────────────────────────────────
// BRIEFS LIST — the dense list pattern (BriefList.tsx)
// ─────────────────────────────────────────────
function BriefsList() {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24, maxWidth: 1100, marginInline: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 16 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 36 }}>Briefs</h1>
          <p style={{ margin: '8px 0 0', fontSize: 18, color: 'var(--muted-foreground)', letterSpacing: '-0.02em' }}>Review producer briefs and manage status transitions.</p>
        </div>
        <button style={{
          all:'unset', cursor: 'pointer',
          height: 32, padding: '0 16px', borderRadius: 9999,
          background: '#fff', color: '#000', fontWeight: 500, fontSize: 14,
          display: 'inline-flex', alignItems: 'center', gap: 6,
        }}><i data-lucide="plus" style={{width:14,height:14}}></i> New brief</button>
      </div>

      <Banner variant="default">
        <span className="label-strong">REVIEW QUEUE</span> &nbsp; 2 briefs awaiting review — open to activate
      </Banner>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {SCREEN_DATA.briefs.map(brief => (
          <a key={brief.id} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
            padding: 24, borderRadius: 6, background: 'var(--card)',
            border: '1px solid var(--border)', boxShadow: '0 1px 3px rgba(0,0,0,.1)',
            cursor: 'pointer', textDecoration: 'none', color: 'inherit',
            transition: 'all 200ms ease',
          }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6, minWidth: 0 }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 8 }}>
                <StatusBadge status={brief.status} />
                <span className="label">DUE {brief.deadline.toUpperCase()}</span>
              </div>
              <p style={{ margin: '4px 0 2px', fontSize: 14, fontWeight: 600, lineHeight: 1.25 }}>{brief.title}</p>
              <p className="label">{brief.producer.toUpperCase()} · {brief.company.toUpperCase()}</p>
              <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginTop: 4 }}>
                {brief.genres.map(g => (
                  <span key={g} style={{
                    padding: '2px 8px', borderRadius: 4,
                    background: 'rgba(255,255,255,.03)', border: '1px solid var(--border)',
                    color: 'var(--muted-foreground)', fontSize: 11
                  }}>{g}</span>
                ))}
              </div>
              <p style={{ margin: '8px 0 0', fontSize: 12, color: 'var(--muted-foreground)' }}>
                <span className="label" style={{marginRight:6}}>BUDGET</span>
                <span className="mono" style={{color:'var(--foreground)'}}>{brief.budget}</span>
              </p>
            </div>
            <button style={{
              all:'unset', cursor:'pointer', flexShrink: 0,
              height: 28, padding: '0 14px', borderRadius: 9999,
              border: '1px solid var(--input)', color: 'var(--foreground)',
              fontSize: 13, fontWeight: 500,
            }}>View</button>
          </a>
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// BRIEF DETAIL — the editorial full-width view (BriefDetailCard.tsx)
// ─────────────────────────────────────────────
function BriefDetail() {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  const brief = SCREEN_DATA.briefs[0];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 32, maxWidth: 1280, marginInline: 'auto' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
          <StatusBadge status={brief.status} />
          <span style={{
            fontFamily: 'var(--font-mono)', fontSize: 10, fontWeight: 900,
            color: 'var(--muted-foreground)', letterSpacing: '0.2em',
            padding: '4px 12px', borderRadius: 9999,
            background: 'rgba(255,255,255,.03)', border: '1px solid var(--border)',
          }}>DEADLINE: {brief.deadline.toUpperCase()}</span>
        </div>
        <h1 className="display" style={{
          margin: 0, fontSize: 92, fontStyle: 'italic',
          textTransform: 'uppercase', letterSpacing: '-0.04em', lineHeight: 0.9,
        }}>{brief.title}</h1>
        <p style={{ margin: '14px 0 0', fontSize: 18, color: 'var(--muted-foreground)', fontWeight: 500, letterSpacing: '-0.02em' }}>
          FOR <span style={{ color: 'var(--foreground)', fontWeight: 900 }}>{brief.company.toUpperCase()}</span>
          <span style={{ opacity: .4 }}> — CURATED BY {brief.producer.toUpperCase()}</span>
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>
        <div style={{
          padding: 40, borderRadius: 6,
          background: 'rgba(22,22,42,.3)', backdropFilter: 'blur(12px)',
          border: '1px solid var(--border)',
          display: 'flex', flexDirection: 'column', gap: 24,
        }}>
          <p className="label" style={{ color: '#4b4bc0', letterSpacing: '0.3em' }}>PROJECT BRIEF / SCOPE</p>
          <p style={{ margin: 0, fontSize: 18, lineHeight: 1.6, fontWeight: 500, color: 'rgba(249,249,249,.9)' }}>
            A taut Lagos-set crime thriller about a money-laundering ring that pulls in a homicide detective with her own debts. We need a main-title cue that telegraphs the city's neon hum and the tightening dread of the case. Modern Afrobeats foundation, low menace, no resolution. Roughly 90 seconds.
          </p>
          <div style={{ paddingTop: 24, borderTop: '1px solid var(--border)', display: 'flex', flexDirection: 'column', gap: 8 }}>
            <p className="label">TIMELINE</p>
            <p style={{ margin: 0, fontSize: 13, opacity: .6 }}>Project initiated on May 21, 2026 · Outreach opened to 4 composers</p>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div style={{
            padding: 28, borderRadius: 6,
            background: 'var(--background)', borderLeft: '4px solid oklch(0.88 0.18 120)',
            border: '1px solid var(--border)',
            display: 'flex', flexDirection: 'column', gap: 12,
          }}>
            <p className="label">ESTIMATED BUDGET</p>
            <p className="display mono" style={{ margin: 0, fontSize: 32, letterSpacing: '-0.04em' }}>{brief.budget}</p>
          </div>

          <div style={{
            padding: 28, borderRadius: 6,
            background: 'rgba(22,22,42,.5)', backdropFilter: 'blur(12px)',
            border: '1px solid var(--border)',
            display: 'flex', flexDirection: 'column', gap: 20,
          }}>
            <p className="label">SONIC DIRECTION</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {brief.genres.map(g => (
                <span key={g} style={{
                  padding: '6px 16px',
                  border: '2px solid rgba(75,75,192,.2)', background: 'transparent',
                  fontFamily: 'var(--font-mono)', fontSize: 10, fontWeight: 900,
                  textTransform: 'uppercase', letterSpacing: '0.2em',
                }}>{g}</span>
              ))}
            </div>
          </div>

          <div style={{
            padding: 28, borderRadius: 6,
            background: 'rgba(22,22,42,.5)', backdropFilter: 'blur(12px)',
            border: '1px solid var(--border)',
            display: 'flex', flexDirection: 'column', gap: 16,
          }}>
            <p className="label">SUGGESTED COMPOSERS · AI MATCH</p>
            {SCREEN_DATA.tracks.slice(0,4).map(t => (
              <div key={t.id} style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                <div style={{ fontSize: 12, color: 'var(--muted-foreground)', minWidth: 110, overflow: 'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{t.artist}</div>
                <div style={{ flex: 1 }}><ScoreBar score={t.score} /></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// CATALOG / TRACKS — the list of tracks page
// ─────────────────────────────────────────────
function CatalogPage({ onPlay }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24, maxWidth: 1280, marginInline: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 16 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 36 }}>Catalog</h1>
          <p style={{ margin: '8px 0 0', fontSize: 18, color: 'var(--muted-foreground)', letterSpacing: '-0.02em' }}>Your library of tracks — ready to pitch.</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button style={{
            all:'unset', cursor:'pointer', height: 32, padding: '0 14px', borderRadius: 9999,
            border: '1px solid var(--input)', color: 'var(--foreground)', fontSize: 13, fontWeight: 500,
            display:'inline-flex', alignItems:'center', gap:6,
          }}><i data-lucide="filter" style={{width:14,height:14}}></i> Filter</button>
          <button style={{
            all:'unset', cursor:'pointer', height: 32, padding: '0 16px', borderRadius: 9999,
            background: '#fff', color: '#000', fontWeight: 500, fontSize: 14,
            display:'inline-flex', alignItems:'center', gap:6,
          }}><i data-lucide="upload" style={{width:14,height:14}}></i> Upload</button>
        </div>
      </div>

      {/* Search */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '0 14px', height: 40, borderRadius: 8, border: '1px solid var(--input)', background: 'transparent' }}>
        <i data-lucide="search" style={{ width: 16, height: 16, color: 'var(--muted-foreground)'}}></i>
        <input placeholder="Search tracks by title, BPM, key…" style={{ all: 'unset', flex: 1, color: 'var(--foreground)', fontFamily: 'var(--font-sans)', fontSize: 14 }} />
        <span className="label" style={{padding:'2px 6px', border:'1px solid var(--border)', borderRadius: 4}}>⌘K</span>
      </div>

      {/* Tracks table */}
      <div style={{ border: '1px solid var(--border)', borderRadius: 12, overflow: 'hidden', background: 'var(--card)' }}>
        <div style={{
          display: 'grid', gridTemplateColumns: '40px 1fr 140px 100px 90px 70px 140px 60px',
          padding: '14px 18px',
          background: 'rgba(255,255,255,.02)',
          borderBottom: '1px solid var(--border)',
          fontSize: 10, fontFamily: 'var(--font-mono)', fontWeight: 600,
          color: 'var(--muted-foreground)', letterSpacing: '0.2em', textTransform: 'uppercase',
        }}>
          <div></div>
          <div>TITLE</div>
          <div>ARTIST</div>
          <div>GENRE</div>
          <div>BPM</div>
          <div>KEY</div>
          <div>AI MATCH</div>
          <div>TIME</div>
        </div>
        {SCREEN_DATA.tracks.map((t, i) => (
          <div key={t.id} style={{
            display: 'grid', gridTemplateColumns: '40px 1fr 140px 100px 90px 70px 140px 60px',
            padding: '14px 18px', alignItems: 'center',
            borderBottom: i < SCREEN_DATA.tracks.length-1 ? '1px solid var(--border)' : 'none',
            fontSize: 13,
          }}>
            <button onClick={() => onPlay && onPlay(t)} style={{
              all:'unset', cursor:'pointer', width:28, height:28, borderRadius: '50%',
              background:'rgba(75,75,192,.1)', color:'#4b4bc0',
              display:'flex', alignItems:'center', justifyContent:'center',
            }}><i data-lucide="play" style={{width:11, height:11, fill:'#4b4bc0'}}></i></button>
            <div style={{ fontWeight: 700, letterSpacing: '-0.02em' }}>{t.title}</div>
            <div style={{ color: 'var(--muted-foreground)' }}>{t.artist}</div>
            <div style={{ color: '#4b4bc0', fontSize:11, fontWeight:700 }}>{t.genre}</div>
            <div className="mono" style={{ color: 'var(--muted-foreground)', fontSize:12 }}>{t.bpm}</div>
            <div className="mono" style={{ color: 'var(--muted-foreground)', fontSize:12 }}>{t.key}</div>
            <div><ScoreBar score={t.score} /></div>
            <div className="mono" style={{ color: 'var(--muted-foreground)', fontSize: 12, textAlign: 'right' }}>{t.duration}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { SCREEN_DATA, DashboardHome, BriefsList, BriefDetail, CatalogPage });
