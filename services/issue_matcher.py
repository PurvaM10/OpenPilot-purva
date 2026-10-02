from utils.scoring import calculate_issue_score


def rank_issues(issues, skills, repository=None):
    """
    Score every GitHub issue and return them
    from highest match to lowest match.
    """

    ranked = []

    for issue in issues:

        result = calculate_issue_score(
            issue,
            skills,
            repository
        )

        ranked.append({
            "issue": issue,
            **result
        })

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked