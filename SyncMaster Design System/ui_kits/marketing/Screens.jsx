'use strict';

// ─────────────────────────────────────────────
// LANDING — home page
// ─────────────────────────────────────────────
function Landing({ onNavigate }) {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  return (
    <>
      {/* HERO */}
      <section style={{ position: 'relative', paddingTop: 80, paddingBottom: 128, overflow: 'hidden' }}>
        {/* purple glow */}
        <div style={{ position:'absolute', top:0, left:'50%', transform:'translateX(-50%)', width:1200, height:600, background:'rgba(75,75,192,.1)', filter:'blur(120px)', borderRadius:'50%', opacity:.5, pointerEvents:'none'}}></div>

        <div style={{ position: 'relative', maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: 40 }}>
            <Capsule icon="sparkles">African Composers. Global Briefs.</Capsule>
            <h1 style={{ margin: 0, color: '#111', maxWidth: 960, fontSize: 'clamp(48px,6vw,80px)', lineHeight: 1.05, letterSpacing: '-0.04em' }}>
              Your music, placed in <span style={{ color: '#4b4bc0', fontStyle: 'italic' }}>film, TV, games and ads</span> worldwide.
            </h1>
            <p style={{ margin: 0, color: '#666', fontSize: 22, fontWeight: 500, letterSpacing: '-0.02em', lineHeight: 1.5, maxWidth: 800 }}>
              SyncMaster connects vetted African composers with briefs from production houses worldwide. Human curation. Rights clarity. 3–5 curated matches — not 500 unvetted submissions.
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, justifyContent: 'center', paddingTop: 16 }}>
              <CTAButton variant="primary" icon="arrow-right">Get early access</CTAButton>
              <CTAButton variant="outline" icon={null}>I'm a composer</CTAButton>
            </div>

            {/* Platforms */}
            <div style={{ marginTop: 48, marginBottom: 32, width: '100%' }}>
              <PlatformStrip />
            </div>

            {/* Dashboard preview frame */}
            <div style={{ marginTop: 48, position: 'relative', width: '100%', maxWidth: 1080 }}>
              <div style={{ position: 'absolute', inset: '-16px', background: 'linear-gradient(90deg, #4b4bc0, #d946ef)', filter: 'blur(60px)', opacity: .2, borderRadius: 40 }}></div>
              <div style={{
                position: 'relative', borderRadius: 40, border: '1px solid #e5e5e5',
                background: '#fff', overflow: 'hidden', boxShadow: '0 32px 64px -16px rgba(0,0,0,.2)',
              }}>
                <div style={{
                  position: 'absolute', top: 0, left: 0, right: 0, height: 48,
                  background: 'rgba(245,245,245,.5)', borderBottom: '1px solid #e5e5e5',
                  display: 'flex', alignItems: 'center', padding: '0 24px', gap: 8, zIndex: 20,
                }}>
                  <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#e5e5e5' }}></div>
                  <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#e5e5e5' }}></div>
                  <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#e5e5e5' }}></div>
                </div>
                <div style={{ paddingTop: 48, aspectRatio: '16 / 9', position: 'relative', background: '#fff' }}>
                  <img src="../../assets/screens/dashboard-preview.png"
                       style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section style={{ padding: '128px 0', borderTop: '1px solid #e5e5e5' }}>
        <div style={{ maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ textAlign: 'center', marginBottom: 80 }}>
            <h2 style={{ margin: '0 0 16px', color: '#111', fontSize: 48 }}>Built for the sync workflow</h2>
            <p style={{ margin: '0 auto', color: '#666', fontSize: 17, maxWidth: 640 }}>
              Every tool a composer or supervisor needs — from first brief to final placement.
            </p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 48 }}>
            <FeatureCard icon="layers" color="#4b4bc0" bg="rgba(75,75,192,.1)" title="Unified Catalog"
              description="Upload, tag, and organize your tracks with your EPK — ready to pitch the moment a brief lands."/>
            <FeatureCard icon="globe" color="#10b981" bg="rgba(16,185,129,.1)" title="Curated Matching"
              description="AI-assisted and human-verified. Producers get 3–5 perfect matches. Composers get real opportunities."/>
            <FeatureCard icon="shield" color="#f97316" bg="rgba(249,115,22,.1)" title="Rights Clarity"
              description="Every composer manually vetted. Every placement fully cleared. No surprises at the licensing stage."/>
          </div>
        </div>
      </section>

      {/* SOLUTIONS — role split */}
      <section style={{ padding: '128px 0', borderTop: '1px solid #e5e5e5', background: 'rgba(245,245,245,.3)' }}>
        <div style={{ maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ textAlign: 'center', marginBottom: 80 }}>
            <h2 style={{ margin: '0 0 16px', color: '#111', fontSize: 48 }}>Who it's built for</h2>
            <p style={{ margin: '0 auto', color: '#666', fontSize: 17, maxWidth: 640 }}>
              Two sides of the same sync deal — both served without compromise.
            </p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 32, maxWidth: 1000, margin: '0 auto' }}>
            <RoleCard icon="mic-2" color="#4b4bc0" bg="rgba(75,75,192,.1)" title="For Composers"
              description="Talented but invisible? We vet you once, then match you to briefs from producers worldwide. Your EPK travels the globe while you focus on music."
              onClick={() => onNavigate && onNavigate('composers')}/>
            <RoleCard icon="film" color="#10b981" bg="rgba(16,185,129,.1)" title="For Supervisors"
              description="Post a brief and receive 3–5 hand-curated African tracks within days. Vetted. Rights-cleared. No directories. No noise."
              onClick={() => onNavigate && onNavigate('supervisors')}/>
          </div>
        </div>
      </section>

      {/* CTA banner */}
      <section style={{ padding: '128px 0', borderTop: '1px solid #e5e5e5' }}>
        <div style={{ maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{
            position: 'relative', overflow: 'hidden',
            display: 'flex', flexDirection: 'column', alignItems: 'center',
            gap: 32, padding: 64, borderRadius: 48,
            background: 'rgba(75,75,192,.05)', border: '1px solid rgba(75,75,192,.2)',
          }}>
            <div style={{ position:'absolute', top:0, left:'50%', transform:'translateX(-50%)', width:800, height:400, background:'rgba(75,75,192,.1)', filter:'blur(120px)', borderRadius:'50%', pointerEvents:'none'}}></div>
            <div style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24, textAlign: 'center' }}>
              <Capsule icon="zap">Early Access Open</Capsule>
              <h2 style={{ margin: 0, color: '#111', fontSize: 48, maxWidth: 640 }}>Ready to get your music placed?</h2>
              <p style={{ margin: 0, color: '#666', fontSize: 17, maxWidth: 560 }}>Join the first cohort of African composers and supervisors on SyncMaster.</p>
              <CTAButton variant="primary">Get early access</CTAButton>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

