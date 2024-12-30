import pytest
from unittest.mock import Mock, patch
from src.config import load_config
from src.scraper import NewsScraper
from src.summarizer import Summarizer
from src.notifier import SMSNotifier
from src.models import Article

@patch('twilio.rest.Client')
@patch('anthropic.Anthropic')
def test_scrape_and_notify(mock_anthropic, mock_twilio):
    # Load real config from .env
    config = load_config()
    
    # Add max_articles verification
    assert config.max_articles is not None, "MAX_ARTICLES not found in .env"
    assert config.max_articles > 0, "MAX_ARTICLES must be greater than 0"
    
    # Verify config loaded correctly
    assert config.llm_provider == "anthropic", "LLM_PROVIDER should be set to 'anthropic' in .env"
    assert config.llm_api_key is not None, "LLM_API_KEY not found in .env"
    assert config.twilio_account_sid is not None, "TWILIO_ACCOUNT_SID not found in .env"
    assert config.twilio_auth_token is not None, "TWILIO_AUTH_TOKEN not found in .env"
    assert config.twilio_from_phone is not None, "TWILIO_FROM_PHONE not found in .env"
    assert config.twilio_to_phone is not None, "TWILIO_TO_PHONE not found in .env"
    
    # Mock Anthropic responses while using real credentials
    mock_anthropic_client = Mock()
    mock_response = Mock()
    mock_response.content = [Mock(text="This is a test summary generated with real credentials")]
    mock_anthropic_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_anthropic_client
    
    # Mock Twilio responses while using real credentials
    mock_messages = Mock()
    mock_messages.create = Mock()
    mock_twilio.return_value = Mock(messages=mock_messages)
    
    # Initialize components
    scraper = NewsScraper()
    summarizer = Summarizer(config)
    notifier = SMSNotifier(config)
    
    # Get real articles from RSS feed
    articles = scraper.get_articles_for_topic("computer vision")
    articles = articles[:config.max_articles]  # Take only max_articles
    assert len(articles) > 0, "No articles found in RSS feed"
    
    # Generate summaries for all articles
    for article in articles:
        try:
            article.summary = summarizer.summarize(article)
            assert article.summary is not None
            print(f"\nProcessing article: {article.title}")
            print(f"Generated summary: {article.summary}")
        except Exception as e:
            pytest.fail(f"Failed to generate summary: {str(e)}")
    
    # Send notification for all articles
    try:
        notifier.send_notifications(articles)
        expected_message = notifier.format_message(articles)[0]
        mock_messages.create(
            from_=config.twilio_from_phone,
            to=config.twilio_to_phone,
            body=expected_message
        )
        print(f"Notification would have been sent to: {config.twilio_to_phone}")
    except Exception as e:
        pytest.fail(f"Failed to send notification: {str(e)}")