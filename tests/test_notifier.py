from unittest.mock import Mock, patch
from src.notifier import SMSNotifier, NotifierError
from src.models import Article
from src.config import Config, load_config

@patch('twilio.rest.Client')
def test_format_message(mock_client):
    # Mock the Twilio client
    mock_instance = Mock()
    mock_client.return_value = mock_instance
    
    # Load config from .env
    config = load_config()
    
    notifier = SMSNotifier(config)
    articles = [
        Article(title="Test Article", url="http://example.com", topic="AI", content="", summary="This is a test summary.")
    ]
    messages = notifier.format_message(articles)
    assert len(messages) == 1
    assert "Test Article" in messages[0]
    assert "This is a test summary." in messages[0]
    assert "http://example.com" in messages[0]

@patch('twilio.rest.Client')
def test_send_notifications(mock_client):
    # Mock the Twilio client
    mock_instance = Mock()
    mock_messages = Mock()
    mock_instance.messages = mock_messages
    mock_client.return_value = mock_instance
    
    # Load config from .env
    config = load_config()
    
    notifier = SMSNotifier(config)
    articles = [
        Article(title="Test Article", url="http://example.com", topic="AI", content="", summary="This is a test summary.")
    ]
    notifier.send_notifications(articles)
    mock_messages.create()