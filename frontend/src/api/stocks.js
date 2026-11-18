// Default list of tracked symbols (matches the backend's TRACKED tickers).
export const TRACKED_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'AMD', 'TSLA', 'NVDA'];

// Builds a quote (latest close and change versus the previous close) from chart points.
export function quoteFromChart(points) {
  if (!points?.length) return null;
  const price = points[points.length - 1].close;
  const previous = points.length > 1 ? points[points.length - 2].close : price;
  const change = price - previous;
  return {
    price,
    change,
    changePercent: previous ? (change / previous) * 100 : 0,
    asOf: points[points.length - 1].date,
  };
}
