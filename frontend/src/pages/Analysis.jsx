// Shows the selected stock's AI analysis and price chart.
import AIAnalysis from '../components/AIAnalysis.jsx';
import PriceChart from '../components/PriceChart.jsx';

export default function Analysis({ selectedSymbol }) {
  return (
    <div className="page-content analysis-page">
      <AIAnalysis symbol={selectedSymbol} />
      <PriceChart symbol={selectedSymbol} />
    </div>
  );
}
