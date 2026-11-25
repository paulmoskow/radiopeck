import { render, screen } from '@testing-library/react';
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
  hook.value = { stations: [jazzFr, rockDe, jazzDe], loading: false, error: null };
});

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
