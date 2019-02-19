from http import HTTPStatus

from flask import jsonify, request
from funcy import decorator

from feedbackcontent.util.logger import get_logger


@decorator
def validate_request_params(request_handler):
    content = request.get_json()
    if not content:
        get_logger().info("Bad request")
        return (jsonify(**{"error": "Incorrect content-type for request"}),
                HTTPStatus.BAD_REQUEST)
    required_keys = set(['text'])
    optional_keys = set(['version'])
    provided_keys = set(content.keys())
    error = (True
             if ((required_keys - provided_keys) or
                 (provided_keys - required_keys - optional_keys))
             else False)
    if error:
        message = "{}: required_keys and {}: optional_keys".format(
                      required_keys, optional_keys)
        get_logger().info(message)
        return (jsonify(**{"error": message}),
                HTTPStatus.BAD_REQUEST)
    else:
        return request_handler(content)


@decorator
def catch_and_log_errors(fn):
    try:
        result = fn()
    except Exception as e:
        get_logger().exception("Error occurred")
        message = "Error occurred {}".format(e)
        result = (jsonify(**{"error": message}),
                  HTTPStatus.INTERNAL_SERVER_ERROR)
    return result
