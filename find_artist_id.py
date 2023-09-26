import argparse

from music.util.log_util import get_logger
from music.api.itunes_api import send_http_request


log = get_logger()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-a", "--artist", type=str, required=True)
arg_parser.add_argument("-l", "--limit", type=int, required=False, default=10)
arguments = arg_parser.parse_args()

# get arguments
artist_name = arguments.artist
search_limit = arguments.limit


# get itunes api response
log.info(f'search results for term = {artist_name}')

response = send_http_request(url=f'https://itunes.apple.com/search'
                                 f'?term={artist_name.replace(" ", "+")}'
                                 f'&limit={search_limit}'
                                 f'&entity=musicArtist')

# iterate through artists
if response:
    for artist in response.json().get("results"):
        log.info(f'{artist.get("artistId")} - {artist.get("artistName")} ({artist.get("artistLinkUrl")})')
