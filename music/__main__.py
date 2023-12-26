"""
A python application for finding the latest search from a list of artists
"""
import argparse

from music.search.music_finder import find_new_music
from music.util.file_util import read_yaml_to_dict

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-p", "--path", type=str, default="music/resources/artists.yaml"
    )
    arg_parser.add_argument(
        "-d", "--days", type=int, required=False, default=31
    )
    args = arg_parser.parse_args()

    artists_yaml = read_yaml_to_dict(args.path)
    find_new_music(days=args.days, artists=artists_yaml["artists"])
