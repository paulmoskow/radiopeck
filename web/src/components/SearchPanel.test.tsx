import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import SearchPanel from './SearchPanel';
import { makeStation } from '../test/makeStation';

type Props = Parameters<typeof SearchPanel>[0];

/** Renders the panel with defaults; a test overrides only what it checks. */
function renderPanel(overrides: Partial<Props> = {}) {
  const props: Props = {
    totalCount: 2,
    query: '',
    onQueryChange: vi.fn(),
    country: '',
    onCountryChange: vi.fn(),
    countries: ['France', 'Germany'],
    searching: false,
    foundCount: 0,
    stations: [],
    currentId: null,
    onSelect: vi.fn(),
    ...overrides,
  };
  render(<SearchPanel {...props} />);
  return props;
}

describe('SearchPanel', () => {
  it('lists the stations it is given', () => {
    renderPanel({
      stations: [
        makeStation({ stationuuid: '1', name: 'Alpha FM' }),
        makeStation({ stationuuid: '2', name: 'Beta FM' }),
      ],
    });
    expect(screen.getByText('Alpha FM')).toBeInTheDocument();
    expect(screen.getByText('Beta FM')).toBeInTheDocument();
  });

  it('calls onSelect with the station that was clicked', async () => {
    const alpha = makeStation({ stationuuid: '1', name: 'Alpha FM' });
    const { onSelect } = renderPanel({ stations: [alpha] });

    await userEvent.click(screen.getByRole('button', { name: /Alpha FM/ }));

    expect(onSelect).toHaveBeenCalledWith(alpha);
  });

  // TODO: an empty list shows "No stations found"
  it('shows "No stations found" for an empty list', () => {
    renderPanel({ stations: [] });
    expect(screen.getByText('No stations found')).toBeInTheDocument();
  });

  // TODO: the selected station (currentId) has aria-pressed="true", the other does not
  it('selected station has aria-pressed="true", the other does not', () => {
    renderPanel({ 
      stations: [
        makeStation({ stationuuid: '1', name: 'Alpha FM' }),
        makeStation({ stationuuid: '2', name: 'Beta FM' }),
      ],
      currentId: '1',
    });

    const selectedButton = screen.getByRole('button', { name: /alpha fm/i });
    const otherButton = screen.getByRole('button', { name: /beta fm/i });

    expect(selectedButton).toHaveAttribute('aria-pressed', 'true');
    expect(otherButton).toHaveAttribute('aria-pressed', 'false');
  });
  
   it('says "Listen right now" when not searching', () => {
    renderPanel({ searching: false });
    expect(screen.getByText('Listen right now')).toBeInTheDocument();
  });

  it('shows how many stations were found when searching', () => {
    renderPanel({ searching: true, foundCount: 2 });
    expect(screen.getByText('2 found')).toBeInTheDocument();
    expect(screen.queryByText('Listen right now')).not.toBeInTheDocument();
  });

  it('calls onQueryChange when the user types in the search field', async () => {
    const { onQueryChange } = renderPanel();

    await userEvent.type(screen.getByLabelText('Search stations'), 'j');

    expect(onQueryChange).toHaveBeenCalledWith('j');
  });

  it('calls onCountryChange with the chosen country', async () => {
    const { onCountryChange } = renderPanel();

    await userEvent.selectOptions(screen.getByLabelText('Country'), 'Germany');

    expect(onCountryChange).toHaveBeenCalledWith('Germany');
  });
  
});
