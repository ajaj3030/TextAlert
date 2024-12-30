from typing import Optional
import openai
from .models import Article
from .config import Config

class SummarizerError(Exception):
    pass

class Summarizer:
    def __init__(self, config: Config):
        self.config = config
        if config.llm_provider == 'openai':
            openai.api_key = config.llm_api_key

    def summarize(self, article: Article) -> Optional[str]:
        if self.config.llm_provider == 'openai':
            return self._summarize_with_openai(article)
        else:
            raise SummarizerError(f"Unsupported LLM provider: {self.config.llm_provider}")

    def _summarize_with_openai(self, article: Article) -> str:
        try:
            prompt = f"""Summarize this article in 2-3 concise sentences:
            Title: {article.title}
            Content: {article.content}"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a concise news summarizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise SummarizerError(f"Failed to summarize article: {str(e)}") 