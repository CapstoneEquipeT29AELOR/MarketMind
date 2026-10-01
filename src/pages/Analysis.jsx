// Shows the selected stock's sample AI analysis and price chart.
import AIAnalysis from '../components/AIAnalysis.jsx';
import PriceChart from '../components/PriceChart.jsx';

export default function Analysis({ selectedStock, analysis }) {
  return (
    <div className="page-content analysis-page"><p className="analysis-intro">Example analysis using sample data for {selectedStock.symbol}.</p><AIAnalysis analysis={analysis} symbol={selectedStock.symbol} /><PriceChart stock={selectedStock} /></div>
  );
}