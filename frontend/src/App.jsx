// Connects the page tabs to shared sample stock and analysis state.
import { useState } from 'react';
import { analysisBySymbol, stocks } from './data/mockData.js';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';
import Analysis from './pages/Analysis.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Markets from './pages/Markets.jsx';
import News from './pages/News.jsx';
import Settings from './pages/Settings.jsx';

const pages = { dashboard: Dashboard, markets: Markets, news: News, analysis: Analysis, settings: Settings };

export default function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [selectedStock, setSelectedStock] = useState(stocks[0]);
  const analysis = analysisBySymbol[selectedStock.symbol] ?? analysisBySymbol.NVDA;
  // Replace these local lookups with API responses when the team is ready to connect a backend.
  const Page = pages[activeSection] ?? Dashboard;

  return (
    <div className="app-shell">
      <Sidebar activeSection={activeSection} onNavigate={setActiveSection} />
      <Header activeSection={activeSection} selectedStock={selectedStock} onSelectStock={setSelectedStock} onNavigate={setActiveSection}/>
      <main className="main-area">
        <Page selectedStock={selectedStock} analysis={analysis} onNavigate={setActiveSection} onSelectStock={setSelectedStock} />
      </main>
    </div>
  );
}