from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    title: str
    url: str
    topic: str
    content: str
    summary: Optional[str] = None
    published_date: Optional[datetime] = None
    relevance_score: float = 0.0  # Higher score means more relevant/trending 