import numpy as np
import pickle
import glob
import cv2
import cv2.aruco as aruco
import math
import time

class Test:
    def __init__(self):
        # Set dictionary
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
       
        # Some image 
        self.img = None 

        # Calibration matrices
        self.mtx = None
        self.dist = None

    def startCamera(self, desiredWidth, desiredHeight, desiredFPS, src=0):
        # Connect to camera
        try:
            self.cam = cv2.VideoCapture(src)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, desiredWidth)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, desiredHeight)
            self.cam.set(cv2.CAP_PROP_FPS, desiredFPS)
            self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            time.sleep(10)
            print('Camera start')
            
        except:
            print('Camera setup failed')

    def getCalibration(self):
        # Open file, retrieve variables, and close
        file = open('calibration.pckl', 'rb')
        self.mtx, self.dist = pickle.load(file)
        file.close()

    def takeSnapShot(self):
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
                    cv2.imwrite('testImg.jpg', frame)
                elif key & 0xFF == ord('q'):
                    break

        # When complete close everything down
        self.cam.release()
        cv2.destroyAllWindows()

    def loadImage(self, fileName='testImg.jpg', showImage=False):
        self.img = cv2.imread(fileName)

        if showImage is True:
            cv2.imshow('Test Image', self.img)                
            cv2.waitKey(0)

    def isRotationMatrix(self, R):
        # Checks if matrix is valid
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    def rotationMatrix2Euler(self, R):
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

    # Calculates Rotation Matrix given euler angles.
    def euler2RotationMatrix(self, roll, pitch, yaw):
        angle = np.array([math.radians(roll), math.radians(pitch), math.radians(yaw)])

        Rx = np.array([[1,         0,                    0                  ],
                       [0,         math.cos(angle[0]),  -math.sin(angle[0]) ],
                       [0,         math.sin(angle[0]),   math.cos(angle[0]) ]])
                             
        Ry = np.array([[ math.cos(angle[1]),    0,      math.sin(angle[1]) ],
                       [ 0,                     1,      0                  ],
                       [-math.sin(angle[1]),    0,      math.cos(angle[1]) ]])
                    
        Rz = np.array([[math.cos(angle[2]),    -math.sin(angle[2]),    0 ],
                       [math.sin(angle[2]),     math.cos(angle[2]),    0 ],
                       [0,                     0,                      1 ]])
                                     
        R = np.dot(Rz, np.dot(Ry, Rx))

        return R

    def analyze(self, lengthMarker=24.7):
        # Get the calibration
        try:
            self.getCalibration()
        except:
            print('Calibration not found!')
            return

        # Set parameters
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10

        # Convert frame to grey and show
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Test Image', gray)                
        # cv2.waitKey(0)

        # Rotate image
        # gray = cv2.rotate(gray, cv2.ROTATE_180)
        # cv2.imshow('Test Image 180', gray)                
        # cv2.waitKey(0)

        # lists of ids and corners belonging to each id
        corners, ids, _ = aruco.detectMarkers(gray, self.arucoDict, parameters=parameters)

        # Only continue if a marker was found
        if np.all(ids != None):
            # Estimate the pose
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, lengthMarker, self.mtx, self.dist)

            # Draw axis for each aruco marker found
            for ii in range(0, ids.size):
                aruco.drawAxis(self.img, self.mtx, self.dist, rvec[ii], tvec[ii], 10)

            # Draw square around markers
            aruco.drawDetectedMarkers(self.img, corners)

            # Print ids found in top left and to the screen
            idz = ''
            for ii in range(0, ids.size):
                idz += str(ids[ii][0])+' '
                x = round(tvec[ii][0][0],1)
                y = round(tvec[ii][0][1],1)
                z = round(tvec[ii][0][2],1)

                # Convert to rotation matrix and extract yaw
                R, _ = cv2.Rodrigues(rvec[ii])
                eulerAngles = self.rotationMatrix2Euler(R)
                roll = math.degrees(eulerAngles[0])
                pitch = math.degrees(eulerAngles[1])
                yaw = math.degrees(eulerAngles[2])
                R2 = self.euler2RotationMatrix(roll, pitch, yaw)

                # Print values
                print(R)
                print(R2)
                print('x: {:<8.1f} y: {:<8.1f} z: {:<8.1f} r: {:<8.1f} p: {:<8.1f} y: {:<8.1f}'.format(x, y, z, roll, pitch, yaw))

        # Show final image
        # cv2.imshow('Processed', self.img)                
        # cv2.waitKey(0)



def main():
    t = Test()

    # t.startCamera(1280, 960, 30)
    # t.takeSnapShot()
    t.loadImage()
    t.analyze()

# Main loop 
if __name__ == '__main__':
    main()