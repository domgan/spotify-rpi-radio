import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import os, stat


scope='playlist-read-private user-modify-playback-state app-remote-control streaming user-read-playback-state'
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))
res = sp.devices()
pprint(res)
