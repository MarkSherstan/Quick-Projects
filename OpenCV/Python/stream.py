import cv2

# Required to communicate with USB capture device
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
# cam.set(cv2.CAP_PROP_FPS, 30)

cam = cv2.VideoCapture(0, cv2.CAP_V4L)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cam.set(cv2.CAP_PROP_FOCUS, 0)
cam.set(cv2.CAP_PROP_ZOOM, 0)

# Display frame forever until q is pressed
while(True):
    _, frame = cam.read()
    cv2.imshow('Frame', frame)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

# Clear connections and window
cam.release()
cv2.destroyAllWindows()