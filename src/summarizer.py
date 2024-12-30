from typing import Optional
import openai
import anthropic
from .models import Article
from .config import Config

class SummarizerError(Exception):
    pass

class Summarizer:
    def __init__(self, config: Config):
        self.config = config
        if config.llm_provider == 'openai':
            openai.api_key = config.llm_api_key
        elif config.llm_provider == 'anthropic':
            self.client = anthropic.Anthropic(api_key=config.llm_api_key)

    def summarize(self, article: Article) -> Optional[str]:
        if self.config.llm_provider == 'openai':
            return self._summarize_with_openai(article)
        elif self.config.llm_provider == 'anthropic':
            return self._summarize_with_anthropic(article)
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
            raise SummarizerError(f"Failed to summarize article with OpenAI: {str(e)}")

    def _summarize_with_anthropic(self, article: Article) -> str:
        try:
            prompt = f"""Summarize this article in 2-3 concise sentences:
            Title: {article.title}
            Content: {article.content}"""

            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=100,
                temperature=0.7,
                system="You are a concise news summarizer.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            raise SummarizerError(f"Failed to summarize article with Anthropic: {str(e)}")