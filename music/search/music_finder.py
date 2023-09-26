from datetime import datetime

from music.api.itunes_api import get_music_by_artist
from music.search.music_filter import (
    filter_music_duplicates,
    get_all_new_releases,
)
from music.util.date_util import format_date, get_start_date
from music.util.log_util import get_logger
from music.util.template_util import get_template

log = get_logger()


def get_new_releases(music_list: [], start_date: datetime):
    """
    Get new music releases from list of music.

    :param music_list: list of music
    :param start_date: release date cut off
    :return: list of new releases
    """
    new_releases = get_all_new_releases(music_list, start_date)
    filtered_releases = filter_music_duplicates(new_releases=new_releases)

    return [
        i
        for n, i in enumerate(filtered_releases)
        if i not in filtered_releases[n + 1 :]
    ]


def generate_html(
    new_release_artists: [], start_date: datetime, song_count: int
):
    """
    Apply new release config to Jinja2 template to generate the final
    index.html file.

    :param new_release_artists: list of artists with new releases.
    :param start_date: release date cut off
    :param song_count: number of new songs releases since start_date
    :return: None
    """
    template = get_template(file_name="index.html.j2")
    formatted_start_date = format_date(date=start_date)

    # Build HTML file from Jinja2 template
    log.info(f"{song_count} new songs found since {formatted_start_date}")
    with open(f"app/index.html", "w", encoding="UTF-8") as file:
        file.write(
            template.render(
                artists=new_release_artists,
                date=formatted_start_date,
                song_count=song_count,
            )
        )


def find_new_music(days: int, artists: [dict]):
    """
    Find new search for a list of artists in the past given days.

    :param days: number of days to check for past releases
    :param artists: a list of search artists
    :return: None
    """
    start_date = get_start_date(days_ago=days)

    # get new releases from artist list
    song_count = 0
    new_release_artists = []

    for artist in artists:
        music = get_music_by_artist(artist=artist)

        if not music:
            log.info(f'no music found for {artist["id"]}: {artist["name"]}')
            continue

        # get artist details
        artist_details = music[0]
        del music[0]

        # get new releases by artist
        new_releases = get_new_releases(
            music_list=music, start_date=start_date
        )

        if new_releases:
            log.info(f"new music found from {artist['name']}")
            # increment new song count
            song_count += len(new_releases)
            artist_link = artist_details.get("artistLinkUrl")

            new_release_artists.append(
                {
                    "artist_name": artist["name"],
                    "new_releases": new_releases,
                    "artist_link": artist_link,
                }
            )

    generate_html(new_release_artists, start_date, song_count)
