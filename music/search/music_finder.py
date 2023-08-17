from datetime import datetime, timedelta

from music.api.itunes_api import get_artist_by_name, get_music_by_artist
from music.util.date_util import format_date, get_start_date
from music.util.log_util import get_logger
from music.util.template_util import get_template

log = get_logger()


def __filter_music_duplicates(new_releases: []) -> []:
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


def __map_new_release(music: dict) -> dict:
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
        .replace(" - EP", ""),
        "preview": preview,
        "song_url": song_url,
        "cover": str(music["artworkUrl100"]).replace("100x100", "600x600"),
        "track_count": track_count,
    }


def __filter_music_by_date(music_list: [], start_date: datetime) -> []:
    # filter out music released before start date
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
                new_releases.append(__map_new_release(music=music))

    filtered_releases = __filter_music_duplicates(new_releases=new_releases)
    return [
        i
        for n, i in enumerate(filtered_releases)
        if i not in filtered_releases[n + 1 :]
    ]


def find_new_music(days: int, artist_names: []):
    """
    Find new search for a list of artists in the past given days.

    :param days: number of days to check for past releases
    :param artist_names: a list of search artists
    :return: None
    """
    template = get_template(file_name="index.html.j2")
    start_date = get_start_date(days_ago=days)
    formatted_start_date = format_date(date=start_date)

    # get new releases from artist list
    artists = []
    song_count = 0

    for artist_name in artist_names:
        artist = get_artist_by_name(name=artist_name)
        if artist:
            music = get_music_by_artist(artist=artist)
            artist_link = artist.get("artistLinkUrl")

            # get new releases by artist
            new_releases = __filter_music_by_date(
                music_list=music, start_date=start_date
            )

            if new_releases:
                log.info(f"new music found from {artist_name}")
                song_count += len(new_releases)

            artists.append(
                {
                    "artist_name": artist_name,
                    "new_releases": new_releases,
                    "artist_link": artist_link,
                }
            )
        else:
            log.error(f"{artist_name} not found")

    # Build HTML file from Jinja2 template
    log.info(f"{song_count} new songs found since {formatted_start_date}")
    with open(f"app/index.html", "w", encoding="UTF-8") as file:
        file.write(
            template.render(
                artists=artists,
                date=formatted_start_date,
                song_count=song_count,
            )
        )
