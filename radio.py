import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
import sys
from simple_term_menu import TerminalMenu
from pprint import pprint
from collections import deque
import os

### Create Radio for current user if "username" not specified.


class Radio:
    def __init__(self, username=None):
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self.device_id = self.get_device_id()
        if username:
            self.playlists_obj = self.sp.user_playlists(username)['items']
            self.username = username
        else:
            self.playlists_obj = self.sp.current_user_playlists()['items']
            # self.username = auth_manager.username # TODO

    def picker(self, names: list):
        terminal_menu = TerminalMenu(names)
        return terminal_menu.show()

    def play(self, start_idx, tracks_uris: list):
        deq = deque(tracks_uris)
        deq.rotate(-start_idx)
        tracks_uris = list(deq)

        #tracks_uris = ['spotify:track:' + tr_id for tr_id in tracks_ids]
        self.sp.start_playback(device_id=self.device_id, uris=tracks_uris)

    def control(self):
        while True:
            curr = self.sp.currently_playing()
            progress = curr['progress_ms']
            uri = curr['item']['uri']

            print('Commands: volume | next | resume | pause | stop.')
            inp = input('Command: ')
            if inp == 'volume':
                self.sp.volume(int(input('From 0 to 100: ')), device_id=self.device_id)
            elif inp == 'next':
                self.sp.next_track(device_id=self.device_id)
            elif inp == 'pause':
                self.sp.pause_playback(device_id=self.device_id)
            elif inp == 'resume':
                self.sp.start_playback(device_id=self.device_id, uris=[uri], position_ms=progress)
            elif inp == 'stop':
                self.sp.pause_playback(device_id=self.device_id)
                break

    def get_device_id(self):
        try:
            devices = self.sp.devices()
        except:
            try:
                os.remove('.cache')
            except FileNotFoundError:
                pass
            raise Exception('Need new .cache file')
        for device in devices['devices']:
            if 'raspotify' in device['name']:
                return device['id']
        raise Exception('Device raspotify not found')

    def get_playlists(self):
        playlists_names, playlists_covers = [], []
        for playlist in self.playlists_obj:
            playlists_covers.append(playlist['images'][0]['url'])
            playlists_names.append(playlist['name'])
        return playlists_names, playlists_covers

    def get_tracks(self, playlist_idx, escape=True):
        playlist_id = self.playlists_obj[playlist_idx]['id']
        context_uri = self.playlists_obj[playlist_idx]['uri']
        tracks = self.sp.playlist(playlist_id)['tracks']['items']
        tracks_info, tracks_uris, tracks_covers = [], [], []
        for track in tracks:
            name = track['track']['name']
            artist = track['track']['artists'][0]['name']
            album = track['track']['album']['name']
            tracks_info.append(' \| '.join([name, artist, album]))
            tracks_uris.append(track['track']['uri'])
            tracks_covers.append(track['track']['album']['images'][0]['url'])
        if not escape:
            tracks_info = [info.replace('\|', '|') for info in tracks_info]
        return tracks_info, tracks_uris, tracks_covers

    def get_cover_url(self):
        return self.sp.currently_playing()['item']['album']['images'][0]['url']

    def run_in_terminal(self):
        playlist_idx = self.picker(self.get_playlists()[0])
        tracks_info, tracks_uris = self.get_tracks(playlist_idx)
        start_idx = self.picker(tracks_info)
        self.play(start_idx, tracks_uris)
        self.control()


if __name__ == '__main__':
    radio = Radio()
    radio.run_in_terminal()

