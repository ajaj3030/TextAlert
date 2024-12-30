from src.config import load_config
from src.scraper import NewsScraper
from src.summarizer import Summarizer
from src.notifier import SMSNotifier
from src.scheduler import Scheduler

def scrape_summarize_notify():
    config = load_config()
    scraper = NewsScraper()
    summarizer = Summarizer(config)
    notifier = SMSNotifier(config)

    all_articles = []

    for topic in config.topics:
        articles = scraper.get_articles_for_topic(topic)
        articles = articles[:config.max_articles // len(config.topics)]
        for article in articles:
            try:
                article.summary = summarizer.summarize(article)
                all_articles.append(article)
            except Exception as e:
                print(f"Error summarizing article {article.title}: {str(e)}")

    try:
        notifier.send_notifications(all_articles)
    except Exception as e:
        print(f"Error sending notifications: {str(e)}")

if __name__ == "__main__":
    config = load_config()
    scheduler = Scheduler(config.schedule_times, scrape_summarize_notify)
    scheduler.start() 