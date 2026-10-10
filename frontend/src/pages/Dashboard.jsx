// Combines the selected stock quote, simple chart, and a few sample headlines.
import { newsItems } from '../data/mockData.js';
import NewsCard from '../components/NewsCard.jsx';
import PriceChart from '../components/PriceChart.jsx';
import StockOverview from '../components/StockOverview.jsx';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

export default function Dashboard({ selectedStock, onNavigate }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);

  return (
    <div className="dashboard">
      <StockOverview stock={selectedStock} />
      <div className="chart-news">
        <PriceChart stock={selectedStock} />
        <section aria-labelledby="latest-news-heading">
          <h2 id="latest-news-heading">{t('latestFinancialNews')}</h2>
          <div>{newsItems.slice(0, 2).map((item) => <NewsCard item={item} key={item.headline} onNavigate={onNavigate}/>)}</div>
        </section>
      </div>
    </div>
  );
}