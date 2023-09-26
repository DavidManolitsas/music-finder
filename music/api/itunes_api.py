import requests

from music.util.log_util import get_logger

log = get_logger()


def __send_http_request(url: str):
    try:
        response = requests.get(url=url, timeout=20)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        log.error(f"iTunes API error {error}")
        return None


def get_music_by_artist(artist: dict) -> []:
    """
    Query itunes api to get all music by given artist.

    :param artist: itunes artist id
    :return: list of music by artist
    """
    music = []
    artist_id = artist.get("id")

    # get all songs by artist
    song_response = __send_http_request(
        url=f"https://itunes.apple.com/lookup?id={artist_id}&entity=song",
    )

    if song_response:
        music.extend(song_response.json().get("results"))

    # get all albums by artist
    album_response = __send_http_request(
        url=f"https://itunes.apple.com/lookup?id={artist_id}&entity=album",
    )
    if album_response:
        music.extend(album_response.json().get("results"))

    return music
