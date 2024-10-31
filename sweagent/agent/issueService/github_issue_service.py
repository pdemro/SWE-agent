from __future__ import annotations

from ghapi.all import GhApi

from sweagent.agent.issueService.issue_service import (
    GITHUB_ISSUE_URL_PATTERN,
    IssueService,
    ProblemStatementResults,
    ProblemStatementSource,
    IssueData
)
from sweagent.environment.utils import InvalidSourceURL
from sweagent.utils.config import keys_config
from sweagent.utils.log import default_logger


def parse_gh_issue_url(issue_url: str) -> tuple[str, str, str]:
    """
    Returns:
        owner: Repo owner
        repo: Repo name
        issue number: Issue number as str

    Raises:
        InvalidGithubURL: If the URL is not a valid github issue URL
    """
    match = GITHUB_ISSUE_URL_PATTERN.search(issue_url)
    if not match:
        msg = f"Invalid GitHub issue URL: {issue_url}"
        raise InvalidGithubURL(msg)
    res = match.groups()
    assert len(res) == 3
    return tuple(res)  # type: ignore

class GitHubIssueService(IssueService):
    def __init__(self, data_path):
        super().__init__(data_path)
        default_logger.debug(f"GitHub Url: {self._data_path}")

        self._github_token: str = keys_config.get("GITHUB_TOKEN", "")  # type: ignore

    def _get_problem_statement_from_github_issue(
        self, owner: str, repo: str, issue_number: str, *, token: str | None = ""
    ) -> str:
        """Return problem statement from github issue"""
        api = GhApi(token=token)
        issue = api.issues.get(owner, repo, issue_number)
        title = issue.title if issue.title else ""
        body = issue.body if issue.body else ""
        problem_statement = f"{title}\n{body}\n"
        instance_id = f"{owner}__{repo}-i{issue_number}"
        issue_data = IssueData(name=title, id=issue_number, url=self._data_path, state=issue.state, assignee=issue.assignee, locked=issue.locked, owner=owner, repo=repo)
        return ProblemStatementResults(problem_statement, instance_id, ProblemStatementSource.ONLINE, issue_data=issue_data)

    def get_problem_statement(self):
        owner, repo, issue_number = parse_gh_issue_url(issue_url=self._data_path)
        return self._get_problem_statement_from_github_issue(
            owner,
            repo,
            issue_number,
            token=self._github_token,
        )
