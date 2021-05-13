import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
import sys
from simple_term_menu import TerminalMenu
import requests
import json
from pprint import pprint

def picker(names: list):
    terminal_menu = TerminalMenu(names)
    return terminal_menu.show()

def play(track_id: str):
    # res = sp.devices()
    # print(res)
    # pprint(res)
    sp.start_playback(uris=['spotify:track:' + track_id])

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

try:
    username = sys.argv[1]
except IndexError:
    username = input('Username: ')

playlists = sp.user_playlists(username)['items']
playlists_names = []
for playlist in playlists:
    playlists_names.append(playlist['name'])

idx = picker(playlists_names)

playlist_id = playlists[idx]['id']
tracks = sp.playlist(playlist_id)['tracks']['items']
tracks_info = []
for track in tracks:
    name = track['track']['name']
    artist = track['track']['artists'][0]['name']
    album = track['track']['album']['name']
    tracks_info.append(' \| '.join([name, artist, album]))

idx = picker(tracks_info)
track_id = tracks[idx]['track']['id']

play(track_id)

