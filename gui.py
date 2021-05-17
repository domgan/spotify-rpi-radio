import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
import base64
import requests
from radio import Radio


def image_obj(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size)

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


def get_playlist_cover(curr_playlist):
    for i, playlist in enumerate(playlists):
        if curr_playlist == playlist:
            break
    return playlists_covers[i]


radio = Radio()
playlists, playlists_covers = radio.get_playlists()
#tracks_info, tracks_uris = radio.get_tracks(playlist_idx)


url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/1024px-Spotify_logo_without_text.svg.png'
size = (225, 225)
image = image_obj(url)

sg.theme('DarkBlack1')

left_column = [[sg.Button('Play')], [sg.Button('Next')]]
central_column = [[sg.Image(data=image, key='-IMAGE-')]]
right_column = [[sg.Button('Vol-')], [sg.Button('Vol+')]]

bot_row = [[sg.Listbox(values=playlists, size=(60, 18), key='-LIST-', enable_events=True)]]

layout = [[sg.Column(left_column, justification='l'),
    sg.Column(central_column, justification='c'),
    sg.Column(right_column, justification='r')],
    
    [sg.Column(bot_row, justification='c')]]

# Create the Window
window = sg.Window('Window Title', layout, size=(250*3, 400))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    image = image_obj(get_playlist_cover(values['-LIST-'][0]))
    window['-IMAGE-'].update(data=image)

window.close()

