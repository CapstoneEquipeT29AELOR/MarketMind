import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from 'react';

const PreferencesContext = createContext(null);

export const DEFAULT_PREFERENCES = {
  language: 'en',
  theme: 'system',
  timeZone: 'America/New_York',
  region: 'US',
  currency: 'USD',
  chartPeriod: '1M',
  notifications: {
    priceAlerts: true,
    marketNews: true,
    dailySummary: false,
  },
};

const STORAGE_KEY = 'market-ai-preferences';

function loadPreferences() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return DEFAULT_PREFERENCES;

    const parsed = JSON.parse(saved);

    const validThemes = ['light', 'dark', 'system'];
    const validLanguages = ['en', 'fr'];
    const validPeriods = ['1D', '1W', '1M', '3M', '1Y'];

    return {
      ...DEFAULT_PREFERENCES,
      ...parsed,
      theme: validThemes.includes(parsed.theme)
        ? parsed.theme
        : DEFAULT_PREFERENCES.theme,
      language: validLanguages.includes(parsed.language)
        ? parsed.language
        : DEFAULT_PREFERENCES.language,
      chartPeriod: validPeriods.includes(parsed.chartPeriod)
        ? parsed.chartPeriod
        : DEFAULT_PREFERENCES.chartPeriod,
      notifications: {
        ...DEFAULT_PREFERENCES.notifications,
        ...(parsed.notifications ?? {}),
      },
    };
  } catch {
    return DEFAULT_PREFERENCES;
  }
}

export function PreferencesProvider({ children }) {
  const [preferences, setPreferences] = useState(loadPreferences);

  const updatePreference = useCallback((key, value) => {
    setPreferences((current) => ({
      ...current,
      [key]: value,
    }));
  }, []);

  const updateNotification = useCallback((key, value) => {
    setPreferences((current) => ({
      ...current,
      notifications: {
        ...current.notifications,
        [key]: value,
      },
    }));
  }, []);

  const resetPreferences = useCallback(() => {
    setPreferences({
      ...DEFAULT_PREFERENCES,
      notifications: {
        ...DEFAULT_PREFERENCES.notifications,
      },
    });
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
    } catch {
      // The app still works if browser storage is unavailable.
    }
  }, [preferences]);

  useEffect(() => {
    const root = document.documentElement;
    const media = window.matchMedia(
      '(prefers-color-scheme: dark)'
    );

    const applyTheme = () => {
      const effectiveTheme =
        preferences.theme === 'system'
          ? media.matches
            ? 'dark'
            : 'light'
          : preferences.theme;

      root.dataset.theme = effectiveTheme;
      root.style.colorScheme = effectiveTheme;
    };

    root.lang = preferences.language;
    applyTheme();

    if (preferences.theme !== 'system') return;

    media.addEventListener('change', applyTheme);

    return () => {
      media.removeEventListener('change', applyTheme);
    };
  }, [preferences.theme, preferences.language]);

  return (
    <PreferencesContext.Provider
      value={{
        preferences,
        updatePreference,
        updateNotification,
        resetPreferences,
      }}
    >
      {children}
    </PreferencesContext.Provider>
  );
}

export function usePreferences() {
  const context = useContext(PreferencesContext);

  if (!context) {
    throw new Error(
      'usePreferences must be used inside PreferencesProvider'
    );
  }

  return context;
}