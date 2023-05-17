import os

import yaml


def read_yaml_to_dict(path: str) -> dict:
    """
    Load yaml file to in-memory dictionary.

    :param path: path to yaml file
    :return: yaml as dict
    """
    if not os.path.isfile(path):
        raise FileNotFoundError

    with open(path, "r", encoding="utf-8") as stream:
        content = yaml.safe_load(stream=stream)

    return content
