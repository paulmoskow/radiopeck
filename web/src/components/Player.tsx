import { useRef, useState } from 'react';
import type { Station } from '../types';

type PlayerProps = {
  station: Station | null;
};

function Player({ station }: PlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!station) {
    return <div className="player">Select a station</div>;
  }

  // skip HLS streams (need hls.js in Chrome/Firefox)
  const unsupported = station.hls;

  function toggle() {
    const audio = audioRef.current;
    if (!audio) return;

    if (audio.paused) {
      audio.load();
      audio.play().catch(() => setError('Could not start playback'));
    } else {
      audio.pause();
    }
  }

  return (
    <div className="player">
      <div className="player__info">
        <strong>{station.name}</strong>
        <span>{station.country}</span>
      </div>

      {unsupported ? (
        <span className="player__error">
          This stream format is not supported yet
        </span>
      ) : (
        <>
          <button className="player__button" onClick={toggle}>
            {playing ? 'Pause' : 'Play'}
          </button>
          {error && <span className="player__error">{error}</span>}
          <audio
            ref={audioRef}
            src={station.url_resolved}
            autoPlay
            onPlay={() => setPlaying(true)}
            onPause={() => setPlaying(false)}
            onError={() => setError('Stream is unavailable')}
          />
        </>
      )}
    </div>
  );
}

export default Player;