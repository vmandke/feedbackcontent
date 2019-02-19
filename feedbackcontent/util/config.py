import configparser
import os

from feedbackcontent.util.path_resolver import get_upper_adjacent


_config = configparser.ConfigParser()
_config.optionxform = str


def get_config(section, item=None):
    if item is None:
        config = dict(_config.items(section))
    else:
        config = _config.get(section, item)
    return config


def set_config():
    settings_file = os.environ.get('SETTINGS', 'settings')
    settings_file += '.cfg'
    resources_dir = get_upper_adjacent('resources')
    _config.read(os.path.join(resources_dir, settings_file))
