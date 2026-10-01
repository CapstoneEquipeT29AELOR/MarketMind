// Provides navigation between the five frontend pages.
const navigation = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'markets', label: 'Markets' },
  { id: 'news', label: 'News' },
  { id: 'analysis', label: 'AI Analysis' },
  { id: 'settings', label: 'Settings' },
];

export default function Sidebar({ activeSection, onNavigate }) {
  return (
    <aside className="sidebar">
      <a className="brand" href="#dashboard" onClick={() => onNavigate('dashboard')}>MarketMind</a>
      <nav className="sidebar-nav" aria-label="Main pages">
        {navigation.map(({ id, label }) => (
          <button
            className={`nav-item ${activeSection === id ? 'active' : ''}`}
            key={id}
            onClick={() => onNavigate(id)}
            aria-current={activeSection === id ? 'page' : undefined}
          >
            <span>{label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}