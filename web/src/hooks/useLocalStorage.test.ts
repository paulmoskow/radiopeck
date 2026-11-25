import { act, renderHook } from '@testing-library/react';
import useLocalStorage from './useLocalStorage';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

afterEach(() => vi.restoreAllMocks());

beforeEach(() => localStorage.clear());

describe('useLocalStorage', () => {
  it('returns the initial value when nothing is stored', () => {
    const { result } = renderHook(() => useLocalStorage('k', 5));
    expect(result.current[0]).toBe(5);
  });

  it('reads a stored value', () => {
    localStorage.setItem('k', JSON.stringify([1, 2]));
    const { result } = renderHook(() => useLocalStorage('k', 5));
    expect(result.current[0]).toEqual([1,2]);
  });

  it('saves a changed value', () => {
    const { result } = renderHook(() => useLocalStorage('k', 5));

    act(() => result.current[1](10));
    expect(result.current[0]).toBe(10);
    expect(localStorage.getItem('k')).toBe('10');

  });

  it('falls back to the initial value when the stored JSON is broken', () => {
    localStorage.setItem('k', '{not json');

    const { result } = renderHook(() => useLocalStorage('k', 5));

    expect(result.current[0]).toBe(5);
  });

  it('keeps working when localStorage throws', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('blocked');
    });

    const { result } = renderHook(() => useLocalStorage('k', 5));

    expect(result.current[0]).toBe(5);
  });

})