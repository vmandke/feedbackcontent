import logging
import logging.config
import os

from feedbackcontent.util.path_resolver import get_upper_adjacent

__logger = None


def set_logger():
    global __logger
    config_file = os.path.join(get_upper_adjacent('resources'), 'logging.cfg')
    logging.config.fileConfig(config_file)
    __logger = logging.getLogger('feedbackcontent')
    __logger.info("{}: Loaded logging config".format(config_file))


def get_logger():
    return __logger
