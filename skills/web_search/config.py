"""Configuration for the Web Search skill (Exa Labs API)."""

import os

EXA_API_BASE_URL = os.getenv("EXA_API_BASE_URL", "https://api.exa.ai")
EXA_API_KEY = os.getenv("EXA_API_KEY", "")
EXA_AUTH_HEADER = "x-api-key"

SEARCH_ENDPOINT = "/search"
CONTENTS_ENDPOINT = "/contents"
FIND_SIMILAR_ENDPOINT = "/find-similar"

DEFAULT_SEARCH_MODE = "auto"
DEFAULT_NUM_RESULTS = 10
DEFAULT_CONTENTS_EXTRACT = ["text"]

REQUEST_TIMEOUT_SECONDS = 30