import { useState } from 'react';
import type { Station } from '../types';
import { initialOf, tintOf } from '../lib/stations';

type StationLogoProps = {
  station: Station;
};

//The station's  favicon or a pastel square with the first letter instead of a broken image

export default function StationLogo({ station }: StationLogoProps) {
  const [failed, setFailed] = useState(false);

  if (!station.favicon || failed) {
    return (
      <span
        className="logo logo--fallback"
        style={{ background: tintOf(station) }}
        aria-hidden="true"
      >
        {initialOf(station)}
      </span>
    );
  }

  return (
    <img
      className="logo"
      src={station.favicon}
      alt=""
      loading="lazy"
      referrerPolicy="no-referrer"
      onError={() => setFailed(true)}
    />
  );
}
