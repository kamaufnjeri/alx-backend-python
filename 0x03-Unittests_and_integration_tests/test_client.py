#!/usr/bin/env python3
""" Module for testing GithubOrgClient """
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Mock the behavior of get_json
        mock_get_json.return_value = {"organization": org_name}

        # Your actual test logic with GithubOrgClient
        github_client = GithubOrgClient(org_name)
        result = github_client.org

        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
        )
        self.assertEqual(result, {"organization": org_name})

    @patch('client.GithubOrgClient.org', new_callable=patched_property)
    def test_public_repos_url(self, mock_org):
        """
        Test that the result of _public_repos_url is
        the expected one based on the mocked payload
        """
        # Mock the org property
        mock_org.return_value = {
            "repos_url": "http://example.com/repos"
        }

        # Your test logic
        github_client = GithubOrgClient("test_org")
        result = github_client._public_repos_url

        self.assertEqual(result, "http://example.com/repos")

    @patch('client.GithubOrgClient.org', new_callable=patched_property)
    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json, mock_org):
        """
        Test that the list of repos is what you expect from the chosen payload.
        Test that the mocked property and the mocked get_json was called once.
        """
        # Mock the org property
        mock_org.return_value = {"repos_url": "http://example.com/repos"}

        # Mock the behavior of get_json
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        # Your test logic
        github_client = GithubOrgClient("test_org")
        result = github_client.public_repos()

        mock_org.assert_called_once()
        mock_get_json.assert_called_once_with("http://example.com/repos")
        self.assertEqual(result, [{"name": "repo1"}, {"name": "repo2"}])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Unit-test for GithubOrgClient.has_license"""
        # Your test logic
        github_client = GithubOrgClient("test_org")
        result = github_client.has_license(repo, license_key)

        self.assertEqual(result, expected_result)


# Utility function to patch a property
def patched_property(f):
    """Utility function to patch a property"""
    return property(lambda *args, **kwargs: f(*args, **kwargs))
