// Lists recent financial news for the selected stock.
import { getStockNews } from '../api/client.js';
import { useApi } from '../api/useApi.js';
import ApiStatus from '../components/ApiStatus.jsx';
import NewsCard from '../components/NewsCard.jsx';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

export default function News({ selectedSymbol }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  const { data: news, error, loading } = useApi((options) => getStockNews(selectedSymbol, 20, options), [selectedSymbol]);

  return (
    <div className="page-content">
      <section className="news-page-panel">
        <div className="panel-heading">
          <h2>{t('latestFinancialNews')}</h2>
          <span className="section-asof">{t('headlinesFor')} {selectedSymbol}</span>
        </div>

        <ApiStatus loading={loading} error={error} empty={!news?.length} />
        {!loading && (
          <div className="news-page-list">
            {(news ?? []).map((item) => <NewsCard item={item} key={item.headline} />)}
          </div>
        )}
      </section>
    </div>
  );
}
