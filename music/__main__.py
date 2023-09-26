"""
A python application for finding the latest search from a list of artists
"""
import argparse

from music.search.music_finder import find_new_music
from music.util.file_util import read_yaml_to_dict

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--days", type=int, required=True)
    arguments = arg_parser.parse_args()

    artists_yaml = read_yaml_to_dict("music/resources/artists.yaml")
    find_new_music(days=arguments.days, artists=artists_yaml["artists"])
