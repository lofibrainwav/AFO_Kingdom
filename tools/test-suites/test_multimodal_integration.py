#!/usr/bin/env python3
"""
Test the integrated Multimodal RAG Engine with Vision and Audio services.
"""
import sys

sys.path.insert(0, "/Users/brnestrm/AFO_Kingdom/packages/afo-core")

from multimodal_rag_engine import MultimodalRAGEngine


def test_multimodal_integration():
    print("=" * 70)
    print("🔥 Multimodal RAG Engine Integration Test")
    print("=" * 70)

    # Initialize engine
    print("\n1. Initializing Multimodal RAG Engine...")
    engine = MultimodalRAGEngine()
    print("   ✅ Engine initialized")
    print(
        f"   Vision Service: {'Available' if engine.vision_service else 'Not Available'}"
    )
    print(
        f"   Audio Service: {'Available' if engine.audio_service else 'Not Available'}"
    )

    # Test image addition with vision analysis
    print("\n2. Testing Image Addition with Vision Analysis...")
    image_path = "/Users/brnestrm/AFO_Kingdom/data/test_images/test_vision.png"
    result = engine.add_image(
        image_path, description="Test image for multimodal RAG", analyze=True
    )
    if result:
        print("   ✅ Image added successfully with vision analysis")
    else:
        print("   ❌ Failed to add image")

    # Test audio addition with transcription
    print("\n3. Testing Audio Addition with Transcription...")
    audio_path = "/Users/brnestrm/AFO_Kingdom/data/test_audio/test_tone.wav"
    result = engine.add_audio(
        audio_path, description="Test audio for multimodal RAG", transcribe=True
    )
    if result:
        print("   ✅ Audio added successfully with transcription")
    else:
        print("   ❌ Failed to add audio")

    # Test search
    print("\n4. Testing Multimodal Search...")

    # Search for image content
    print("\n   a) Searching for image-related content (사각형)...")
    results = engine.search("사각형", content_types=["image"])
    print(f"      Found {len(results)} results")
    if results:
        for i, doc in enumerate(results[:2], 1):
            print(f"\n      Result {i}:")
            print(f"      Type: {doc.content_type}")
            print(f"      Path: {doc.metadata.get('path', 'N/A')}")
            if doc.metadata.get("analyzed"):
                print(f"      Vision Model: {doc.metadata.get('vision_model', 'N/A')}")
            content_preview = (
                doc.content[:200] if len(doc.content) > 200 else doc.content
            )
            print(f"      Content: {content_preview}...")

    # Search across all types
    print("\n   b) Searching across all content types (test)...")
    results = engine.search("test", top_k=5)
    print(f"      Found {len(results)} results")
    for i, doc in enumerate(results, 1):
        print(
            f"      {i}. Type: {doc.content_type}, Path: {doc.metadata.get('path', 'N/A')[:50]}"
        )

    # Get engine statistics
    print("\n5. Engine Statistics...")
    stats = engine.get_stats()
    print(f"   Total Documents: {stats['total_documents']}")
    print(f"   By Type: {stats['by_type']}")
    print(
        f"   Memory Usage: {stats['memory_stats']['current_memory_mb']} MB / {stats['memory_stats']['max_memory_mb']} MB"
    )
    print(
        f"   Memory Utilization: {stats['memory_stats']['memory_utilization'] * 100:.1f}%"
    )
    print(f"   Health Status: {stats['health_status']}")

    print("\n" + "=" * 70)
    print("✅ Multimodal RAG Engine Integration Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_multimodal_integration()
