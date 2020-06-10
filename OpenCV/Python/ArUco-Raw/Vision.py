import numpy as np
import pickle
import glob
import cv2
import cv2.aruco as aruco
import math

class Vision:
    def __init__(self, desiredWidth, desiredHeight, desiredFPS, autoFocus=0, src=1):
        # Set dictionary
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_5X5_1000)

        # Camera config 
        self.desiredWidth  = desiredWidth
        self.desiredHeight = desiredHeight
        self.desiredFPS    = desiredFPS   
        self.autoFocus     = autoFocus 
        
        # Connect to camera
        try:
            self.cam = cv2.VideoCapture(src)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.desiredWidth)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.desiredHeight)
            self.cam.set(cv2.CAP_PROP_FPS, self.desiredFPS)
            self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            print('Camera start')
        except:
            print('Camera setup failed')

        # Calibration matrices
        self.mtx = None
        self.dist = None

    def getCalibration(self):
        # Open file, retrieve variables, and close
        file = open('calibration.pckl', 'rb')
        self.mtx, self.dist = pickle.load(file)
        file.close()

    def isRotationMatrix(self, R):
        # Checks if matrix is valid
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    def rotationMatrixToEulerAngles(self, R):
        # Check if rotation matrix is valid
        assert(self.isRotationMatrix(R))

        # Check if singular
        sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

        if (sy < 1e-6):
            # Singular
            x = math.atan2(-R[1,2], R[1,1])
            y = math.atan2(-R[2,0], sy)
            z = 0
        else:
            # Not singular
            x = math.atan2(R[2,1] , R[2,2])
            y = math.atan2(-R[2,0], sy)
            z = math.atan2(R[1,0], R[0,0])

        # Return roll, pitch, and yaw in some order
        return np.array([x, y, z])

    def trackAruco(self, lengthMarker=0.247):
        # Get calibration data
        try:
            self.getCalibration()
        except:
            print('Calibration not found!')
            return

        # Font and color for screen writing
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontColor = (0, 255, 0)

        # Set parameters
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10

        while(True):
            # Get frame and convert to gray
            _, frame = self.cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # lists of ids and corners belonging to each id
            corners, ids, _ = aruco.detectMarkers(gray, self.arucoDict, parameters=parameters)

            # Only continue if a marker was found
            if np.all(ids != None):
                # Estimate the pose
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, lengthMarker, self.mtx, self.dist)

                # Draw axis for each aruco marker found
                for ii in range(0, ids.size):
                    aruco.drawAxis(frame, self.mtx, self.dist, rvec[ii], tvec[ii], 10)

                # Draw square around markers
                aruco.drawDetectedMarkers(frame, corners)

                # Print ids found in top left and to the screen
                idz = ''
                for ii in range(0, ids.size):
                    idz += str(ids[ii][0])+' '
                    x = round(tvec[ii][0][0],1)
                    y = round(tvec[ii][0][1],1)
                    z = round(tvec[ii][0][2],1)

                    cv2.putText(frame, "ID: " + idz, (0, 25), font, 1, fontColor, 2)
                    cv2.putText(frame, "X: " + str(x), (0, 50), font, 1, fontColor, 2)
                    cv2.putText(frame, "Y: " + str(y), (0, 75), font, 1, fontColor, 2)
                    cv2.putText(frame, "Z: " + str(z), (0, 100), font, 1, fontColor, 2)

                    # Convert to rotation matrix and extract yaw
                    R, _ = cv2.Rodrigues(rvec[ii])
                    eulerAngles = self.rotationMatrixToEulerAngles(R)
                    roll = math.degrees(eulerAngles[2])
                    pitch = math.degrees(eulerAngles[0])
                    yaw = math.degrees(eulerAngles[1])

                    # Print values
                    print('x: {:<8.1f} y: {:<8.1f} z: {:<8.1f} r: {:<8.1f} p: {:<8.1f} y: {:<8.1f}'.format(x, y, z, roll, pitch, yaw))

            # display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When complete close everything down
        self.cam.release()
        cv2.destroyAllWindows()
