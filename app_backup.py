import streamlit as st

from services.github_service import GitHubService
from services.issue_matcher import rank_issues
from services.repository_analyzer import RepositoryAnalyzer
from utils.github_parser import parse_github_url


st.set_page_config(
    page_title="DevPortfolio Agent",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 DevPortfolio Agent")

st.markdown(
    """
    ### Find open-source issues that match your skills.

    Enter a GitHub repository and your skills.
    The agent will analyze the repository, find open issues,
    and rank them based on your profile.
    """
)

# -----------------------------
# Developer Profile
# -----------------------------

st.sidebar.header("👩‍💻 Developer Profile")

skills_input = st.sidebar.text_input(
    "Your skills",
    value="Python, Git, SQL, Machine Learning"
)

skills = [
    skill.strip()
    for skill in skills_input.split(",")
    if skill.strip()
]

# -----------------------------
# Repository Input
# -----------------------------

st.subheader("1️⃣ Choose a Repository")

repo_url = st.text_input(
    "GitHub repository URL",
    placeholder="https://github.com/owner/repository"
)

analyze = st.button(
    "🔍 Analyze Repository",
    type="primary"
)

# -----------------------------
# Analyze Repository
# -----------------------------

if analyze:

    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
        st.stop()

    try:

        owner, repo = parse_github_url(repo_url)

        github = GitHubService()

        analyzer = RepositoryAnalyzer(github)

        # Repository analysis
        with st.spinner("Analyzing repository..."):

            repository = analyzer.analyze(
                owner,
                repo
            )

        st.success(
            "Repository analyzed successfully!"
        )

        # -----------------------------
        # Repository Overview
        # -----------------------------

        st.subheader("📦 Repository Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "⭐ Stars",
            repository["stars"]
        )

        col2.metric(
            "🍴 Forks",
            repository["forks"]
        )

        col3.metric(
            "🐛 Open Issues",
            repository["open_issues"]
        )

        col4.metric(
            "💻 Language",
            repository["language"] or "Unknown"
        )

        if repository["description"]:

            st.info(
                repository["description"]
            )

        # -----------------------------
        # Issue Matching
        # -----------------------------

        st.subheader(
            "2️⃣ Matching Open Issues"
        )

        with st.spinner(
            "Finding and ranking issues..."
        ):

            issues = github.get_issues(
                owner,
                repo
            )

            ranked_issues = rank_issues(
                issues,
                skills
            )

        if not ranked_issues:

            st.warning(
                "No open issues were found."
            )

        else:

            st.write(
                f"Found {len(ranked_issues)} open issues."
            )

            for item in ranked_issues:

                issue = item["issue"]
                score = item["score"]
                matched = item["matched_skills"]

                with st.container(border=True):

                    col1, col2 = st.columns([4, 1])

                    with col1:

                        st.markdown(
                            f"### #{issue['number']} "
                            f"{issue['title']}"
                        )

                    with col2:

                        st.metric(
                            "Skill Match",
                            f"{score}%"
                        )

                    if matched:

                        st.write(
                            "**Matched skills:** "
                            + ", ".join(matched)
                        )

                    labels = [
                        label["name"]
                        for label in issue.get(
                            "labels",
                            []
                        )
                    ]

                    if labels:

                        st.write(
                            "**Labels:** "
                            + ", ".join(labels)
                        )

                    body = issue.get("body")

                    if body:

                        st.write(
                            body[:700]
                            + (
                                "..."
                                if len(body) > 700
                                else ""
                            )
                        )

                    st.link_button(
                        "View Issue →",
                        issue["html_url"]
                    )

    except ValueError as error:

        st.error(str(error))

    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )