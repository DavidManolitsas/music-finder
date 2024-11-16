import requests

from music.util.log_util import get_logger

log = get_logger()


class HttpService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str):
        try:
            response = requests.get(url=f"{self.base_url}{path}", timeout=20)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as error:
            log.error(
                f"Encountered an error calling {self.base_url}{path} -> {error}"
            )
            return None
