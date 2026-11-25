import type { Station } from '../types';
import useLocalStorage from './useLocalStorage';

const KEY = 'radiopeck:recent:v1';
const MAX_RECENT = 20;

export function pushRecent(list: Station[], station: Station, max = MAX_RECENT): Station[] {
  const others = list.filter(s => s.stationuuid !== station.stationuuid);
  return [station, ...others].slice(0, max);
}

export default function useRecent() {
  const [recent, setRecent] = useLocalStorage<Station[]>(KEY, []);

  function addRecent(station: Station) {
    setRecent(prev => pushRecent(prev, station));
  }

  return { recent, addRecent };
}