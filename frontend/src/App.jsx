// Connects the page tabs to the shared selected-stock state.
import { useState } from 'react';
import { TRACKED_SYMBOLS } from './api/stocks.js';
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
  const [selectedSymbol, setSelectedSymbol] = useState(TRACKED_SYMBOLS[0]);
  const Page = pages[activeSection] ?? Dashboard;

  return (
    <div className="app-shell">
      <Sidebar activeSection={activeSection} onNavigate={setActiveSection} />
      <Header activeSection={activeSection} selectedSymbol={selectedSymbol} onSelectSymbol={setSelectedSymbol} onNavigate={setActiveSection} />
      <main className="main-area">
        <Page selectedSymbol={selectedSymbol} onNavigate={setActiveSection} onSelectSymbol={setSelectedSymbol} />
      </main>
    </div>
  );
}
