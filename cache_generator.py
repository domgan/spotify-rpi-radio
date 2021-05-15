import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import os, stat

#os.chmod('.cache', stat.S_IWRITE)
try:
    os.remove('.cache')
except FileNotFoundError:
    pass

scope='playlist-read-private user-modify-playback-state app-remote-control streaming user-read-playback-state'
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))
res = sp.devices()
pprint(res)
