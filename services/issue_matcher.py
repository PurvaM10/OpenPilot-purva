from utils.scoring import calculate_issue_score


def rank_issues(issues, skills):

    ranked = []

    for issue in issues:

        result = calculate_issue_score(
            issue,
            skills
        )

        ranked.append({
            "issue": issue,
            "score": result["score"],
            "matched_skills": result["matched_skills"],
            "beginner_labels": result["beginner_labels"],
            "skill_score": result["skill_score"],
            "beginner_score": result["beginner_score"],
            "activity_score": result["activity_score"],
            "description_score": result["description_score"]
        })

    return sorted(
        ranked,
        key=lambda item: item["score"],
        reverse=True
    )