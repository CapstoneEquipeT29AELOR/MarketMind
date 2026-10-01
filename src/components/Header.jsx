// Displays the current page title and lets the user choose a sample stock.
import { stocks } from '../data/mockData.js';

const sectionTitles = {
  dashboard: 'Market Overview',
  markets: 'Markets',
  news: 'Financial News',
  analysis: 'AI Analysis',
  settings: 'Settings',
};

export default function Header({ activeSection, selectedStock, onSelectStock }) {
  const title = sectionTitles[activeSection] ?? sectionTitles.dashboard;

  return (
    <header className="page-header">
      <div>
        <h1>{title}</h1>
        <p>MarketMind · sample data</p>
      </div>
      <label className="stock-selector">
        Stock
        <select value={selectedStock.symbol} onChange={(event) => onSelectStock(stocks.find((stock) => stock.symbol === event.target.value))}>
          {stocks.map((stock) => <option key={stock.symbol} value={stock.symbol}>{stock.symbol}</option>)}
        </select>
      </label>
    </header>
  );
}