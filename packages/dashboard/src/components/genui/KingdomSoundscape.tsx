"use client";

import { useRef, forwardRef, useImperativeHandle } from "react";

export interface KingdomSoundscapeRef {
  playBell: () => void;
  playHum: () => void;
  stopAll: () => void;
}

const KingdomSoundscape = forwardRef<KingdomSoundscapeRef, Record<string, never>>((props, ref) => {
  const bellRef = useRef<HTMLAudioElement | null>(null);
  const humRef = useRef<HTMLAudioElement | null>(null);

  useImperativeHandle(ref, () => ({
    playBell: () => {
      if (bellRef.current) {
        bellRef.current.currentTime = 0;
        bellRef.current.play().catch(e => console.log("Audio play blocked (user interaction needed first):", e));
      }
    },
    playHum: () => {
      if (humRef.current) {
        humRef.current.volume = 0.3;
        humRef.current.play().catch(e => console.log("Audio play blocked:", e));
      }
    },
    stopAll: () => {
      if (humRef.current) {
        humRef.current.pause();
        humRef.current.currentTime = 0;
      }
      if (bellRef.current) {
        bellRef.current.pause();
        bellRef.current.currentTime = 0;
      }
    }
  }));

  return (
    <div className="hidden">
      {/* 
        Ideally, these would be real asset files. 
        For now, we can use online free-to-use samples or placeholders.
        I will use data URIs for simple synthesized sounds to ensure they work without external deps 
        if I can generate them, but for high quality I'll point to assumptions or public URLs.
        
        Since I cannot download files, I will use a reliable CDN or assume local files are placed.
        However, to ensure it works "out of the box" for the user demo, 
        I'll try to use standard placeholder URLs, but ideally the user should provide assets.
        
        Wait, I can use the 'sounds' directory found earlier: packages/dashboard/public/sounds
        Let's assume we need to create/place files there. 
        Actually, for now, I will use a simple synth approach if possible or just placeholders.
        
        Let's use a reliable public domain sound for the "Bell" and "Hum".
      */}
      <audio ref={bellRef} src="https://cdn.freesound.org/previews/337/337049_3232293-lq.mp3" preload="auto" /> 
      {/* Above is a placeholder for a clear bell-like sound */}
      
      <audio ref={humRef} src="https://cdn.freesound.org/previews/145/145656_2437292-lq.mp3" loop preload="auto" />
      {/* Above is a placeholder for a low drone/hum */}
    </div>
  );
});

KingdomSoundscape.displayName = "KingdomSoundscape";

export default KingdomSoundscape;
