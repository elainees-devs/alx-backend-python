#!/usr/bin/env python3
"""A GitHub org client
"""
from typing import List, Dict

from utils import (
    get_json,
    access_nested_map,
    memoize,
)


class GithubOrgClient:
    """A GitHub org client"""
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self._org_name = org_name

    @property
    @memoize
    def org(self) -> Dict:
        """Memoized property: org info"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return public repos URL"""
        return self.org["repos_url"]

    @property
    @memoize
    def repos_payload(self) -> Dict:
        """Memoized property: repos payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """List of public repos, optionally filtered by license"""
        public_repos = [
            repo["name"] for repo in self.repos_payload
            if license is None or self.has_license(repo, license)
        ]
        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if repo has a specific license"""
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
