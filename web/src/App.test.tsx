import { fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { makeStation } from './test/makeStation';

// The hook is replaced: each test decides what the "catalogue" is.
const hook = vi.hoisted(() => ({
  value: { stations: [] as unknown[], loading: false, error: null as string | null },
}));
vi.mock('./hooks/useStations', () => ({ default: () => hook.value }));

const jazzFr = makeStation({ stationuuid: '1', name: 'Jazz FM', country: 'France', tags: ['jazz'] });
const rockDe = makeStation({ stationuuid: '2', name: 'Rock Radio', country: 'Germany', tags: ['rock'] });
const jazzDe = makeStation({ stationuuid: '3', name: 'Berlin Jazz', country: 'Germany', tags: ['jazz'] });

beforeEach(() => {
  // History lives in localStorage and would leak from one test into the next.
  localStorage.clear();
  hook.value = { stations: [jazzFr, rockDe, jazzDe], loading: false, error: null };
});

/** Selects a station and fires the "play" event (jsdom never plays audio by itself). */
async function playStation(name: RegExp) {
  await userEvent.click(screen.getByRole('button', { name }));
  fireEvent.play(document.querySelector('audio')!);
}

const openRecent = () => userEvent.click(screen.getByRole('button', { name: 'Recently played' }));

describe('App', () => {
  it('shows stations from the catalogue before the user searches', () => {
    render(<App />);
    expect(screen.getByText('Jazz FM')).toBeInTheDocument();
    expect(screen.getByText('Rock Radio')).toBeInTheDocument();
    expect(screen.getByText('Listen right now')).toBeInTheDocument();
  });

  it('filters the list by name as the user types', async () => {
    render(<App />);

    await userEvent.type(screen.getByLabelText('Search stations'), 'jazz');

    expect(screen.getByText('Jazz FM')).toBeInTheDocument();
    expect(screen.getByText('Berlin Jazz')).toBeInTheDocument();
    expect(screen.queryByText('Rock Radio')).not.toBeInTheDocument();
    expect(screen.getByText('2 found')).toBeInTheDocument();
  });

  it('shows the selected station in the player', async () => {
    render(<App />);
    expect(screen.getByRole('heading', { level: 2, name: 'Pick a station' })).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: /Rock Radio/ }));

    expect(screen.getByRole('heading', { level: 2, name: 'Rock Radio' })).toBeInTheDocument();
  });

  it('filters the list by country', async () => {
    render(<App />);

    await userEvent.selectOptions(screen.getByLabelText('Country'), 'France');

    expect(screen.getByText('Jazz FM')).toBeInTheDocument();
    expect(screen.queryByText('Rock Radio')).not.toBeInTheDocument();
    expect(screen.queryByText('Berlin Jazz')).not.toBeInTheDocument();
    expect(screen.getByText('1 found')).toBeInTheDocument();
  });

  it('combines the name and country filters', async () => {
    render(<App />);

    await userEvent.type(screen.getByLabelText('Search stations'), 'jazz');
    await userEvent.selectOptions(screen.getByLabelText('Country'), 'Germany');

    expect(screen.getByText('Berlin Jazz')).toBeInTheDocument();
    expect(screen.queryByText('Jazz FM')).not.toBeInTheDocument();
    expect(screen.queryByText('Rock Radio')).not.toBeInTheDocument();
    expect(screen.getByText('1 found')).toBeInTheDocument();
  });

  it('shows "No stations found" when nothing matches the search', async () => {
    render(<App />);

    await userEvent.type(screen.getByLabelText('Search stations'), 'zzz');

    expect(screen.getByText('No stations found')).toBeInTheDocument();
    expect(screen.getByText('0 found')).toBeInTheDocument();
  });

  it('shows a loading message while the catalogue loads', () => {
    hook.value = { stations: [], loading: true, error: null };
    render(<App />);
    expect(screen.getByText('Loading…')).toBeInTheDocument();
  });

  it('shows the error when the catalogue fails to load', () => {
    hook.value = { stations: [], loading: false, error: 'Failed to load stations' };
    render(<App />);
    expect(screen.getByRole('alert')).toHaveTextContent('Failed to load stations');
  });
});

describe('App: recently played', () => {
  it('shows a hint when nothing has been played yet', async () => {
    render(<App />);

    await openRecent();

    expect(screen.getByText('Stations you listen to will appear here')).toBeInTheDocument();
  });

  it('lists a station after it started playing', async () => {
    render(<App />);
    await playStation(/Jazz FM/);

    await openRecent();

    const list = screen.getByRole('list');
    expect(within(list).getByText('Jazz FM')).toBeInTheDocument();
    expect(within(list).queryByText('Rock Radio')).not.toBeInTheDocument();
  });

  it('does not list a station that was selected but never started', async () => {
    render(<App />);
    await userEvent.click(screen.getByRole('button', { name: /Rock Radio/ }));

    await openRecent();

    expect(screen.getByText('Stations you listen to will appear here')).toBeInTheDocument();
  });

  it('puts the latest station first and keeps no duplicates', async () => {
    render(<App />);
    await playStation(/Jazz FM/);
    await playStation(/Rock Radio/);
    await playStation(/Jazz FM/);

    await openRecent();

    const cards = within(screen.getByRole('list')).getAllByRole('button');
    expect(cards).toHaveLength(2);
    expect(cards[0]).toHaveTextContent('Jazz FM');
    expect(cards[1]).toHaveTextContent('Rock Radio');
  });

  it('clears the search when switching to "Recently played"', async () => {
    render(<App />);
    await playStation(/Jazz FM/);
    await userEvent.type(screen.getByLabelText('Search stations'), 'rock');

    await openRecent();

    expect(screen.getByLabelText('Search stations')).toHaveValue('');
    expect(within(screen.getByRole('list')).getByText('Jazz FM')).toBeInTheDocument();
  });

  it('returns to the usual list when the clock is clicked again', async () => {
    render(<App />);
    await playStation(/Jazz FM/);

    await openRecent();
    expect(screen.getByText('Recently played')).toBeInTheDocument();

    await openRecent();
    expect(screen.getByText('Listen right now')).toBeInTheDocument();
  });

  it('keeps the history after the app is opened again', async () => {
    const first = render(<App />);
    await playStation(/Jazz FM/);
    first.unmount();

    render(<App />);
    await openRecent();

    expect(within(screen.getByRole('list')).getByText('Jazz FM')).toBeInTheDocument();
  });
});