import { describe, expect, it } from 'vitest';
import { makeStation } from '../test/makeStation';
import {
  codecLabel,
  compactLine,
  initialOf,
  originLine,
  sample,
  stationMeta,
  tintOf,
  topTags,
  websiteOf,
} from './stations';


describe('topTags', () => {
  it('returns first two tags by default', () => {
    const s = makeStation({ tags: ['rock', 'pop', 'jazz'] });
    expect(topTags(s)).toEqual(['rock', 'pop']);
  })

  it('returns fewer when the station has fewer tags', () => {
    expect(topTags(makeStation({ tags: ['rock'] }))).toEqual(['rock']);
  });
});

describe('codecLabel', () => {
  it('joins codec and bitrate', () => {
    expect(codecLabel(makeStation())).toBe('MP3 · 128 kbps');
  });

  it('skips an UNKNOWN codec', () => {
    expect(codecLabel(makeStation({ codec: 'UNKNOWN' }))).toBe('128 kbps');
  });

  it('skips 0 bitrate', () => {
    expect(codecLabel(makeStation({ bitrate: 0 }))).toBe('MP3');
  });
  
  it('skips 0 bitrate and UNKNOWN codec', () => {
    expect(codecLabel(makeStation({ bitrate: 0, codec: 'UNKNOWN' }))).toBe('');
  });

});

describe('stationMeta', () => {
  it('joins country and the two main tags', () => {
    const s = makeStation({ tags: ['rock', 'pop', 'jazz'] });
    expect(stationMeta(s)).toBe('Germany · rock · pop');
  });

  it('skips an empty country', () => {
    const s = makeStation({ country: '', tags: ['rock', 'pop'] });
    expect(stationMeta(s)).toBe('rock · pop');
  });

  it('shows only the country when there are no tags', () => {
    expect(stationMeta(makeStation({ tags: [] }))).toBe('Germany');
  });
});

describe('originLine', () => {
  it('shows country and state', () => {
    const s = makeStation({ country: 'Germany', state: 'Bavaria' });
    expect(originLine(s)).toBe('from Germany, Bavaria');
  });

  it('shows only the country when there is no state', () => {
    expect(originLine(makeStation({ state: '' }))).toBe('from Germany');
  });

  it('is empty when the catalogue has no place', () => {
    expect(originLine(makeStation({ country: '', state: '' }))).toBe('');
  });
});

describe('compactLine', () => {
  it('joins country and tags', () => {
    const s = makeStation({ tags: ['rock', 'pop', 'jazz'] });
    expect(compactLine(s)).toBe('from Germany · rock, pop');
  });

  it('shows only the country when there are no tags', () => {
    expect(compactLine(makeStation({ tags: [] }))).toBe('from Germany');
  });

  it('shows only the tags when there is no country', () => {
    const s = makeStation({ country: '', tags: ['rock', 'pop'] });
    expect(compactLine(s)).toBe('rock, pop');
  });
});

describe('initialOf', () => {
  it('upper-cases the first letter', () => {
    expect(initialOf(makeStation({ name: 'radio one' }))).toBe('R');
  });

  it('ignores spaces at the start', () => {
    expect(initialOf(makeStation({ name: '   jazz fm' }))).toBe('J');
  });

  it('gives # for an empty or blank name', () => {
    expect(initialOf(makeStation({ name: '' }))).toBe('#');
    expect(initialOf(makeStation({ name: '   ' }))).toBe('#');
  });
});

describe('tintOf', () => {
  it('always gives the same colour for the same station', () => {
    const s = makeStation({ stationuuid: 'same-id' });
    expect(tintOf(s)).toBe(tintOf(s));
  });

  it('gives a hex colour', () => {
    expect(tintOf(makeStation())).toMatch(/^#[0-9A-F]{6}$/i);
  });
});

describe('sample', () => {
  const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  it('returns the requested number of items', () => {
    expect(sample(numbers, 3)).toHaveLength(3);
  });

  it('returns everything when asked for more than exists', () => {
    expect(sample(numbers, 50)).toHaveLength(10);
  });

  it('returns only items from the input', () => {
    for (const item of sample(numbers, 5)) {
      expect(numbers).toContain(item);
    }
  });

  it('has no duplicates', () => {
    const result = sample(numbers, 10);
    expect(new Set(result).size).toBe(result.length);
  });

  it('does not change the original array', () => {
    const original = [...numbers];
    sample(numbers, 5);
    expect(numbers).toEqual(original);
  });
});

//tests for link
describe('websiteOf', () => {
  it('returns a normal website address', () => {
    expect(websiteOf(makeStation({ homepage: 'https://example.com/radio' }))).toBe(
      'https://example.com/radio',
    );
  });

  it('accepts plain http too', () => {
    expect(websiteOf(makeStation({ homepage: 'http://example.com/' }))).toBe('http://example.com/');
  });

  it('adds the trailing slash to a bare domain', () => {
    expect(websiteOf(makeStation({ homepage: 'https://example.com' }))).toBe('https://example.com/');
  });

  it('is empty when the station has no website', () => {
    expect(websiteOf(makeStation({ homepage: '' }))).toBe('');
    expect(websiteOf(makeStation())).toBe('');
  });

  it('rejects addresses that are not http or https', () => {
    expect(websiteOf(makeStation({ homepage: 'javascript:alert(1)' }))).toBe('');
    expect(websiteOf(makeStation({ homepage: 'ftp://example.com/file' }))).toBe('');
    expect(websiteOf(makeStation({ homepage: 'data:text/html,<b>hi</b>' }))).toBe('');
  });

  it('rejects text that is not an address', () => {
    expect(websiteOf(makeStation({ homepage: 'not a url' }))).toBe('');
  });
});