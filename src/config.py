import os
from typing import List
from dataclasses import dataclass
from dotenv import load_dotenv
from datetime import datetime

@dataclass
class Config:
    llm_provider: str
    llm_api_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_phone: str
    twilio_to_phone: str
    topics: List[str]
    schedule_times: List[str]
    max_articles: int

def load_config() -> Config:
    load_dotenv()
    
    # Get and validate topics
    topics = [t.strip().lower() for t in os.getenv('TOPICS', '').split(',') if t.strip()]
    valid_topics = [
        "computer vision", "robotics", "llms", "nlp", "ml",
        "blockchain", "cryptocurrency", "computational finance",
        "reinforcement learning"
    ]
    
    invalid_topics = [t for t in topics if t not in valid_topics]
    if invalid_topics:
        print(f"Warning: Invalid topics found: {', '.join(invalid_topics)}")
        print(f"Available topics: {', '.join(valid_topics)}")
        # Filter out invalid topics
        topics = [t for t in topics if t in valid_topics]
    
    # Get and validate schedule times
    schedule_times = []
    raw_times = os.getenv('SCHEDULE_TIMES', '').split(',')
    
    for time_str in raw_times:
        time_str = time_str.strip()
        try:
            # Validate time format (HH:MM)
            datetime.strptime(time_str, '%H:%M')
            schedule_times.append(time_str)
        except ValueError:
            print(f"Warning: Invalid time format '{time_str}'. Using format HH:MM (e.g., 09:00)")
            continue
    
    if not schedule_times:
        # Default to 9 AM if no valid times provided
        schedule_times = ['09:00']
    
    return Config(
        llm_provider=os.getenv('LLM_PROVIDER', 'openai'),
        llm_api_key=os.getenv('LLM_API_KEY'),
        twilio_account_sid=os.getenv('TWILIO_ACCOUNT_SID'),
        twilio_auth_token=os.getenv('TWILIO_AUTH_TOKEN'),
        twilio_from_phone=os.getenv('TWILIO_FROM_PHONE'),
        twilio_to_phone=os.getenv('TWILIO_TO_PHONE'),
        topics=topics,
        schedule_times=schedule_times,
        max_articles=int(os.getenv('MAX_ARTICLES', '3'))
    ) 