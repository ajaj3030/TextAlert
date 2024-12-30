from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    title: str
    url: str
    topic: str
    content: str
    published_date: Optional[datetime] = None
    summary: Optional[str] = None
    is_sent: bool = False 