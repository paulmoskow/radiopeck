import { describe, expect, it } from 'vitest';
import { makeStation } from '../test/makeStation';
import { pushRecent } from './useRecent';

const a = makeStation({ stationuuid: 'a', name: 'A' });
const b = makeStation({ stationuuid: 'b', name: 'B' });
const c = makeStation({ stationuuid: 'c', name: 'C' });

describe('pushRecent', () => {
  it('puts a new station first', () => {
    expect(pushRecent([a], b)).toEqual([b, a]);
  });

    it('moves a station that is already in the list to the front, without a duplicate', () => {
    expect(pushRecent([a, b, c], b)).toEqual([b, a, c]);
  });

  it('cuts the list to max items, dropping the oldest', () => {
    expect(pushRecent([a, b], c, 2)).toEqual([c, a]);
  });

  it('does not change the original array', () => {
    const list = [a, b];
    const copy = [...list];

    pushRecent(list, c);

    expect(list).toEqual(copy);
  });
});