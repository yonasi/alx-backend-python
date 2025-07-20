#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ 
    Unit tests for the GithubOrgClient class.
    This class tests the behavior of the GithubOrgClient's methods
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns
        correct data and calls get_json once
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with
        (f"https://api.github.com/orgs/{org_name}")


def test_public_repos_url(self):
    """
    Test that _public_repos_url returns
    the expected URL from the mocked org
    """
    test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

    with patch.object(GithubOrgClient, 'org',
                      new_callable=property) as mock_org:
        mock_org.return_value = test_payload
        client = GithubOrgClient("testorg")
        result = client._public_repos_url
        self.assertEqual(result, test_payload["repos_url"])


@patch('client.get_json')
def test_public_repos(self, mock_get_json):
    """
    Test public_repos returns expected list
    of repository names
    """
    # Define fake repos payload
    test_payload = [
        {"name": "repo1"},
        {"name": "repo2"},
        {"name": "repo3"},
        ]
    mock_get_json.return_value = test_payload

    # Patch _public_repos_url to avoid calling actual URL
    with patch.object(GithubOrgClient,
                      "_public_repos_url",
                      new_callable=PropertyMock) as mock_url:
        mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

        client = GithubOrgClient("testorg")
    result = client.public_repos()

    self.assertEqual(result, ["repo1", "repo2", "repo3"])
    mock_get_json.assert_called_once_with
    ("https://api.github.com/orgs/testorg/repos")
    mock_url.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    # Previous tests...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


org_payload = {
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {
        "id": 7697149,
        "name": "episodes.dart",
        "full_name": "google/episodes.dart",
        "license": {"key": "bsd-3-clause"}
    },
    {
        "id": 123456,
        "name": "another-repo",
        "full_name": "google/another-repo",
        "license": {"key": "mit"}
    }
]

expected_repos = ["episodes.dart", "another-repo"]

apache2_repos = []


def test_public_repos(self):
    """Test that public_repos returns expected repo names."""
    client = GithubOrgClient("google")
    self.assertEqual(client.public_repos(), self.expected_repos)


def test_public_repos_with_license(self):
    """Test public_repos with license filter 'apache-2.0'."""
    client = GithubOrgClient("google")
    self.assertEqual(
        client.public_repos(license="apache-2.0"),
        self.apache2_repos
    )
