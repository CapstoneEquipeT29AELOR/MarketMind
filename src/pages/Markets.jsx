// Lists the sample stocks and lets a user select one for the dashboard.
import { stocks } from '../data/mockData.js';

export default function Markets({ onSelectStock }) {
  return (
    <div className="page-content">
      <section aria-labelledby="stocks-heading">
        <h2 id="stocks-heading">Sample stocks</h2>
        <div className="stocks-list">
          {stocks.map((stock) => (
            <button className="stock-row" key={stock.symbol} onClick={() => onSelectStock(stock)}>
              <strong>{stock.symbol}</strong>
              <span>${stock.price.toFixed(2)}</span>
              <span className={stock.change >= 0 ? 'positive' : 'negative'}>
                {stock.changePercent > 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
              </span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}