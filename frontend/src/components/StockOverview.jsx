// Shows the selected stock's latest close and change, derived from POST /api/stocks/chart.
import { ArrowUpRight, ArrowDownRight, DollarSign, CalendarDays, TrendingUp, Activity } from 'lucide-react';
import { getStockChart } from '../api/client.js';
import { quoteFromChart } from '../api/stocks.js';
import { useApi } from '../api/useApi.js';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';
import ApiStatus from './ApiStatus.jsx';

function Metric({ icon: Icon, label, value }) {
  return (
    <div className="overview-metric">
      <span className="overview-metric-icon">
        <Icon size={16} />
      </span>
      <div>
        <span className="overview-metric-label">{label}</span>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

const formatPrice = (value) => (value != null ? `$${value.toFixed(2)}` : '—');

export default function StockOverview({ symbol }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  const { data: points, error, loading } = useApi((options) => getStockChart(symbol, '1mo', options), [symbol]);
  const quote = quoteFromChart(points);

  if (!quote) {
    return (
      <section aria-labelledby="stock-heading">
        <h2 id="stock-heading">{symbol}</h2>
        <ApiStatus loading={loading} error={error} empty />
      </section>
    );
  }

  const isPositive = quote.change >= 0;
  const ChangeIcon = isPositive ? ArrowUpRight : ArrowDownRight;
  const closes = points.map((point) => point.close);
  const previousClose = points.length > 1 ? points[points.length - 2].close : null;

  return (
    <section aria-labelledby="stock-heading">
      <h2 id="stock-heading">{symbol}</h2>
      <p className="stock-quote">{formatPrice(quote.price)}</p>
      <div className={`stock-change ${isPositive ? 'positive' : 'negative'}`}>
        <ChangeIcon size={16} />
        <span>
          {isPositive ? '+' : '-'}$
          {Math.abs(quote.change).toFixed(2)}
          {' '}({quote.changePercent > 0 ? '+' : ''}
          {quote.changePercent.toFixed(2)}%)
        </span>
        <span className="stock-change-period">{t('today')}</span>
      </div>

      <div className="overview-metrics">
        <Metric icon={DollarSign} label={t('previousClose')} value={formatPrice(previousClose)} />
        <Metric icon={TrendingUp} label={t('monthHigh')} value={formatPrice(Math.max(...closes))} />
        <Metric icon={Activity} label={t('monthLow')} value={formatPrice(Math.min(...closes))} />
        <Metric icon={CalendarDays} label={t('asOf')} value={quote.asOf} />
      </div>
    </section>
  );
}
