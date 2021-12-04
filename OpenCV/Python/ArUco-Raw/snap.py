import numpy as np
import cv2

desiredWidth=1280
desiredHeight=720
desiredFPS=30
cameraIdx=0

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, desiredWidth)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, desiredHeight)
cam.set(cv2.CAP_PROP_FPS, desiredFPS)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
print('Camera start')

for _ in range(10):
    _, frame = cam.read()

cv2.imwrite('Snap.png',frame)

cam.release()