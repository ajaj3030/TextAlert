import pytest
from src.scraper import NewsScraper, NewsScraperError

def test_fetch_feed():
    scraper = NewsScraper()
    url = "https://arxiv.org/rss/cs.CV"
    content = scraper.fetch_feed(url)
    assert content is not None
    assert "<rss" in content

def test_parse_feed():
    scraper = NewsScraper()
    sample_feed = """
    <rss>
        <channel>
            <item>
                <title>Sample Article</title>
                <link>http://example.com/article</link>
                <description>This is a sample article description.</description>
                <pubDate>Mon, 01 Jan 2023 00:00:00 +0000</pubDate>
            </item>
        </channel>
    </rss>
    """
    articles = scraper.parse_feed(sample_feed, "computer vision")
    assert len(articles) == 1
    assert articles[0].title == "Sample Article"
    assert articles[0].url == "http://example.com/article"
    assert articles[0].content == "This is a sample article description." 