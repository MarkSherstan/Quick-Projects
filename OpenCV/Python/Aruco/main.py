import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import time


class A:
    def __init__(self):
        self.

    def createGrid(self):




# Define some variables
index = 0
directory = 'calibration/'
fileName = 'IMG_'
fileExtension = '.jpg'

# Required to communicate with USB webcam. Set some parameters
# https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
# Changed in the app (Camera settings)
# Disabled auto focus and auto white
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(True):
    # Get frame and show
    _, frame = cam.read()
    cv2.imshow('Frame', frame)

    # Check keyboard commands
    #   'space' -> Snapshot
    #   'q' -> Quit
    key = cv2.waitKey(1)

    if key != -1:
        if key & 0xFF == ord(' '):
            indexedFile = directory + fileName + str(index) + fileExtension
            print(indexedFile)
            cv2.imwrite(indexedFile, frame)
            index += 1
        elif key & 0xFF == ord('q'):
            break

# Clear connections and window
cam.release()
cv2.destroyAllWindows()



def main():
    # Set up class
    gyro = 250      # 250, 500, 1000, 2000 [deg/s]
    acc = 2         # 2, 4, 7, 16 [g]
    tau = 0.98
    mpu = MPU(gyro, acc, tau)

    # Set up sensor and calibrate gyro with N points
    mpu.setUp()
    mpu.calibrateGyro(500)

    # Run for 20 secounds
    startTime = time.time()
    while(time.time() < (startTime + 20)):
        mpu.compFilter()

    # End
    print("Closing")

# Main loop
if __name__ == '__main__':
	main()
