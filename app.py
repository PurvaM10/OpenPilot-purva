import streamlit as st

from services.github_service import GitHubService
from services.repository_analyzer import RepositoryAnalyzer
from services.issue_matcher import rank_issues
from services.ai_service import AIService
from utils.github_parser import parse_github_url


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OPENPILOT",
    page_icon="↗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>
    /* =========================================================
       OPENPILOT — EDITORIAL DEVELOPER THEME
       Inspired by bold editorial/product-launch design:
       warm paper, ink black, red signal, yellow highlight.
       ========================================================= */

    .stApp {
        background: #F4F0E8;
        color: #111111;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1240px !important;
        padding: 1.6rem 2rem 3rem !important;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Typography */
    h1, h2, h3, h4, p, label,
    [data-testid="stMarkdownContainer"] {
        color: #111111 !important;
    }

    h1, h2, h3, h4 {
        letter-spacing: -0.035em !important;
    }

    /* Brand */
    .op-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0 0 0.35rem 0;
    }

    .op-brand-mark {
        font-size: 2rem;
        line-height: 1;
        font-weight: 900;
        color: #111111;
    }

    .op-brand-name {
        font-size: 2rem;
        line-height: 1;
        font-weight: 900;
        letter-spacing: -0.055em;
        color: #111111;
    }

    /* Navigation */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background: transparent !important;
        border: 0 !important;
        color: #3F3B36 !important;
        box-shadow: none !important;
        font-weight: 650 !important;
        min-height: 2.1rem !important;
        padding: 0.25rem 0.4rem !important;
        border-radius: 999px !important;
    }

    div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
        background: #E8E2D8 !important;
        color: #111111 !important;
    }

    /* Active navigation — never let Streamlit's inner text inherit black */
    div[data-testid="stHorizontalBlock"] button[kind="primary"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"] *,
    div[data-testid="stHorizontalBlock"] button[kind="primary"] p,
    div[data-testid="stHorizontalBlock"] button[kind="primary"] span {
        background: transparent !important;
        border: 0 !important;
        border-bottom: 2px solid #A70D16 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        border-radius: 0 !important;
        min-height: 2.35rem !important;
        font-weight: 800 !important;
        box-shadow: none !important;
        font-size: 0.84rem !important;
    }

    div[data-testid="stHorizontalBlock"] button[kind="secondary"] *,
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] p,
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] span {
        color: #3F3B36 !important;
        -webkit-text-fill-color: #3F3B36 !important;
    }

    /* Primary action buttons — warm red signal */
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[kind="primary"] p,
    div[data-testid="stButton"] button[kind="primary"] span,
    div[data-testid="stButton"] button[kind="primary"] div {
        background: #F7F2E9 !important;
        border: 1px solid #1C1B19 !important;
        color: #1C1B19 !important;
        -webkit-text-fill-color: #1C1B19 !important;
        border-radius: 7px !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        min-height: 2.7rem !important;
        box-shadow: none !important;
        transition: background 120ms ease, border-color 120ms ease, color 120ms ease !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover,
    div[data-testid="stButton"] button[kind="primary"]:hover *,
    div[data-testid="stButton"] button[kind="primary"]:hover p,
    div[data-testid="stButton"] button[kind="primary"]:hover span {
        background: #FFFDF8 !important;
        border-color: #A70D16 !important;
        color: #A70D16 !important;
        -webkit-text-fill-color: #A70D16 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Secondary buttons */
    div[data-testid="stButton"] button[kind="secondary"],
    div[data-testid="stButton"] button[kind="secondary"] * {
        color: #24211E !important;
        -webkit-text-fill-color: #24211E !important;
    }

    /* Streamlit link buttons */
    div[data-testid="stLinkButton"] a,
    div[data-testid="stLinkButton"] a *,
    a[data-testid="stLinkButton"],
    a[data-testid="stLinkButton"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background: #111111 !important;
        border-color: #111111 !important;
        font-weight: 800 !important;
    }

    /* Dividers */
    hr {
        border-color: #D5CFC4 !important;
        margin: 1.25rem 0 !important;
    }

    /* Hero */
    .op-eyebrow,
    .op-section-label {
        display: inline-block;
        font-size: 0.68rem;
        letter-spacing: 0.13em;
        font-weight: 900;
        color: #A70D16 !important;
    }

    .op-eyebrow {
        margin: 0.6rem 0 0.75rem;
    }

    .op-hero-title {
        max-width: 1050px;
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(3.1rem, 6vw, 5.8rem);
        line-height: 0.92;
        letter-spacing: -0.065em;
        font-weight: 700;
        color: #111111;
        margin-bottom: 1rem;
    }

    .op-hero-copy {
        max-width: 650px;
        color: #625E57 !important;
        font-size: 1.06rem;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }

    /* Section labels */
    .op-section-label {
        margin-top: 0.2rem;
        margin-bottom: 0.15rem;
        font-size: 0.72rem;
    }

    /* Inputs — black editor/code-block feel */
    div[data-baseweb="input"] {
        background: #111111 !important;
        border: 2px solid #111111 !important;
        border-radius: 8px !important;
        box-shadow: 5px 5px 0 #E0D9CD !important;
    }

    div[data-baseweb="input"] input {
        color: #F7F3EA !important;
        font-family: "SFMono-Regular", Consolas, monospace !important;
        font-size: 0.88rem !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #8E8A82 !important;
    }

    /* Buttons */
    .stButton button {
        background: #F4F0E8 !important;
        color: #111111 !important;
        border: 1px solid #BDB5A8 !important;
        border-radius: 7px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    .stButton button:hover {
        border-color: #111111 !important;
        background: #EAE4D9 !important;
    }

    button[kind="primary"] {
        background: #C80E18 !important;
        border-color: #C80E18 !important;
        color: #FFFFFF !important;
        border-radius: 7px !important;
        font-weight: 800 !important;
        box-shadow: 4px 4px 0 #111111 !important;
    }

    button[kind="primary"]:hover {
        background: #A70D16 !important;
        border-color: #A70D16 !important;
        transform: translate(-1px, -1px);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stButton"] button {
        min-height: 2.6rem !important;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #625E57 !important;
        font-size: 0.84rem !important;
    }

    /* Selects / sliders */
    div[data-baseweb="select"] > div {
        background: #111111 !important;
        border-color: #111111 !important;
        color: #F7F3EA !important;
    }

    div[data-testid="stSlider"] {
        color: #C80E18 !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        background: #FFF8D9 !important;
        border: 1px solid #D8C56A !important;
        color: #111111 !important;
        border-radius: 8px !important;
    }

    /* Empty state */
    .op-empty {
        margin: 0.8rem auto 0;
        max-width: 700px;
        padding: 1.7rem 1.8rem;
        border: 1px solid #D5CFC4;
        border-radius: 10px;
        background: #ECE6DC;
        text-align: center;
    }

    .op-empty-icon {
        width: 38px;
        height: 38px;
        margin: 0 auto 0.75rem;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        background: #111111;
        font-size: 1rem;
    }

    .op-empty-kicker {
        font-size: 0.65rem;
        letter-spacing: 0.13em;
        font-weight: 900;
        color: #A70D16 !important;
        margin-bottom: 0.4rem;
    }

    .op-empty-title {
        font-size: 1.1rem;
        font-weight: 850;
        color: #111111 !important;
        margin-bottom: 0.25rem;
    }

    .op-empty-copy {
        font-size: 0.84rem;
        color: #706B63 !important;
    }

    /* Metrics/cards */
    div[data-testid="stMetric"] {
        background: #ECE6DC;
        border: 1px solid #D5CFC4;
        border-radius: 8px;
        padding: 0.8rem;
    }

    /* Links */
    a {
        color: #A70D16 !important;
        font-weight: 650;
    }

    /* Final text-contrast safety net for Streamlit buttons */
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[kind="primary"] p,
    div[data-testid="stButton"] button[kind="primary"] span,
    div[data-testid="stButton"] button[kind="primary"] div {
        background: #F7F2E9 !important;
        color: #1C1B19 !important;
        -webkit-text-fill-color: #1C1B19 !important;
    }

    div[data-testid="stHorizontalBlock"] button[kind="primary"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"] *,
    div[data-testid="stHorizontalBlock"] button[kind="primary"] p,
    div[data-testid="stHorizontalBlock"] button[kind="primary"] span {
        background: transparent !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    button[kind="secondary"] *,
    button[kind="secondary"] p,
    button[kind="secondary"] span,
    button[kind="secondary"] div {
        color: #3F3B36 !important;
        -webkit-text-fill-color: #3F3B36 !important;
    }

        /* =========================================================
       CONTRIBUTION RESULTS
       ========================================================= */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FBF8F1 !important;
        border: 1px solid #D5CFC4 !important;
        border-radius: 10px !important;
        box-shadow: 4px 4px 0 #E5DED2 !important;
        padding: 0.35rem !important;
        margin: 0.9rem 0 !important;
    }

    .op-issue-number {
        color: #A70D16 !important;
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .op-issue-title {
        color: #111111 !important;
        font-size: 1.55rem;
        line-height: 1.12;
        font-weight: 850;
        letter-spacing: -0.035em;
        margin-bottom: 0.6rem;
    }

    .op-issue-description {
        color: #625E57 !important;
        font-size: 0.96rem;
        line-height: 1.6;
        max-width: 780px;
    }

    .op-issue-tags {
        margin-top: 0.8rem;
    }

    .op-issue-tag {
        display: inline-block;
        padding: 0.22rem 0.48rem;
        margin: 0 0.3rem 0.25rem 0;
        border: 1px solid #CFC7BB;
        border-radius: 999px;
        background: #F0EBE2;
        color: #393631 !important;
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: 0.67rem;
    }

    .op-match-score {
        text-align: right;
        padding-top: 0.15rem;
    }

    .op-match-number {
        color: #A70D16 !important;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2.6rem;
        line-height: 0.95;
        font-weight: 700;
        letter-spacing: -0.06em;
    }

    .op-match-label {
        color: #777169 !important;
        font-size: 0.62rem;
        letter-spacing: 0.14em;
        font-weight: 900;
        margin-top: 0.35rem;
    }

    .op-why {
        border-top: 1px solid #DDD6CA;
        margin-top: 1rem;
        padding-top: 0.8rem;
    }

    .op-why-title {
        color: #111111 !important;
        font-size: 0.66rem;
        letter-spacing: 0.13em;
        font-weight: 900;
        margin-bottom: 0.45rem;
    }

    .op-reason {
        color: #625E57 !important;
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 0.12rem 0;
    }

    .op-ai-kicker {
        color: #A70D16 !important;
        font-size: 0.68rem;
        letter-spacing: 0.13em;
        font-weight: 900;
        margin-top: 0.4rem;
        margin-bottom: 0.55rem;
    }

    .op-ai-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1.5rem;
        padding: 1.25rem 1.35rem;
        background: #111111;
        color: #F7F3EA;
        border-radius: 9px;
        box-shadow: 5px 5px 0 #D8D0C4;
    }

    .op-ai-title {
        color: #F7F3EA !important;
        font-size: 1.45rem;
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .op-ai-repo {
        color: #AAA49B !important;
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: 0.75rem;
        margin-top: 0.35rem;
    }

    .op-ai-score {
        text-align: right;
        flex-shrink: 0;
    }

    .op-ai-score strong {
        display: block;
        color: #F1D84B !important;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2rem;
        line-height: 1;
    }

    .op-ai-score span {
        color: #AAA49B !important;
        font-size: 0.58rem;
        letter-spacing: 0.13em;
        font-weight: 900;
    }

    .op-ai-note {
        margin: 0.9rem 0;
        padding: 0.7rem 0.9rem;
        background: #FFF8D9;
        border-left: 3px solid #D4BC28;
        color: #5F5849 !important;
        font-size: 0.78rem;
        line-height: 1.5;
    }

    div[data-testid="stMetric"] {
        background: #FBF8F1;
        border: 1px solid #D5CFC4;
        border-radius: 8px;
        padding: 0.75rem;
        box-shadow: 3px 3px 0 #E5DED2;
    }

    div[data-testid="stMetricLabel"] {
        color: #777169 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #111111 !important;
    }

    /* Responsive */
    @media (max-width: 900px) {
        [data-testid="stAppViewContainer"] .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .op-hero-title {
            font-size: 3.1rem;
        }
    }

    @media (max-width: 600px) {
        .op-hero-title {
            font-size: 2.5rem;
        }

        .op-brand-name {
            font-size: 1.75rem;
        }
    }
    
    /* FINAL BUTTON RESET — flat, normal controls */
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stHorizontalBlock"] button,
    div[data-testid="stHorizontalBlock"] button * {
        box-shadow: none !important;
        transform: none !important;
    }

    /* Active navigation: simple text, no box */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background: transparent !important;
        border: 0 !important;
        border-bottom: 2px solid #A70D16 !important;
        border-radius: 0 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    /* Main actions: one clean rectangular button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #F7F2E9 !important;
        border: 1px solid #1C1B19 !important;
        border-radius: 6px !important;
        color: #1C1B19 !important;
        -webkit-text-fill-color: #1C1B19 !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #1C1B19 !important;
        border-color: #1C1B19 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* FINAL: single-box red action buttons */
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[kind="primary"] p,
    div[data-testid="stButton"] button[kind="primary"] span,
    div[data-testid="stButton"] button[kind="primary"] div {
        background: #A70D16 !important;
        border: 1px solid #A70D16 !important;
        border-radius: 6px !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        box-shadow: none !important;
        outline: none !important;
        transform: none !important;
        text-shadow: none !important;
        font-weight: 800 !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover,
    div[data-testid="stButton"] button[kind="primary"]:hover *,
    div[data-testid="stButton"] button[kind="primary"]:hover p,
    div[data-testid="stButton"] button[kind="primary"]:hover span {
        background: #8F0B13 !important;
        border-color: #8F0B13 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        box-shadow: none !important;
        outline: none !important;
        transform: none !important;
    }

    /* Remove any pseudo-element decorations that can create a layered look */
    div[data-testid="stButton"] button[kind="primary"]::before,
    div[data-testid="stButton"] button[kind="primary"]::after {
        content: none !important;
        display: none !important;
    }

    /* Larger red editorial section labels / eyebrow lines */
    .eyebrow,
    .section-eyebrow,
    .dp-eyebrow,
    [class*="eyebrow"] {
        font-size: 0.78rem !important;
        line-height: 1.2 !important;
        letter-spacing: 0.14em !important;
        font-weight: 850 !important;
        color: #A70D16 !important;
    }


    /* Larger OpenPilot application name */
    .dp-brand,
    .brand,
    [class*="brand"] {
        font-size: 1.65rem !important;
        line-height: 1.05 !important;
        font-weight: 900 !important;
        letter-spacing: -0.035em !important;
    }

    .dp-brand .dp-logo,
    .brand .brand-mark,
    [class*="brand"] [class*="logo"],
    [class*="brand"] [class*="mark"] {
        font-size: 1.45rem !important;
    }

</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "repository" not in st.session_state:
    st.session_state.repository = None

if "issues" not in st.session_state:
    st.session_state.issues = []

if "ranked_issues" not in st.session_state:
    st.session_state.ranked_issues = []

if "skills" not in st.session_state:
    st.session_state.skills = []

if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""

if "selected_issue" not in st.session_state:
    st.session_state.selected_issue = None

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "history" not in st.session_state:
    st.session_state.history = []

if "contributions" not in st.session_state:
    st.session_state.contributions = []


# ============================================================
# SERVICES
# ============================================================

github = GitHubService()
analyzer = RepositoryAnalyzer(github)

try:
    ai = AIService()
    ai_available = True
except Exception:
    ai = None
    ai_available = False


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_issue_number(issue):
    if issue.get("number"):
        return issue["number"]

    url = issue.get("html_url", "")

    import re

    match = re.search(
        r"/issues/(\d+)",
        url
    )

    if match:
        return match.group(1)

    return ""


def get_labels(issue):

    return [
        label.get("name", "")
        for label in issue.get("labels", [])
        if label.get("name")
    ]


def get_difficulty(issue):

    labels = [
        x.lower()
        for x in get_labels(issue)
    ]

    if any(
        x in labels
        for x in [
            "good first issue",
            "beginner",
            "easy"
        ]
    ):
        return "Beginner"

    if any(
        x in labels
        for x in [
            "hard",
            "difficult",
            "advanced"
        ]
    ):
        return "Advanced"

    return "Intermediate"


def get_issue_type(issue):

    labels = [
        x.lower()
        for x in get_labels(issue)
    ]

    if "bug" in labels:
        return "Bug"

    if any(
        x in labels
        for x in [
            "enhancement",
            "feature",
            "feature request"
        ]
    ):
        return "Feature"

    if any(
        x in labels
        for x in [
            "documentation",
            "docs"
        ]
    ):
        return "Documentation"

    return "Other"


def get_match_reasons(item, repository):

    reasons = []

    matched = item.get(
        "matched_skills",
        []
    )

    if matched:
        reasons.append(
            f"✓ {', '.join(matched)} matches your skills"
        )

    if item.get("beginner_labels"):
        reasons.append(
            "✓ Beginner-friendly issue"
        )

    if item.get("activity_score", 0) > 0:
        reasons.append(
            "✓ Active issue discussion"
        )

    if item.get("description_score", 0) > 0:
        reasons.append(
            "✓ Detailed issue requirements"
        )

    language = repository.get(
        "language"
    )

    if language:
        reasons.append(
            f"✓ Repository uses {language}"
        )

    if not reasons:
        reasons.append(
            "✓ Matched against your selected skills"
        )

    return reasons[:4]


# ============================================================
# ANALYZE REPOSITORY
# ============================================================

def analyze_repository():

    repo_url = st.session_state.repo_input.strip()

    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
        return

    if not st.session_state.skills:
        st.warning("Please add at least one skill first.")
        return

    try:
        owner, repo = parse_github_url(repo_url)

    except ValueError as error:
        st.error(str(error))
        return

    try:

        with st.status(
            f"Analyzing {owner}/{repo}...",
            expanded=True
        ) as status:

            st.write("Connecting to GitHub...")

            repository = analyzer.analyze(
                owner,
                repo
            )

            st.write("✓ Repository information fetched")

            st.write("Fetching open issues...")

            issues = github.get_issues(
                owner,
                repo
            )

            st.write(
                f"✓ Found {len(issues)} open issues"
            )

            st.write(
                "Matching issues with your skills..."
            )

            ranked = rank_issues(
                issues,
                st.session_state.skills
            )

            st.write(
                "✓ Match scores calculated"
            )

            st.session_state.repository = repository
            st.session_state.issues = issues
            st.session_state.ranked_issues = ranked
            st.session_state.repo_url = repo_url

            history_entry = {
                "repo_url": repo_url,
                "name": repository.get("name") or f"{owner}/{repo}",
                "issues": len(issues),
                "skills": list(st.session_state.skills),
            }

            st.session_state.history = [
                entry
                for entry in st.session_state.history
                if entry.get("repo_url") != repo_url
            ]
            st.session_state.history.insert(0, history_entry)
            st.session_state.history = st.session_state.history[:10]

            status.update(
                label="Repository analysis complete",
                state="complete",
                expanded=False
            )

    except Exception as error:

        st.error("Repository analysis failed.")

        st.code(
            str(error)
        )


# ============================================================
# AI PLAN
# ============================================================

def generate_ai_plan(item):

    if not ai_available:

        st.error(
            "Gemini AI is not configured. "
            "Check your GEMINI_API_KEY."
        )

        return

    try:

        st.session_state.selected_issue = (
            item["issue"]
        )

        with st.spinner(
            "Generating contribution plan..."
        ):

            result = ai.analyze_issue(
                item["issue"],
                st.session_state.repository,
                st.session_state.skills
            )

        st.session_state.ai_result = result

        issue_url = item["issue"].get("html_url", "")
        contribution = {
            "issue": item["issue"].get("title", "Selected issue"),
            "issue_number": get_issue_number(item["issue"]),
            "issue_url": issue_url,
            "repository": st.session_state.repository.get("name", ""),
            "score": item.get("score", 0),
            "plan": result,
        }

        st.session_state.contributions = [
            entry
            for entry in st.session_state.contributions
            if entry.get("issue_url") != issue_url
        ]
        st.session_state.contributions.insert(0, contribution)
        st.session_state.contributions = st.session_state.contributions[:10]

        st.session_state.page = "Contributions"

    except Exception:

        st.error(
            "Unable to generate the AI plan. "
            "Please try again."
        )


# ============================================================
# ============================================================
# BRAND + NAVIGATION
# ============================================================

st.markdown(
    """
    <div class="op-brand">
        <span class="op-brand-mark">↗</span>
        <span class="op-brand-name">OpenPilot</span>
    </div>
    """,
    unsafe_allow_html=True,
)

nav_left, n1, n2, n3, n4, nav_right = st.columns(
    [2.8, 1, 1, 1, 1, 2.8]
)

with n1:
    if st.button(
        "Dashboard",
        key="nav_dashboard",
        type="primary" if st.session_state.page == "Dashboard" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Dashboard"
        st.rerun()

with n2:
    if st.button(
        "Contributions",
        key="nav_contributions",
        type="primary" if st.session_state.page == "Contributions" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Contributions"
        st.rerun()

with n3:
    if st.button(
        "History",
        key="nav_history",
        type="primary" if st.session_state.page == "History" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "History"
        st.rerun()

with n4:
    if st.button(
        "Settings",
        key="nav_settings",
        type="primary" if st.session_state.page == "Settings" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Settings"
        st.rerun()

st.divider()


# ============================================================
# NON-DASHBOARD PAGES
# ============================================================

if st.session_state.page == "Contributions":
    st.title("Contributions")
    st.caption("AI plans generated from issues you selected.")

    if not st.session_state.contributions:
        st.info(
            "No contribution plans yet. Go to Dashboard, "
            "analyze a repository, and generate an AI plan."
        )
    else:
        for index, contribution in enumerate(st.session_state.contributions):
            st.subheader(
                f"#{contribution.get('issue_number', '')} — "
                f"{contribution.get('issue', 'Untitled issue')}"
            )

            meta1, meta2 = st.columns([4, 1])
            with meta1:
                st.caption(contribution.get("repository", ""))
                if contribution.get("issue_url"):
                    st.link_button(
                        "View issue on GitHub ↗",
                        contribution["issue_url"],
                        key=f"contribution_link_{index}",
                    )

            with meta2:
                st.metric("Match", f"{int(contribution.get('score', 0))}%")

            st.markdown(contribution.get("plan", "No plan available."))
            st.divider()

elif st.session_state.page == "History":
    st.title("History")
    st.caption("Repositories analyzed during this session.")

    if not st.session_state.history:
        st.info("No repository analyses yet.")
    else:
        for index, entry in enumerate(st.session_state.history):
            st.subheader(entry.get("name", "Repository"))
            st.caption(entry.get("repo_url", ""))

            h1, h2, h3 = st.columns(3)
            with h1:
                st.metric("Open Issues", entry.get("issues", 0))
            with h2:
                st.metric("Skills Used", len(entry.get("skills", [])))
            with h3:
                if st.button(
                    "Open in Dashboard",
                    key=f"history_open_{index}",
                    use_container_width=True,
                ):
                    st.session_state.repo_input = entry.get("repo_url", "")
                    st.session_state.page = "Dashboard"
                    st.rerun()

            if entry.get("skills"):
                st.caption("Skills: " + " · ".join(entry["skills"]))

            st.divider()

elif st.session_state.page == "Settings":
    st.title("Settings")
    st.caption("Connection and developer preferences.")

    st.subheader("GitHub")
    st.success("● GitHub service available")

    st.subheader("AI")
    if ai_available:
        st.success("● Gemini AI configured")
    else:
        st.warning(
            "Gemini AI is not configured. "
            "Check your GEMINI_API_KEY."
        )

    st.subheader("Current skills")
    if st.session_state.skills:
        st.write(" · ".join(st.session_state.skills))
    else:
        st.caption("No skills added yet.")

    st.subheader("Session")
    st.caption(
        "Your repository analyses and contribution plans are kept "
        "in the current Streamlit session."
    )

elif st.session_state.page != "Dashboard":
    st.session_state.page = "Dashboard"
    st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    # HERO
    # ============================================================

    st.markdown(
        '<div class="op-eyebrow">OPEN-SOURCE CONTRIBUTION COPILOT</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="op-hero-title">Find GitHub issues you can actually contribute to.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="op-hero-copy">AI-powered repository analysis, skill matching, and contribution planning for developers.</div>',
        unsafe_allow_html=True,
    )

    # ============================================================
    # REPOSITORY
    # ============================================================

    st.divider()

    st.markdown(
        '<div class="op-section-label">REPOSITORY</div>',
        unsafe_allow_html=True,
    )
    st.subheader("GitHub Repository")

    st.caption(
        "Paste a repository to discover issues matched to your skills."
    )

    repo_col, button_col = st.columns(
        [5, 1]
    )

    with repo_col:

        st.text_input(
            "Repository URL",
            placeholder="github.com/owner/repository",
            key="repo_input",
            label_visibility="collapsed"
        )

    with button_col:

     if st.button(
        "Analyze Repository →",
        type="primary",
        use_container_width=True
    ):
        analyze_repository()

    # ============================================================
    # SKILLS
    # ============================================================

    st.markdown(
        '<div class="op-section-label">YOUR SKILLS</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Skills")

    skill_col, add_col = st.columns(
        [5, 1]
    )

    with skill_col:

        skill_input = st.text_input(
            "Skill",
            placeholder="Python, Git, Docker, DevOps...",
            key="skill_input",
            label_visibility="collapsed"
        )

    with add_col:

        if st.button(
            "+ Add Skill",
            use_container_width=True
        ):

            skill = skill_input.strip()

            if skill:

                if skill not in st.session_state.skills:

                    st.session_state.skills.append(
                        skill
                    )

                    st.rerun()


    if st.session_state.skills:

        chip_count = min(len(st.session_state.skills), 6)
        chip_cols = st.columns(chip_count)

        for index, skill in enumerate(st.session_state.skills):
            with chip_cols[index % chip_count]:
                if st.button(
                    f"{skill}  ×",
                    key=f"remove_{index}",
                    use_container_width=True,
                ):
                    st.session_state.skills.pop(index)
                    st.rerun()

    else:
        st.caption(
            "Add the languages, tools, and technologies you know."
        )


    # ============================================================
    # EMPTY STATE
    # ============================================================

    if not st.session_state.repository:

        st.divider()

        st.markdown(
            """
            <div class="op-empty">
                <div class="op-empty-icon">⌁</div>
                <div class="op-empty-kicker">READY WHEN YOU ARE</div>
                <div class="op-empty-title">No repository analyzed yet</div>
                <div class="op-empty-copy">
                    Paste a GitHub repository above to get started.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ============================================================
    # REPOSITORY OVERVIEW
    # ============================================================

    if st.session_state.repository:

        repository = (
            st.session_state.repository
        )

        st.divider()

        st.subheader(
            "Repository Overview"
        )

        st.caption(
            repository.get(
                "description",
                "GitHub repository"
            )
            or "GitHub repository"
        )

        metrics = st.columns(4)

        with metrics[0]:

            st.metric(
                "Language",
                repository.get(
                    "language",
                    "Unknown"
                )
                or "Unknown"
            )

        with metrics[1]:

            st.metric(
                "Stars",
                f"{repository.get('stars', 0):,}"
            )

        with metrics[2]:

            st.metric(
                "Forks",
                f"{repository.get('forks', 0):,}"
            )

        with metrics[3]:

            st.metric(
                "Open Issues",
                f"{repository.get('open_issues', 0):,}"
            )


    # ============================================================
    # CONTRIBUTION OPPORTUNITIES
    # ============================================================

    if st.session_state.ranked_issues:

        st.divider()

        st.markdown(
            '<div class="op-section-label">CONTRIBUTION OPPORTUNITIES</div>',
            unsafe_allow_html=True,
        )

        st.subheader(
            "Issues you can actually contribute to"
        )

        st.caption(
            "Ranked by how well they match your skills."
        )

        filters = st.columns(5)

        repository_language = (
            st.session_state.repository.get(
                "language"
            )
        )

        with filters[0]:

            language_options = ["All"]

            if repository_language:
                language_options.append(
                    repository_language
                )

            selected_language = st.selectbox(
                "Language",
                language_options
            )

        with filters[1]:

            selected_difficulty = st.selectbox(
                "Difficulty",
                [
                    "All",
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ]
            )

        with filters[2]:

            selected_type = st.selectbox(
                "Issue Type",
                [
                    "All",
                    "Bug",
                    "Feature",
                    "Documentation",
                    "Other"
                ]
            )

        with filters[3]:

            minimum_score = st.slider(
                "Minimum Match",
                0,
                100,
                0,
                5
            )

        with filters[4]:

            selected_sort = st.selectbox(
                "Sort",
                [
                    "Best Match",
                    "Newest"
                ]
            )


        filtered = []

        for item in st.session_state.ranked_issues:

            issue = item["issue"]

            if item["score"] < minimum_score:
                continue

            if (
                selected_difficulty != "All"
                and get_difficulty(issue)
                != selected_difficulty
            ):
                continue

            if (
                selected_type != "All"
                and get_issue_type(issue)
                != selected_type
            ):
                continue

            if (
                selected_language != "All"
                and repository_language
                != selected_language
            ):
                continue

            filtered.append(item)


        if selected_sort == "Best Match":

            filtered.sort(
                key=lambda x: x["score"],
                reverse=True
            )

        else:

            filtered.sort(
                key=lambda x: x["issue"].get(
                    "created_at",
                    ""
                ),
                reverse=True
            )


        if not filtered:

            st.warning(
                "No matching issues found. "
                "Try changing your filters."
            )


        # ========================================================
        # ISSUE CARDS — editorial developer cards
        # ========================================================

        for item in filtered:

            issue = item["issue"]

            number = get_issue_number(issue)

            title = issue.get(
                "title",
                "Untitled Issue"
            )

            description = (
                issue.get("body")
                or "No description provided."
            )

            if len(description) > 280:

                description = (
                    description[:280]
                    + "..."
                )

            score = int(
                item["score"]
            )

            labels = get_labels(issue)

            labels_html = "".join(
                f'<span class="op-issue-tag">{label}</span>'
                for label in labels[:5]
            )

            reasons = get_match_reasons(
                item,
                repository
            )

            reasons_html = "".join(
                f'<div class="op-reason">✓ {reason.lstrip("✓ ").strip()}</div>'
                for reason in reasons[:4]
            )

            issue_url = issue.get(
                "html_url",
                "#"
            )

            with st.container(border=True):

                left, right = st.columns(
                    [5, 1]
                )

                with left:

                    st.markdown(
                        f'''
                        <div class="op-issue-number">#{number}</div>
                        <div class="op-issue-title">{title}</div>
                        <div class="op-issue-description">{description}</div>
                        <div class="op-issue-tags">{labels_html}</div>
                        ''',
                        unsafe_allow_html=True,
                    )

                with right:

                    st.markdown(
                        f'''
                        <div class="op-match-score">
                            <div class="op-match-number">{score}%</div>
                            <div class="op-match-label">MATCH</div>
                        </div>
                        ''',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f'''
                    <div class="op-why">
                        <div class="op-why-title">WHY THIS MATCHES</div>
                        {reasons_html}
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )

                action1, action2, spacer = st.columns(
                    [1.15, 1.35, 4]
                )

                with action1:

                    st.link_button(
                        "View Issue ↗",
                        issue_url,
                        use_container_width=True
                    )

                with action2:

                    if st.button(
                        "Generate AI Plan →",
                        key=f"plan_{number}",
                        use_container_width=True
                    ):

                        generate_ai_plan(
                            item
                        )



    # ============================================================
    # AI PLAN
    # ============================================================

    if (
        st.session_state.ai_result
        and st.session_state.selected_issue
    ):

        issue = (
            st.session_state.selected_issue
        )

        st.divider()

        selected_score = 0

        for item in st.session_state.ranked_issues:

            if (
                item["issue"].get("html_url")
                == issue.get("html_url")
            ):

                selected_score = item["score"]
                break

        st.markdown(
            '<div class="op-ai-kicker">AI CONTRIBUTION PLAN</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'''
            <div class="op-ai-header">
                <div>
                    <div class="op-ai-title">{issue.get("title", "Selected issue")}</div>
                    <div class="op-ai-repo">
                        {st.session_state.repository.get("name", "")}
                    </div>
                </div>
                <div class="op-ai-score">
                    <strong>{int(selected_score)}%</strong>
                    <span>MATCH</span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.markdown(
            '''
            <div class="op-ai-note">
                OpenPilot's plan is a draft based on the repository and issue context.
                Verify repository-specific details before implementing.
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.markdown(
            st.session_state.ai_result
        )



    # ============================================================
    # FOOTER
    # ============================================================

    st.divider()

    st.caption(
        "OpenPilot · Open-Source Contribution Copilot"
    )
