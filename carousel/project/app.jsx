// app.jsx — DesignCanvas with 9 SyncMaster slides + Tweaks panel.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#3661FE",
  "background": "paper",
  "dotGrid": true,
  "pillsFilled": false,
  "displayWeight": "medium"
}/*EDITMODE-END*/;

const ACCENT_OPTIONS = [
  '#3661FE', // Linkedist blue (default)
  '#FF5A1F', // Vivid orange
  '#0E7C3A', // Forest green
  '#E8C547', // Mustard
];

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  // Display-weight tweak swaps the font-weight stack via a CSS var
  React.useEffect(() => {
    const w = { light: 400, medium: 500, bold: 700 }[t.displayWeight] || 500;
    document.documentElement.style.setProperty('--display-weight', String(w));
  }, [t.displayWeight]);

  const slideProps = {
    mode: t.background,
    accent: t.accent,
    showGrid: t.dotGrid,
    filledPills: t.pillsFilled,
  };

  const slides = [
    { id: '01', label: '01 · Hook',       Comp: Slide1 },
    { id: '02', label: '02 · Walk-in',    Comp: Slide2 },
    { id: '03', label: '03 · Deal',       Comp: Slide3 },
    { id: '04', label: '04 · Release',    Comp: Slide4 },
    { id: '05', label: '05 · Silence',    Comp: Slide5 },
    { id: '06', label: '06 · Reframe',    Comp: Slide6 },
    { id: '07', label: '07 · Mechanism',  Comp: Slide7 },
    { id: '08', label: '08 · Promise',    Comp: Slide8 },
    { id: '09', label: '09 · CTA',        Comp: Slide9 },
  ];

  return (
    <>
      <DesignCanvas>
        <DCSection
          id="carousel"
          title="SyncMaster Carousel 01 — The Tunde Problem"
          subtitle="9 slides · 1080×1350 portrait · waitlist CTA · Space Grotesk · Linkedist visual system"
        >
          {slides.map(({ id, label, Comp }) => (
            <DCArtboard key={id} id={id} label={label} width={1080} height={1350}>
              <div data-screen-label={label}>
                <Comp {...slideProps} />
              </div>
            </DCArtboard>
          ))}
        </DCSection>
      </DesignCanvas>

      <TweaksPanel title="Tweaks">
        <TweakSection label="Accent colour">
          <TweakColor
            label="Accent"
            value={t.accent}
            options={ACCENT_OPTIONS}
            onChange={(v) => setTweak('accent', v)}
          />
        </TweakSection>
        <TweakSection label="Surface">
          <TweakRadio
            label="Background"
            value={t.background}
            options={[
              { value: 'paper', label: 'Warm' },
              { value: 'pure',  label: 'Pure' },
              { value: 'dark',  label: 'Dark' },
            ]}
            onChange={(v) => setTweak('background', v)}
          />
          <TweakToggle
            label="Dot grid"
            value={t.dotGrid}
            onChange={(v) => setTweak('dotGrid', v)}
          />
          <TweakToggle
            label="Filled pills"
            value={t.pillsFilled}
            onChange={(v) => setTweak('pillsFilled', v)}
          />
        </TweakSection>
        <TweakSection label="Display type">
          <TweakRadio
            label="Weight"
            value={t.displayWeight}
            options={[
              { value: 'light',  label: 'Light' },
              { value: 'medium', label: 'Medium' },
              { value: 'bold',   label: 'Bold' },
            ]}
            onChange={(v) => setTweak('displayWeight', v)}
          />
        </TweakSection>
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
