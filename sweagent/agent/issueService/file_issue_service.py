from __future__ import annotations

import hashlib
from pathlib import Path

from sweagent.agent.issueService.issue_service import IssueService, ProblemStatementResults, ProblemStatementSource
from sweagent.utils.log import default_logger


class FileIssueService(IssueService):
    def __init__(self, data_path):
        super().__init__(data_path)
        default_logger.debug(f"File: {self.data_path}")

    def _get_problem_statement_results_from_text(self, text: str):
        instance_id = hashlib.sha256(text.encode()).hexdigest()[:6]
        return ProblemStatementResults(text, instance_id, ProblemStatementSource.LOCAL)

    def get_problem_statement(self):
        if self.data_path.startswith("text://"):
            results = self._get_problem_statement_results_from_text(self.data_path.removeprefix("text://"))
        elif Path(self.data_path).is_file():
            results = self._get_problem_statement_results_from_text(Path(self.data_path).read_text())
        else:
            error_message = f"Invalid file path: {self.data_path}"
            raise ValueError(error_message)

        return results
