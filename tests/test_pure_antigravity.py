import unittest
from unittest.mock import patch

from AFO..config.antigravity import import antigravity


class TestPureAntigravity(unittest.TestCase):
    def setUp(self):
        pass

    @patch.object(antigravity, "get_feature_flag")
    def test_governance_truth(self, mock_flag):
        # Case 1: Flag Disabled (Truth says NO)
        mock_flag.return_value = False
        result = antigravity.check_governance("new_feature")
        assert not result

    @patch.object(antigravity, "get_feature_flag")
    def test_governance_goodness_risk(self, mock_flag):
        # Case 2: Flag Enabled, but Risk High (Goodness says NO)
        mock_flag.return_value = True

        # Key with "delete" triggers Risk=80 > 10
        result = antigravity.check_governance("delete_database")
        assert not result

    @patch.object(antigravity, "get_feature_flag")
    def test_governance_eternity_dryrun(self, mock_flag):
        # Case 3: Flag Enabled, Risk Low, but DRY_RUN blocks Write
        mock_flag.return_value = True

        # Ensure DRY_RUN is True
        antigravity.DRY_RUN_DEFAULT = True

        # Key with "write" triggers DRY_RUN check
        result = antigravity.check_governance("write_file")
        assert not result

    @patch.object(antigravity, "get_feature_flag")
    def test_governance_pass(self, mock_flag):
        # Case 4: All Pass
        mock_flag.return_value = True
        # Safer key
        result = antigravity.check_governance("read_data")
        assert result


if __name__ == "__main__":
    unittest.main()
