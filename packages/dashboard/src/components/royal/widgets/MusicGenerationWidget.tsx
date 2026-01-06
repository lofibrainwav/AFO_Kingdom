"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useState, useRef, useCallback } from "react";
import { Play, Pause, Download, Music, Volume2, VolumeX } from "lucide-react";

interface TimelineSection {
  start: number;
  end: number;
  text: string;
  music_directive: string;
}

interface TimelineState {
  title: string;
  sections: TimelineSection[];
  music?: {
    style: string;
    mood: string;
    tempo: string;
  };
}

interface MusicGenerationWidgetProps {
  className?: string;
}

export function MusicGenerationWidget({ className = "" }: MusicGenerationWidgetProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedMusic, setGeneratedMusic] = useState<{
    url: string;
    duration: number;
    title: string;
  } | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [volume, setVolume] = useState(0.7);
  const [isMuted, setIsMuted] = useState(false);

  const audioRef = useRef<HTMLAudioElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  // 샘플 TimelineState (실제로는 props나 state에서 받아옴)
  const sampleTimeline: TimelineState = {
    title: "AFO Kingdom Victory Theme",
    sections: [
      { start: 0, end: 10, text: "Epic orchestral introduction", music_directive: "slow_heroic_build" },
      { start: 10, end: 20, text: "Intense battle climax", music_directive: "powerful_orchestral_climax" },
      { start: 20, end: 30, text: "Triumphant victory fanfare", music_directive: "triumphant_brass_fanfare" }
    ],
    music: {
      style: "epic_orchestral_cinematic",
      mood: "heroic_triumphant",
      tempo: "dramatic"
    }
  };

  const generateMusic = useCallback(async () => {
    if (isGenerating) return;

    setIsGenerating(true);
    try {
      // 실제로는 FastAPI 백엔드 호출
      const response = await fetch('/api/music/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          timeline_state: sampleTimeline,
          provider: 'mlx_musicgen',
          quality: 'high'
        })
      });

      if (!response.ok) {
        throw new Error(`Music generation failed: ${response.status}`);
      }

      const result = await response.json();

      if (result.success && result.audio_path) {
        // 백엔드에서 생성된 오디오 파일 URL 반환
        const audioUrl = `/api/audio/${result.audio_path}`;
        setGeneratedMusic({
          url: audioUrl,
          duration: result.duration || 30,
          title: sampleTimeline.title
        });
      } else {
        throw new Error(result.error || 'Unknown error occurred');
      }
    } catch (error) {
      console.error('Music generation error:', error);
      alert(`음악 생성 실패: ${error instanceof Error ? error.message : '알 수 없는 오류'}`);
    } finally {
      setIsGenerating(false);
    }
  }, [isGenerating, sampleTimeline]);

  const togglePlay = useCallback(() => {
    if (!audioRef.current || !generatedMusic) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  }, [isPlaying, generatedMusic]);

  const handleTimeUpdate = useCallback(() => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  }, []);

  const handleProgressClick = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    if (!audioRef.current || !progressRef.current) return;

    const rect = progressRef.current.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const progressWidth = rect.width;
    const newTime = (clickX / progressWidth) * (generatedMusic?.duration || 30);

    audioRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  }, [generatedMusic?.duration]);

  const handleVolumeChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(event.target.value);
    setVolume(newVolume);
    if (audioRef.current) {
      audioRef.current.volume = newVolume;
    }
    setIsMuted(newVolume === 0);
  }, []);

  const toggleMute = useCallback(() => {
    if (!audioRef.current) return;

    const newMuted = !isMuted;
    setIsMuted(newMuted);
    audioRef.current.volume = newMuted ? 0 : volume;
  }, [isMuted, volume]);

  const downloadMusic = useCallback(async () => {
    if (!generatedMusic) return;

    try {
      const response = await fetch(generatedMusic.url);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${generatedMusic.title.replace(/[^a-zA-Z0-9]/g, '_')}.wav`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
      alert('다운로드 실패');
    }
  }, [generatedMusic]);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 p-6 shadow-inner ${className}`}
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
          <Music className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-700">🎵 음악 생성 (Music Generation)</h3>
          <p className="text-sm text-slate-500">TimelineState → MLX MusicGen 자동 변환</p>
        </div>
      </div>

      {/* Timeline Preview */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-slate-600 mb-3">📋 현재 TimelineState</h4>
        <div className="bg-white/5 rounded-lg p-4 border border-white/10">
          <div className="text-sm font-medium text-slate-700 mb-2">{sampleTimeline.title}</div>
          <div className="space-y-1">
            {sampleTimeline.sections.map((section, index) => (
              <div key={index} className="text-xs text-slate-500 flex items-center gap-2">
                <span className="bg-slate-200 px-2 py-0.5 rounded text-slate-600 font-mono">
                  {section.start}-{section.end}s
                </span>
                <span>{section.music_directive}: {section.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Generate Button */}
      <div className="mb-6">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={generateMusic}
          disabled={isGenerating}
          className={`w-full py-3 px-4 rounded-xl font-semibold transition-all ${
            isGenerating
              ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600 shadow-lg hover:shadow-xl'
          }`}
        >
          {isGenerating ? (
            <div className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-slate-500 border-t-transparent rounded-full animate-spin" />
              🎵 음악 생성 중...
            </div>
          ) : (
            '🎵 MLX MusicGen으로 음악 생성'
          )}
        </motion.button>
      </div>

      {/* Audio Player */}
      <AnimatePresence>
        {generatedMusic && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-white/20 pt-6"
          >
            <audio
              ref={audioRef}
              src={generatedMusic.url}
              onTimeUpdate={handleTimeUpdate}
              onEnded={() => setIsPlaying(false)}
              preload="metadata"
            />

            <div className="space-y-4">
              {/* Title */}
              <div className="text-center">
                <h4 className="text-lg font-semibold text-slate-700">{generatedMusic.title}</h4>
                <p className="text-sm text-slate-500">MLX MusicGen 생성 • {formatTime(generatedMusic.duration)}</p>
              </div>

              {/* Progress Bar */}
              <div
                ref={progressRef}
                onClick={handleProgressClick}
                className="w-full h-2 bg-slate-200 rounded-full cursor-pointer overflow-hidden"
              >
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-100"
                  style={{ width: `${(currentTime / generatedMusic.duration) * 100}%` }}
                />
              </div>

              {/* Controls */}
              <div className="flex items-center justify-center gap-4">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={togglePlay}
                  className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white shadow-lg hover:shadow-xl transition-all"
                >
                  {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-1" />}
                </motion.button>

                <div className="flex items-center gap-2">
                  <button
                    onClick={toggleMute}
                    className="p-2 text-slate-600 hover:text-slate-800 transition-colors"
                  >
                    {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                  </button>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={isMuted ? 0 : volume}
                    onChange={handleVolumeChange}
                    className="w-20 h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={downloadMusic}
                  className="px-4 py-2 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-lg font-medium hover:from-green-600 hover:to-blue-600 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                >
                  <Download className="w-4 h-4" />
                  다운로드
                </motion.button>
              </div>

              {/* Time Display */}
              <div className="text-center text-sm text-slate-500 font-mono">
                {formatTime(currentTime)} / {formatTime(generatedMusic.duration)}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
