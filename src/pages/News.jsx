// Lists all of the financial news items stored in the local mock data.
import { newsItems } from '../data/mockData.js';
import NewsCard from '../components/NewsCard.jsx';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

export default function News() {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  
  return (
    <div className="page-content">
      <section className="news-page-panel">
        <div className="panel-heading">
          <h2>{t('latestFinancialNews')}</h2>
          <span className="section-asof">{t('sampleHeadlines')}</span>
        </div>
        
        <div className="news-page-list">{newsItems.map((item) => 
          <NewsCard item={item} key={item.headline} />)}
        </div>
      </section>
    </div>
  );
}