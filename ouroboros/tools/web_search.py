import os
import json
import httpx
from typing import Dict, List
from .base import ToolBase

class WebSearch(ToolBase):
    name = 'web_search'
    description = 'Search the web via DuckDuckGo API. Falls back to Google Programmable Search if quota exceeded.'
    
    def __init__(self):
        self.duckduckgo_url = 'https://api.duckduckgo.com/'
        self.google_url = 'https://www.googleapis.com/customsearch/v1'
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_cx = os.getenv('GOOGLE_CX')
        
    def _duckduckgo_search(self, query: str) -> Dict:
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1',
            't': 'ouroboros'
        }
        response = httpx.get(self.duckduckgo_url, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()

    def _google_search(self, query: str) -> Dict:
        if not all([self.google_api_key, self.google_cx]):
            raise ValueError('GOOGLE_API_KEY and GOOGLE_CX required for fallback')
        
        params = {
            'key': self.google_api_key,
            'cx': self.google_cx,
            'q': query,
            'num': 3
        }
        response = httpx.get(self.google_url, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()

    def run(self, query: str) -> Dict:
        try:
            # Primary: DuckDuckGo (500 req/day)
            result = self._duckduckgo_search(query)
            return {
                'results': result.get('Results', [])[:3],  # FIX: Capitalized 'Results' per API spec
                'source': 'duckduckgo'
            }
        except Exception as e:
            if 'GOOGLE_API_KEY' in str(e):
                raise
            # Fallback: Google Programmable Search (100 free req/day)
            try:
                google_result = self._google_search(query)
                return {
                    'results': [{
                        'title': i['title'],
                        'snippet': i['snippet'],
                        'url': i['link']
                    } for i in google_result.get('items', [])[:3]],
                    'source': 'google'
                }
            except Exception as fallback_error:
                return {
                    'error': str(fallback_error),
                    'suggestion': 'Configure GOOGLE_API_KEY and GOOGLE_CX for fallback search'
                }