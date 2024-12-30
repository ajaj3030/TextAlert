from unittest.mock import Mock, patch
from src.notifier import SMSNotifier, NotifierError
from src.models import Article
from src.config import Config, load_config

@patch('twilio.rest.Client')
def test_format_message(mock_client):
    config = load_config()
    notifier = SMSNotifier(config)
    
    # Create multiple test articles
    articles = [
        Article(title=f"Test Article {i}", 
               url=f"http://example.com/article{i}", 
               topic="AI", 
               content="", 
               summary=f"This is test summary {i}.")
        for i in range(3)
    ]
    
    messages = notifier.format_message(articles)
    assert len(messages) >= 1
    for i in range(3):
        assert f"Test Article {i}" in messages[0]
        assert f"This is test summary {i}" in messages[0]

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