// Combines the selected stock quote, simple chart, and a few sample headlines.
import { newsItems } from '../data/mockData.js';
import NewsCard from '../components/NewsCard.jsx';
import PriceChart from '../components/PriceChart.jsx';
import StockOverview from '../components/StockOverview.jsx';

export default function Dashboard({ selectedStock }) {
  return (
    <div className="dashboard">
      <StockOverview stock={selectedStock} />
      <div className="chart-news">
        <PriceChart stock={selectedStock} />
        <section aria-labelledby="latest-news-heading">
          <h2 id="latest-news-heading">Latest financial news</h2>
          <div>{newsItems.slice(0, 2).map((item) => <NewsCard item={item} key={item.headline} />)}</div>
        </section>
      </div>
    </div>
  );
}