import unittest
from unittest.mock import MagicMock, patch

from AFO..config.antigravity import import antigravity


class TestAntigravityFlags(unittest.TestCase):
    def setUp(self):
        pass

    @patch.object(antigravity, "_get_redis_conn")
    def test_flag_defaults(self, mock_get_conn):
        # Setup Mock Redis
        mock_redis = MagicMock()
        mock_get_conn.return_value = mock_redis

        # Case 1: Redis returns empty (Key not found) -> Should user default
        mock_redis.hgetall.return_value = {}

        result = antigravity.get_feature_flag("missing_feature", default=False)
        assert not result

        result = antigravity.get_feature_flag("missing_feature_true", default=True)
        assert result

    @patch.object(antigravity, "_get_redis_conn")
    def test_global_enabled(self, mock_get_conn):
        mock_redis = MagicMock()
        mock_get_conn.return_value = mock_redis

        # Enabled = True, Rollout = 100
        mock_redis.hgetall.return_value = {
            "enabled": "true",
            "rollout_percentage": "100",
        }

        assert antigravity.get_feature_flag("global_on")

        # Enabled = False
        mock_redis.hgetall.return_value = {
            "enabled": "false",
            "rollout_percentage": "100",
        }
        assert not antigravity.get_feature_flag("global_off")

    @patch.object(antigravity, "_get_redis_conn")
    def test_rollout_percentage(self, mock_get_conn):
        mock_redis = MagicMock()
        mock_get_conn.return_value = mock_redis

        # 50% Rollout
        mock_redis.hgetall.return_value = {
            "enabled": "true",
            "rollout_percentage": "50",
        }

        # Validating determinism
        res1 = antigravity.get_feature_flag("test_rollout", user_id="user_a")
        res2 = antigravity.get_feature_flag("test_rollout", user_id="user_a")
        assert res1 == res2  # Must be deterministic

    @patch.object(antigravity, "_get_redis_conn")
    def test_targeted_users(self, mock_get_conn):
        mock_redis = MagicMock()
        mock_get_conn.return_value = mock_redis

        # Enabled = True, Rollout = 0 (Only targets)
        mock_redis.hgetall.return_value = {
            "enabled": "true",
            "rollout_percentage": "0",
            "targeted_users": "user_vip,user_admin",
        }

        assert antigravity.get_feature_flag("beta", user_id="user_vip")
        assert not antigravity.get_feature_flag("beta", user_id="user_normal")


if __name__ == "__main__":
    unittest.main()
