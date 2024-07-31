from app.api.auth.schemas import UserSchema, TokenSchema
from app.api.crypto_price.schemas import CryptoPriceSchema
from app.api.fetch.schemas import FetchJobSchema
from app.api.information_retrieval.schemas import TextFetchResponseSchema
from app.api.nlp.schemas import NLPTaggerResponseSchema, NLPTaggedTextSchema
from app.api.sentiment_price.schemas import SentimentPriceSnapshotSchema, \
    ComputedSentimentPriceSchema, SentimentPriceSourceSchema
from app.api.status.schemas import DetailedStatusSchema, SimpleStatusSchema

from app.api.text_analysis.schemas import TextAnalysisSchema
from app.api.text_sources.schemas import TextSourcesSchema
from app.api.text_topics.schemas import TextTopicsSchema

fetch_job_schema = FetchJobSchema()
detailed_status_schema = DetailedStatusSchema()
simple_status_schema = SimpleStatusSchema()
user_schema = UserSchema()
token_schema = TokenSchema()
text_fetch_response_schema = TextFetchResponseSchema()
text_analysis_schema = TextAnalysisSchema()
crypto_price_schema = CryptoPriceSchema()
nlp_tagger_response_schema = NLPTaggerResponseSchema()
nlp_tagged_text_schema = NLPTaggedTextSchema()
sentiment_price_snapshot_schema = SentimentPriceSnapshotSchema()
computed_sentiment_price_schema = ComputedSentimentPriceSchema()
sentiment_price_source_schema = SentimentPriceSourceSchema()
text_topics_schema = TextTopicsSchema()
text_sources_schema = TextSourcesSchema()
