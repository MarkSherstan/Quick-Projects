import numpy as np
import pickle
import glob
import cv2
import cv2.aruco as aruco

class CalibrateCamera:
    def __init__(self):
        # Set dictionary
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
                
        # Camera
        self.cam = None
        
        # Calibration matrices
        self.mtx = None
        self.dist = None

        # Folder paths and extensions
        self.calibrationDir = 'calibrationImgs/'
        self.imgExtension = '.jpg'

    def connectCamera(self, desiredWidth, desiredHeight, desiredFPS, autoFocus=0, src=1):
        # Connect to camera
        try:
            self.cam = cv2.VideoCapture(src)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, desiredWidth)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, desiredHeight)
            self.cam.set(cv2.CAP_PROP_FPS, desiredFPS)
            self.cam.set(cv2.CAP_PROP_AUTOFOCUS, autoFocus)
            print('Camera start')
        except:
            print('Camera setup failed')
        
        
    def generateCharucoBoard(self, rows=7, columns=5):
        # Create the board
        board = aruco.CharucoBoard_create(
                    squaresX=columns,
                    squaresY=rows,
                    squareLength=0.025,
                    markerLength=0.0125,
                    dictionary=self.arucoDict)
        img = board.draw((100*columns, 100*rows))

        # Save it to a file
        cv2.imwrite('CharucoBoard.png', img)

    def generateArucoMarker(self, ID=7, size=700):
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

        while(True):
            # Get frame and show
            _, frame = self.cam.read()
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
        self.cam.release()
        cv2.destroyAllWindows()

    def calibrateCamera(self, rows=7, columns=5, lengthSquare=0.035, lengthMarker=0.0175):
        # Create charuco board with actual measured dimensions from print out
        board = aruco.CharucoBoard_create(
                    squaresX=columns,
                    squaresY=rows,
                    squareLength=lengthSquare,
                    markerLength=lengthMarker,
                    dictionary=self.arucoDict)

        # Storage variables
        cornerList = []
        idList = []

        # Get image paths from calibration folder
        paths = glob.glob(self.calibrationDir + '*' + self.imgExtension)

        # Empty imageSize variable to be determined at runtime
        imageSize = None

        # Loop through all images
        for filePath in paths:
            # Read image and convert to gray
            img = cv2.imread(filePath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find aruco markers in the query image
            corners, ids, _ = aruco.detectMarkers(image=gray, dictionary=self.arucoDict)

            # Outline the aruco markers found in the query image
            img = aruco.drawDetectedMarkers(image=img, corners=corners)

            # Get charuco corners and ids from detected aruco markers
            response, charucoCorners, charucoIDs = aruco.interpolateCornersCharuco(
                    markerCorners=corners,
                    markerIds=ids,
                    image=gray,
                    board=board)

            # If at least 20 corners were found
            if response > 20:
                # Add the corners and ids to calibration list
                cornerList.append(charucoCorners)
                idList.append(charucoIDs)

                # Draw the Charuco board detected to show calibration results
                img = aruco.drawDetectedCornersCharuco(
                        image=img,
                        charucoCorners=charucoCorners,
                        charucoIds=charucoIDs)

                # If image size is still None, set it to the image size
                if not imageSize:
                    imageSize = gray.shape[::-1]
                    
            else:
                # Error message
                print('Error in: ' + str(filePath))
                cv2.imshow('ERROR: ' + str(filePath), img)                
                cv2.waitKey(0)

        # Destroy any open windows
        cv2.destroyAllWindows()

        # Make sure at least one image was found
        if len(paths) < 1:
            print('No images of charucoboards were found.')
            return

        # Make sure at least one charucoboard was found
        if not imageSize:
            print('Images supplied were not regonized by calibration')
            return

        # Run calibration
        _, self.mtx, self.dist, _, _ = aruco.calibrateCameraCharuco(
                charucoCorners=cornerList,
                charucoIds=idList,
                board=board,
                imageSize=imageSize,
                cameraMatrix=None,
                distCoeffs=None)

        # Display matrix and distortion coefficients
        print(self.mtx)
        print(self.dist)

        # Pickle the results
        f = open('calibration.pckl', 'wb')
        pickle.dump((self.mtx, self.dist), f)
        f.close()

    def getCalibration(self):
        # Open file, retrieve variables, and close
        file = open('resources/calibration.pckl', 'rb')
        self.mtx, self.dist = pickle.load(file)
        file.close()
        