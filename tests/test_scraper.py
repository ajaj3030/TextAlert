import pytest
from src.scraper import NewsScraper, NewsScraperError
from datetime import datetime, timezone, timedelta

def test_fetch_feed():
    scraper = NewsScraper()
    url = "https://arxiv.org/rss/cs.CV"
    content = scraper.fetch_feed(url)
    assert content is not None
    assert "<rss" in content

def test_parse_feed():
    scraper = NewsScraper()
    current_time = datetime.now(timezone.utc)
    recent_date = current_time - timedelta(hours=12)
    
    sample_feed = f"""
    <rss>
        <channel>
            <item>
                <title>Sample Article</title>
                <link>http://example.com/article</link>
                <description>This is a sample article description.</description>
                <pubDate>{recent_date.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>
            </item>
        </channel>
    </rss>
    """
    articles = scraper.parse_feed(sample_feed, "computer vision")
    assert len(articles) == 1
    assert articles[0].title == "Sample Article"
    assert articles[0].url == "http://example.com/article"
    assert articles[0].content == "This is a sample article description."

def test_parse_arxiv_results():
    scraper = NewsScraper()
    articles = scraper.get_articles_for_topic("computer vision")
    
    if articles:  # Some days might not have new papers
        article = articles[0]
        assert article.title is not None
        assert article.url is not None
        assert article.published_date is not None
        assert article.relevance_score >= 0
        assert (datetime.now(timezone.utc) - article.published_date).days <= 1 

def test_parse_feed_with_dates():
    scraper = NewsScraper()
    current_time = datetime.now(timezone.utc)
    recent_date = current_time - timedelta(hours=12)
    old_date = current_time - timedelta(days=2)
    
    # Create test feed with both recent and old articles
    sample_feed = f"""
    <rss>
        <channel>
            <item>
                <title>Recent Article</title>
                <link>http://example.com/recent</link>
                <description>This is a recent article from MIT and Stanford.</description>
                <pubDate>{recent_date.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>
            </item>
            <item>
                <title>Old Article</title>
                <link>http://example.com/old</link>
                <description>This is an old article.</description>
                <pubDate>{old_date.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>
            </item>
        </channel>
    </rss>
    """
    
    articles = scraper.parse_feed(sample_feed, "computer vision")
    
    # Should only get the recent article
    assert len(articles) == 1
    assert articles[0].title == "Recent Article"
    assert articles[0].relevance_score > 0  # Should have some relevance score
    assert articles[0].published_date > (datetime.now(timezone.utc) - timedelta(days=1)) 