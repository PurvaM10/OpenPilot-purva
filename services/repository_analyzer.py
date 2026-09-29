class RepositoryAnalyzer:

    def __init__(self, github):
        self.github = github

    def analyze(self, owner, repo):

        repository = self.github.get_repository(
            owner,
            repo
        )

        contents = self.github.get_contents(
            owner,
            repo
        )

        files = []

        if isinstance(contents, list):

            files = [
                item["name"]
                for item in contents
            ]

        return {
            "name": repository.get("full_name"),
            "description": repository.get("description"),
            "language": repository.get("language"),
            "stars": repository.get(
                "stargazers_count",
                0
            ),
            "forks": repository.get(
                "forks_count",
                0
            ),
            "open_issues": repository.get(
                "open_issues_count",
                0
            ),
            "files": files
        }