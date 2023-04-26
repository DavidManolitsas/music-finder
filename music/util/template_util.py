"""
Jinja2 templating utilities.
"""
import jinja2
from jinja2 import Environment, FileSystemLoader


def get_template(file_name: str) -> jinja2.environment.Template:
    """
    Get jinja2 template

    :param file_name: jinja2 template file name
    :return: jinja2 template
    """
    env = Environment(
        loader=FileSystemLoader("music/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    return env.get_template(file_name)
