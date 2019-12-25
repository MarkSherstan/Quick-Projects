# Import the necessary packages
import numpy as np
import imutils
import time
import cv2


class video:
	def __init__(self):
		# Video properties
		self.width = 720
		self.height = 480
		self.FPS = 10

		# HSV mask range
		self.HSVlower = np.array([140,0,200])
		self.HSVupper = np.array([160,255,255])

		# Kernal
		self.kernel = np.ones((7,7), np.uint8)

		# Location of object and laser
		self.objectX = 0
		self.objectY = 0
		self.laserX = 0
		self.laserY = 0

	def startCamera(self):
		# Create video capture object and configure settings
		self.cam = cv2.VideoCapture(1)
		self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
		self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
		self.cam.set(cv2.CAP_PROP_FPS, self.FPS)

		# Build the foreground/background detection algorithm
		self.subtractor = cv2.createBackgroundSubtractorMOG2(history=600, varThreshold=100, detectShadows=False)

	def findObject(self):
		# Read a frame
		_, frame = self.cam.read()

		# Dilate the frame and convert to HSV
		frameDilate = cv2.dilate(frame, self.kernel, iterations=1)
		HSV = cv2.cvtColor(frameDilate, cv2.COLOR_BGR2HSV)

		# Laser mask
		laserMask = cv2.inRange(HSV, self.HSVlower, self.HSVupper)

		# cv2.RETR_EXTERNAL: Only extreme outer flags. All child contours are left behind.
		# CHAIN_APPROX_SIMPLE: Removes all redundant points and compresses the contour.
		laser = cv2.findContours(laserMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		laser = imutils.grab_contours(laser)

		# Only proceed if laser was found
		if len(laser) > 0:
			c = max(laser, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 1)
			self.laserX = int(x)
			self.laserY = int(y)


		# Motion mask
		motionMask = self.subtractor.apply(frame)
		motionMask = cv2.erode(motionMask, self.kernel, iterations=1)
		motionMask = cv2.dilate(motionMask, self.kernel, iterations=1)

		# cv2.RETR_EXTERNAL: Only extreme outer flags. All child contours are left behind.
		# CHAIN_APPROX_SIMPLE: Removes all redundant points and compresses the contour.
		motion = cv2.findContours(motionMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		motion = imutils.grab_contours(motion)

		# only proceed if at least one contour was found
		if len(motion) > 0:
			c = max(motion, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			cv2.circle(frame, (int(x), int(y)), int(radius), (255,0,0), 1)
			self.objectX = int(x)
			self.objectY = int(y)

		# Show the frames
		key = cv2.waitKey(1) & 0xFF
		cv2.imshow('Frame', frame)
		# cv2.imshow('Laser', laserMask)
		# cv2.imshow('Motion', motionMask)

	def stopCamera(self):
		# Clear connections
		self.cam.release()


def main():
	# Connect to webcam
	v = video()
	v.startCamera()

	# Run for a set amount of time
	T = int(input("Enter time to run program: "))
	startTime = time.time()
	count = 0

	while(time.time() < (startTime + T)):
		v.findObject()
		print(count, v.laserX, v.laserY, v.objectX, v.objectY)
		count += 1

	# Print average frame rate
	print("Frames per second: ", int(count / (time.time()-startTime)))

	# Close all connections
	v.stopCamera()


if __name__ == '__main__':
	main()
