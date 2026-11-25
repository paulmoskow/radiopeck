import { useEffect, useState } from 'react';

export default function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const saved = localStorage.getItem(key);
      return saved === null ? initial : (JSON.parse(saved) as T);
    }
    catch {
      return initial;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    }
    catch {
      // Storage can be full or blocked (private mode): the app still works, it just forgets
    }
  }, [key, value]);

  return [value, setValue] as const;
}