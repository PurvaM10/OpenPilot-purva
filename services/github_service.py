import requests
from config import GITHUB_API, GITHUB_TOKEN


class GitHubService:

    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    def get_repository(self, owner, repo):
        response = requests.get(
            f"{GITHUB_API}/repos/{owner}/{repo}",
            headers=self.headers,
            timeout=15
        )

        response.raise_for_status()
        return response.json()

    def get_issues(self, owner, repo):
        response = requests.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=self.headers,
            params={
                "state": "open",
                "per_page": 30
            },
            timeout=15
        )

        response.raise_for_status()

        issues = response.json()

        return [
            issue
            for issue in issues
            if "pull_request" not in issue
        ]

    def get_contents(self, owner, repo, path=""):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/contents"

        if path:
            url += f"/{path}"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=15
        )

        response.raise_for_status()
        return response.json()