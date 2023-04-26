from datetime import datetime, timedelta

import requests


def __filter_new_releases(new_releases: []) -> []:
    # filter duplicate songs to prioritise songs with music previews
    filtered_releases = []

    for new_release_1 in new_releases:
        for new_release_2 in new_releases:
            if new_release_1["song"] == new_release_2["song"]:
                if "preview" in new_release_2:
                    filtered_releases.append(new_release_2)
                else:
                    filtered_releases.append(new_release_1)
                break

    return filtered_releases


def __process_music_release(music: dict) -> dict:
    track_count = None
    preview = music.get("previewUrl")
    song_url = music.get("collectionViewUrl")

    if "trackCensoredName" in music:
        song_name: str = music["trackCensoredName"]
    else:
        song_name: str = music["collectionName"]
        if "trackCount" in music:
            if music["trackCount"] > 1:
                track_count = music["trackCount"]

    return {
        "song": song_name.replace(" - Single", "")
        .replace(" (Extended Mix)", "")
        .replace(" - EP", ""),
        "preview": preview,
        "song_url": song_url,
        "cover": str(music["artworkUrl100"]).replace("100x100", "600x600"),
        "track_count": track_count,
    }


def get_new_releases(music_list: [], start_date: datetime) -> []:
    new_releases = []
    for music in music_list:
        if "releaseDate" in music:
            release_date = datetime.strptime(
                music["releaseDate"], "%Y-%m-%dT%H:%M:%SZ"
            )
            if (
                start_date
                < release_date
                < (datetime.today() + timedelta(days=365))
            ):
                new_releases.append(__process_music_release(music=music))

    filtered_releases = __filter_new_releases(new_releases=new_releases)
    return [
        i
        for n, i in enumerate(filtered_releases)
        if i not in filtered_releases[n + 1 :]
    ]


def search_for_itunes_artist(artist_name: str) -> dict:
    url_query = f'term={artist_name.replace(" ", "+")}&entity=musicArtist'

    artist_response = requests.get(
        url=f"https://itunes.apple.com/search?{url_query}", timeout=10
    )

    if len(artist_response.json()["results"]) > 1:
        for potential_artist in artist_response.json()["results"]:
            if potential_artist["artistName"] == artist_name:
                return potential_artist

    return artist_response.json()["results"][0]


def get_artists_music(artist: dict) -> []:
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
