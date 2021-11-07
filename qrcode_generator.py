import os
import pyqrcode
from dbController import getRow
def generate():
    qrImg = str(os.getcwd()) + '/qrcode/' + str(getRow()) + '.png'

    code = pyqrcode.create(
        str(getRow()),
        error='L',
        version=3,
        mode='binary'
    )
    code.png(
        qrImg,
        scale=5,
        module_color=[0, 0, 0, 128],
        background=[255, 255, 255]
    )
