// Draws a simple line chart from the selected stock's local sample prices.
const chartWidth = 760;
const chartHeight = 180;

// Map mock prices into a stable SVG viewBox so the chart scales with its panel.
function getPoints(values) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const spread = max - min || 1;
  return values.map((value, index) => {
    const x = (index / (values.length - 1)) * chartWidth;
    const y = 10 + ((max - value) / spread) * (chartHeight - 20);
    return `${x},${y}`;
  }).join(' ');
}

export default function PriceChart({ stock }) {
  return (
    <section aria-labelledby="chart-heading">
      <h2 id="chart-heading">Price today</h2>
      <svg className="price-chart" viewBox={`0 0 ${chartWidth} ${chartHeight}`} preserveAspectRatio="none" role="img" aria-label={`${stock.symbol} mock price chart`}>
        <polyline points={getPoints(stock.chart['1D'])} fill="none" stroke="#38bdf8" strokeWidth="3" vectorEffect="non-scaling-stroke" />
      </svg>
      <p className="chart-times"><span>Open</span><span>Midday</span><span>Close</span></p>
    </section>
  );
}