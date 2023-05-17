import requests
from music.util.log_util import get_logger

log = get_logger()


def __send_request(url: str):
    print(url)  # testing
    return requests.get(url=url, timeout=20)


def __remove_artist_details(response):
    results = response.json().get("results")
    del results[0]
    return results


def get_artist_by_name(name: str) -> dict:
    """
    Query itunes api to retrieve artist by artist name

    :param name: artists name
    :return: artist
    """
    url_query = f'term={name.replace(" ", "+")}&entity=musicArtist'

    response = __send_request(
        url=f"https://itunes.apple.com/search?{url_query}"
    )

    print(f"status: {response.status_code}")  # testing

    if len(response.json().get("results")) > 1:

        for artist in response.json().get("results"):
            if artist["artistName"] == name:
                return artist

    return response.json().get("results")[0]


def get_music_by_artist(artist: dict) -> []:
    """
    Query itunes api to get all music by given artist.

    :param artist: itunes artist
    :return: list of music by artist
    """
    music = []

    if "amgArtistId" in artist:
        artist_id = f'amgArtistId={artist["amgArtistId"]}'
    else:
        artist_id = f'id={artist["artistId"]}'

    # get all songs by artist
    song_response = __send_request(
        url=f"https://itunes.apple.com/lookup?{artist_id}&entity=song",
    )
    songs = __remove_artist_details(response=song_response)
    music.extend(songs)

    # get all albums by artist
    album_response = __send_request(
        url=f"https://itunes.apple.com/lookup?{artist_id}&entity=album",
    )
    albums = __remove_artist_details(response=album_response)
    music.extend(albums)

    return music
