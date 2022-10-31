from platform import release
import requests
import argparse
import os

from datetime import datetime
from datetime import timedelta
from jinja2 import Environment, FileSystemLoader
from alive_progress import alive_bar


def __search_for_itunes_artist(artist_name: str) -> dict:
    artist_response = requests.get(f'https://itunes.apple.com/search?term={artist_name.replace(" ", "+")}&entity=musicArtist')
    
    if (len(artist_response.json()["results"]) > 1):
        for potential_artist in artist_response.json()["results"]:
            if potential_artist["artistName"] == artist_name:
                artist = potential_artist
                break
    else:
        artist = artist_response.json()["results"][0]
    
    return artist


def __get_artists_music(artist: dict) -> []:
    music = []

    if "amgArtistId" in artist:
        artist_id = f'amgArtistId={artist["amgArtistId"]}'
    else:
        artist_id = f'id={artist["artistId"]}'

    song_response = requests.get(f'https://itunes.apple.com/lookup?{artist_id}&entity=song')
    songs = song_response.json()["results"]
    del songs[0]
    music = music + songs

    # no previewUrl title := collectionName
    album_response = requests.get(f'https://itunes.apple.com/lookup?{artist_id}&entity=album')
    albums = album_response.json()["results"]
    del albums[0]
    music = music + albums
            
    return music

def __filter_new_releases(new_releases: []) -> []:
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


def __get_new_releases(music_list: [], days_ago: int) -> []:
    new_releases = []    
    for music in music_list:
        if "releaseDate" in music:
            release_date = datetime.strptime(music["releaseDate"], "%Y-%m-%dT%H:%M:%SZ")

            if release_date > days_ago and release_date < (datetime.today() + timedelta(days=365)):
                preview = None
                if "previewUrl" in music:
                    preview = music["previewUrl"]

                if music["collectionName"]:
                    new_releases.append({"song": music["collectionName"], "preview": preview, "cover": music["artworkUrl100"] })
                else:
                    new_releases.append({"song": music["track"], "preview": preview, "cover": music["artworkUrl100"]})
            
    
    filtered_releases = __filter_new_releases(new_releases=new_releases)
    return [i for n, i in enumerate(filtered_releases)
            if i not in filtered_releases[n + 1:]]


def __get_date(date: datetime) -> str:
    return f'{date.day}/{date.month}/{date.year}'


def find_new_music(days: int, artists: []):
    # open Jinja2 template
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('index.html.j2')

    # get date range
    days_ago = datetime.today() - timedelta(days=days)
    date = __get_date(date=days_ago)
    
    # get new releases from artist list
    all_artists = []
    song_count = 0
    print() # line break in CLI
    with alive_bar(len(artists), title=f'Finding new music since {date}') as bar:
        for artist_name in artists:
            artist = __search_for_itunes_artist(artist_name=artist_name)
            music = __get_artists_music(artist=artist)
            new_releases = __get_new_releases(music_list=music, days_ago=days_ago)
    
            if new_releases:
                song_count += len(new_releases)
                all_artists.append({
                    "artist_name": artist["artistName"],
                    "new_releases": new_releases,
                })
            bar()
    
    # Build HTML file from Jinja2 template
    print("exporting html...")
    with open(f'{root}/app/index.html', 'w') as fh:
        fh.write(template.render(artists = all_artists, date=date, song_count=song_count)
    )

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--days", type=int, required=True)
    arg_parser.add_argument('--artists', metavar='N', type=str, nargs='+', required=True)
    arguments = arg_parser.parse_args()

    find_new_music(days=arguments.days, artists=arguments.artists)
    
    
