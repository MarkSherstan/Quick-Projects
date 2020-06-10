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
            self.cam.set(cv2.CAP_PROP_AUTOFOCUS, self.autoFocus)
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

    def rotationMatrix2EulerAngles(self, R):
        try:
            # Check if rotation matrix is valid
            assert(self.isRotationMatrix(R))

            # Dont rotate more than 45 degrees in any direction and we will not get gimbal lock / singularities
            roll  = math.degrees(-math.asin(R[2,0]))
            pitch = math.degrees(math.atan2(R[2,1], R[2,2]))
            yaw   = math.degrees(math.atan2(R[1,0], R[0,0]))
            
            # Return results
            return roll, pitch, yaw
        except:
            # Return 0's upon failure
            print('Not a rotation matrix')
            return 0, 0, 0

    def transform2Body(self, R, t):
        # Original
        Tca = np.append(R, np.transpose(t), axis=1)
        Tca = np.append(Tca, np.array([[0, 0, 0, 1]]), axis=0)

        # Transformation
        Tbc = np.array([[0,  0,  1,  10],
                        [1,  0,  0,   0],
                        [0,  1,  0,  -2],
                        [0,  0,  0,   1]])

        # Resultant pose
        Tba = np.dot(Tbc, Tca)

        # Return results
        R = Tba[0:3,0:3]
        t = Tba[0:3,3]

        # Return reults 
        return R, t

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

            # Flip the image back to normal
            # gray = cv2.rotate(gray, cv2.ROTATE_180)

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

                # Hopefully there is only one marker for now... 
                for ii in range(0, ids.size):
                    # Convert to rotation matrix
                    R, _ = cv2.Rodrigues(rvec[ii])

                    # Convert to body frame and get roll, pitch, yaw
                    R, t = self.transform2Body(R, tvec[ii])
                    roll, pitch, yaw = self.rotationMatrix2EulerAngles(R)

                    # Extract NED
                    north = t[0]
                    east  = t[1]
                    down  = t[2]

                    # Fix yaw
                    roll = roll
                    pitch = (pitch + 90) * -1
                    yaw = (yaw - 90) * -1

                    # Add values to frame 
                    cv2.putText(frame, "N: " + str(round(north,1)), (0, 50), font, 1, fontColor, 2)
                    cv2.putText(frame, "E: " + str(round(east,1)), (0, 75), font, 1, fontColor, 2)
                    cv2.putText(frame, "D: " + str(round(down,1)), (0, 100), font, 1, fontColor, 2)

                    cv2.putText(frame, "R: " + str(round(roll,1)), (0, 150), font, 1, fontColor, 2)
                    cv2.putText(frame, "P: " + str(round(pitch,1)), (0, 175), font, 1, fontColor, 2)
                    cv2.putText(frame, "Y: " + str(round(yaw,1)), (0, 200), font, 1, fontColor, 2)

                    # Print values
                    print('n: {:<8.1f} e: {:<8.1f} d: {:<8.1f} r: {:<8.1f} p: {:<8.1f} y: {:<8.1f}'.format(north, east, down, roll, pitch, yaw))

            # display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When complete close everything down
        self.cam.release()
        cv2.destroyAllWindows()
