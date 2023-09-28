from datetime import datetime, timedelta


def filter_music_duplicates(new_releases: []) -> []:
    """
    Remove any duplicate music releases.

    :param new_releases: all new music releases by artist
    :return: filtered music releases
    """
    # Dictionary to keep track of seen songs
    seen_songs = {}

    for release in new_releases:
        song = release["song"]
        if song in seen_songs:
            # Check if the current release has a preview
            if "preview" in release:
                seen_songs[song] = release
        else:
            seen_songs[song] = release

    return list(seen_songs.values())


def map_itunes_music_to_new_release(music: dict) -> dict:
    """
    Map the music config to the final artist config.

    :param music: raw music data
    :return: refined artist new release
    """
    preview = music.get("previewUrl")
    song_url = music.get("collectionViewUrl")
    song_name: str = music.get("trackCensoredName")

    track_count = None

    if not song_name:
        song_name: str = music.get("collectionName")
        if "trackCount" in music:
            if music.get("trackCount") > 1:
                track_count = music.get("trackCount")

    return {
        "song": song_name.replace(" - Single", "")
        .replace(" (Extended Mix)", "")
        .replace(" [Extended Mix]", "")
        .replace(" - EP", ""),
        "preview": preview,
        "song_url": song_url,
        "cover": str(music["artworkUrl100"]).replace("100x100", "600x600"),
        "track_count": track_count,
    }


def get_all_new_releases(music_list: [], start_date: datetime):
    """
    Get all new music releases unfiltered.

    :param music_list: all artist music
    :param start_date: release date cut off
    :return: all new music by artist
    """
    new_releases = []

    for music in music_list:
        if "releaseDate" in music:
            release_date = datetime.strptime(
                music["releaseDate"], "%Y-%m-%dT%H:%M:%SZ"
            )
            year_from_now = datetime.today() + timedelta(days=365)

            if start_date < release_date < year_from_now:
                new_releases.append(
                    map_itunes_music_to_new_release(music=music)
                )

    return new_releases
