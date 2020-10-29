import spotipy
import configargparse
from spotipy.oauth2 import SpotifyClientCredentials

def main(client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    urn = 'spotify:artist:3fZgTHf9UHEA1oLYLEhnk2'


if __name__ == "__main__":
    parser = configargparse.ArgParser(default_config_files=["auth.cfg"])
    parser.add_argument("-c", "--config", is_config_file=True, help="config file path")
    parser.add_argument(
        "--client-id",
        required=True,
        help="Spotify Client ID"
    )
    parser.add_argument(
        "--client-secret",
        required=True,
        help="Spotify Client Secret"
    )

    args = parser.parse_args()

    main(args.client_id, args.client_secret)
