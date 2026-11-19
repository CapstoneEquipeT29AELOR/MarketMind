// Connects the page tabs to the shared selected-stock state.
import { useEffect, useState } from 'react';
import { TRACKED_SYMBOLS } from './api/stocks.js';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';
import Analysis from './pages/Analysis.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Landing from './pages/Landing.jsx';
import Markets from './pages/Markets.jsx';
import News from './pages/News.jsx';
import Settings from './pages/Settings.jsx';

const pages = { dashboard: Dashboard, markets: Markets, news: News, analysis: Analysis, settings: Settings };

// The landing page is shown unless the URL hash is #app, so the browser back button returns to it.
const isAppHash = () => window.location.hash === '#app';

export default function App() {
  const [inApp, setInApp] = useState(isAppHash);
  const [activeSection, setActiveSection] = useState('dashboard');
  const [selectedSymbol, setSelectedSymbol] = useState(TRACKED_SYMBOLS[0]);
  const Page = pages[activeSection] ?? Dashboard;

  useEffect(() => {
    const onHashChange = () => setInApp(isAppHash());
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  useEffect(() => {
    document.title = inApp ? 'MarketMind | Market Overview' : 'MarketMind | AI market insights';
    window.scrollTo(0, 0);
  }, [inApp]);

  if (!inApp) {
    return <Landing onEnter={() => { window.location.hash = 'app'; }} />;
  }

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
