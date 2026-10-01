// Lists all of the financial news items stored in the local mock data.
import { newsItems } from '../data/mockData.js';
import NewsCard from '../components/NewsCard.jsx';

export default function News() {
  return (
    <div className="page-content"><section className="news-page-panel"><div className="panel-heading"><h2>Latest financial news</h2><span className="section-asof">Sample headlines</span></div><div className="news-page-list">{newsItems.map((item) => <NewsCard item={item} key={item.headline} />)}</div></section></div>
  );
}