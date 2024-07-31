import logging

from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        request_present = has_request_context()

        record.url = request.url if request_present else None
        record.remote_addr = request.remote_addr if request_present else None

        return super().format(record)
