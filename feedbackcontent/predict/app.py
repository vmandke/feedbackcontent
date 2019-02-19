from http import HTTPStatus
import logging
import os

from flask import Flask, request, jsonify

from feedbackcontent.predict.model import Loader
from feedbackcontent.util.config import get_config
from feedbackcontent.util.decorators import (
    validate_request_params, catch_and_log_errors)
from feedbackcontent.util.path_resolver import get_upper_adjacent
from feedbackcontent.util.logger import get_logger


def get_app():
    def get_models(path):
        return map(lambda x: x[:x.rfind('.')],
                   filter(lambda x: x.endswith('.npz'),
                          os.listdir(path)))

    mpath = get_upper_adjacent(get_config('model', 'path'))
    loader = Loader(mpath)
    models = {m: loader.load_model(m) for m in get_models(mpath)}
    models['default'] = loader.load_model(
                            get_config('model', 'default'))

    wsgi_app = Flask(__name__)

    def predict(text, version='default'):
        if version in models:
            __model = models[version]
        else:
            get_logger().info(
                "{}: not found. Using default model".format(version))
            __model = models['default']
        return {'toxicity': __model.predict(text)[0]}

    @wsgi_app.route('/feedback/', methods=['POST'])
    @catch_and_log_errors
    @validate_request_params
    def _feedback(content=None):
        return jsonify(**predict(**content)), HTTPStatus.OK
    # Return the webapp
    return wsgi_app
