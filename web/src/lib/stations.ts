import type { Station } from '../types';

const TINTS = ['#D7CDE8', '#F4D2B6', '#E6D2E0', '#F6DDC3', '#D0C8E4', '#F2CDBC'];

/** Two main tags of a station (the first two the catalogue lists). */
export function topTags(station: Station, count = 2): string[] {
  return station.tags.slice(0, count);
}

/** "Germany · music · variety": the second line of a list row. */
export function stationMeta(station: Station): string {
  return [station.country, ...topTags(station)].filter(Boolean).join(' · ');
}

/** "from Germany, Rheinland-Pfalz" (empty when the catalogue has no place). */
export function originLine(station: Station): string {
  const place = [station.country, station.state].filter(Boolean).join(', ');
  return place ? `from ${place}` : '';
}

/** "from Germany · music, variety": the compact line used on phones. */
export function compactLine(station: Station): string {
  const country = station.country ? `from ${station.country}` : '';
  return [country, topTags(station).join(', ')].filter(Boolean).join(' · ');
}

/** "MP3 · 128 kbps"; skips values the catalogue does not know. */
export function codecLabel(station: Station): string {
  const codec =
    station.codec && station.codec.toUpperCase() !== 'UNKNOWN' ? station.codec : '';
  const bitrate = station.bitrate > 0 ? `${station.bitrate} kbps` : '';
  return [codec, bitrate].filter(Boolean).join(' · ');
}

//station's website with http(s) address, a value like "javascript:..." mustn't become a link
 
export function websiteOf(station: Station): string {
  try {
    const url = new URL(station.homepage ?? '');
    return url.protocol === 'http:' || url.protocol === 'https:' ? url.href : '';
  } catch {
    return '';
  }
}

export function initialOf(station: Station): string {
  return station.name.trim().charAt(0).toUpperCase() || '#';
}

/** A stable pastel colour per station, so a row keeps its colour between renders. */
export function tintOf(station: Station): string {
  let sum = 0;
  for (const ch of station.stationuuid) sum += ch.charCodeAt(0);
  return TINTS[sum % TINTS.length];
}

/** Random sample without modifying the input (partial Fisher-Yates). */
export function sample<T>(items: T[], count: number): T[] {
  const copy = items.slice();
  const take = Math.min(count, copy.length);
  for (let i = 0; i < take; i++) {
    const j = i + Math.floor(Math.random() * (copy.length - i));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, take);
}
