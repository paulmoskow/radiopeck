import { useMemo, useState } from 'react';
import useStations from './hooks/useStations';
import SearchPanel from './components/SearchPanel';
import Player from './components/Player';
import { sample } from './lib/stations';
import type { ListMode, Station } from './types';
import useRecent from './hooks/useRecent';

const PAGE_SIZE = 50;

function App() {
  const { stations, loading, error } = useStations();
  const { recent, addRecent } = useRecent();
  const [query, setQuery] = useState('');
  const [country, setCountry] = useState('');
  const [current, setCurrent] = useState<Station | null>(null);
  const [mode, setMode] = useState<ListMode>('discover');

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

  // Recent stations are saved in the browser as snapshots
  const recentList = useMemo(() => {
    const byId = new Map(stations.map(s => [s.stationuuid, s]));
    return recent.map(s => byId.get(s.stationuuid) ?? s);
  }, [stations, recent]);

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

  function changeMode(next: ListMode) {
    setMode(next);
    if (next === 'recent') {
      setQuery('');
      setCountry('');
    }
  };

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

  const shown = searching ? matches.slice(0, PAGE_SIZE) : mode === 'recent' ? recentList : discover;

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
        mode={mode}
        onModeChange={changeMode}
      />
      <Player station={current} onPlayStart={addRecent} />
    </main>
  );
}

export default App;