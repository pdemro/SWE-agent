from sweagent.utils.log import default_logger
from sweagent.agent.issueService.issue_service import (
    IssueService,
    ProblemStatementResults,
    ProblemStatementSource,
    JIRA_ISSUE_URL_PATTERN,
    IssueData
)
from jira import JIRA
from sweagent.environment.utils import InvalidSourceURL
from sweagent.utils.config import keys_config


class JiraIssueService(IssueService):
    def __init__(self, data_path):
        default_logger.debug(f"Initializing Jira Issue Service (problem statement) {data_path}")
        self.data_path = data_path
        self._token: str = keys_config.get("JIRA_TOKEN", "")
        self._email: str = keys_config.get("JIRA_EMAIL", "")
        self.repo_owner, self.issue_number = self._parse_issue_url(self.data_path)
        self.jira = JIRA(options={'server': f"https://{self.repo_owner}.atlassian.net"}, basic_auth=(self._email,self._token))

        super().__init__(data_path)

    def _parse_issue_url(self, issue_url: str) -> tuple[str, str]:
        """
        Returns:
            repo owner: Repo owner (subdomain of *.atlassian.com)
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
        issue = self.jira.issue(self.issue_number)
        summary = issue.fields.summary
        description = issue.fields.description

        problem_statement = f"{summary}\n{description}\n"
        instance_id = f"{self.repo_owner}__Jira-i{self.issue_number}"

        issue_data = IssueData(
            name=summary,
            id=self.issue_number,
            url="",
            state=issue.fields.status.name,
            assignee=issue.fields.assignee.displayName if issue.fields.assignee else None,
            locked=False,
            owner=self.repo_owner,
        )

        return ProblemStatementResults(
            problem_statement=problem_statement,
            instance_id=instance_id,
            problem_statement_source=ProblemStatementSource.ONLINE,
            issue_data=issue_data
        )

            