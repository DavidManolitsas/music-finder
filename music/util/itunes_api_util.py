import requests


def get_artist_by_name(artist_name: str) -> dict:
    """
    Query itunes api to retrieve artist by artist name

    :param artist_name: artists name
    :return: artist
    """
    url_query = f'term={artist_name.replace(" ", "+")}&entity=musicArtist'

    artist_response = requests.get(
        url=f"https://itunes.apple.com/search?{url_query}", timeout=10
    )

    if len(artist_response.json()["results"]) > 1:
        for potential_artist in artist_response.json()["results"]:
            if potential_artist["artistName"] == artist_name:
                return potential_artist

    return artist_response.json()["results"][0]


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

    song_response = requests.get(
        url=f"https://itunes.apple.com/lookup?{artist_id}&entity=song",
        timeout=10,
    )
    songs = song_response.json()["results"]
    del songs[0]
    music.extend(songs)

    # no previewUrl title := collectionName
    album_response = requests.get(
        url=f"https://itunes.apple.com/lookup?{artist_id}&entity=album",
        timeout=10,
    )
    albums = album_response.json()["results"]
    del albums[0]
    music.extend(albums)

    return music
