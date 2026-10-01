// Displays a single sample financial news headline and its source.
export default function NewsCard({ item }) {
  return (
    <article className="news-item">
      <h3>{item.headline}</h3>
      {item.summary && <p>{item.summary}</p>}
      <small>{item.source} · {item.time}</small>
    </article>
  );
}