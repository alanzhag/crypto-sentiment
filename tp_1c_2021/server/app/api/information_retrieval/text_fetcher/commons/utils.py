from newspaper import Config

from app.api.information_retrieval.models import Text


def article_config() -> Config:
    config = Config()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    config.browser_user_agent = user_agent
    config.request_timeout = 20
    return config


def add_elapsed_time(text: Text, elapsed_time):
    text.metadata["mapping_time"] = elapsed_time
