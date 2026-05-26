// app-02.jsx — DesignCanvas for SyncMaster Carousel 02 — Did You Catch This?
// Brand-first defaults: purple bg, lime accent, no dot grid.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#C9E834",
  "pillsFilled": false,
  "displayWeight": "medium"
}/*EDITMODE-END*/;

const ACCENT_OPTIONS = [
  '#C9E834', // SyncMaster lime (default)
  '#FFFFFF', // Pure white — minimal
  '#FF5A1F', // Vivid orange
  '#3661FE', // Linkedist blue
];

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  React.useEffect(() => {
    const w = { light: 400, medium: 500, bold: 700 }[t.displayWeight] || 500;
    document.documentElement.style.setProperty('--display-weight', String(w));
  }, [t.displayWeight]);

  const slideProps = {
    accent: t.accent,
    filledPills: t.pillsFilled,
  };

  const slides = [
    { id: '01', label: '01 · Opener',    Comp: Slide1  },
    { id: '02', label: '02 · One Dance', Comp: Slide2  },
    { id: '03', label: '03 · Location',  Comp: Slide3  },
    { id: '04', label: '04 · Free Mind', Comp: Slide4  },
    { id: '05', label: '05 · Peru',      Comp: Slide5  },
    { id: '06', label: '06 · Wakanda',   Comp: Slide6  },
    { id: '07', label: '07 · The Turn',  Comp: Slide7  },
    { id: '08', label: '08 · The Stats', Comp: Slide8  },
    { id: '09', label: '09 · The Gap',   Comp: Slide9  },
    { id: '10', label: '10 · CTA',       Comp: Slide10 },
  ];

  return (
    <>
      <DesignCanvas>
        <DCSection
          id="carousel-02"
          title="SyncMaster Carousel 02 — Did You Catch This?"
          subtitle="10 slides · 1080×1350 portrait · SyncMaster brand purple #5252E0 + lime #C9E834 · Space Grotesk"
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

      <TweaksPanel title="Tweaks — Carousel 02">
        <TweakSection label="Accent colour">
          <TweakColor
            label="Accent"
            value={t.accent}
            options={ACCENT_OPTIONS}
            onChange={(v) => setTweak('accent', v)}
          />
        </TweakSection>
        <TweakSection label="Pills">
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
              { value: 'light',  label: 'Light'  },
              { value: 'medium', label: 'Medium' },
              { value: 'bold',   label: 'Bold'   },
            ]}
            onChange={(v) => setTweak('displayWeight', v)}
          />
        </TweakSection>
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
