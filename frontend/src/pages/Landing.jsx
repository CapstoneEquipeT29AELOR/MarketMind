// Public landing page shown before the dashboard; "Open dashboard" enters the app.
import { ArrowRight, BarChart3, BrainCircuit, Globe2, Moon, Newspaper, Sun } from 'lucide-react';
import { TRACKED_SYMBOLS } from '../api/stocks.js';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';
import './Landing.css';

const features = [
  { icon: BarChart3, title: 'landingFeatureChartsTitle', body: 'landingFeatureChartsBody' },
  { icon: Newspaper, title: 'landingFeatureNewsTitle', body: 'landingFeatureNewsBody' },
  { icon: BrainCircuit, title: 'landingFeatureAiTitle', body: 'landingFeatureAiBody' },
  { icon: Globe2, title: 'landingFeaturePrefsTitle', body: 'landingFeaturePrefsBody' },
];

const steps = [
  { title: 'landingStep1Title', body: 'landingStep1Body' },
  { title: 'landingStep2Title', body: 'landingStep2Body' },
  { title: 'landingStep3Title', body: 'landingStep3Body' },
];

// Decorative preview of the dashboard; the shape is illustrative, not real market data.
function HeroPreview({ t }) {
  const line = 'M0,118 C30,112 48,96 72,100 C98,104 112,80 140,74 C168,68 182,86 210,70 C238,54 256,40 284,46 C306,50 322,30 340,22';
  return (
    <div className="landing-preview" aria-hidden="true">
      <div className="landing-preview-head">
        <div>
          <span className="landing-preview-symbol">NVDA</span>
          <span className="landing-preview-label">{t('priceChart')}</span>
        </div>
        <span className="landing-preview-chip">1M</span>
      </div>
      <svg className="landing-preview-chart" viewBox="0 0 340 140" preserveAspectRatio="none">
        <defs>
          <linearGradient id="landing-fill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="var(--accent-color)" stopOpacity="0.35" />
            <stop offset="100%" stopColor="var(--accent-color)" stopOpacity="0" />
          </linearGradient>
        </defs>
        {[35, 70, 105].map((y) => (
          <line key={y} x1="0" x2="340" y1={y} y2={y} className="landing-preview-grid" />
        ))}
        <path d={`${line} L340,140 L0,140 Z`} fill="url(#landing-fill)" />
        <path d={line} className="landing-preview-line" />
      </svg>
      <div className="landing-preview-rows">
        <div className="landing-preview-row">
          <span className="landing-dot positive" />
          <span className="landing-bar" style={{ width: '78%' }} />
          <span className="landing-tag positive">{t('positive')}</span>
        </div>
        <div className="landing-preview-row">
          <span className="landing-dot neutral" />
          <span className="landing-bar" style={{ width: '62%' }} />
          <span className="landing-tag neutral">{t('neutral')}</span>
        </div>
        <div className="landing-preview-row">
          <span className="landing-dot negative" />
          <span className="landing-bar" style={{ width: '70%' }} />
          <span className="landing-tag negative">{t('negative')}</span>
        </div>
      </div>
    </div>
  );
}

export default function Landing({ onEnter }) {
  const { preferences, updatePreference } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  const isDark = preferences.theme === 'system'
    ? window.matchMedia('(prefers-color-scheme: dark)').matches
    : preferences.theme === 'dark';

  return (
    <div className="landing">
      <nav className="landing-nav">
        <a className="landing-brand" href="#">
          <span className="landing-logo" aria-hidden="true"><BarChart3 size={18} /></span>
          MarketMind
        </a>
        <div className="landing-nav-actions">
          <button
            type="button"
            className="landing-icon-button"
            onClick={() => updatePreference('language', preferences.language === 'fr' ? 'en' : 'fr')}
            aria-label={t('language')}
            title={t('language')}
          >
            {preferences.language === 'fr' ? 'EN' : 'FR'}
          </button>
          <button
            type="button"
            className="landing-icon-button"
            onClick={() => updatePreference('theme', isDark ? 'light' : 'dark')}
            aria-label={t('appearance')}
            title={t('appearance')}
          >
            {isDark ? <Sun size={16} /> : <Moon size={16} />}
          </button>
          <button type="button" className="landing-button primary small" onClick={onEnter}>
            {t('landingOpen')}
          </button>
        </div>
      </nav>

      <header className="landing-hero">
        <div className="landing-hero-copy">
          <span className="landing-eyebrow">{t('landingEyebrow')}</span>
          <h1>
            {t('landingTitleA')} <span className="landing-gradient">{t('landingTitleB')}</span>
          </h1>
          <p className="landing-lead">{t('landingLead')}</p>
          <div className="landing-cta-row">
            <button type="button" className="landing-button primary" onClick={onEnter}>
              {t('landingOpen')} <ArrowRight size={18} />
            </button>
            <a className="landing-button ghost" href="#features">{t('landingLearnMore')}</a>
          </div>
        </div>
        <HeroPreview t={t} />
      </header>

      <section className="landing-tickers" aria-label={t('trackedStocks')}>
        <span className="landing-tickers-label">{t('trackedStocks')}</span>
        <div className="landing-tickers-list">
          {TRACKED_SYMBOLS.map((symbol) => <span key={symbol}>{symbol}</span>)}
        </div>
      </section>

      <section id="features" className="landing-section">
        <h2>{t('landingFeaturesTitle')}</h2>
        <p className="landing-section-lead">{t('landingFeaturesLead')}</p>
        <div className="landing-features">
          {features.map(({ icon: Icon, title, body }) => (
            <article className="landing-feature" key={title}>
              <span className="landing-feature-icon"><Icon size={20} /></span>
              <h3>{t(title)}</h3>
              <p>{t(body)}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-section">
        <h2>{t('landingStepsTitle')}</h2>
        <ol className="landing-steps">
          {steps.map(({ title, body }, index) => (
            <li className="landing-step" key={title}>
              <span className="landing-step-number">{index + 1}</span>
              <h3>{t(title)}</h3>
              <p>{t(body)}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="landing-final">
        <h2>{t('landingFinalTitle')}</h2>
        <p>{t('landingFinalBody')}</p>
        <button type="button" className="landing-button primary" onClick={onEnter}>
          {t('landingOpen')} <ArrowRight size={18} />
        </button>
      </section>

      <footer className="landing-footer">
        <span>© {new Date().getFullYear()} MarketMind</span>
        <span>{t('landingDisclaimer')}</span>
      </footer>
    </div>
  );
}
