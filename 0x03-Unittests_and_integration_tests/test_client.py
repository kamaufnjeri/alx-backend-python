#!/usr/bin/env python3
""" Module for testing GithubOrgClient """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """ Class for Testing Github Org Client """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, input_org, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_client = GithubOrgClient(input_org)
        test_client.org()
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{input_org}'
        )

    def test_public_repos_url(self):
        """ Test that the result of _public_repos_url is the expected one
        based on the mocked payload
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            payload = {"repos_url": "World"}
            mock_org.return_value = payload
            test_client = GithubOrgClient('test')
            result = test_client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """
        Test that the list of repos is what you expect from the chosen payload.
        Test that the mocked property and the mocked get_json was called once.
        """
        json_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:

            mock_public_repos_url.return_value = "hello/world"
            test_client = GithubOrgClient('test')
            result = test_client.public_repos()

            check = [i["name"] for i in json_payload]
            self.assertEqual(result, check)

            mock_public_repos_url.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """ unit-test for GithubOrgClient.has_license """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock_requests_get = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_client = GithubOrgClient("google")

        self.assertEqual(test_client.org, self.org_payload)
        self.assertEqual(test_client.repos_payload, self.repos_payload)
        self.assertEqual(test_client.public_repos(), self.expected_repos)
        self.assertEqual(test_client.public_repos("XLICENSE"), [])
        self.mock_requests_get.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public repos with License """
        test_client = GithubOrgClient("google")

        self.assertEqual(test_client.public_repos(), self.expected_repos)
        self.assertEqual(test_client.public_repos("XLICENSE"), [])
        self.assertEqual(test_client.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock_requests_get.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()