// ─────────────────────────────────────────────
// COMPOSERS — /composers page
// ─────────────────────────────────────────────
function ComposersPage() {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  const steps = [
    ['01', 'Apply to the platform', "Submit your profile, genre, and a sample of your best work. Our team reviews every application personally — no bots, no automated rejections."],
    ['02', 'Get vetted by our team', "Once approved, you join a curated roster of composers. Your rights documentation is verified so you're ready to pitch any brief, anywhere."],
    ['03', 'Receive brief invites', "When a brief matches your sound, we invite you directly. No browsing thousands of listings. No cold submissions into a void."],
    ['04', 'Submit and get placed', "Submit up to 3 tracks per brief. If your track is shortlisted, we facilitate the deal. You focus on creating — we handle the rest."],
  ];
  return (
    <>
      <section style={{ paddingTop: 80, paddingBottom: 128, position: 'relative', overflow: 'hidden' }}>
        <div style={{ position:'absolute', top:0, left:'50%', transform:'translateX(-50%)', width:1000, height:500, background:'rgba(75,75,192,.1)', filter:'blur(120px)', borderRadius:'50%', opacity:.5, pointerEvents:'none'}}></div>
        <div style={{ position: 'relative', maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: 40, maxWidth: 960, margin: '0 auto' }}>
            <Capsule icon="mic-2">For Composers</Capsule>
            <h1 style={{ margin: 0, color: '#111', fontSize: 'clamp(48px,5.5vw,80px)', lineHeight: 1.05, letterSpacing: '-0.04em' }}>
              Your talent belongs on <span style={{ color: '#4b4bc0', fontStyle: 'italic' }}>the world stage.</span>
            </h1>
            <p style={{ margin: 0, color: '#666', fontSize: 22, fontWeight: 500, lineHeight: 1.5 }}>
              You have the sound. We have the connections. SyncMaster is the bridge between African composers and the global briefs that need you — without the gatekeepers, the guesswork, or the silence.
            </p>
            <CTAButton variant="primary">Apply as a composer</CTAButton>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 24, justifyContent: 'center', paddingTop: 16, fontSize: 13, color: '#666', fontWeight: 500 }}>
              {['Manually vetted', 'Rights verified', 'No submission fees', 'Direct brief invites'].map(label => (
                <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <i data-lucide="check-circle-2" style={{ width: 16, height: 16, color: '#10b981' }}></i>
                  {label}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Two-column problem / solution */}
      <section style={{ padding: '128px 0', borderTop: '1px solid #e5e5e5', background: 'rgba(245,245,245,.3)' }}>
        <div style={{ maxWidth: 1100, margin: '0 auto', padding: '0 24px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 64, alignItems: 'center' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
            <Capsule color="#ef4444">The problem</Capsule>
            <h2 style={{ margin: 0, color: '#111', fontSize: 36 }}>Technically skilled. Professionally invisible.</h2>
            <p style={{ margin: 0, color: '#666', fontSize: 16, lineHeight: 1.6, fontWeight: 500 }}>
              African composers produce world-class music every day. But the global sync industry doesn't have a direct line to you. Platforms built for the West ignore the African sound. The music exists — the pathway doesn't.
            </p>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
            <Capsule color="#10b981" icon="sparkles">The SyncMaster way</Capsule>
            <h2 style={{ margin: 0, color: '#111', fontSize: 36 }}>One vetting. Lifetime access.</h2>
            <p style={{ margin: 0, color: '#666', fontSize: 16, lineHeight: 1.6, fontWeight: 500 }}>
              Apply once. Get verified once. Then sit back and let the briefs come to you. Every time a producer needs your sound, we call you — not the other 500 composers on an open directory.
            </p>
          </div>
        </div>
      </section>

      {/* Steps */}
      <section style={{ padding: '128px 0', borderTop: '1px solid #e5e5e5' }}>
        <div style={{ maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ textAlign: 'center', marginBottom: 80 }}>
            <h2 style={{ margin: '0 0 16px', color: '#111', fontSize: 48 }}>How it works</h2>
            <p style={{ margin: 0, color: '#666', fontSize: 17 }}>Four steps from application to placement.</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 32 }}>
            {steps.map(([n, t, d]) => <StepCard key={n} number={n} title={t} description={d} />)}
          </div>
        </div>
      </section>
    </>
  );
}

