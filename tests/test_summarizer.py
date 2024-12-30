from src.summarizer import Summarizer, SummarizerError
from src.models import Article
from src.config import Config

def test_summarize(monkeypatch):
    def mock_summarize_with_openai(self, article):
        return "This is a mock summary."

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
    assert summary == "This is a mock summary." 