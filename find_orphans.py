import configargparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

SCOPE = 'playlist-modify-private user-library-read playlist-read-private'

EXCLUDED_PLAYLISTS = (
    "Discover Weekly Archive",
)

def add_tracks_to_playlist(sp: spotipy.Spotify, playlist_id: str, tracks: list):
    """
    Add a list of tracks to a playlist, respecting pagination
    """
    index = 0
    while True:
        sp.playlist_add_items(playlist_id,
                              tracks[index:index+100],
                              )
        print(f"Added {len(tracks[index:index+100])} tracks to playlist")
        index += 100
        if index >= len(tracks):
            break

def get_user_playlists(sp: spotipy.Spotify):
    """
    Get all playlists for a user, respecting pagination
    """

    # get User ID
    user_id = sp.me()['id']

    playlists = []
    index=0
    while True:
        playlist_results = sp.current_user_playlists(limit=50,
                                                     offset=index,
                                                     )
        if len(playlist_results['items']) == 0:
            break
        # only get my-owned playlists - I follow a lot of other playlists and some have 5000+ songs.
        # Also
        playlists.extend([playlist for playlist in playlist_results['items'] if playlist['owner']['id'] == user_id and playlist['name'] not in EXCLUDED_PLAYLISTS])
        index += 50
        print(f"Added {len(playlist_results['items'])} playlists")
    return playlists

def get_user_saved_tracks(sp: spotipy.Spotify):
    """
    Get all tracks that a user has saved, respecting pagination
    """
    tracks = []
    index=0
    while True:
        saved_tracks_results = sp.current_user_saved_tracks(limit=50,
                                                           offset=index,
                                                           )
        if len(saved_tracks_results['items']) == 0:
            break
        tracks.extend([item['track']['uri'] for item in saved_tracks_results['items']])
        index += 50
        print(f"Added {len(saved_tracks_results['items'])} tracks from saved tracks")
    return tracks

def get_tracks(sp: spotipy.Spotify, playlist):
    """
    Get all the tracks from a playlist, respecting pagination
    """
    tracks = []
    index=0
    while True:
        playlist_results = sp.playlist_items(playlist['uri'],
                                             offset=index,
                                             fields='items(track(uri))',
                                             additional_types=['track'],
                                             )
        if len(playlist_results['items']) == 0:
            break
        tracks.extend([item['track']['uri'] for item in playlist_results['items'] if item['track'] is not None])
        index += 100
        print(f"Added {len(playlist_results['items'])} tracks from {playlist['name']}")
    return tracks

def main(args: configargparse.Namespace):

    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=args.client_id,
                                client_secret=args.client_secret,
                                redirect_uri=args.redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlists = get_user_playlists(sp)
    
    # Add all tracks from all playlists to a list
    all_tracks = []
    for playlist in playlists:
        tracks = get_tracks(sp, playlist)
        all_tracks.extend(tracks)

    print(f"Found {len(all_tracks)} tracks")
    
    # remove duplicates
    all_tracks = list(set(all_tracks))
    print(f"Left with {len(all_tracks)} unique tracks after removing duplicates")

    # get user saved tracks
    saved_tracks = get_user_saved_tracks(sp)

    # find tracks that saved_tracks has that all_tracks doesn't
    orphans = [track for track in saved_tracks if track not in all_tracks]
    print(f"Found {len(orphans)} orphaned tracks")

    # Write out to file
    with open("orphans.txt", "w") as f:
        for orphan in orphans:
            f.write(f"{orphan}\n")

    # add to playlist
    orphaned_playlist_name = sp.playlist(args.playlist)['id']

    add_tracks_to_playlist(sp, orphaned_playlist_name, orphans)

def add_existing(args: configargparse.Namespace):
    """
    """
    auth_manager = SpotifyOAuth(scope=SCOPE,
                                client_id=args.client_id,
                                client_secret=args.client_secret,
                                redirect_uri=args.redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    with open("orphans.txt", "r") as f:
        orphans = f.readlines()
        orphans = [orphan.strip() for orphan in orphans]

    # add to playlist
    orphaned_playlist_name = sp.playlist(args.playlist)['id']

    add_tracks_to_playlist(sp, orphaned_playlist_name, orphans)

if __name__ == "__main__":
    parser = configargparse.ArgParser(default_config_files=["auth.cfg"])
    parser.add_argument("-c", "--config", is_config_file=True, help="config file path")
    parser.add_argument("--client-id", required=True, help="Spotify Client ID")
    parser.add_argument("--client-secret", required=True, help="Spotify Client Secret")
    parser.add_argument("--playlist", required=True, help="Playlist URI")
    parser.add_argument("--redirect-uri", default="http://localhost:8090", help="OAuth Redirect URI")
    parser.add_argument("--existing", action="store_true", help="add cached list")

    args = parser.parse_args()

    if args.existing:
        add_existing(args)
    else:
        main(args)
