import './App.css'
import { useState, useMemo } from 'react';
import useStations from './hooks/useStations';
import StationCard from './components/StationCard';
import Player from './components/Player';
import type { Station } from './types';

function App() {
  const { stations, loading, error } = useStations();
  const [query, setQuery] = useState('');
  const [country, setCountry] = useState('');
  const [current, setCurrent] = useState<Station | null>(null);

  // Country options depend only on the data, so compute them once per load.
  const countries = useMemo(
    () =>
      Array.from(new Set(stations.map(s => s.country)))
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b)),
    [stations],
  );

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  const q = query.trim().toLowerCase();
  const filtered = stations.filter(
    s =>
      s.name.toLowerCase().includes(q) &&
      (!country || s.country === country),
  );

  return (
    <>
      <h1>RadioPeck</h1>

      <input
        type="search"
        placeholder="Search by name"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />

      <select value={country} onChange={e => setCountry(e.target.value)}>
        <option value="">Any country</option>
        {countries.map(c => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>

      <p>Found: {filtered.length}</p>

      <ul style={{ paddingBottom: 90 }}>
        {filtered.slice(0, 50).map(s => (
          <li key={s.stationuuid}>
            <StationCard
              station={s}
              selected={s.stationuuid === current?.stationuuid}
              onSelect={() => setCurrent(s)}
            />
          </li>
        ))}
      </ul>

      <Player key={current?.stationuuid } station={current} />
    </>
  );
}

export default App;