import spotipy
import configargparse
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import logging

logging.basicConfig(level=logging.INFO)

SCOPE = 'playlist-modify-public'


def main(args: configargparse.Namespace):
    # auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=args.client_id,
                                client_secret=args.client_secret,
                                redirect_uri=args.redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_name = sp.playlist(args.playlist)['name']
    user_uri = sp.me()['id']

    logging.info(f"Getting artists from playlist: {playlist_name}")

    response = sp.playlist_items(args.playlist,
                                 fields='items(track(artists(uri)))'
                                 )

    items = response['items']

    # TODO handle invalid response/empty playlist

    # filter to artists
    artists = [item['track']['artists'] for item in items]

    # filter to first URI (primary artist)
    artists_uris = [artist[0]['uri'] for artist in artists]

    # filter out duplicates
    artists_unique = list(set(artists_uris))

    logging.info(f"Found {len(artists_uris)} artists ({len(artists_unique)} unique)")

    # get top songs from each artist
    top_tracks_per_artist = [sp.artist_top_tracks(artist) for artist in artists_unique]

    top_tracks = [tracks['tracks'] for tracks in top_tracks_per_artist]

    # TODO error check for artists with less than 3 songs!
    track_urls = [track['uri'] for artist in top_tracks for track in artist[:3]]

    # create a playlist
    new_playlist_name = f"Top tracks from artists in {playlist_name}"
    playlist_response = sp.user_playlist_create(user_uri,
                                                new_playlist_name,
                                                description="Auto-generated playlist! (https://github.com/bsecker/spotify-scripts)")

    logging.info(f"Created playlist: {new_playlist_name}")

    # add top tracks to playlist, only adding 100 at a time
    # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    chunks = [track_urls[i:i + 100] for i in range(0, len(track_urls), 100)]
    for chunk in chunks:
        logging.info(f"Adding {len(chunk)} songs to playlist...")
        sp.playlist_add_items(playlist_response['uri'], chunk)

    logging.info(f"Added {len(track_urls)} songs to playlist titled \"{new_playlist_name}\". URL: {playlist_response['href']}")


if __name__ == "__main__":
    parser = configargparse.ArgParser(default_config_files=["auth.cfg"])
    parser.add_argument("-c", "--config", is_config_file=True, help="config file path")
    parser.add_argument("--client-id", required=True, help="Spotify Client ID")
    parser.add_argument("--client-secret", required=True, help="Spotify Client Secret")
    parser.add_argument("--playlist", required=True, help="Playlist URI")
    parser.add_argument("--redirect-uri", default="http://localhost:8090", help="OAuth Redirect URI")
    parser.add_argument("--n-top", default=3, help="Number of tracks to get for each artist")

    args = parser.parse_args()

    main(args)
