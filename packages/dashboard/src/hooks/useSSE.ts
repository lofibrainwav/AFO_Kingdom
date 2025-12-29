'use client';
import { useEffect, useState } from 'react';

export default function useSSE(url: string) {
  const [data, setData] = useState<any>(null);
  
  useEffect(() => {
    const eventSource = new EventSource(url);
    eventSource.onmessage = (event) => {
       try {
         const parsed = JSON.parse(event.data);
         setData(parsed);
       } catch (e) {
         console.error('SSE Parse Error', e);
       }
    };
    eventSource.onerror = (e) => {
        // Optional: Handle error or reconnection logic if needed
        // For minimal PR, we just log. Browser handles reconnection often.
        console.warn('SSE Error', e);
    };
    return () => eventSource.close();
  }, [url]);

  return { data };
}
