import cv2
import numpy as np

from qr_data import QRCode

def detect():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()

        data = detector.detectAndDecode(frame)

        if data[0] != '':
            print(data[0])
            break

        cv2.imshow('frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key != 255 or cv2.getWindowProperty('frame', cv2.WND_PROP_AUTOSIZE) == -1:
            break

    cap.release()
    cv2.destroyAllWindows()
    return data[0]