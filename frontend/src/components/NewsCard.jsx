// Displays a single sample financial news headline and its source.
import { ArrowUpRight, Clock3, Newspaper } from 'lucide-react';

export default function NewsCard({ item, onNavigate }) {
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
              : item.tone === 'caution'
                ? 'Caution'
                : 'Neutral'}
          </span>
        )}
      </div>

      <h3>{item.headline}</h3>

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

        <button
          type="button"
          className="news-card-arrow"
          onClick={() => onNavigate?.('news')}
          aria-label="Voir toutes les actualités"
          title="Voir toutes les actualités"
        >
          <ArrowUpRight size={15} />
        </button>
      </div>
    </article>
  );
}