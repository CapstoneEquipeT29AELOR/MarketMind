// Shows the selected sample stock's name, price, and daily change.
export default function StockOverview({ stock }) {
  const isPositive = stock.change >= 0;

  return (
    <section aria-labelledby="stock-heading">
      <h2 id="stock-heading">{stock.name} ({stock.symbol})</h2>
      <p className="stock-quote">${stock.price.toFixed(2)}</p>
      <p className={isPositive ? 'positive' : 'negative'}>
        {isPositive ? '+' : '-'}${Math.abs(stock.change).toFixed(2)} ({stock.changePercent > 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%) today
      </p>
    </section>
  );
}