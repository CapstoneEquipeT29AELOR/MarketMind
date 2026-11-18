// Lists the tracked stocks with their latest close and lets a user select one.
import { getStockChart } from '../api/client.js';
import { quoteFromChart, TRACKED_SYMBOLS } from '../api/stocks.js';
import { useApi } from '../api/useApi.js';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

function StockRow({ symbol, onSelect }) {
  const { data, error, loading } = useApi((options) => getStockChart(symbol, '5d', options), [symbol]);
  const quote = quoteFromChart(data);

  return (
    <button className="stock-row" onClick={() => onSelect(symbol)}>
      <strong>{symbol}</strong>
      <span>{quote ? `$${quote.price.toFixed(2)}` : loading ? '…' : '—'}</span>
      {quote ? (
        <span className={quote.change >= 0 ? 'positive' : 'negative'}>
          {quote.changePercent > 0 ? '+' : ''}{quote.changePercent.toFixed(2)}%
        </span>
      ) : (
        <span title={error?.message}>{loading ? '…' : '—'}</span>
      )}
    </button>
  );
}

export default function Markets({ onSelectSymbol }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);

  return (
    <div className="page-content">
      <section aria-labelledby="stocks-heading">
        <h2 id="stocks-heading">{t('trackedStocks')}</h2>
        <div className="stocks-list">
          {TRACKED_SYMBOLS.map((symbol) => (
            <StockRow key={symbol} symbol={symbol} onSelect={onSelectSymbol} />
          ))}
        </div>
      </section>
    </div>
  );
}
