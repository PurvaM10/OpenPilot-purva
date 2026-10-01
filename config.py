import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st

    GITHUB_TOKEN = st.secrets.get(
        "GITHUB_TOKEN",
        os.getenv("GITHUB_TOKEN", "")
    )

    GEMINI_API_KEY = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY", "")
    )

    GEMINI_MODEL = st.secrets.get(
        "GEMINI_MODEL",
        os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    )

except Exception:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )

GITHUB_API = "https://api.github.com"