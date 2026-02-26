from .tool import Tool
import json
import re
from browser import browse_page

class WebSearchTool(Tool):
    name = 'web_search'
    description = 'Search the web via DuckDuckGo API (fallback when OpenAI key missing)'
    
    def call(self, query: str) -> dict:
        # DuckDuckGo API call
        url = f'https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1&t=ouroboros'
        response = browse_page(url, output='text')
        
        try:
            data = json.loads(response)
            results = []
            # Process main results
            for result in data.get('Results', [])[:3]:
                results.append({
                    'title': result.get('Text', ''),
                    'url': result.get('FirstURL', ''),
                    'snippet': re.sub('<[^<]+?>', '', result.get('Abstract', ''))[:200]
                })
            return {
                'answer': f'Found {len(results)} results via DuckDuckGo',
                'sources': results
            }
        except Exception as e:
            return {'error': f'DuckDuckGo processing failed: {str(e)}'}
        
    def schema(self) -> dict:
        return {
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': 'Search query'}
            },
            'required': ['query']
        }