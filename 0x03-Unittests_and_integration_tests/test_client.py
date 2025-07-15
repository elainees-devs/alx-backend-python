#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.org
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Test setup
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Execute
        client = GithubOrgClient(org_name)
        result = client.org

        # Verify
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns correct value from org payload"""
        # Test setup
        test_url = "https://api.github.com/orgs/google/repos"
        mock_org.return_value = {"repos_url": test_url}

        # Execute and verify
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, test_url)


if __name__ == "__main__":
    unittest.main()