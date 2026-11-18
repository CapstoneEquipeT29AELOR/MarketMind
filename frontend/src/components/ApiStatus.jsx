// Shows a loading, error, or empty message for a section backed by an API call.
import { usePreferences } from '../context/PreferencesContext';
import { getTranslation } from '../i18n/translations';

export default function ApiStatus({ loading, error, empty }) {
  const { preferences } = usePreferences();
  const t = (key) => getTranslation(preferences.language, key);

  if (loading) return <p className="api-status" role="status">{t('loading')}</p>;
  if (error) return <p className="api-status api-status-error" role="alert">{error.message}</p>;
  if (empty) return <p className="api-status">{t('noData')}</p>;
  return null;
}
