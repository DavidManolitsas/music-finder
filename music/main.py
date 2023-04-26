"""
A python application for finding the latest search from a list of artists
"""
import argparse

from music.search.music_finder import find_new_music

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--days", type=int, required=True)
    arg_parser.add_argument(
        "--artists", metavar="N", type=str, nargs="+", required=True
    )
    arguments = arg_parser.parse_args()

    find_new_music(days=arguments.days, artist_names=arguments.artists)
