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


#radio = Radio()
#playlists = radio.get_playlists()
#tracks_info, tracks_uris = radio.get_tracks(playlist_idx)


url = 'https://i.scdn.co/image/ab67616d0000b273bfcd8d6b28c07d92a902e1c2'
size = (250, 250)
image = image_obj(url)

sg.theme('DarkBlack1')

left_column = [[sg.Button('Play')], [sg.Button('Next')]]
central_column = [[sg.Image(data=image, key='-IMAGE-')]]
right_column = [[sg.Button('Vol-')], [sg.Button('Vol+')]]

layout = [[sg.Column(left_column, justification='left'),
    sg.Column(central_column, justification='center'),
    sg.Column(right_column, justification='right')]]

# Create the Window
window = sg.Window('Window Title', layout, size=(250*3, 400))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

