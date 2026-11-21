import type { Station } from '../types';
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
}: SearchPanelProps) {
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
        <span className="filters__label" aria-live="polite">
          {searching ? `${foundCount.toLocaleString('en-US')} found` : 'Listen right now'}
        </span>
      </div>

      {stations.length === 0 ? (
        <p className="empty">No stations found</p>
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
