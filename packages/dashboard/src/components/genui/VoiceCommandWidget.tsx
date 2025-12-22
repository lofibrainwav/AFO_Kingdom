'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { Mic, MicOff, Volume2, Loader2 } from 'lucide-react';
import { logError } from '@/lib/logger';

interface VoiceCommandWidgetProps {
  onCommand?: (text: string) => void;
  onResponse?: (response: string) => void;
}

export function VoiceCommandWidget({ onCommand, onResponse }: VoiceCommandWidgetProps) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  // Hoist speak function to be available for effects
  const speak = useCallback((text: string) => {
    if (!window.speechSynthesis) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ko-KR';
    utterance.rate = 0.9;
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
    onResponse?.(text);
  }, [onResponse]);

  // Check browser support
  useEffect(() => {
    const SpeechRecognitionAPI = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognitionAPI) {
      setIsSupported(false); // eslint-disable-line react-hooks/set-state-in-effect
      return;
    }

    const recognition = new SpeechRecognitionAPI();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'ko-KR'; // Korean language

    recognition.onresult = (event: any) => {
      const current = event.resultIndex;
      const result = event.results[current];
      const text = result[0].transcript;
      setTranscript(text);

      if (result.isFinal) {
        onCommand?.(text);
        // Mock response for now
        setTimeout(() => {
          speak(`명령을 받았습니다: ${text}`);
        }, 500);
      }
    };

    recognition.onerror = (event: any) => {
      logError('Speech Recognition Error', { error: event.error });
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, [onCommand, speak]);

  const toggleListening = useCallback(() => {
    if (!recognitionRef.current) return;

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setTranscript('');
      recognitionRef.current.start();
      setIsListening(true);
    }
  }, [isListening]);



  // Check browser support

  if (!isSupported) {
    return (
      <div className="p-4 bg-red-900/30 rounded-xl border border-red-500/40 text-center">
        <p className="text-red-300">음성 인식이 지원되지 않는 브라우저입니다.</p>
      </div>
    );
  }

  return (
    <div className="relative p-6 bg-gradient-to-br from-purple-900/40 to-cyan-900/40 rounded-2xl border border-purple-500/40 backdrop-blur-xl shadow-2xl">
      {/* Title */}
      <div className="flex items-center gap-3 mb-4">
        <Volume2 className="w-6 h-6 text-purple-400" />
        <h3 className="text-xl font-bold text-white">Commander's Voice</h3>
        {isSpeaking && (
          <span className="px-2 py-1 text-xs bg-cyan-500/30 text-cyan-300 rounded-full animate-pulse">
            Speaking...
          </span>
        )}
      </div>

      {/* Microphone Button */}
      <div className="flex flex-col items-center gap-4">
        <button
          onClick={toggleListening}
          className={`relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 ${
            isListening
              ? 'bg-red-500/80 shadow-lg shadow-red-500/50 animate-pulse'
              : 'bg-purple-600/60 hover:bg-purple-500/80 shadow-lg shadow-purple-500/30'
          }`}
        >
          {isListening ? (
            <MicOff className="w-10 h-10 text-white" />
          ) : (
            <Mic className="w-10 h-10 text-white" />
          )}
          
          {/* Pulse Ring Animation */}
          {isListening && (
            <>
              <span className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-50" />
              <span className="absolute inset-0 rounded-full border-2 border-red-300 animate-pulse" />
            </>
          )}
        </button>

        <p className="text-sm text-gray-400">
          {isListening ? '듣고 있습니다...' : '마이크를 클릭하여 명령하세요'}
        </p>
      </div>

      {/* Transcript Display */}
      {transcript && (
        <div className="mt-4 p-4 bg-black/30 rounded-xl border border-white/10">
          <p className="text-sm text-gray-400 mb-1">인식된 명령:</p>
          <p className="text-lg text-white font-medium">{transcript}</p>
        </div>
      )}

      {/* Status Indicator */}
      <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-500">
        <span className={`w-2 h-2 rounded-full ${isListening ? 'bg-red-500' : 'bg-green-500'}`} />
        <span>{isListening ? '음성 인식 중' : '대기 중'}</span>
      </div>
    </div>
  );
}
