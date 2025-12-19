import asyncio
import pytest
from AFO.schemas.sage import SageRequest, SageType
from pydantic import ValidationError

def test_sage_schema_validation():
    print("\n🧪 Testing SageRequest Schema...")
    
    # 1. Valid Request
    try:
        req = SageRequest(
            sage=SageType.SAMAHWI,
            prompt="Test Prompt",
            temperature=0.5
        )
        print("✅ Valid request passed")
    except ValidationError as e:
        print(f"❌ Valid request failed: {e}")

    # 2. Invalid Sage Type
    try:
        SageRequest(
            sage="invalid_sage",
            prompt="Test",
        )
        print("❌ Invalid sage type failed to raise error")
    except ValidationError:
        print("✅ Invalid sage type caught")

    # 3. Invalid Temperature
    try:
        SageRequest(
            sage=SageType.JWAJA,
            prompt="Test",
            temperature=2.0 
        )
        print("❌ Invalid temperature failed to raise error")
    except ValidationError:
        print("✅ Invalid temperature caught")

    # 4. Missing Prompt
    try:
        SageRequest(
            sage=SageType.HWATA,
            # prompt missing
        )
        print("❌ Missing prompt failed to raise error")
    except ValidationError:
        print("✅ Missing prompt caught")

if __name__ == "__main__":
    test_sage_schema_validation()
