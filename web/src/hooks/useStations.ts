  import { useState, useEffect } from 'react';
  import type { Station } from '../types';
  
  function useStations () {
    const [stations, setStations] = useState<Station[]>([]); 
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState< string | null>(null); 

    useEffect(() => {
      async function load() {
        try {
          const res = await fetch(import.meta.env.BASE_URL + 'data/stations.json');
          if (!res.ok) throw new Error('error fetching stations');
          const data: Station[] = await res.json();

          setStations(data);
        }
        catch (e) {
          setError(e instanceof Error ? e.message : String(e));
        }
        finally {
          setLoading(false);
        }
      }
      load()
    }, []); 

    return { stations, loading, error }
  }
  
  export default useStations