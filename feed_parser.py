import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

import feedparser
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import (
    RSS_FEEDS,
    SIMILARITY_THRESHOLD,
    MODEL_NAME,
    KEYWORDS_FILE,
    OUTPUT_DIR,
    SCHEDULE_TIME,
)

class NewsParser:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.keywords_dict = self._load_keywords()
        self.keyword_embeddings = self._create_keyword_embeddings()
        
    def _load_keywords(self) -> Dict[str, List[str]]:
        """Load keywords from TSV file."""
        keywords_dict = {}
        with open(KEYWORDS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) == 2:
                    category, keywords = row
                    keywords_dict[category] = [k.strip() for k in keywords.split(',')]
        return keywords_dict

    def _create_keyword_embeddings(self) -> Dict[str, np.ndarray]:
        """Create embeddings for all keywords."""
        embeddings = {}
        for category, keywords in self.keywords_dict.items():
            # Combine all keywords for a category into one string
            combined_keywords = ' '.join(keywords)
            embeddings[category] = self.model.encode(combined_keywords)
        return embeddings

    def _clean_html(self, html_content: str) -> str:
        """Remove HTML tags from content."""
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()

    def _extract_image(self, entry) -> str:
        """Extract first image URL from entry content."""
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if 'url' in media:
                    return media['url']
        
        if hasattr(entry, 'content'):
            for content in entry.content:
                soup = BeautifulSoup(content.value, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    return img['src']
        
        return ""

    def _is_relevant(self, title: str) -> List[str]:
        """Check if article is relevant based on semantic similarity."""
        print(f"\nAnalyzing title: {title}")
        title_embedding = self.model.encode(title)
        relevant_categories = []
        
        for category, embedding in self.keyword_embeddings.items():
            similarity = np.dot(title_embedding, embedding) / (
                np.linalg.norm(title_embedding) * np.linalg.norm(embedding)
            )
            print(f"Similarity with {category}: {similarity:.4f}")
            if similarity > SIMILARITY_THRESHOLD:
                relevant_categories.append(category)
        
        return relevant_categories

    def parse_feeds(self) -> List[Dict]:
        """Parse all RSS feeds and return relevant articles."""
        articles = []
        
        for source, url in RSS_FEEDS.items():
            try:
                print(f"\nFetching feed from: {url}")
                feed = feedparser.parse(url)
                print(f"Found {len(feed.entries)} entries")
                for entry in feed.entries:
                    title = entry.title
                    categories = self._is_relevant(title)
                    
                    if categories:
                        article = {
                            "title": title,
                            "categories": categories,
                            "text": self._clean_html(entry.summary if hasattr(entry, 'summary') else entry.description),
                            "image": self._extract_image(entry),
                            "source": source,
                            "link": entry.link,
                            "published": entry.published if hasattr(entry, 'published') else None
                        }
                        articles.append(article)
            except Exception as e:
                print(f"Error parsing {source}: {str(e)}")
        
        return articles

    def save_articles(self, articles: List[Dict]):
        """Save articles to JSON file."""
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        filename = os.path.join(OUTPUT_DIR, f"{datetime.now().strftime('%Y-%m-%d')}-news.json")
        with open(filename, 'w') as f:
            json.dump(articles, f, indent=2)
        print(f"Saved {len(articles)} articles to {filename}")

def run_parser():
    """Run the news parser."""
    parser = NewsParser()
    articles = parser.parse_feeds()
    parser.save_articles(articles)

def main():
    """Set up scheduler and run the parser."""
    # Run once immediately
    run_parser()

    scheduler = BlockingScheduler()
    # Schedule the job to run daily at 1:00 AM
    hour, minute = SCHEDULE_TIME.split(':')
    scheduler.add_job(
        run_parser,
        CronTrigger(hour=int(hour), minute=int(minute))
    )
    print(f"Starting scheduler. Will run daily at {SCHEDULE_TIME}")
    scheduler.start()

if __name__ == "__main__":
    main() 