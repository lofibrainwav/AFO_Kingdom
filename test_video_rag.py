#!/usr/bin/env python3
"""
Test the complete Video RAG pipeline.
"""
import sys
sys.path.insert(0, '/Users/brnestrm/AFO_Kingdom/packages/afo-core')

from services.video_rag_service import get_video_rag_service
from multimodal_rag_engine import MultimodalRAGEngine

def test_video_rag():
    print("=" * 70)
    print("🎥 Video RAG Pipeline Test")
    print("=" * 70)

    # Initialize services
    print("\n1. Initializing Video RAG Service...")
    video_service = get_video_rag_service()
    print(f"   ✅ Video RAG Service initialized")

    # Process video
    video_path = "/Users/brnestrm/AFO_Kingdom/data/test_video/test_video.mp4"
    print(f"\n2. Processing video: {video_path}")

    result = video_service.process_video(
        video_path=video_path,
        num_frames=3,
        transcribe=True,
        language="ko"
    )

    if result.get("success"):
        print(f"   ✅ Video processed successfully")
        print(f"   Keyframes extracted: {len(result['frames'])}")

        # Show frame descriptions
        print("\n   Frame Descriptions:")
        for frame in result["frames"]:
            print(f"\n   Frame {frame['frame_number']}:")
            print(f"   Path: {frame['path']}")
            desc = frame.get("description")
            if desc:
                desc_preview = desc[:200] if len(desc) > 200 else desc
                print(f"   Description: {desc_preview}...")
            else:
                print(f"   Description: (None - vision service may not be available)")

        # Show transcript
        if result.get("transcript"):
            print("\n   Audio Transcript:")
            transcript_text = result["transcript"].get("text", "")[:200]
            print(f"   Language: {result['transcript'].get('language', 'unknown')}")
            print(f"   Text: {transcript_text}...")

        # Show combined text
        print("\n   Combined Text Preview:")
        combined = result.get("combined_text", "")[:300]
        print(f"   {combined}...")

    else:
        print(f"   ❌ Video processing failed")

    # Test integration with Multimodal RAG Engine
    print("\n3. Adding video to Multimodal RAG Engine...")
    engine = MultimodalRAGEngine()

    # Add the processed video as a document
    engine.add_document(
        content=result.get("combined_text", ""),
        content_type="video",
        metadata={
            "path": video_path,
            "frames": len(result.get("frames", [])),
            "has_transcript": result.get("transcript") is not None
        }
    )
    print(f"   ✅ Video added to RAG engine")

    # Test search
    print("\n4. Testing search on video content...")
    search_results = engine.search("frame", content_types=["video"])
    print(f"   Found {len(search_results)} results")

    if search_results:
        doc = search_results[0]
        print(f"   Result type: {doc.content_type}")
        print(f"   Content preview: {doc.content[:100]}...")

    # Get final statistics
    print("\n5. Final Statistics...")
    stats = engine.get_stats()
    print(f"   Total Documents: {stats['total_documents']}")
    print(f"   By Type: {stats['by_type']}")

    print("\n" + "=" * 70)
    print("✅ Video RAG Pipeline Test Complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_video_rag()
