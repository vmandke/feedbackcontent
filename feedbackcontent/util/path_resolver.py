import os


def get_upper_adjacent(path):
    return os.path.join(
               os.path.dirname(os.path.dirname(__file__)),
               path)
