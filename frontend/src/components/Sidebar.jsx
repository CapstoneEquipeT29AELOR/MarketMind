// Provides navigation between the five frontend pages.
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

const navigation = [
  { id: 'dashboard', key: 'dashboard' },
  { id: 'markets', key: 'markets' },
  { id: 'news', key: 'news' },
  { id: 'analysis', key: 'aiAnalysis' },
  { id: 'settings', key: 'settings' },
];

export default function Sidebar({ activeSection, onNavigate }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);
  
  return (
    <aside className="sidebar">
      <a className="brand" href="#dashboard" onClick={() => onNavigate('dashboard')}>MarketMind</a>
      <nav className="sidebar-nav" aria-label="Main pages">
        {navigation.map(({ id, key }) => (
          <button
            className={`nav-item ${activeSection === id ? 'active' : ''}`}
            key={id}
            onClick={() => onNavigate(id)}
            aria-current={activeSection === id ? 'page' : undefined}
          >
            <span>{t(key)}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}