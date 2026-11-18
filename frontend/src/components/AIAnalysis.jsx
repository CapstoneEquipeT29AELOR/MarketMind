// Presents sentiment, confidence, and factors from POST /api/stocks/analysis.
import { getStockAnalysis } from '../api/client.js';
import { useApi } from '../api/useApi.js';
import ApiStatus from './ApiStatus.jsx';

export default function AIAnalysis({ symbol }) {
  const { data: analysis, error, loading } = useApi((options) => getStockAnalysis(symbol, options), [symbol]);

  return (
    <section aria-labelledby="analysis-heading">
      <h2 id="analysis-heading">MarketMind AI analysis: {symbol}</h2>
      <ApiStatus loading={loading} error={error} empty={!analysis} />
      {!loading && analysis && (
        <>
          <p className="analysis-summary">{analysis.summary}</p>
          <p><strong>Sentiment:</strong> {analysis.sentiment} ({analysis.score}/100)</p>
          <p><strong>Confidence:</strong> {analysis.confidence}%</p>
          <h3>Key factors</h3>
          <ul>{(analysis.factors ?? []).map((factor) => <li key={factor.label}>{factor.label}: {factor.detail}</li>)}</ul>
          <small>Generated from recent news sentiment and price movement. Not financial advice.</small>
        </>
      )}
    </section>
  );
}
