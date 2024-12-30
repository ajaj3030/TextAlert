import pytest
from unittest.mock import Mock, patch
from src.summarizer import Summarizer, SummarizerError
from src.models import Article
from src.config import Config

def test_summarize_openai(monkeypatch):
    def mock_summarize_with_openai(self, article):
        return "This is a mock OpenAI summary."

    monkeypatch.setattr(Summarizer, "_summarize_with_openai", mock_summarize_with_openai)

    config = Config(
        llm_provider="openai",
        llm_api_key="fake_key",
        twilio_account_sid="",
        twilio_auth_token="",
        twilio_from_phone="",
        twilio_to_phone="",
        topics=[],
        schedule_times=[]
    )
    summarizer = Summarizer(config)
    article = Article(title="Test", url="", topic="", content="Test content")
    summary = summarizer.summarize(article)
    assert summary == "This is a mock OpenAI summary."

@patch('anthropic.Anthropic')
def test_summarize_anthropic(mock_anthropic):
    mock_client = Mock()
    mock_response = Mock()
    mock_response.content = [Mock(text="This is a mock Anthropic summary.")]
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client

    config = Config(
        llm_provider="anthropic",
        llm_api_key="fake_key",
        twilio_account_sid="",
        twilio_auth_token="",
        twilio_from_phone="",
        twilio_to_phone="",
        topics=[],
        schedule_times=[]
    )
    summarizer = Summarizer(config)
    article = Article(title="Test", url="", topic="", content="Test content")
    summary = summarizer.summarize(article)
    assert summary == "This is a mock Anthropic summary."