import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
import base64
import requests
from radio import Radio


def image_obj(url):
    size = (225, 225)
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size)

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


def get_idx(current, all_list):
    for i, elem in enumerate(all_list):
        if current == elem:
            return i


radio = Radio()
playlists, playlists_covers_urls = radio.get_playlists()
playlists_covers = [image_obj(u) for u in playlists_covers_urls]


url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/1024px-Spotify_logo_without_text.svg.png'
image = image_obj(url)

sg.theme('DarkBlack1')

left_column = [[sg.Button('Play')], [sg.Button('Pause')]]
central_column = [[sg.Image(data=image, key='-IMAGE-')]]
right_column = [[sg.Button('Vol+')], [sg.Button('Vol-')]]

bot_row = [[sg.Listbox(values=playlists, size=(85, 20), key='-LIST-', enable_events=True)]]

layout = [[sg.Column(left_column),
    sg.Column(central_column, justification='c'),
    sg.Column(right_column)],
    
    [sg.Column(bot_row, justification='c')]]

# Create the Window
window = sg.Window('Window Title', layout, size=(250*3, 400))
# Event Loop to process "events" and get the "values" of the inputs
choosing_playlist, choosing_track = True, False
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if choosing_playlist:
        playlist_idx = get_idx(values['-LIST-'][0], playlists)
        image = playlists_covers[playlist_idx]
        window['-IMAGE-'].update(data=image)
        if event == 'Play':
            tracks_info, tracks_uris, tracks_covers = \
                    radio.get_tracks(playlist_idx, escape=False)
            choosing_playlist, choosing_track = False, True
            window['-LIST-'].update(values=tracks_info)
    elif choosing_track:
        track_idx = get_idx(values['-LIST-'][0], tracks_info)
        image = image_obj(tracks_covers[track_idx])
        window['-IMAGE-'].update(data=image)
        if event == 'Play':
            radio.play(track_idx, tracks_uris)


window.close()

