// Displays a single financial news headline and its source.
import { ArrowUpRight, Clock3, ExternalLink, Newspaper } from 'lucide-react';
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

export default function NewsCard({ item, onNavigate }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);

  return (
    <article className="news-item">
      <div className="news-card-top">
        <span className="news-category">
          <Newspaper size={13} />
          {item.category || 'Markets'}
        </span>

        {item.tone && (
          <span className={`news-tone news-tone-${item.tone}`}>
            {item.tone === 'positive'
              ? 'Positive'
              : item.tone === 'negative'
                ? 'Negative'
                : item.tone === 'caution'
                  ? 'Caution'
                  : 'Neutral'}
          </span>
        )}
      </div>

      <h3>
        {item.url ? (
          <a
            className="news-headline-link"
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            title="Open article in a new tab"
          >
            {item.headline}
          </a>
        ) : (
          item.headline
        )}
      </h3>

      {item.summary && (
        <p>{item.summary}</p>
      )}

      <div className="news-card-footer">
        <span className="news-source">{item.source}</span>

        <span className="news-time">
          <Clock3 size={12} />
          {item.time}
        </span>

        {item.symbols?.length > 0 && (
          <div className="news-symbols">
            {item.symbols.slice(0, 3).map((symbol) => (
              <span key={symbol}>{symbol}</span>
            ))}
          </div>
        )}

        {item.url ? (
          <a
            className="news-open-button"
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            title={t('openArticle')}
          >
            <ExternalLink size={13} />
            {t('openArticle')}
          </a>
        ) : onNavigate && (
          <button
            type="button"
            className="news-card-arrow"
            onClick={() => onNavigate('news')}
            aria-label="View all news"
            title="View all news"
          >
            <ArrowUpRight size={15} />
          </button>
        )}
      </div>
    </article>
  );
}