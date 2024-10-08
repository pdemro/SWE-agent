

from enum import Enum, auto
from sweagent.agent.repoService.github_repo_service import GITHUB_REPO_URL_PATTERN, GitHub

class RepoDatabaseType(Enum):
    GITHUB = auto()
    UNSUPPORTED = auto()


class RepoServiceFactory:
    def _parse_repo_type(self, repo_path: str) -> RepoDatabaseType:
        """Parse the repo_path and determine what kind of issue repository we're using"""
        if GITHUB_ISSUE_URL_PATTERN.search(repo_path) is not None:
            return RepoDatabaseType.GITHUB
        else:
            return RepoDatabaseType.UNSUPPORTED

    def create_repo_factory(self, repo_path: str):
        repo_type = self._parse_repo_type(repo_path)

        if repo_type == RepoDatabaseType.GITHUB:
            return GitHubRepoService(repo_path)

        else:
            error_message = "Invalid Repo Source"
            raise ValueError(error_message)