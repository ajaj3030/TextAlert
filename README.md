# Research News Text Updater

An automated system that scrapes the latest research papers from various sources, ranks them by relevance, summarizes them using LLMs, and sends daily updates via SMS.

---

## Features

- 📚 Scrapes papers from multiple sources (arXiv, Medium)
- 🎯 Customizable topics in AI/ML 
- 🔍 Smart relevance ranking based on:
  - Paper recency (last 24 hours)
  - Content length
  - Institution/company mentions (MIT, Stanford, Google, etc.)
- 🤖 AI-powered summarization using Claude or GPT
- 📱 SMS notifications via Twilio
- ⏰ Configurable schedule for updates

---

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/ajaj3030/TextAlert.git 
   cd TextAlert
   ```

2. **Create and activate a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Copy `.env.example` to `.env` and fill in your credentials:**
   ```
   cp .env.example .env
   ```

---

## Configuration

Create a `.env` file with the following configuration:

```
# LLM Configuration (Choose one: 'openai' or 'anthropic')
LLM_PROVIDER=anthropic
LLM_API_KEY=your_anthropic_api_key

# Twilio Configuration for SMS notifications
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_PHONE=+1234567890
TWILIO_TO_PHONE=+1234567890

# Topic Configuration (comma-separated)
TOPICS=computer vision,nlp,reinforcement learning

# Schedule Configuration (comma-separated 24h format)
SCHEDULE_TIMES=09:00,17:00

# Maximum articles per update
MAX_ARTICLES=3
```

---

### Available Topics

The following topics are supported (see `src/scraper.py`, lines 16-53):

- computer vision - ArXiv CV papers and Medium articles
- robotics - ArXiv Robotics papers and robotics.news
- llms - ArXiv CL papers and Medium LLM articles
- nlp - ArXiv CL papers and Medium NLP articles
- ml - ArXiv Machine Learning papers
- blockchain - ArXiv Cryptography papers and Medium articles
- cryptocurrency - Medium and CoinTelegraph articles
- computational finance - ArXiv Quantitative Finance papers
- reinforcement learning - ArXiv RL papers and Medium articles

---

### Customizing Topics

To modify which topics you want to follow:

1. Choose from the available topics listed above.
2. Update the `TOPICS` variable in your `.env` file.
3. Use comma-separated values without quotes.
4. Topics are case-insensitive.

Example:
```
TOPICS=computer vision,nlp,ml
```

---

### Schedule Configuration

Set when you want to receive updates using 24-hour format times:
```
SCHEDULE_TIMES=09:00,17:00,23:00
```

---

## Running the Application

### One-time Run

To run the scraper once without scheduling:
```
python -c "from src.main import scrape_summarize_notify; scrape_summarize_notify()"
```

### Scheduled Run

To run the scheduler that will send updates at configured times:
```
python -m src.main
```

### Running Tests

Run tests:
```
pytest
```

For verbose output:
```
pytest -v
```

---

## How It Works

1. **Scraping**: The system fetches articles from configured RSS feeds for each topic (see `src/scraper.py`, lines 150-167).
2. **Relevance Scoring**: Each article is scored based on (see `src/scraper.py`, lines 63-85):
   - Recency (max 5 points)
   - Content length (max 2 points)
   - Institution mentions (max 3 points)
3. **Summarization**: Articles are summarized using either:
   - OpenAI's GPT-3.5 (see `src/summarizer.py`, lines 26-44)
   - Anthropic's Claude Haiku (see `src/summarizer.py`, lines 46-65)
4. **Notification**: Summaries are sent via SMS at scheduled times (see `src/main.py`, lines 7-31).

---

## Troubleshooting

1. **No articles found**: 
   - Check if your topics are valid.
   - Verify RSS feeds are accessible.
   - Ensure articles are within the last 24 hours.

2. **SMS not received**: 
   - Verify your Twilio credentials.
   - Check phone number formats (include country code).
   - Monitor console for error messages.

3. **LLM errors**:
   - Ensure API key is valid.
   - Check for sufficient credits.
   - Verify network connectivity.

## Docker

docker build -t ai-paper-summarizer .
docker run --env-file .env ai-paper-summarizer
