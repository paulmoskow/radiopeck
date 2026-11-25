import { useEffect, useRef, useState } from 'react';
import type { CSSProperties } from 'react';
import type { Station } from '../types';
import Bird from './Bird';
import StationLogo from './StationLogo';
import { codecLabel, compactLine, originLine, topTags, websiteOf } from '../lib/stations';
import Hls from 'hls.js';

//Safari plays HLS natively; Chrome and Firefox need hls.js (Media Source Extensions)
const NATIVE_HLS =
  typeof document !== 'undefined' &&
  document.createElement('audio').canPlayType('application/vnd.apple.mpegurl') !== '';
const HLS_JS = Hls.isSupported();

// Formats no browser can play.
const UNPLAYABLE_CODECS = ['FLV'];

type PlayerProps = {
  station: Station | null;
};

//Volume kept despite the change of station. PlayerBody is re-created for every station (key), with its "playing" and "error" state and fresh <audio> element
export default function Player({ station }: PlayerProps) {
  const [volume, setVolume] = useState(70);

  return (
    <PlayerBody
      key={station?.stationuuid ?? 'none'}
      station={station}
      volume={volume}
      onVolumeChange={setVolume}
    />
  );
}

type PlayerBodyProps = {
  station: Station | null;
  volume: number;
  onVolumeChange: (value: number) => void;
};

function PlayerBody({ station, volume, onVolumeChange }: PlayerBodyProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const hlsRef = useRef<Hls | null>(null);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (audioRef.current) audioRef.current.volume = volume / 100;
  }, [volume]);

const unsupported = station
    ? UNPLAYABLE_CODECS.includes((station.codec ?? '').toUpperCase()) ||
      (station.hls && !NATIVE_HLS && !HLS_JS)
    : false;
  const message = unsupported ? 'This stream format is not supported' : error;

  // Lock screen / notification controls: show the station and a proper cover image.
  useEffect(() => {
    if (!station || !('mediaSession' in navigator)) return;
    const session = navigator.mediaSession;
    session.metadata = new MediaMetadata({
      title: station.name,
      artist: station.country || 'RadioPeck',
      album: 'RadioPeck',
      artwork: [
        { src: `${import.meta.env.BASE_URL}icon-512.png`, sizes: '512x512', type: 'image/png' },
      ],
    });
    session.setActionHandler('play', () => audioRef.current?.play());
    session.setActionHandler('pause', () => audioRef.current?.pause());
    return () => {
      session.setActionHandler('play', null);
      session.setActionHandler('pause', null);
    };
  }, [station]);
  

  // HLS: attach the stream to the <audio> element. Plain streams use the src attribute.
  useEffect(() => {
    const audio = audioRef.current;
    if (!station || !station.hls || unsupported || !audio) return;

    if (NATIVE_HLS) {
      audio.src = station.url_resolved;
      return;
    }

    const hls = new Hls();
    hlsRef.current = hls;
    hls.on(Hls.Events.ERROR, (_event, data) => {
      if (data.fatal) setError('Stream is unavailable');
    });
    hls.loadSource(station.url_resolved);
    hls.attachMedia(audio);

    return () => {
      hls.destroy();
      hlsRef.current = null;
    };
  }, [station, unsupported]);

  function toggle() {
    const audio = audioRef.current;
    if (!audio) return;

    if (audio.paused) {
      setError(null);
      // A live stream has no buffer to resume: jump to "now".
      if (hlsRef.current) {
        const live = hlsRef.current.liveSyncPosition;
        if (live) audio.currentTime = live;
      } else {
        audio.load();
      }
      audio.play().catch(() => setError('Could not start playback'));
    } else {
      audio.pause();
    }
  }

  const tags = station ? topTags(station) : [];
  const codec = station ? codecLabel(station) : '';
  const origin = station ? originLine(station) : '';
  const compact = station ? compactLine(station) : '';
  const website = station ? websiteOf(station) : '';

  return (
    <section className={playing ? 'player is-playing' : 'player'} aria-label="Player">
      <h1 className="brand brand--player">RadioPeck</h1>

      <div className="stage">
        <div className="ring ring--a" aria-hidden="true" />
        <div className="ring ring--b" aria-hidden="true" />
        <button
          type="button"
          className="play"
          onClick={toggle}
          disabled={!station || unsupported}
          aria-label={playing ? 'Pause' : 'Play'}
        >
          {playing ? (
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <rect x="6" y="5" width="4.2" height="14" rx="1.6" fill="#3A3148" />
              <rect x="13.8" y="5" width="4.2" height="14" rx="1.6" fill="#3A3148" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"
                fill="#3A3148"
                stroke="#3A3148"
                strokeWidth="2"
                strokeLinejoin="round"
              />
            </svg>
          )}
        </button>
        <Bird className="bird" />
      </div>

      <div className="meta">
        <h2 className="station-name">{station ? station.name : 'Pick a station'}</h2>
      </div>

      {station && (
        <div className="identity">
          <StationLogo station={station} />
          <div className="identity__text">
             {(origin || compact || website) && (
              <div className="lead-row">
                {origin && <p className="lead lead--desktop">{origin}</p>}
                {compact && <p className="lead lead--mobile">{compact}</p>}
                {website && (
                  <a
                    className="station-link"
                    href={website}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`Website of ${station?.name ?? 'the station'} (opens in a new tab)`}
                  >
                    Link
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                      <path d="M7 17L17 7M9 7h8v8" />
                    </svg>
                  </a>
                )}
              </div>
            )}
            {codec && <p className="lead codec-line">{codec}</p>}
            {(tags.length > 0 || codec) && (
              <div className="chips">
                {tags.map(t => (
                  <span key={t} className="chip">
                    {t}
                  </span>
                ))}
                {codec && <span className="chip chip--quiet">{codec}</span>}
              </div>
            )}
          </div>
        </div>
      )}

      {message && (
        <p className="player__error" role="alert">
          {message}
        </p>
      )}

      <div className="volume">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#4A3F5F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M4 9v6h4l5 4V5L8 9H4z" />
        </svg>
        <label htmlFor="volume" className="sr-only">
          Volume
        </label>
        <input
          id="volume"
          className="volume__range"
          type="range"
          min={0}
          max={100}
          value={volume}
          onChange={e => onVolumeChange(Number(e.target.value))}
          style={{ '--vol': `${volume}%` } as CSSProperties}
        />
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#4A3F5F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M4 9v6h4l5 4V5L8 9H4z" />
          <path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" />
        </svg>
      </div>

      {station && !unsupported && (
        <audio
          ref={audioRef}
          src={station.hls ? undefined : station.url_resolved}
          autoPlay
          onPlay={() => setPlaying(true)}
          onPause={() => setPlaying(false)}
          onError={() => setError('Stream is unavailable')}
        />
      )}
    </section>
  );
}
