def calculate_issue_score(issue, skills, repository=None):
    """
    Calculate an explainable 0-100 contribution match score.

    Score breakdown:
        Skill relevance:        45 points
        Repository technology: 25 points
        Beginner friendliness: 15 points
        Issue clarity:          10 points
        Issue activity:          5 points
    """

    # Clean skills
    skills = [
        skill.lower().strip()
        for skill in skills
        if skill and skill.strip()
    ]

    skills = list(dict.fromkeys(skills))

    # Issue information
    title = (issue.get("title") or "").lower()
    body = (issue.get("body") or "").lower()

    labels = [
        label.get("name", "").lower()
        for label in issue.get("labels", [])
        if label.get("name")
    ]

    searchable_text = f"{title} {body} {' '.join(labels)}"

    # Skill aliases
    skill_aliases = {
        "python": [
            "python",
            ".py",
            "python3",
        ],

        "streamlit": [
            "streamlit",
            "file_uploader",
            "st.file_uploader",
            "session_state",
            "st.session_state",
            "st.button",
            "st.selectbox",
            "st.text_input",
            "st.metric",
            "st.columns",
            "st.markdown",
        ],

        "github": [
            "github",
            "github api",
            "github actions",
            "gh api",
            "github-api",
        ],

        "git": [
            "git",
            "gitlab",
            "github",
            "commit",
            "branch",
            "pull request",
            "pull-request",
        ],

        "pandas": [
            "pandas",
            "dataframe",
            "data frame",
            "pd.",
        ],

        "numpy": [
            "numpy",
            "ndarray",
            "np.",
        ],

        "sql": [
            "sql",
            "sqlite",
            "postgresql",
            "postgres",
            "mysql",
            "database query",
        ],

        "javascript": [
            "javascript",
            "js",
            "jsx",
            "node.js",
            "nodejs",
        ],

        "typescript": [
            "typescript",
            "tsx",
            ".ts",
        ],

        "react": [
            "react",
            "reactjs",
            "jsx",
            "tsx",
        ],

        "docker": [
            "docker",
            "dockerfile",
            "container",
            "containerization",
        ],

        "java": [
            "java",
            ".java",
            "spring",
            "spring boot",
        ],

        "c++": [
            "c++",
            "cpp",
            ".cpp",
        ],

        "c": [
            "c programming",
            ".c",
        ],

        "html": [
            "html",
            "html5",
        ],

        "css": [
            "css",
            "stylesheet",
            "styles",
        ],
    }

    def aliases_for(skill):
        return skill_aliases.get(skill, [skill])

    # ==================================================
    # 1. SKILL RELEVANCE - 45 POINTS
    # ==================================================

    repository = repository or {}

    repository_language = (
        repository.get("language")
        or repository.get("primary_language")
        or ""
    ).lower().strip()

    repository_name = (
        repository.get("name")
        or ""
    ).lower()

    repository_description = (
        repository.get("description")
        or ""
    ).lower()

    repository_text = (
        f"{repository_name} "
        f"{repository_description} "
        f"{repository_language}"
    )

    matched_skills = []

    for skill in skills:
        aliases = aliases_for(skill)

        issue_match = any(
            alias in searchable_text
            for alias in aliases
        )

        repository_match = any(
            alias in repository_text
            for alias in aliases
        )

        # A skill matches if it appears either
        # in the issue OR in the repository technology.
        if issue_match or repository_match:
            matched_skills.append(skill)

    if skills:
        skill_score = (
            len(matched_skills) / len(skills)
        ) * 45
    else:
        skill_score = 0

    # ==================================================
    # 2. REPOSITORY TECHNOLOGY - 25 POINTS
    # ==================================================

    repository_matches = []

    for skill in skills:
        aliases = aliases_for(skill)

        # Direct language match
        language_match = (
            skill == repository_language
        )

        # Repository name/description/technology match
        text_match = any(
            alias in repository_text
            for alias in aliases
        )

        if language_match or text_match:
            repository_matches.append(skill)

    repository_matches = list(
        dict.fromkeys(repository_matches)
    )

    if skills:
        repository_score = (
            len(repository_matches) / len(skills)
        ) * 25
    else:
        repository_score = 0

    repository_score = min(
        repository_score,
        25
    )

    # ==================================================
    # 3. BEGINNER FRIENDLINESS - 15 POINTS
    # ==================================================

    beginner_labels = {
        "good first issue",
        "beginner",
        "easy",
        "help wanted",
        "first issue",
    }

    beginner_matches = [
        label
        for label in labels
        if label in beginner_labels
    ]

    beginner_score = min(
        len(beginner_matches) * 7.5,
        15
    )

    # ==================================================
    # 4. ISSUE CLARITY - 10 POINTS
    # ==================================================

    description_score = 0

    if len(body) > 100:
        description_score += 5

    if len(body) > 300:
        description_score += 5

    # ==================================================
    # 5. ISSUE ACTIVITY - 5 POINTS
    # ==================================================

    comments = issue.get("comments", 0)

    if comments >= 10:
        activity_score = 5
    elif comments > 0:
        activity_score = 2.5
    else:
        activity_score = 0

    # ==================================================
    # FINAL SCORE
    # ==================================================

    total_score = (
        skill_score
        + repository_score
        + beginner_score
        + description_score
        + activity_score
    )

    total_score = round(
        min(total_score, 100)
    )

    return {
        "score": total_score,
        "matched_skills": matched_skills,
        "repository_matches": repository_matches,
        "beginner_labels": beginner_matches,
        "skill_score": round(skill_score),
        "repository_score": round(repository_score),
        "beginner_score": round(beginner_score),
        "activity_score": round(activity_score),
        "description_score": round(description_score),
    }