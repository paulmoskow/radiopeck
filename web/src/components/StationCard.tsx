import type { Station } from '../types';

type StationProps = {
  station: Station;
  selected: boolean;
  onSelect: () => void
};

function StationCard({ station, selected, onSelect }: StationProps) {
  return (
    <div 
      onClick={onSelect}
      className={ selected ? 'station-card station-card--selected' : 'station-card'}
    >
      <h2>{station.name}</h2>
      <p>{station.country}</p>
      <p>{station.tags.join(', ')}</p>
    </div>
  );
}

export default StationCard