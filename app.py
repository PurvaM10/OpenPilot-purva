import streamlit as st

from services.github_service import GitHubService
from services.issue_matcher import rank_issues
from services.repository_analyzer import RepositoryAnalyzer
from utils.github_parser import parse_github_url


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="DevPortfolio Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .hero {
        padding: 2rem 0 1rem 0;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.15rem;
        color: #6b7280;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .match-score {
        font-size: 1.8rem;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("DevPortfolio")

    st.caption(
        "AI-powered open-source contribution assistant"
    )

    st.divider()

    st.subheader("Developer Profile")

    skills_input = st.text_area(
        "Your skills",
        value="Python, Git, SQL, Machine Learning",
        help="Separate your skills with commas."
    )

    experience = st.selectbox(
        "Experience level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.caption(
        "Your profile is used to personalize issue recommendations."
    )


# --------------------------------------------------
# Hero Section
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

    <h1>Find your next open-source contribution.</h1>

    <p>
    DevPortfolio Agent analyzes GitHub repositories and
    finds issues that match your skills and experience.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Repository Input
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Repository</div>',
    unsafe_allow_html=True
)

repo_url = st.text_input(
    "GitHub repository",
    placeholder="https://github.com/owner/repository",
    label_visibility="collapsed"
)

analyze = st.button(
    "Analyze Repository",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Analysis
# --------------------------------------------------

if analyze:

    if not repo_url:

        st.error(
            "Please enter a GitHub repository URL."
        )

        st.stop()

    skills = [
        skill.strip()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    try:

        owner, repo = parse_github_url(repo_url)

        github = GitHubService()

        analyzer = RepositoryAnalyzer(github)

        # ------------------------------------------
        # Repository Analysis
        # ------------------------------------------

        with st.spinner(
            "Analyzing repository..."
        ):

            repository = analyzer.analyze(
                owner,
                repo
            )

        st.success(
            "Repository analyzed successfully."
        )

        # ------------------------------------------
        # Repository Header
        # ------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Repository Intelligence'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            repository["name"]
        )

        if repository["description"]:

            st.write(
                repository["description"]
            )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Stars",
            repository["stars"]
        )

        col2.metric(
            "Forks",
            repository["forks"]
        )

        col3.metric(
            "Open Issues",
            repository["open_issues"]
        )

        col4.metric(
            "Language",
            repository["language"] or "Unknown"
        )

        # ------------------------------------------
        # Issues
        # ------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Recommended Issues'
            '</div>',
            unsafe_allow_html=True
        )

        with st.spinner(
            "Finding issues that match your profile..."
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

            st.info(
                "This repository currently has no open issues."
            )

        else:

            st.caption(
                f"{len(ranked_issues)} open issues analyzed"
            )

            # --------------------------------------
            # Issue Cards
            # --------------------------------------

            for item in ranked_issues:

                issue = item["issue"]

                score = item["score"]

                matched = item["matched_skills"]

                labels = [
                    label["name"]
                    for label in issue.get(
                        "labels",
                        []
                    )
                ]

                with st.container(
                    border=True
                ):

                    left, right = st.columns(
                        [5, 1]
                    )

                    # ------------------------------
                    # Left Side
                    # ------------------------------

                    with left:

                        st.markdown(
                            f"### #{issue['number']} "
                            f"{issue['title']}"
                        )

                        if matched:

                            st.write(
                                "**Matching skills:** "
                                + ", ".join(matched)
                            )

                        else:

                            st.write(
                                "**Matching skills:** "
                                "None detected"
                            )

                        if labels:

                            st.caption(
                                " · ".join(labels)
                            )

                        body = issue.get(
                            "body"
                        )

                        if body:

                            preview = body[:500]

                            if len(body) > 500:

                                preview += "..."

                            st.write(
                                preview
                            )

                        # --------------------------
                        # Score Explanation
                        # --------------------------

                        with st.expander(
                            "Why this score?"
                        ):

                            st.write(
                                f"**Skill match:** "
                                f"{item['skill_score']}/45"
                            )

                            st.write(
                                f"**Beginner-friendly "
                                f"signals:** "
                                f"{item['beginner_score']}/20"
                            )

                            st.write(
                                f"**Issue activity:** "
                                f"{item['activity_score']}/5"
                            )

                            st.write(
                                f"**Description quality:** "
                                f"{item['description_score']}/10"
                            )

                            if item[
                                "beginner_labels"
                            ]:

                                st.write(
                                    "**Helpful labels:** "
                                    + ", ".join(
                                        item[
                                            "beginner_labels"
                                        ]
                                    )
                                )

                    # ------------------------------
                    # Right Side
                    # ------------------------------

                    with right:

                        st.markdown(
                            f'<div class="match-score">'
                            f'{score}%'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        st.caption(
                            "Skill match"
                        )

                    # ------------------------------
                    # Issue Link
                    # ------------------------------

                    st.link_button(
                        "View issue",
                        issue["html_url"]
                    )

    except ValueError as error:

        st.error(
            str(error)
        )

    except Exception as error:

        st.error(
            "We couldn't analyze this repository. "
            "Please check the URL and try again."
        )

        with st.expander(
            "Technical details"
        ):

            st.code(
                str(error)
            )