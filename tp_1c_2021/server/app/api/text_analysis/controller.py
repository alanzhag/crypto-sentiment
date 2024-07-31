import logging

from flask import request
from flask_restx import Resource, Namespace, fields

from app.api.schemas import text_analysis_schema
from app.api.text_analysis.services.text_analyser import text_analyser
from app.exceptions.schemas import exception_message_schema

text_analysis_ns = Namespace("textAnalysis", "Text Analysis")

resource_fields = text_analysis_ns.model('TextAnalysis', {
    'text': fields.String,
})


@text_analysis_ns.route("")
class TextAnalysisResource(Resource):
    # @auth.login_required()
    @text_analysis_ns.expect(resource_fields)
    def post(self):
        data = request.get_json()
        text = data["text"]
        if not text:
            return exception_message_schema.dump({"message": "Text to analyse cannot be empty", "status": 400}), 400
        logging.debug(data)
        response = text_analyser.analyse(text)
        return text_analysis_schema.dump(response), 200
