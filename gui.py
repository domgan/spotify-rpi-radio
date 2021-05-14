import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
import base64
import requests

def image_obj(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size)

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

url = 'https://i.scdn.co/image/ab67616d0000b273bfcd8d6b28c07d92a902e1c2'
size = (250, 250)
image = image_obj(url)

sg.theme('DarkBlack1')
layout = [[sg.Image(data=image, key='-IMAGE-')]]
# Create the Window
window = sg.Window('Window Title', layout, size=(800, 800))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()

