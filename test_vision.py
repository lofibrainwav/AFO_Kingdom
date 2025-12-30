#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/brnestrm/AFO_Kingdom/packages/afo-core')

from services.vision_service import VisionService

def test_vision():
    service = VisionService()

    # Test with local image
    image_path = "/Users/brnestrm/AFO_Kingdom/data/test_images/test_vision.png"

    print("Testing vision analysis with qwen3-vl...")
    result = service.analyze_image(
        image_path=image_path,
        prompt="Describe everything you see in this image in detail."
    )

    print("\n=== Vision Analysis Result ===")
    if result.get("success"):
        print(f"✅ Success!")
        print(f"Model: {result['model']}")
        print(f"\nDescription:")
        print(result['description'])
    else:
        print(f"❌ Failed: {result.get('error')}")

    print("\n" + "="*50)
    print("Testing object detection...")
    objects = service.detect_objects(image_path)
    if objects.get("success"):
        print(objects['description'])

    print("\n" + "="*50)
    print("Testing text extraction (OCR)...")
    text = service.extract_text(image_path)
    if text.get("success"):
        print(text['description'])

    print("\n✅ Vision service test completed!")

if __name__ == "__main__":
    test_vision()
