// Displays the current page title and lets the user choose a sample stock.
import { stocks } from '../data/mockData.js';
import { useEffect, useState } from 'react';
import { Clock3, Settings2 } from 'lucide-react';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

const sectionTitleKeys = {
  dashboard: 'marketOverview',
  markets: 'markets',
  news: 'news',
  analysis: 'aiAnalysis',
  settings: 'settings',
};

export default function Header({ activeSection, selectedStock, onSelectStock, onNavigate }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  const title = t(sectionTitleKeys[activeSection] ?? 'marketOverview');
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setNow(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const locale = preferences.language === 'fr' ? 'fr-CA' : 'en-US';

  const marketTime = new Intl.DateTimeFormat(locale, {
    timeZone: preferences.timeZone,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short',
  }).format(now);

  return (
    <header className="page-header">
      <div className="header-title">
        <h1>{title}</h1>
        <p>MarketMind · {t('sampleData')}</p>
      </div>

      <div className="header-tools">
        <div
          className="header-market-time"
          title={`Timezone: ${preferences.timeZone}`}
        >
          <Clock3 size={16} />
          <div>
            <span className="header-tool-label">{t('marketTime')}</span>
            <strong>{marketTime}</strong>
          </div>
        </div>

        <div className="header-currency">
          <span className="header-tool-label">{t('currency')}</span>
          <strong>{preferences.currency}</strong>
        </div>

        <label className="stock-selector">
          {t('stock')}
          <select
            value={selectedStock.symbol}
            onChange={(event) => {
              const stock = stocks.find(
                (item) => item.symbol === event.target.value
              );

              if (stock) onSelectStock(stock);
            }}
          >
            {stocks.map((stock) => (
              <option key={stock.symbol} value={stock.symbol}>
                {stock.symbol}
              </option>
            ))}
          </select>
        </label>

        <button
          type="button"
          className="header-settings-button"
          onClick={() => onNavigate('settings')}
          aria-label="Open settings"
          title="Open settings"
        >
          <Settings2 size={18} />
        </button>
      </div>
    </header>
  );
}