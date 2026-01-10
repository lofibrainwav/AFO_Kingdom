import contextlib

from pydantic import ValidationError

from AFO.schemas.sage import SageRequest, SageType


def test_sage_schema_validation():
    # 1. Valid Request
    with contextlib.suppress(ValidationError):
        SageRequest(sage=SageType.SAMAHWI, prompt="Test Prompt", temperature=0.5)

    # 2. Invalid Sage Type
    with contextlib.suppress(ValidationError):
        SageRequest(
            sage="invalid_sage",
            prompt="Test",
        )

    # 3. Invalid Temperature
    with contextlib.suppress(ValidationError):
        SageRequest(sage=SageType.JWAJA, prompt="Test", temperature=2.0)

    # 4. Missing Prompt
    try:
        SageRequest(
            sage=SageType.HWATA,
            # prompt missing
        )
    except ValidationError:
        pass


if __name__ == "__main__":
    test_sage_schema_validation()
