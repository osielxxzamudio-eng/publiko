"""Configuration for the Investigacion skill (Exa Labs API for academic research)."""

import os

EXA_API_BASE_URL = os.getenv("EXA_API_BASE_URL", "https://api.exa.ai")
EXA_API_KEY = os.getenv("EXA_API_KEY", "")
EXA_AUTH_HEADER = "x-api-key"

SEARCH_ENDPOINT = "/search"
CONTENTS_ENDPOINT = "/contents"
FIND_SIMILAR_ENDPOINT = "/find-similar"

DEFAULT_SEARCH_MODE = "neural"
DEFAULT_NUM_RESULTS = 10
DEFAULT_CONTENTS_EXTRACT = ["text", "summaries"]

ACADEMIC_DOMAINS = [
    "arxiv.org",
    "scholar.google.com",
    "researchgate.net",
    "semanticscholar.org",
    "springer.com",
    "ieee.org",
    "acm.org",
    "sciencedirect.com",
    "jstor.org",
    "tandfonline.com",
]

RESEARCH_CATEGORIES = [
    "research paper",
    "academic",
    "scientific",
    "methodology",
    "literature review",
]

REQUEST_TIMEOUT_SECONDS = 30