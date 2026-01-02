#!/usr/bin/env python3
import sys

sys.path.insert(0, "/Users/brnestrm/AFO_Kingdom/packages/afo-core")

from services.audio_service import AudioService


def test_audio():
    print("=== Initializing Audio Service ===")
    service = AudioService(model="base")

    # Test with the tone audio we created
    audio_path = "/Users/brnestrm/AFO_Kingdom/data/test_audio/test_tone.wav"

    print(f"\nTesting audio analysis with: {audio_path}")
    result = service.transcribe(audio_path)

    print("\n=== Audio Analysis Result ===")
    if result.get("success"):
        print("✅ Success!")
        print(f"Model: {result['model']}")
        print(f"Language: {result.get('language')}")
        print("\nTranscription:")
        print(result["text"])

        if "segments" in result:
            print(f"\nSegments: {len(result['segments'])}")
    else:
        print(f"⚠️  {result.get('error')}")
        if "audio_info" in result:
            print("\nAudio Info Available (Whisper not installed)")

    print("\n" + "=" * 50)
    print("✅ Audio service test completed!")
    print("\n💡 Note: For full functionality, install Whisper:")
    print("   pip install openai-whisper")


if __name__ == "__main__":
    test_audio()
