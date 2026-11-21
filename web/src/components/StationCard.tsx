import type { Station } from '../types';
import { initialOf, stationMeta, tintOf } from '../lib/stations';

type StationCardProps = {
  station: Station;
  selected: boolean;
  onSelect: () => void;
};

export default function StationCard({ station, selected, onSelect }: StationCardProps) {
  const meta = stationMeta(station);

  return (
    <button
      type="button"
      className={selected ? 'card card--selected' : 'card'}
      onClick={onSelect}
      aria-pressed={selected}
    >
      <span className="card__avatar" style={{ background: tintOf(station) }} aria-hidden="true">
        {initialOf(station)}
      </span>
      <span className="card__text">
        <span className="card__name">{station.name}</span>
        {meta && <span className="card__meta">{meta}</span>}
      </span>
      {selected && (
        <svg className="card__now" width="26" height="26" viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="12" cy="12" r="12" fill="#E6B79C" />
          <path
            d="M9.5 7.8v8.4a.7.7 0 0 0 1.05.6l6.6-4.2a.7.7 0 0 0 0-1.2l-6.6-4.2a.7.7 0 0 0-1.05.6z"
            fill="#3A3148"
          />
        </svg>
      )}
    </button>
  );
}
