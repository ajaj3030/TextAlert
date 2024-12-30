from typing import List
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .models import Article
from .config import Config

class NotifierError(Exception):
    pass

class SMSNotifier:
    def __init__(self, config: Config):
        self.config = config
        self.client = Client(
            config.twilio_account_sid,
            config.twilio_auth_token
        )

    def format_message(self, articles: List[Article]) -> List[str]:
        """Split articles into SMS-sized chunks."""
        messages = []
        current_message = []
        current_length = 0
        
        for article in articles:
            article_text = (
                f"[{article.topic}]\n"
                f"Title: {article.title}\n"
                f"Summary: {article.summary}\n"
                f"Link: {article.url}\n\n"
            )
            
            # SMS length limit is roughly 1600 characters
            if current_length + len(article_text) > 1500:
                messages.append("".join(current_message))
                current_message = [article_text]
                current_length = len(article_text)
            else:
                current_message.append(article_text)
                current_length += len(article_text)
        
        if current_message:
            messages.append("".join(current_message))
            
        return messages

    def send_notifications(self, articles: List[Article]) -> None:
        if not articles:
            return

        messages = self.format_message(articles)
        
        for message in messages:
            try:
                self.client.messages.create(
                    from_=self.config.twilio_from_phone,
                    to=self.config.twilio_to_phone,
                    body=message
                )
            except TwilioRestException as e:
                raise NotifierError(f"Failed to send SMS: {str(e)}") 