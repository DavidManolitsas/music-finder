"""
Script to find an artists iTunes ID from their artist name.
"""
import argparse

from music.api.http_service import HttpService
from music.util.log_util import get_logger


log = get_logger()
service = HttpService(base_url="https://itunes.apple.com")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-a", "--artist", type=str, required=True)
arg_parser.add_argument("-l", "--limit", type=int, required=False, default=10)
arguments = arg_parser.parse_args()

# get arguments
artist_name = arguments.artist
search_limit = arguments.limit


# get itunes api response
log.info(f'search results for term = {artist_name}')

response = service.get(path=f'/search?term={artist_name.replace(" ", "+")}'
                            f'&limit={search_limit}'
                            f'&entity=musicArtist')

# iterate through artists
if response:
    for artist in response.json().get("results"):
        log.info(f'- id: {artist.get("artistId")} name: '
                 f'"{artist.get("artistName")}" '
                 f'({artist.get("artistLinkUrl")})')
