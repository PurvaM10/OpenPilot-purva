from urllib.parse import urlparse


def parse_github_url(url):
    parsed = urlparse(url.strip())

    if parsed.netloc.lower() not in {
        "github.com",
        "www.github.com"
    }:
        raise ValueError(
            "Please enter a valid GitHub URL."
        )

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError(
            "Invalid GitHub repository URL."
        )

    return parts[0], parts[1]