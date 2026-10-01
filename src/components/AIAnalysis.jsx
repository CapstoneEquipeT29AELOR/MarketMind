// Presents sample sentiment, confidence, and factors for the selected stock.
export default function AIAnalysis({ analysis, symbol }) {
  return (
    <section aria-labelledby="analysis-heading">
      <h2 id="analysis-heading">MarketMind AI analysis: {symbol}</h2>
      <p className="analysis-summary">{analysis.summary}</p>
      <p><strong>Sentiment:</strong> {analysis.sentiment}</p>
      <p><strong>Confidence:</strong> {analysis.confidence}%</p>
      <h3>Key factors</h3>
      <ul>{analysis.factors.map((factor) => <li key={factor.label}>{factor.label}: {factor.detail}</li>)}</ul>
      <small>Sample AI analysis for demonstration only.</small>
    </section>
  );
}