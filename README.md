# Spotify Scripts

Setup:

`pip install -r requirements.txt`

optionally: create a file called `auth.cfg` and populate the following:

```ini
client-id=<fill me in>
client-secret=<fill me in>
playlist=<fill me in>
redirect-uri=http://localhost:8090
```

## Artist Top Songs from Playlist

_Script: `top-songs.py`_

Usage: `python3 top-songs.py --help`

A script that takes a playlist as input, and creates a new playlist with the top N songs for each artist in the original playlist.

__Inspiration__: If I add a newly-discovered track to one of my playlists, I often open the artists page to find more songs I like by them.

## Bulk add songs to playlist (From Mixcloud)

_Script: `bulk_add.py`_

Usage: `python3 bulk_add.py --help`

Given a file of song names, formatted to the table output from [this script](https://github.com/max-bp/New-Mixcloud-Tracklist-Enabler), add all the songs to a new playlist.
Script uses a regex to get the names from each line.

Example file contents:
```
1 	KEENO - UNREACHABLE 	00:00
2 	KEENO - SUNFLOWERS 	00:00
3 	PYXIS - INNERSPACE 	00:00
4 	FRED V - ATMOSPHERE 	00:00
5 	WINSLOW - MUMBLES OF GRACE 	00:00
6 	FLUIDITY - STILL HOPE 	00:00
```

Alternatively you can use the `--pre-formatted` flag if the file has been cleaned already:

```
Metrik & Grafix - Parallel
Lexurus - Crystallize
Sub Focus & Wilkinson - Air I Breathe
Grafix - Distressed
Metrik - Ex Machina
```

__Inspiration__: So I can save the songs I listened to in a mixcloud mix. Mixcloud hides the tracklist for free users, but the script mentioned above generates a table in the mix description. The eventual goal with this script is to incorporate the mixcloud track-list script into here so all the user needs to do is put in the mix url and it generates the playlist

## Playlist Poster Generator

_Script: `playlist_poster_generator.py`_

Generates a poster using the album art from the songs in a playlist.

