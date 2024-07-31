import concurrent
import logging
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer as timer

from app.api.information_retrieval.models import TextsByTopic, GroupedSourceFetch, TextFetchResponse
from app.api.information_retrieval.text_fetcher.topics.text_topics import TextTopicsRepo, text_topics_repo
from app.api.text_sources.services.text_sources_service import text_sources_service


class TextFetcher:

    def __init__(self, sources_service, topics_repo: TextTopicsRepo):
        self.sources_service = sources_service
        self.topics_repo = topics_repo

    def __sources(self, preferred_source_name):
        preferred_source = [s for s in self.sources_service.get_active_sources() if s.name == preferred_source_name] \
            if preferred_source_name else self.sources_service.get_active_sources()
        if not preferred_source:
            raise RuntimeError(f"Source {preferred_source_name} does not exist or is disabled")
        return preferred_source

    def __get_texts_by_topic(self, topic, source, n) -> TextsByTopic:
        logging.info(f"Fetching {n} texts about {topic} from source {source.name}")
        start = timer()
        try:
            texts = source.fetch(topic, n)
            is_error = False
        except Exception as e:
            logging.error(f"Fetching of {topic} in {source.name} failed. Reason: {str(e)}")
            is_error = True
            texts = []
        finally:
            time_took = timer() - start
        logging.info(f"Finished fetching {n} texts about {topic} from source {source.name}. Took {time_took}.")
        return TextsByTopic(topic=topic, texts=texts, status={"elapsed_time": time_took, "error": is_error})

    def __concurrent_fetch(self, source: str = None, n: int = 1) -> TextFetchResponse:
        elapsed_time_start = timer()
        topics = self.topics_repo.topics()
        sources = self.__sources(preferred_source_name=source)
        results = []
        for source in sources:
            source_time_start = timer()
            with ThreadPoolExecutor() as executor:
                res = [executor.submit(self.__get_texts_by_topic, topic, source, n) for topic in topics]
                concurrent.futures.wait(res)
            by_topics = [r.result() for r in res]
            source_time = timer() - source_time_start
            results.append(
                GroupedSourceFetch(
                    source_name=source.name,
                    by_topics=by_topics,
                    status={"elapsed_time": source_time}
                )
            )
        elapsed_time = timer() - elapsed_time_start
        return TextFetchResponse(results=results, status={"elapsed_time": elapsed_time})

    def __sequential_fetch(self, source: str = None, n: int = 1) -> TextFetchResponse:
        elapsed_time_start = timer()
        sources = self.__sources(preferred_source_name=source)
        topics = self.topics_repo.topics()
        results = []
        for source in sources:
            source_time_start = timer()
            by_topics = []
            for topic in topics:
                logging.info(f"Fetching {n} texts about {topic} from source {source.name}")
                start = timer()
                texts = source.fetch(topic, n)
                time_took = timer() - start
                logging.info(f"Finished fetching {n} texts about {topic} from source {source.name}. Took {time_took}.")
                by_topics.append(TextsByTopic(topic=topic, texts=texts, status={"elapsed_time": time_took}))
            source_time = timer() - source_time_start
            results.append(
                GroupedSourceFetch(source_name=source.name, by_topics=by_topics, status={"elapsed_time": source_time})
            )
        elapsed_time = timer() - elapsed_time_start
        return TextFetchResponse(results=results, status={"elapsed_time": elapsed_time})

    # For each source it fetches n texts of each topic
    def fetch(self, source: str = None, n: int = 1) -> TextFetchResponse:
        return self.__concurrent_fetch(source, n)


text_fetcher = TextFetcher(
    sources_service=text_sources_service,
    topics_repo=text_topics_repo
)
