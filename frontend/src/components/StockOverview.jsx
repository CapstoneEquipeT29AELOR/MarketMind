// Shows the selected sample stock's name, price, and daily change.
import { ArrowUpRight, ArrowDownRight, DollarSign, BarChart3, TrendingUp, Activity } from 'lucide-react';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

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

export default function StockOverview({ stock }) {
  const isPositive = stock.change >= 0;
  const ChangeIcon = isPositive ? ArrowUpRight : ArrowDownRight;
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);

  return (
    <section aria-labelledby="stock-heading">
      <h2 id="stock-heading">{stock.name} ({stock.symbol})</h2>
      <p className="stock-quote">${stock.price.toFixed(2)}</p>
      <div className={`stock-change ${isPositive ? 'positive' : 'negative'}`}>
        <ChangeIcon size={16} />
        <span>
          {isPositive ? '+' : '-'}$
          {Math.abs(stock.change).toFixed(2)}
          {' '}({stock.changePercent > 0 ? '+' : ''}
          {stock.changePercent.toFixed(2)}%)
        </span>
        <span className="stock-change-period">{t('today')}</span>
      </div>

      <div className="overview-metrics">
        <Metric
          icon={DollarSign}
          label={t('marketCap')}
          value={stock.marketCap ?? '—'}
        />
        <Metric
          icon={BarChart3}
          label={t('volume')}
          value={stock.volume ?? '—'}
        />
        <Metric
          icon={TrendingUp}
          label={t('dayHigh')}
          value={stock.dayHigh != null ? `$${stock.dayHigh.toFixed(2)}` : '—'}
        />
        <Metric
          icon={Activity}
          label={t('dayLow')}
          value={stock.dayLow != null ? `$${stock.dayLow.toFixed(2)}` : '—'}
        />
      </div>
    </section>
  );
}