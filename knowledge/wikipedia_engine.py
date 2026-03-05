"""
Wikipedia Knowledge Engine - No API Key Needed
"""

import urllib.request
import urllib.parse
import json
import re
import html
from pathlib import Path

class WikipediaEngine:
    """Access Wikipedia knowledge without API key"""
    
    def __init__(self):
        self.cache_file = Path('data/cache.json')
        self.cache = self.load_cache()
        self.headers = {
            'User-Agent': 'KingAssistant/1.0 (https://github.com/kingassistant)'
        }
        print("  • Wikipedia Engine: Ready")
    
    def load_cache(self):
        """Load cached knowledge"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        """Save to cache"""
        self.cache_file.parent.mkdir(exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def search(self, query: str) -> str:
        """Search Wikipedia for information"""
        # Check cache first
        cache_key = query.lower().strip()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try to get summary
        result = self.get_summary(query)
        if result:
            self.cache[cache_key] = result
            self.save_cache()
            return result
        
        # Try search
        result = self.search_articles(query)
        if result:
            self.cache[cache_key] = result
            self.save_cache()
            return result
        
        return None
    
    def get_summary(self, query: str) -> str:
        """Get Wikipedia summary"""
        try:
            # Clean query for URL
            clean_query = urllib.parse.quote(query.replace(' ', '_'))
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}"
            
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    title = data.get('title', query)
                    extract = data.get('extract', '')
                    
                    if extract:
                        # Clean up text
                        extract = re.sub(r'\s+', ' ', extract)
                        
                        response = f"📚 **{title}**\n\n{extract}"
                        
                        # Add description if available
                        if 'description' in data:
                            response = f"📚 **{title}** ({data['description']})\n\n{extract}"
                        
                        return response
        except:
            pass
        
        return None
    
    def search_articles(self, query: str) -> str:
        """Search for articles"""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 3,
                'utf8': 1
            }
            
            url = f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    search_results = data.get('query', {}).get('search', [])
                    
                    if search_results:
                        result = search_results[0]
                        title = html.unescape(result.get('title', ''))
                        snippet = html.unescape(result.get('snippet', ''))
                        
                        # Clean HTML tags from snippet
                        snippet = re.sub(r'<[^>]+>', '', snippet)
                        snippet = re.sub(r'\s+', ' ', snippet)
                        
                        return f"📚 **{title}**\n\n{snippet}\n\n(I found this on Wikipedia. Try a more specific search for full details.)"
        except:
            pass
        
        return None