// ─────────────────────────────────────────────
// SUPERVISORS — /supervisors page
// ─────────────────────────────────────────────
function SupervisorsPage() {
  React.useEffect(() => { window.lucide && window.lucide.createIcons(); });
  const briefSample = { title:'Lagos crime thriller — main title cue', genres:['Afrobeats','Cinematic','Tense'], budget:'$15,000 – $25,000', deadline:'14 days' };
  return (
    <>
      <section style={{ paddingTop: 80, paddingBottom: 128, position: 'relative', overflow: 'hidden' }}>
        <div style={{ position:'absolute', top:0, left:'50%', transform:'translateX(-50%)', width:1000, height:500, background:'rgba(16,185,129,.08)', filter:'blur(120px)', borderRadius:'50%', opacity:.5, pointerEvents:'none'}}></div>
        <div style={{ position: 'relative', maxWidth: 1440, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: 40, maxWidth: 960, margin: '0 auto' }}>
            <Capsule icon="film" color="#10b981">For Supervisors</Capsule>
            <h1 style={{ margin: 0, color: '#111', fontSize: 'clamp(48px,5.5vw,80px)', lineHeight: 1.05, letterSpacing: '-0.04em' }}>
              Post a brief. Get a <span style={{ color: '#10b981', fontStyle: 'italic' }}>shortlist</span> in 48 hours.
            </h1>
            <p style={{ margin: 0, color: '#666', fontSize: 22, fontWeight: 500, lineHeight: 1.5 }}>
              We hand-curate 3–5 vetted African tracks for every brief. Rights-cleared. Ready to license. Without you ever opening a directory of 5,000 unvetted submissions.
            </p>
            <CTAButton variant="primary">Post your first brief</CTAButton>

            {/* Mini brief preview */}
            <div style={{
              marginTop: 24, padding: 28, borderRadius: 32,
              background: '#fff', border: '1px solid #e5e5e5',
              boxShadow: '0 25px 50px -16px rgba(0,0,0,.1)',
              maxWidth: 560, width: '100%', textAlign: 'left',
              display: 'flex', flexDirection: 'column', gap: 16,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ padding: '4px 12px', borderRadius: 9999, background: 'oklch(0.88 0.18 120)', color: '#000', fontSize: 10, fontWeight: 900, letterSpacing: '0.2em' }}>ACTIVE</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: '#666' }}>DEADLINE · {briefSample.deadline}</span>
              </div>
              <h3 style={{ margin: 0, color: '#111', fontSize: 20 }}>{briefSample.title}</h3>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {briefSample.genres.map(g => (
                  <span key={g} style={{ padding: '4px 10px', borderRadius: 6, background: '#f5f5f5', color: '#4b4bc0', fontSize: 11, fontWeight: 700 }}>{g}</span>
                ))}
              </div>
              <div style={{ paddingTop: 14, borderTop: '1px solid #e5e5e5', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: '#666', letterSpacing: '0.2em', textTransform: 'uppercase' }}>BUDGET</div>
                  <div style={{ fontSize: 14, fontWeight: 900, letterSpacing: '-0.04em', marginTop: 2, color: '#111' }}>{briefSample.budget}</div>
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: '#666' }}>4 composers matched</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats strip */}
      <section style={{ padding: '64px 0', borderTop: '1px solid #e5e5e5' }}>
        <div style={{ maxWidth: 1100, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 32 }}>
            {[
              ['24–48h', 'Curated shortlist turnaround'],
              ['3–5',    'Tracks per brief, not 500'],
              ['100%',   'Rights-verified roster'],
              ['$0',     'To post a brief'],
            ].map(([big, label]) => (
              <div key={big} style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                <div style={{ fontSize: 48, fontWeight: 900, letterSpacing: '-0.068em', color: '#111', lineHeight: 1 }}>{big}</div>
                <div style={{ fontSize: 13, fontWeight: 700, color: '#666' }}>{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

Object.assign(window, { Landing, ComposersPage, SupervisorsPage });
