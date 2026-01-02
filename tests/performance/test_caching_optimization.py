# tests/performance/test_caching_optimization.py
import asyncio
import os
import pathlib
import sys
from unittest.mock import patch

import pytest


# Ensure AFO package is importable
sys.path.append(
    pathlib.Path(
        os.path.join(pathlib.Path(__file__).parent, "../../packages/afo-core")
    ).resolve()
)

from AFO..utils.cache_utils import import cache, cached


# Mock Redis Client
class MockRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def setex(self, key, time, value):
        self.store[key] = value

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            return 1
        return 0


@pytest.mark.asyncio
async def test_cache_hit_miss():
    """Test cache hit results in faster response (mocked)."""

    # Setup Mock
    mock_redis = MockRedis()

    # Patch the global 'cache' instance's redis client
    with patch.object(cache, "redis", mock_redis):
        # Enable cache manually since init might have failed if no real redis
        cache.enabled = True

        call_count = 0

        @cached(expire=60)
        async def expensive_func(arg):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return f"result_{arg}"

        # 1. First Call (Miss)
        res1 = await expensive_func("test")
        assert res1 == "result_test"
        assert call_count == 1
        # Key includes kwargs representation: "expensive_func:('test',){}"
        assert len(mock_redis.store) == 1

        # 2. Second Call (Hit)
        res2 = await expensive_func("test")
        assert res2 == "result_test"
        assert call_count == 1  # Should NOT increment


@pytest.mark.asyncio
async def test_cache_expiration_simulation():
    """Test that if cache returns None (expired/missing), function is called."""
    mock_redis = MockRedis()

    with patch.object(cache, "redis", mock_redis):
        cache.enabled = True
        call_count = 0

        @cached(expire=60)
        async def flaky_func(arg):
            nonlocal call_count
            call_count += 1
            return "data"

        # Call 1
        await flaky_func("a")
        assert call_count == 1

        # Simulate Expiration (delete key)
        # Key format in decorator: f"{func.__name__}:{str(args) + str(kwargs)}"
        # Note: Depending on string representation, exact key might vary.
        # But MockRedis relies on exact key match.
        # Let's verify key presence first.
        keys = list(mock_redis.store.keys())
        assert len(keys) == 1
        real_key = keys[0]

        mock_redis.delete(real_key)

        # Call 2 (Should run again)
        await flaky_func("a")
        assert call_count == 2
