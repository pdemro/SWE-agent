from sweagent.utils.log import default_logger
from sweagent.agent.issueService.issue_service import (
    IssueService,
    ProblemStatementResults,
    ProblemStatementSource,
    JIRA_ISSUE_URL_PATTERN
)
from jira import JIRA
from sweagent.environment.utils import InvalidSourceURL


class JiraIssueService(IssueService):
    def __init__(self, data_path):
        default_logger.debug(f"Initializing Jira Issue Service (problem statement) {data_path}")
        self.data_path = data_path
        # self.jira = JIRA()

        super().__init__(data_path)

    def _parse_jira_issue_url(self, issue_url: str) -> tuple[str, str]:
        """
        Returns:
            server: Jira server as str
            issue number: Issue number as str

        Raises:
            InvalidSourceUrl: If the URL is not a valid github issue URL
        """

        match = JIRA_ISSUE_URL_PATTERN.search(issue_url)
        if not match:
            msg = f"Invalid Jira issue URL: {issue_url}"
            raise InvalidSourceURL(msg)
        res = match.groups()
        assert len(res) == 2
        return tuple(res)

    def get_problem_statement(self):
        default_logger.debug("do something")
        silly = self._parse_jira_issue_url(self.data_path)
        default_logger.debug(f"silly!: {silly}")
        