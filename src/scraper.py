import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from .models import Article

class NewsScraperError(Exception):
    pass

class NewsScraper:
    def __init__(self):
        # For now, we'll use a simple dictionary to track seen URLs
        self.seen_urls = set()
        
        # Map topics to RSS feeds (expand this based on needs)
        self.topic_feeds = {
            "computer vision": [
                "https://arxiv.org/rss/cs.CV",
                "https://medium.com/feed/tag/computer-vision"
            ],
            "ai robotics": [
                "https://arxiv.org/rss/cs.RO",
                "https://robotics.news/feed"
            ]
        }

    def fetch_feed(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise NewsScraperError(f"Failed to fetch feed {url}: {str(e)}")

    def parse_feed(self, content: str, topic: str) -> List[Article]:
        articles = []
        soup = BeautifulSoup(content, 'lxml-xml')
        
        for item in soup.find_all('item'):
            url = item.link.text if item.link else None
            if not url or url in self.seen_urls:
                continue
                
            article = Article(
                title=item.title.text if item.title else "No title",
                url=url,
                topic=topic,
                content=item.description.text if item.description else "",
                published_date=datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S %z') 
                if item.pubDate else None
            )
            
            articles.append(article)
            self.seen_urls.add(url)
            
        return articles

    def get_articles_for_topic(self, topic: str) -> List[Article]:
        articles = []
        feeds = self.topic_feeds.get(topic.lower(), [])
        
        for feed_url in feeds:
            try:
                content = self.fetch_feed(feed_url)
                articles.extend(self.parse_feed(content, topic))
            except (NewsScraperError, Exception) as e:
                print(f"Error processing feed {feed_url}: {str(e)}")
                continue
                
        return articles 