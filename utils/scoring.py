def calculate_issue_score(issue, skills):
    skills = [skill.lower().strip() for skill in skills if skill.strip()]

    title = (issue.get("title") or "").lower()
    body = (issue.get("body") or "").lower()
    labels = [
        label.get("name", "").lower()
        for label in issue.get("labels", [])
    ]

    searchable_text = f"{title} {body} {' '.join(labels)}"

    # Common aliases / related terms
    skill_aliases = {
        "python": [
            "python",
            ".py",
        ],
        "streamlit": [
            "streamlit",
            "streamlit runtime",
            "streamlit app",
            "st.",
            "st_",
        ],
        "github": [
            "github",
            "github api",
        ],
        "pandas": [
            "pandas",
            "pd.",
        ],
        "numpy": [
            "numpy",
            "np.",
        ],
        "sql": [
            "sql",
            "sqlite",
            "postgresql",
            "mysql",
        ],
        "javascript": [
            "javascript",
            "typescript",
            "js",
            "tsx",
            "jsx",
        ],
        "typescript": [
            "typescript",
            "tsx",
        ],
    }

    # -------------------------
    # 1. Skill relevance - 60%
    # -------------------------

    matched_skills = []

    for skill in skills:
        aliases = skill_aliases.get(skill, [skill])

        if any(alias in searchable_text for alias in aliases):
            matched_skills.append(skill)

    if skills:
        skill_score = (len(matched_skills) / len(skills)) * 60
    else:
        skill_score = 0

    # -------------------------
    # 2. Beginner friendliness - 15%
    # -------------------------

    beginner_labels = {
        "good first issue",
        "beginner",
        "easy",
        "help wanted",
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

    # -------------------------
    # 3. Issue activity - 10%
    # -------------------------

    comments = issue.get("comments", 0)

    if comments >= 10:
        activity_score = 10
    elif comments > 0:
        activity_score = 5
    else:
        activity_score = 0

    # -------------------------
    # 4. Description quality - 15%
    # -------------------------

    description_score = 0

    if len(body) > 100:
        description_score += 7.5

    if len(body) > 300:
        description_score += 7.5

    # -------------------------
    # Final score
    # -------------------------

    total_score = round(
        min(
            skill_score
            + beginner_score
            + activity_score
            + description_score,
            100,
        )
    )

    return {
        "score": total_score,
        "matched_skills": matched_skills,
        "beginner_labels": beginner_matches,
        "skill_score": round(skill_score),
        "beginner_score": round(beginner_score),
        "activity_score": activity_score,
        "description_score": round(description_score),
    }