import requests

from music.api.http_service import HttpService
from music.util.log_util import get_logger

log = get_logger()
service = HttpService(base_url="https://itunes.apple.com")


def get_music_by_artist_id(artist_id: str) -> []:
    """
    Query itunes api to get all music by given artist.

    :param artist_id: itunes artist id
    :return: list of music by artist
    """
    music = []

    # get all songs by artist
    song_response = service.get(path=f"/lookup?id={artist_id}&entity=song")

    if song_response:
        music.extend(song_response.json().get("results"))

    # get all albums by artist
    album_response = service.get(path=f"/lookup?id={artist_id}&entity=album")

    if album_response:
        music.extend(album_response.json().get("results"))

    return music
