from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


class AIService:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def analyze_issue(self, issue, repository, skills):
        title = issue.get("title", "")
        body = issue.get("body") or "No description provided."

        repo_name = repository.get("name", "")
        repo_description = (
            repository.get("description")
            or "No repository description."
        )
        language = repository.get("language") or "Unknown"

        labels = [
            label.get("name", "")
            for label in issue.get("labels", [])
        ]

        prompt = f"""
You are an open-source contribution assistant.

Analyze this GitHub repository and issue.

REPOSITORY
Name: {repo_name}
Description: {repo_description}
Primary Language: {language}

ISSUE
Title: {title}

Description:
{body}

Labels:
{", ".join(labels) if labels else "None"}

DEVELOPER SKILLS
{", ".join(skills)}

Provide:
1. Issue Summary
2. Why This Issue Matches the Developer
3. Technologies Involved
4. Requirements
5. Step-by-Step Implementation Plan
6. Files or Components Likely Involved
7. Testing Plan
8. Potential Challenges
9. Suggested PR Title
10. Suggested PR Description

Do not invent repository-specific facts.
Clearly identify anything that must be verified
from the actual repository.
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text