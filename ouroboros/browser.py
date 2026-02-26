import os
import logging
import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify
from .utils import clean_url
from .llm import get_model_config

logger = logging.getLogger(__name__)

# Strip whitespace from model name to prevent 400 errors
current_model = os.getenv('OUROBOROS_MODEL', 'qwen/qwen3-235b-a22b-thinking-2507:free').strip()

# Get model config for token limits
model_config = get_model_config(current_model)
MAX_TOKENS = model_config.get('max_completion_tokens', 8192) if model_config else 8192