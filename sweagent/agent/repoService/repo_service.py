import re
from abc import ABC, abstractmethod
from enum import Enum

class PRResponse:
    def __init__(self, pr_url:str):
        self.url = pr_url

class RepoService(ABC):
    def __init__(self, repo_path:str, logger):
        self.repo_path = repo_path
        self.logger = logger


    #TODO return status somehow?
    @abstractmethod
    def open_pr(self, branch_name:str, title: str, body: str) -> PRResponse:
        pass

    # ... other common methods