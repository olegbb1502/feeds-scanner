from typing import Dict, List

# RSS Feed URLs
RSS_FEEDS: Dict[str, str] = {
    'reuters': 'http://feeds.reuters.com/reuters/topNews',
    'bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
    'techcrunch': 'https://techcrunch.com/feed/',
    'wired': 'https://www.wired.com/feed/rss',
    'forbes': 'https://www.forbes.com/business/feed/',
}

# Semantic search settings
SIMILARITY_THRESHOLD = 0.6
MODEL_NAME = 'all-MiniLM-L6-v2'

# File paths
KEYWORDS_FILE = 'keywords.tsv'
OUTPUT_DIR = 'output'

# Scheduler settings
SCHEDULE_TIME = '01:00'  # 1:00 AM 