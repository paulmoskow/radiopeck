import { useMemo, useState } from 'react';
import useStations from './hooks/useStations';
import SearchPanel from './components/SearchPanel';
import Player from './components/Player';
import { sample } from './lib/stations';
import type { Station } from './types';

const PAGE_SIZE = 50;

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

  //random pickup stations
  const discover = useMemo(
    () => sample(stations.filter(s => s.country && s.tags.length > 0), PAGE_SIZE),
    [stations],
  );

  const q = query.trim().toLowerCase();
  const searching = q !== '' || country !== '';

  const matches = useMemo(
    () =>
      searching
        ? stations.filter(
            s => s.name.toLowerCase().includes(q) && (!country || s.country === country),
          )
        : [],
    [stations, q, country, searching],
  );

  if (loading) {
    return (
      <div className="app app--status">
        <p className="status">Loading…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app app--status">
        <p className="status" role="alert">
          {error}
        </p>
      </div>
    );
  }

  const shown = searching ? matches.slice(0, PAGE_SIZE) : discover;

  return (
    <main className="app">
      <SearchPanel
        totalCount={stations.length}
        query={query}
        onQueryChange={setQuery}
        country={country}
        onCountryChange={setCountry}
        countries={countries}
        searching={searching}
        foundCount={matches.length}
        stations={shown}
        currentId={current?.stationuuid ?? null}
        onSelect={setCurrent}
      />
      <Player station={current} />
    </main>
  );
}

export default App;