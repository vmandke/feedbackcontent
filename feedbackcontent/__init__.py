from feedbackcontent.predict.app import get_app
from feedbackcontent.util.config import set_config
from feedbackcontent.util.logger import set_logger
from feedbackcontent.util.decorators import catch_and_log_errors


@catch_and_log_errors
def setup_app():
    set_logger()
    set_config()
    return get_app()
