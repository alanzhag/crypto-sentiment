from app.api.information_retrieval.text_fetcher.sources.google_news.google_news_text_source import GoogleNewsTextSource
from app.api.information_retrieval.text_fetcher.sources.news.news_text_source import NewsTextSource
from app.api.information_retrieval.text_fetcher.sources.reddit.reddit_text_source import RedditTextSource
from app.api.information_retrieval.text_fetcher.sources.twitter.twitter_text_source import TwitterTextSource
from app.api.text_sources.models import TextSourceStatus, TextSourcesStatusResponse, TextSource


class TextSourcesService:

    def __init__(self):
        self.sources = [TwitterTextSource(), GoogleNewsTextSource(), RedditTextSource(), NewsTextSource()]

    def __is_source_enabled(self, source) -> bool:
        source_status = TextSource.query.get(source.name)
        return source_status.enabled if source_status else True

    def get_active_sources(self):
        return [s for s in self.sources if self.__is_source_enabled(s)]

    def get_active_sources_names(self):
        return [s.name for s in self.get_active_sources()]

    def get_sources_status(self) -> TextSourcesStatusResponse:
        return TextSourcesStatusResponse(
            sources=[TextSourceStatus(name=s.name, enabled=self.__is_source_enabled(s)) for s in self.sources]
        )


text_sources_service = TextSourcesService()
