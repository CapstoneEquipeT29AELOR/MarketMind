// Combines the selected stock quote, price chart, and a few recent headlines.
import { getStockNews } from '../api/client.js';
import { useApi } from '../api/useApi.js';
import ApiStatus from '../components/ApiStatus.jsx';
import NewsCard from '../components/NewsCard.jsx';
import PriceChart from '../components/PriceChart.jsx';
import StockOverview from '../components/StockOverview.jsx';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

export default function Dashboard({ selectedSymbol, onNavigate }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  const { data: news, error, loading } = useApi((options) => getStockNews(selectedSymbol, 2, options), [selectedSymbol]);

  return (
    <div className="dashboard">
      <StockOverview symbol={selectedSymbol} />
      <div className="chart-news">
        <PriceChart symbol={selectedSymbol} />
        <section aria-labelledby="latest-news-heading">
          <h2 id="latest-news-heading">{t('latestFinancialNews')}</h2>
          <ApiStatus loading={loading} error={error} empty={!news?.length} />
          {!loading && (
            <div>{(news ?? []).map((item) => <NewsCard item={item} key={item.headline} onNavigate={onNavigate} />)}</div>
          )}
        </section>
      </div>
    </div>
  );
}
