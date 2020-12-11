"""
Bulk import of search results to playlist.

Inspiration comes from wanting to import track playlists from mixcloud mixes: https://github.com/max-bp/New-Mixcloud-Tracklist-Enabler

Usage:

1. Use mixcloud tracklist enabler to create the table of results
2. copy the entire table to a text file
3. pass the file as an argument to the script (the script will parse out the useless stuff)
"""
import configargparse
import re
import logging
import sys
import urllib.parse

import spotipy
from spotipy import SpotifyOAuth


## TODO: this doesn't work for tracks with numbers in the title!
SEARCH_REGEX = "[0-9]+\W+([^0-9]+)" # regexr.com/5ibe1
SCOPE = "playlist-modify-public"
logging.basicConfig(level=logging.INFO)


def main(args):
    # Auth with spotify
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=args.client_id,
                                client_secret=args.client_secret,
                                redirect_uri=args.redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_uri = sp.me()['id']

    # load file contents or stdin
    with open(args.file, "r") if not args.stdin else sys.stdin as f_in:
        file_contents = f_in.readlines()

    # Match lines against regex, trim whitespace
    if not args.pre_formatted:
        lines_trimmed = [re.match(SEARCH_REGEX, line)[1].strip() for line in file_contents]
    else:
        lines_trimmed = [line.strip() for line in file_contents]
    logging.debug(lines_trimmed)

    # Create new playlist
    new_playlist_name = "Mixcloud tracklist output"
    playlist_response = sp.user_playlist_create(user_uri,
                                                new_playlist_name,
                                                description=f"From {args.file if args.file else 'stdin'}")
    logging.info(f"Created playlist: {new_playlist_name}")

    # search for song and add it to the playlist
    uris = []
    dnf = []
    for track_name in lines_trimmed:

        if track_name == "ID - ID":
            continue

        query = track_name.lower().replace("&"," ").replace(" ", "+")
        logging.info(f"Searching for {track_name}... (query: {query})")
        results = sp.search(query, limit=1, type='track')

        if len(results['tracks']['items']) > 0:
            track = results['tracks']['items'][0]
            uris.append(track['uri'])
            logging.info(f"Found {track['name']} by {track['artists'][0]['name']}")
        else:
            dnf.append(track_name)
            logging.info("No search results found")

    sp.playlist_add_items(playlist_response['uri'], uris)
    logging.info(f"Added {len(uris)} songs to playlist.")

    logging.info("Could not find these tracks:")
    for track_name in dnf:
        logging.info(track_name)


if __name__ == '__main__':
    parser = configargparse.ArgParser(default_config_files=["auth.cfg"])
    parser.add_argument("-c", "--config", is_config_file=True, help="config file path")
    parser.add_argument("--client-id", required=True, help="Spotify Client ID")
    parser.add_argument("--client-secret", required=True, help="Spotify Client Secret")
    parser.add_argument("--playlist", required=True, help="Playlist URI")
    parser.add_argument("--redirect-uri", default="http://localhost:8090", help="OAuth Redirect URI")
    parser.add_argument("--stdin", action="store_true", help="get file input from stdin instead")
    parser.add_argument("--pre-formatted", action="store_true", help="file has been cleaned already")
    parser.add_argument("file", help="text file of results")

    args = parser.parse_args()

    main(args)

