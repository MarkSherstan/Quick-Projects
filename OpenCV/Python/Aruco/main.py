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

    def calibrateCamera(self):
        # Based on: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
        # Store object points (3D) and image points (2D) from processed images
        objpoints = []
        imgpoints = []

        # Chessboard size
        rowCount = 9
        colCount = 6

        # prepare object points, e.g (0,0,0), (1,0,0), (2,0,0) ... (rowCount-1,colCount-1,0)
        objp = np.zeros((rowCount*colCount,3), np.float32)
        objp[:,:2] = np.mgrid[0:rowCount,0:colCount].T.reshape(-1,2)

        # Get image paths from calibration folder
        paths = glob.glob(self.calibrationDir + '*' + self.imgExtension)

        # Empty imageSize variable for run time
        imageSize = None

        # Loop through all the images
        for filePath in paths:
            # Read image and convert to gray
            img = cv2.imread(filePath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (rowCount,colCount), None)

            # If points are found
            if ret == True:
                # Add points discovered
                objpoints.append(objp)

                # Refines the corner locations and add the points
                corners2 = cv2.cornerSubPix(
                                image = gray,
                                corners = corners,
                                winSize = (11,11),
                                zeroZone = (-1,-1),
                                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
                imgpoints.append(corners2)

                # Get image size for calibration later
                if not imageSize:
                    imageSize = gray.shape[::-1]

                # Draw and display the calibration. Wait for user to smash a key before moving on
                img = cv2.drawChessboardCorners(gray, (rowCount,colCount), corners2, ret)
                cv2.imshow(filePath, img)
                cv2.waitKey(0)
            else:
                print('Not able to detect a chessboard in image: {}'.format(filePath))

        # Close all windows
        cv2.destroyAllWindows()

        # Error handling
        if not imageSize:
            print('Calibration failed. Try again with more / new images')
            exit()

        # Run calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                                            objectPoints = objpoints,
                                            imagePoints = imgpoints,
                                            imageSize = imageSize,
                                            cameraMatrix = None,
                                            distCoeffs = None)

        # Display matrix and distortion coefficients
        print(mtx)
        print(dist)

        # Pickle the results
        f = open('calibration.pckl', 'wb')
        pickle.dump((mtx, dist), f)
        f.close()

    def getCalibration(self, calFile):
        # Open file, retrieve variables, and close
        file = open(calFile, 'rb')
        self.mtx, self.dist = pickle.load(file)
        file.close()


def main():
    # Set up class
    ac = ARUCO_CLAW(aruco.DICT_5X5_1000)

    # ac.generateMarker()


# Main loop
if __name__ == '__main__':
	main()
