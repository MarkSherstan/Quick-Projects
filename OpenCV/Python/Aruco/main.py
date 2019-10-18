import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import time
import pickles


class ARUCO_CLAW:
    def __init__(self, arucoDict=aruco.DICT_6X6_250):
        self.arucoDict = aruco.Dictionary_get(arucoDict)
        self.frameWidth = 1280
        self.frameHeight = 720

        self.calibrationDir = 'calibration/'
        self.imgExtension = '.jpg'

    def generateMarker(self, ID=7, size=700):
        # Create an image from the marker
        img = aruco.drawMarker(self.arucoDict, ID, size)

        # Save and display (press any key to exit)
        cv2.imwrite('ARUCO_'+str(ID)+'.png', img)
        cv2.imshow('Marker ID: ' + str(ID), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def captureCalibrationImages(self):
        # Initialize snapshot counter
        index = 0

        # Start webcam
        cam = cv2.VideoCapture(1)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.frameWidth)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frameHeight)

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
                    indexedFile = self.calibrationDir + 'IMG_' + str(index) + self.imgExtension
                    print(indexedFile)
                    cv2.imwrite(indexedFile, frame)
                    index += 1
                elif key & 0xFF == ord('q'):
                    break

        # Clear connections and window
        cam.release()
        cv2.destroyAllWindows()

    def calibrateData(self):


def main():
    # Set up class
    ac = ARUCO_CLAW(aruco.DICT_5X5_1000)

    # ac.generateMarker()


# Main loop
if __name__ == '__main__':
	main()
