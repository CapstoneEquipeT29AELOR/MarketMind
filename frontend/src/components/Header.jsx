// Displays the current page title and lets the user search for and choose a stock.
import { useEffect, useRef, useState } from 'react';
import { searchStocks } from '../api/client.js';
import { Clock3, Loader2, Search, Settings2 } from 'lucide-react';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

const sectionTitleKeys = {
  dashboard: 'marketOverview',
  markets: 'markets',
  news: 'news',
  analysis: 'aiAnalysis',
  settings: 'settings',
};

// The API only accepts symbols of 1-6 characters (see the Symbol schema in openapi.yaml).
const isValidSymbol = (value) => value.length >= 1 && value.length <= 6;

function StockSearch({ selectedSymbol, onSelectSymbol, label, placeholder, noResultsText }) {
  const [draft, setDraft] = useState(selectedSymbol);
  // status: idle | loading | done | error
  const [search, setSearch] = useState({ status: 'idle', results: [], error: null });
  const containerRef = useRef(null);
  const controllerRef = useRef(null);

  useEffect(() => setDraft(selectedSymbol), [selectedSymbol]);

  // Close the results panel when clicking anywhere outside the search box.
  useEffect(() => {
    const handleClick = (event) => {
      if (!containerRef.current?.contains(event.target)) close();
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  // Abort any in-flight lookup when the component unmounts.
  useEffect(() => () => controllerRef.current?.abort(), []);

  const close = () => {
    controllerRef.current?.abort();
    setSearch({ status: 'idle', results: [], error: null });
  };

  const choose = (symbol) => {
    onSelectSymbol(symbol);
    setDraft(symbol);
    close();
  };

  // Only called on Enter or the search button, so POST /api/stocks/search runs once per submit.
  const runSearch = (event) => {
    event.preventDefault();
    const query = draft.trim();
    if (!query) return;

    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    setSearch({ status: 'loading', results: [], error: null });

    searchStocks(query.slice(0, 50), { signal: controller.signal })
      .then((symbols) => {
        const results = [...new Set(symbols.map((symbol) => String(symbol).toUpperCase()))]
          .filter(isValidSymbol);
        setSearch({ status: 'done', results, error: null });
      })
      .catch((error) => {
        if (error.name === 'AbortError') return;
        setSearch({ status: 'error', results: [], error: error.message });
      });
  };

  const isOpen = search.status !== 'idle';

  return (
    <form
      ref={containerRef}
      className="stock-selector stock-search"
      role="search"
      onSubmit={runSearch}
      onKeyDown={(event) => {
        if (event.key === 'Escape') close();
      }}
    >
      <label htmlFor="stock-search-input">{label}</label>
      <div className="stock-search-field">
        <input
          id="stock-search-input"
          type="search"
          value={draft}
          placeholder={placeholder}
          autoComplete="off"
          maxLength={50}
          onFocus={(event) => event.target.select()}
          onChange={(event) => setDraft(event.target.value)}
        />
        <button type="submit" className="stock-search-button" aria-label={placeholder} title={placeholder}>
          {search.status === 'loading' ? <Loader2 size={16} className="spin" /> : <Search size={16} />}
        </button>

        {isOpen && (
          <div className="stock-search-results" role="listbox" aria-label={label}>
            {search.status === 'loading' && <p className="stock-search-message">…</p>}
            {search.status === 'error' && (
              <p className="stock-search-message stock-search-error">{search.error}</p>
            )}
            {search.status === 'done' && !search.results.length && (
              <p className="stock-search-message">{noResultsText}</p>
            )}
            {search.results.map((symbol) => (
              <button
                type="button"
                role="option"
                aria-selected={symbol === selectedSymbol}
                key={symbol}
                className="stock-search-option"
                onClick={() => choose(symbol)}
              >
                {symbol}
              </button>
            ))}
          </div>
        )}
      </div>
    </form>
  );
}

export default function Header({ activeSection, selectedSymbol, onSelectSymbol, onNavigate }) {
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
        <p>MarketMind · {t('liveData')}</p>
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

        <StockSearch
          selectedSymbol={selectedSymbol}
          onSelectSymbol={onSelectSymbol}
          label={t('stock')}
          placeholder={t('searchStocks')}
          noResultsText={t('noResults')}
        />

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