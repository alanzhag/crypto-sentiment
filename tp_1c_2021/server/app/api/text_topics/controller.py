from flask_restx import Resource, Namespace

from app.api.information_retrieval.text_fetcher.topics.text_topics import text_topics_repo
from app.api.schemas import text_topics_schema

text_topics_ns = Namespace("textTopics", "Text topics to be fetched")


@text_topics_ns.route("")
class TextTopics(Resource):
    # @auth.login_required()
    def get(self):
        response = text_topics_repo.topics()
        return text_topics_schema.dump({"topics": response}), 200
