import type { ListMode, Station } from '../types';
import StationCard from './StationCard';

type SearchPanelProps = {
  totalCount: number;
  query: string;
  onQueryChange: (value: string) => void;
  country: string;
  onCountryChange: (value: string) => void;
  countries: string[];
  searching: boolean;
  foundCount: number;
  stations: Station[];
  currentId: string | null;
  onSelect: (station: Station) => void;
  mode: ListMode;
  onModeChange: (mode: ListMode) => void;
};

export default function SearchPanel({
  totalCount,
  query,
  onQueryChange,
  country,
  onCountryChange,
  countries,
  searching,
  foundCount,
  stations,
  currentId,
  onSelect,
  mode,
  onModeChange,
}: SearchPanelProps) {
  const recentMode = mode === 'recent';

  const label = searching
    ? `${foundCount.toLocaleString('en-US')} found`
    : recentMode
      ? 'Recently played'
      : 'Listen right now';

  const emptyText =
    recentMode && !searching ? 'Stations you listen to will appear here' : 'No stations found';

  return (
    <section className="panel" aria-label="Station search">
      <div className="panel__head">
        <h1 className="brand">RadioPeck</h1>
        <span className="count">{totalCount.toLocaleString('en-US')} stations</span>
      </div>

      <div className="search">
        <label htmlFor="q" className="sr-only">
          Search stations
        </label>
        <svg
          className="search__icon"
          width="22"
          height="22"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#5C5170"
          strokeWidth="2.2"
          strokeLinecap="round"
          aria-hidden="true"
        >
          <circle cx="11" cy="11" r="7" />
          <path d="M20 20l-3.5-3.5" />
        </svg>
        <input
          id="q"
          className="search__input"
          type="search"
          placeholder="Find your station"
          value={query}
          onChange={e => onQueryChange(e.target.value)}
        />
      </div>

      <div className="filters">
        <label htmlFor="country" className="sr-only">
          Country
        </label>
        <select
          id="country"
          className="select"
          value={country}
          onChange={e => onCountryChange(e.target.value)}
        >
          <option value="">Any country</option>
          {countries.map(c => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <button
          type="button"
          className="mode-btn"
          aria-pressed={recentMode}
          aria-label="Recently played"
          title="Recently played"
          onClick={() => onModeChange(recentMode ? 'discover' : 'recent')}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="9" />
            <path d="M12 7v5l3 2" />
          </svg>
        </button>

        <span className="filters__label" aria-live="polite">
          {label}
        </span>
      </div>

      {stations.length === 0 ? (
        <p className="empty">{emptyText}</p>
      ) : (
        <ul className="list">
          {stations.map(s => (
            <li key={s.stationuuid}>
              <StationCard
                station={s}
                selected={s.stationuuid === currentId}
                onSelect={() => onSelect(s)}
              />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}