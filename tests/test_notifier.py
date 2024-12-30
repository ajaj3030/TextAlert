from src.notifier import SMSNotifier, NotifierError
from src.models import Article
from src.config import Config

def test_format_message():
    config = Config(
        llm_provider="",
        llm_api_key="",
        twilio_account_sid="",
        twilio_auth_token="",
        twilio_from_phone="",
        twilio_to_phone="",
        topics=[],
        schedule_times=[]
    )
    notifier = SMSNotifier(config)
    articles = [
        Article(title="Test Article", url="http://example.com", topic="AI", content="", summary="This is a test summary.")
    ]
    messages = notifier.format_message(articles)
    assert len(messages) == 1
    assert "Test Article" in messages[0]
    assert "This is a test summary." in messages[0]
    assert "http://example.com" in messages[0] 