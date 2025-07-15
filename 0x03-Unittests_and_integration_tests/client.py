#!/usr/bin/env python3
"""Module for interacting with Github API"""

import requests
from typing import Dict, List


def get_json(url: str) -> Dict:
    """Get JSON from remote URL"""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class GithubOrgClient:
    """A client for interacting with Github organizations"""

    def __init__(self, org_name: str) -> None:
        """Initialize with organization name"""
        self._org_name = org_name
        self._org_data = None
        self._repos_data = None

    @property
    def org(self) -> Dict:
        """Get organization information"""
        if self._org_data is None:
            url = f"https://api.github.com/orgs/{self._org_name}"
            self._org_data = get_json(url)
        return self._org_data

    @property
    def _public_repos_url(self) -> str:
        """Get public repos URL from org data"""
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """Get list of public repositories"""
        if self._repos_data is None:
            self._repos_data = get_json(self._public_repos_url)
        repos = [repo["name"] for repo in self._repos_data]
        if license:
            repos = [
                repo["name"] for repo in self._repos_data
                if repo.get("license", {}).get("key") == license
            ]
        return repos

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has specified license"""
        return repo.get("license", {}).get("key") == license_key
