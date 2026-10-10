import { useEffect, useState } from 'react';
import {
  BellRing,
  Clock3,
  Globe2,
  Languages,
  Moon,
  RotateCcw,
  SlidersHorizontal,
} from 'lucide-react';

import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

const timeZones = [
  ['America/New_York', 'newYork'],
  ['America/Toronto', 'toronto'],
  ['America/Los_Angeles', 'losAngeles'],
  ['Europe/London', 'london'],
  ['Europe/Paris', 'paris'],
  ['Asia/Tokyo', 'tokyo'],
  ['UTC', 'utc'],
];

const regions = [
  ['US', 'unitedStates'],
  ['CA', 'canada'],
  ['EU', 'europe'],
  ['ASIA', 'asia'],
];

const currencies = ['USD', 'CAD', 'EUR', 'GBP', 'JPY'];

const chartPeriods = [
  ['1D', 'day'],
  ['1W', 'week'],
  ['1M', 'month'],
  ['3M', 'threeMonths'],
  ['1Y', 'year'],
  ['5Y', 'fiveYears'],
];

function SettingRow({ icon: Icon, title, detail, children }) {
  return (
    <div className="setting-row">
      <span className="setting-icon" aria-hidden="true">
        <Icon size={18} />
      </span>

      <div className="setting-copy">
        <strong>{title}</strong>
        <span>{detail}</span>
      </div>

      <div className="setting-control">{children}</div>
    </div>
  );
}

function Toggle({ checked, onChange, label }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      className={`setting-toggle ${checked ? 'is-on' : ''}`}
      onClick={() => onChange(!checked)}
    >
      <span />
    </button>
  );
}

export default function Settings() {
  const {
    preferences,
    updatePreference,
    updateNotification,
    resetPreferences,
  } = usePreferences();

  const t = (key) =>
    getTranslation(preferences.language, key);

  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = window.setInterval(
      () => setNow(Date.now()),
      1000
    );

    return () => window.clearInterval(timer);
  }, []);

  const marketTime = new Intl.DateTimeFormat(
    preferences.language === 'fr' ? 'fr-CA' : 'en-US',
    {
      timeZone: preferences.timeZone,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZoneName: 'short',
    }
  ).format(now);

  return (
    <div className="page-content settings-page">
      <section
        className="settings-panel panel"
        aria-labelledby="settings-heading"
      >
        <div className="panel-heading">
          <div>
            <div className="section-kicker">
              {t('preferences').toUpperCase()}
            </div>

            <h2 id="settings-heading">{t('settings')}</h2>

            <p className="settings-intro">{t('subtitle')}</p>
          </div>

          <span className="settings-icon" aria-hidden="true">
            <SlidersHorizontal size={19} />
          </span>
        </div>

        <div className="settings-section">
          <h3>
            <Moon size={17} />
            {t('appearance')}
          </h3>

          <SettingRow
            icon={Moon}
            title={t('appearance')}
            detail={t('appearance')}
          >
            <div className="theme-options" aria-label={t('appearance')}>
              {['light', 'dark', 'system'].map((theme) => (
                <button
                  key={theme}
                  type="button"
                  className={
                    preferences.theme === theme
                      ? 'theme-option active'
                      : 'theme-option'
                  }
                  aria-pressed={preferences.theme === theme}
                  onClick={() => updatePreference('theme', theme)}
                >
                  {t(theme)}
                </button>
              ))}
            </div>
          </SettingRow>

          <SettingRow
            icon={Languages}
            title={t('language')}
            detail={t('languageDetail')}
          >
            <select
              aria-label={t('language')}
              value={preferences.language}
              onChange={(event) =>
                updatePreference('language', event.target.value)
              }
            >
              <option value="en">English</option>
              <option value="fr">Français</option>
            </select>
          </SettingRow>
        </div>

        <div className="settings-section">
          <h3>
            <Globe2 size={17} />
            {t('marketPreferences')}
          </h3>

          <SettingRow
            icon={Globe2}
            title={t('region')}
            detail={t('regionDetail')}
          >
            <select
              aria-label={t('region')}
              value={preferences.region}
              onChange={(event) =>
                updatePreference('region', event.target.value)
              }
            >
              {regions.map(([value, key]) => (
                <option key={value} value={value}>
                  {t(key)}
                </option>
              ))}
            </select>
          </SettingRow>

          <SettingRow
            icon={Clock3}
            title={t('timeZone')}
            detail={t('timeZoneDetail')}
          >
            <select
              aria-label={t('timeZone')}
              value={preferences.timeZone}
              onChange={(event) =>
                updatePreference('timeZone', event.target.value)
              }
            >
              {timeZones.map(([value, key]) => (
                <option key={value} value={value}>
                  {t(key)}
                </option>
              ))}
            </select>
          </SettingRow>

          <div className="market-time-preview">
            <Clock3 size={16} aria-hidden="true" />
            <span>{t('currentMarketTime')}</span>
            <strong>{marketTime}</strong>
          </div>

          <SettingRow
            icon={Globe2}
            title={t('currency')}
            detail={t('currencyDetail')}
          >
            <select
              aria-label={t('currency')}
              value={preferences.currency}
              onChange={(event) =>
                updatePreference('currency', event.target.value)
              }
            >
              {currencies.map((currency) => (
                <option key={currency} value={currency}>
                  {currency}
                </option>
              ))}
            </select>
          </SettingRow>
        </div>

        <div className="settings-section">
          <h3>
            <SlidersHorizontal size={17} />
            {t('chartPreferences')}
          </h3>

          <SettingRow
            icon={SlidersHorizontal}
            title={t('chartPeriod')}
            detail={t('chartPeriodDetail')}
          >
            <select
              aria-label={t('chartPeriod')}
              value={preferences.chartPeriod}
              onChange={(event) =>
                updatePreference('chartPeriod', event.target.value)
              }
            >
              {chartPeriods.map(([value, key]) => (
                <option key={value} value={value}>
                  {t(key)}
                </option>
              ))}
            </select>
          </SettingRow>
        </div>

        <div className="settings-section">
          <h3>
            <BellRing size={17} />
            {t('notifications')}
          </h3>

          {[
            ['priceAlerts', 'priceAlertsDetail'],
            ['marketNews', 'marketNewsDetail'],
            ['dailySummary', 'dailySummaryDetail'],
          ].map(([key, detailKey]) => (
            <SettingRow
              key={key}
              icon={BellRing}
              title={t(key)}
              detail={t(detailKey)}
            >
              <Toggle
                label={t(key)}
                checked={preferences.notifications[key]}
                onChange={(value) => updateNotification(key, value)}
              />
            </SettingRow>
          ))}
        </div>

        <div className="settings-footer">
          <p role="status">{t('saved')}</p>

          <button
            type="button"
            className="reset-button"
            onClick={resetPreferences}
          >
            <RotateCcw size={15} />
            {t('reset')}
          </button>
        </div>
      </section>
    </div>
  );
}