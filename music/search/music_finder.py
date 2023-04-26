from music.util.date_util import format_date, get_start_date
from music.util.itunes_api_util import (
    get_artists_music,
    get_new_releases,
    search_for_itunes_artist,
)
from music.util.log_util import get_logger
from music.util.template_util import get_template

log = get_logger()


def find_new_music(days: int, artists: []):
    """
    Find new search for a list of artists in the past given days
    :param days: number of days to check for past releases
    :param artists: a list of search artists
    :return: None
    """
    template = get_template(file_name="index.html.j2")
    start_date = get_start_date(days_ago=days)
    formatted_start_date = format_date(date=start_date)

    # get new releases from artist list
    all_artists = []
    song_count = 0

    for artist_name in artists:
        artist = search_for_itunes_artist(artist_name=artist_name)
        if artist:

            music = get_artists_music(artist=artist)
            new_releases = get_new_releases(
                music_list=music, start_date=start_date
            )

            artist_link = artist.get("artistLinkUrl")

            if new_releases:
                log.info(f"new music found from {artist_name}")
                song_count += len(new_releases)

            all_artists.append(
                {
                    "artist_name": artist_name,
                    "new_releases": new_releases,
                    "artist_link": artist_link,
                }
            )
        else:
            print(f"{artist_name} not found")

    # Build HTML file from Jinja2 template
    log.info(f"{song_count} new songs found since {formatted_start_date}")
    with open(f"app/index.html", "w", encoding="UTF-8") as file:
        file.write(
            template.render(
                artists=all_artists,
                date=formatted_start_date,
                song_count=song_count,
            )
        )
