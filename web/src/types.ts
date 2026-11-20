export type Station = {
  name: string;
  stationuuid: string;
  url_resolved: string;
  homepage: string;
  favicon: string;
  tags: string[];
  country: string;
  countrycode: string;
  state: string;
  language: string[];
  codec: string;
  bitrate: number;
  hls: boolean;
  votes: number;
  clickcount: number;
  geo_lat: number | null;
  geo_long: number | null;
};
