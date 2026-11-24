import type { Station } from '../types';

/** A station with sensible defaults; each test overrides only what it cares about. */
export function makeStation(overrides: Partial<Station> = {}): Station {
  return {
    stationuuid: 'abc-123',
    name: 'Test FM',
    country: 'Germany',
    state: '',
    tags: [],
    codec: 'MP3',
    bitrate: 128,
    hls: false,
    ...overrides,
  } as Station;
}