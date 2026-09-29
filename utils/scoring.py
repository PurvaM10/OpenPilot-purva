def calculate_issue_score(issue, skills):
    """
    Calculate an explainable match score between
    a GitHub issue and a developer's skills.
    """

    skills = [
        skill.lower().strip()
        for skill in skills
        if skill.strip()
    ]

    title = (issue.get("title") or "").lower()
    body = (issue.get("body") or "").lower()

    labels = [
        label["name"].lower()
        for label in issue.get("labels", [])
    ]

    searchable_text = (
        title + " " + body + " " + " ".join(labels)
    )

    matched_skills = []

    for skill in skills:
        if skill in searchable_text:
            matched_skills.append(skill)

    # -----------------------------
    # Skill Match
    # -----------------------------

    skill_score = min(
        len(matched_skills) * 15,
        45
    )

    # -----------------------------
    # Beginner-Friendly Labels
    # -----------------------------

    beginner_labels = {
        "good first issue",
        "beginner",
        "easy",
        "help wanted"
    }

    beginner_matches = [
        label
        for label in labels
        if label in beginner_labels
    ]

    beginner_score = min(
        len(beginner_matches) * 10,
        20
    )

    # -----------------------------
    # Activity
    # -----------------------------

    activity_score = 5 if issue.get(
        "comments", 0
    ) > 0 else 0

    # -----------------------------
    # Issue Description Quality
    # -----------------------------

    description_score = 0

    if body:

        if len(body) > 100:
            description_score += 5

        if len(body) > 300:
            description_score += 5

    # -----------------------------
    # Final Score
    # -----------------------------

    total_score = min(
        skill_score
        + beginner_score
        + activity_score
        + description_score,
        100
    )

    return {
        "score": total_score,
        "matched_skills": matched_skills,
        "beginner_labels": beginner_matches,
        "skill_score": skill_score,
        "beginner_score": beginner_score,
        "activity_score": activity_score,
        "description_score": description_score
    }