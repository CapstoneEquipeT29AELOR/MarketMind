// Shows example dashboard preferences that are not saved to an account.
import { Bell, Clock3, Globe2, SlidersHorizontal } from 'lucide-react';

const preferences = [
  { icon: Globe2, title: 'Market region', value: 'United States', detail: 'Default market for your dashboard.' },
  { icon: Clock3, title: 'Market hours', value: 'Eastern Time (ET)', detail: 'Times are shown in the selected market timezone.' },
  { icon: Bell, title: 'Market notifications', value: 'Enabled', detail: 'Price and news alerts are currently displayed as sample data.' },
];

export default function Settings() {
  return (
    <div className="page-content"><section className="settings-panel panel"><div className="panel-heading"><div><div className="section-kicker">DASHBOARD PREFERENCES</div><h2>General settings</h2></div><span className="settings-icon"><SlidersHorizontal size={17} /></span></div><p className="settings-intro">These preferences are local demo values and are not saved to an account.</p>{preferences.map(({ icon: Icon, title, value, detail }) => <div className="setting-row" key={title}><span className="setting-icon"><Icon size={17} /></span><div className="setting-copy"><strong>{title}</strong><span>{detail}</span></div><span className="setting-value">{value}</span></div>)}</section></div>
  );
}