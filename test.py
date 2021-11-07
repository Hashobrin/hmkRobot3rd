import cv2
import numpy as np
import PySimpleGUI as sg

layout = [
    [sg.Image(filename='', key='-image-')],
]

window = sg.Window('title', layout=layout)

while True:
    event, values = window.read()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    retval, frame = cap.read()
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window['-image-'].update(data=imgbytes)

    if event in ('Quit', sg.WIN_CLOSED):
        break

window.close()
