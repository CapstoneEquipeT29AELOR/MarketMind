// Draws a simple line chart of closing prices from POST /api/stocks/chart.
import { useEffect, useState } from 'react';
import { getStockChart } from '../api/client.js';
import { useApi } from '../api/useApi.js';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';
import ApiStatus from './ApiStatus.jsx';

const chartWidth = 760;
const chartHeight = 180;
// UI periods mapped to the API's `timeline` values.
const periods = [
  { value: '1D', label: '1D', timeline: '1d' },
  { value: '1W', label: '1W', timeline: '5d' },
  { value: '1M', label: '1M', timeline: '1mo' },
  { value: '6M', label: '6M', timeline: '6mo' },
  { value: '1Y', label: '1Y', timeline: '1y' },
  { value: '5Y', label: '5Y', timeline: '5y' },
];

// Map prices into a stable SVG viewBox so the chart scales with its panel.
function getPoints(values) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const spread = max - min || 1;
  return values.map((value, index) => {
    const x = (index / Math.max(values.length - 1, 1)) * chartWidth;
    const y = 10 + ((max - value) / spread) * (chartHeight - 20);
    return { x, y, value };
  });
}

export default function PriceChart({ symbol }) {
  const { preferences, updatePreference } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  const [period, setPeriod] = useState(
    periods.some((item) => item.value === preferences.chartPeriod)
      ? preferences.chartPeriod
      : '1M'
  );

  useEffect(() => {
    if (periods.some((item) => item.value === preferences.chartPeriod)) {
      setPeriod(preferences.chartPeriod);
    }
  }, [preferences.chartPeriod]);

  const timeline = periods.find((item) => item.value === period)?.timeline ?? '1mo';
  const { data, error, loading } = useApi((options) => getStockChart(symbol, timeline, options), [symbol, timeline]);
  const series = data ?? [];
  const values = series.map((point) => point.close);
  const points = getPoints(values);
  const linePoints = points.map(({ x, y }) => `${x},${y}`).join(' ');
  const firstPrice = values[0];
  const lastPrice = values[values.length - 1];
  const change = lastPrice - firstPrice;
  const changePercent = firstPrice ? (change / firstPrice) * 100 : 0;
  const isPositive = change >= 0;
  const gradientId = `chart-gradient-${symbol}`;

  return (
    <section className="price-chart-section" aria-labelledby="chart-heading">
      <div className="chart-topline">
        <div>
          <h2 id="chart-heading">
            {period === '1D' ? <span>{t('intradayPrice')}</span> : <span>{t('historicalPrice')}</span>}
          </h2>
          <p className="chart-period-caption">
            {period}
            {series.length > 0 && ` · ${series[0].date} – ${series[series.length - 1].date}`}
          </p>
        </div>

        {values.length > 0 && <span className={isPositive ? 'positive' : 'negative'}>
          {change > 0 ? '+' : change < 0 ? '-' : ''}
          ${Math.abs(change).toFixed(2)}
          {' '}({changePercent > 0 ? '+' : ''}
          {changePercent.toFixed(2)}%)
        </span>}
      </div>

      <div className="chart-periods" aria-label="Chart time range">
        {periods.map((item) => (
          <button
            key={item.value}
            type="button"
            className={period === item.value ? 'chart-period active' : 'chart-period'}
            aria-pressed={period === item.value}
            onClick={() => {
              setPeriod(item.value);
              updatePreference('chartPeriod', item.value);
            }}
          >
            {item.label}
          </button>
        ))}
      </div>

      <ApiStatus loading={loading && !values.length} error={error} empty={!loading && !values.length} />

      {values.length > 0 && !error && (<>
      <svg
        className="price-chart"
        viewBox={`0 0 ${chartWidth} ${chartHeight}`}
        preserveAspectRatio="none"
        role="img"
        aria-label={`${symbol} price chart for ${period}`}
      >
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.22" />
            <stop offset="100%" stopColor="#38bdf8" stopOpacity="0" />
          </linearGradient>
        </defs>

        {[0.25, 0.5, 0.75].map((fraction) => (
          <line
            key={fraction}
            x1="0"
            x2={chartWidth}
            y1={chartHeight * fraction}
            y2={chartHeight * fraction}
            className="chart-grid-line"
          />
        ))}

        <polygon
          points={`0,${chartHeight} ${linePoints} ${chartWidth},${chartHeight}`}
          fill={`url(#${gradientId})`}
        />

        <polyline
          points={linePoints}
          fill="none"
          stroke={isPositive ? '#38bdf8' : '#fb7185'}
          strokeWidth="2.5"
          strokeLinejoin="round"
          strokeLinecap="round"
          vectorEffect="non-scaling-stroke"
        />

        {points.length > 0 && (
          <circle
            cx={points[points.length - 1].x}
            cy={points[points.length - 1].y}
            r="4"
            fill={isPositive ? '#38bdf8' : '#fb7185'}
            stroke="var(--panel-bg)"
            strokeWidth="2"
            vectorEffect="non-scaling-stroke"
          />
        )}
      </svg>

      <p className="chart-times">
        <span>{period === '1D' ? <span>{t('open')}</span> : <span>{t('start')}</span>}</span>
        <span>{period === '1D' ? <span>{t('midday')}</span> : <span>{t('midPeriod')}</span>}</span>
        <span>{period === '1D' ? <span>{t('close')}</span> : <span>{t('latest')}</span>}</span>
      </p>
      </>)}
    </section>
  );
}