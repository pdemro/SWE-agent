from sweagent.agent.repoService.repo_service import RepoService
from sweagent.utils.config import keys_config
from sweagent.environment.utils import InvalidGithubURL


GITHUB_REPO_URL_PATTERN = re.compile(r".*[/@]?github\.com\/([^/]+)\/([^/]+)")

def parse_gh_repo_url(repo_url: str) -> tuple[str, str]:
    """
    Returns:
        owner: Repo owner/org
        repo: Repo name

    Raises:
        InvalidGithubURL: If the URL is not a valid github repo URL
    """
    match = GITHUB_REPO_URL_PATTERN.search(repo_url)
    if not match:
        msg = f"Invalid GitHub issue URL: {repo_url}"
        raise InvalidGithubURL(msg)
    res = match.groups()
    assert len(res) == 2
    return tuple(res)  # type: ignore

class GitHubRepoService(RepoService):
    def __init__(self, repo_path, logger):
        super().__init__(repo_path, logger)

        self._github_token: str = keys_config.get("GITHUB_TOKEN", "")  # type: ignore
        self.api = GhApi(token=self._github_token)

    def open_pr(self, branch_name:str, title: str, body: str):
        """Create PR to repository

        Args:
            trajectory: Trajectory of actions taken by the agent
            dry_run: Whether to actually push anything or just simulate it
        """
        self.logger.info("Opening PR")

        owner, repo, _ = parse_gh_repo_url(repo_url)
        
        # pr_info = api.pulls.create(
        #     owner=owner,
        #     repo=repo,
        #     title=title,
        #     head=head,
        #     base="main",
        #     body=body,
        #     draft=True,
        # )
        self.logger.info(
            f"🎉 PR created as a draft at {pr_info.html_url}. Please review it carefully, push "
            "any required changes onto the branch and then click "
            "'Ready for Review' to bring it to the attention of the maintainers.",
        )
        
