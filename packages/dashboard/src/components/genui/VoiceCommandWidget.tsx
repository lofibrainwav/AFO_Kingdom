/**
 * VoiceCommandWidget.tsx
 * 
 * 음성 명령 위젯 컴포넌트
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import ErrorBoundary from "@/components/common/ErrorBoundary";
import { logError } from "@/lib/logger";
import { Mic, MicOff, Volume2 } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

interface VoiceCommandWidgetProps {
  onCommand?: (text: string) => void;
  onResponse?: (response: string) => void;
}

function VoiceCommandWidgetContent({
  onCommand,
  onResponse,
}: VoiceCommandWidgetProps) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  // Memoize speak function
  const speak = useCallback(
    (text: string) => {
      if (!window.speechSynthesis) return;

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "ko-KR";
      utterance.rate = 0.9;
      utterance.pitch = 1.0;

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);

      window.speechSynthesis.speak(utterance);
      onResponse?.(text);
    },
    [onResponse]
  );

  // Memoize toggle handler
  const toggleListening = useCallback(() => {
    if (!recognitionRef.current) return;

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setTranscript("");
      recognitionRef.current.start();
      setIsListening(true);
    }
  }, [isListening]);

  // Memoize button styles
  const buttonStyles = useMemo(() => {
    return isListening
      ? "bg-red-500/80 shadow-lg shadow-red-500/50 animate-pulse"
      : "bg-purple-600/60 hover:bg-purple-500/80 shadow-lg shadow-purple-500/30";
  }, [isListening]);

  // Memoize status text
  const statusText = useMemo(() => {
    return isListening ? "듣고 있습니다..." : "마이크를 클릭하여 명령하세요";
  }, [isListening]);

  // Check browser support
  useEffect(() => {
    const SpeechRecognitionAPI =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognitionAPI) {
      // Use setTimeout to avoid synchronous setState in effect
      setTimeout(() => {
        setIsSupported(false);
      }, 0);
      return;
    }

    const recognition = new SpeechRecognitionAPI();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "ko-KR";

    recognition.onresult = (event: any) => {
      const current = event.resultIndex;
      const result = event.results[current];
      const text = result[0].transcript;
      setTranscript(text);

      if (result.isFinal) {
        onCommand?.(text);
        setTimeout(() => {
          speak(`명령을 받았습니다: ${text}`);
        }, 500);
      }
    };

    recognition.onerror = (event: any) => {
      logError("Speech Recognition Error", { error: event.error });
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, [onCommand, speak]);

  if (!isSupported) {
    return (
      <div
        className="p-4 bg-red-900/30 rounded-xl border border-red-500/40 text-center"
        role="alert"
        aria-live="assertive"
      >
        <p className="text-red-300">음성 인식이 지원되지 않는 브라우저입니다.</p>
      </div>
    );
  }

  return (
    <div
      className="relative p-6 bg-gradient-to-br from-purple-900/40 to-cyan-900/40 rounded-2xl border border-purple-500/40 backdrop-blur-xl shadow-2xl"
      role="region"
      aria-labelledby="voice-command-title"
    >
      {/* Title */}
      <header className="flex items-center gap-3 mb-4">
        <Volume2 className="w-6 h-6 text-purple-400" aria-hidden="true" />
        <h3 id="voice-command-title" className="text-xl font-bold text-white">
          Commander's Voice
        </h3>
        {isSpeaking && (
          <span
            className="px-2 py-1 text-xs bg-cyan-500/30 text-cyan-300 rounded-full animate-pulse"
            role="status"
            aria-live="polite"
            aria-label="Speaking"
          >
            Speaking...
          </span>
        )}
      </header>

      {/* Microphone Button */}
      <div className="flex flex-col items-center gap-4">
        <button
          onClick={toggleListening}
          className={`relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 ${buttonStyles}`}
          aria-label={isListening ? "Stop listening" : "Start listening"}
          aria-pressed={isListening ? "true" : "false"}
        >
          {isListening ? (
            <MicOff className="w-10 h-10 text-white" aria-hidden="true" />
          ) : (
            <Mic className="w-10 h-10 text-white" aria-hidden="true" />
          )}

          {/* Pulse Ring Animation */}
          {isListening && (
            <>
              <span
                className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-50"
                aria-hidden="true"
              />
              <span
                className="absolute inset-0 rounded-full border-2 border-red-300 animate-pulse"
                aria-hidden="true"
              />
            </>
          )}
        </button>

        <p className="text-sm text-gray-400" aria-live="polite">
          {statusText}
        </p>
      </div>

      {/* Transcript Display */}
      {transcript && (
        <div
          className="mt-4 p-4 bg-black/30 rounded-xl border border-white/10"
          role="status"
          aria-live="polite"
          aria-label="Recognized command"
        >
          <p className="text-sm text-gray-400 mb-1">인식된 명령:</p>
          <p className="text-lg text-white font-medium">{transcript}</p>
        </div>
      )}

      {/* Status Indicator */}
      <div
        className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-500"
        role="status"
        aria-live="polite"
        aria-label={isListening ? "Listening" : "Waiting"}
      >
        <span
          className={`w-2 h-2 rounded-full ${isListening ? "bg-red-500" : "bg-green-500"}`}
          aria-hidden="true"
        />
        <span>{isListening ? "음성 인식 중" : "대기 중"}</span>
      </div>
    </div>
  );
}

export function VoiceCommandWidget(props: VoiceCommandWidgetProps) {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("VoiceCommandWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="p-4 bg-red-900/30 rounded-xl border border-red-500/40 text-center"
          role="alert"
        >
          <p className="text-red-300">음성 명령 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <VoiceCommandWidgetContent {...props} />
    </ErrorBoundary>
  );
}

export default VoiceCommandWidget;
