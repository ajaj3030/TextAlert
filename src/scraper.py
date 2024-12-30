import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime, timezone, timedelta
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

    def calculate_relevance_score(self, article: Article) -> float:
        score = 0.0
        
        # Recency score (max 5 points)
        if article.published_date:
            hours_old = (datetime.now(timezone.utc) - article.published_date).total_seconds() / 3600
            recency_score = max(0, 5 - (hours_old / 24) * 5)  # Full points if < 24h old
            score += recency_score
        
        # Content length score (max 2 points)
        if article.content:
            content_length = len(article.content)
            content_score = min(2, content_length / 500)  # Adjusted threshold to be more lenient
            score += content_score
        
        # Institution/company mentions score (max 3 points)
        prestigious_institutions = ["MIT", "Stanford", "Berkeley", "Oxford", "Cambridge", "Google", "Microsoft", "DeepMind"]
        mentioned_institutions = sum(1 for inst in prestigious_institutions 
                                   if inst.lower() in (article.content + article.title).lower())
        institution_score = min(3, mentioned_institutions * 0.5)  # 0.5 points per mention, max 3
        score += institution_score
        
        return round(score, 2)  # Round to 2 decimal places for cleaner numbers

    def parse_feed(self, content: str, topic: str) -> List[Article]:
        articles = []
        soup = BeautifulSoup(content, 'lxml-xml')
        
        for item in soup.find_all('item'):
            url = item.link.text if item.link else None
            if not url or url in self.seen_urls:
                continue
            
            try:
                # Parse the publication date
                pub_date = None
                if item.pubDate:
                    try:
                        pub_date = datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S %z')
                    except ValueError:
                        try:
                            pub_date = datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S GMT')
                            pub_date = pub_date.replace(tzinfo=timezone.utc)
                        except ValueError:
                            print(f"Could not parse date: {item.pubDate.text}")
                            continue
                
                # Only include articles from the last 24 hours
                if pub_date and (datetime.now(timezone.utc) - pub_date) > timedelta(days=1):
                    continue
                
                article = Article(
                    title=item.title.text if item.title else "No title",
                    url=url,
                    topic=topic,
                    content=item.description.text if item.description else "",
                    published_date=pub_date,
                    relevance_score=0.0
                )
                
                # Calculate and set the relevance score
                article.relevance_score = self.calculate_relevance_score(article)
                
                if article.relevance_score > 0:  # Only add articles with positive relevance
                    articles.append(article)
                    self.seen_urls.add(url)
                
            except Exception as e:
                print(f"Error processing article {url}: {str(e)}")
                continue
        
        # Sort by relevance score
        articles.sort(key=lambda x: x.relevance_score, reverse=True)
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