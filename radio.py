import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
import sys
from simple_term_menu import TerminalMenu
import requests
import json
from pprint import pprint
from collections import deque

def picker(names: list):
    terminal_menu = TerminalMenu(names)
    return terminal_menu.show()

def play(start_idx, tracks_uris: list):
    device_id = get_device_id()

    deq = deque(tracks_uris)
    deq.rotate(-start_idx)
    tracks_uris = list(deq)

    #tracks_uris = ['spotify:track:' + tr_id for tr_id in tracks_ids]
    sp.start_playback(device_id=device_id, uris=tracks_uris)
    control()

def control():
    while True:
        uri = sp.currently_playing()['item']['uri']
        print('Commands: volume | next | resume | pause.')
        inp = input('Command: ')
        device_id = get_device_id()
        if inp == 'volume':
            sp.volume(int(input('From 0 to 100: ')), device_id=device_id)
        elif inp == 'next':
            sp.next_track(device_id=device_id)
        elif inp == 'pause':
            sp.pause_playback(device_id=device_id)
        elif inp == 'resume':
            sp.start_playback(device_id=device_id, uris=[uri])

def get_device_id():
    devices = sp.devices()
    for device in devices['devices']:
        if 'raspotify' in device['name']:
            return device['id']
    raise Exception('Device raspotify not found')

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
context_uri = playlists[idx]['uri']
tracks = sp.playlist(playlist_id)['tracks']['items']
tracks_info, tracks_uris = [], []
for track in tracks:
    name = track['track']['name']
    artist = track['track']['artists'][0]['name']
    album = track['track']['album']['name']
    tracks_info.append(' \| '.join([name, artist, album]))
    tracks_uris.append(track['track']['uri'])

start_idx = picker(tracks_info)

play(start_idx, tracks_uris)

