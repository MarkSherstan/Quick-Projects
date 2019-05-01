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
		self.FPS = 30

		# HSV mask range
		self.HSVlower = np.array([0,0,0])
		self.HSVupper = np.array([180,255,255])

		# Define location of object and laser
		self.objectX = 0
		self.objectY = 0
		self.laserX = 0
		self.laserY = 0

	def startCamera(self):
		# Create video capture object and configure settings
		self.cam = cv2.VideoCapture(0)
		self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
		self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
		self.cam.set(cv2.CAP_PROP_FPS, self.FPS)

		# Get rid of initial garbo frames
		for ii in range(10):
			_, frame = self.cam.read()

		# Get a good first frame for mask
		_, frame = self.cam.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		self.firstFrame = gray

	def findObject(self):
		# Read a frame
		_, frame = self.cam.read()

		# Removes high frequency components and converts to HSV color space
		frameBlur = cv2.GaussianBlur(frame, (7, 7), 0)
		HSV = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2HSV)
		gray = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2GRAY)

		# Mask for the laser dot
		mask = cv2.inRange(HSV, self.HSVlower, self.HSVupper)
		laser = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		laser = imutils.grab_contours(laser)

		# only proceed if laser was found
		if len(laser) > 0:
			c = max(laser, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			self.laserX = int(x)
			self.laserY = int(y)

		# compute the absolute difference between the current frame and first frame
		frameDelta = cv2.absdiff(self.firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours on thresholded image
		# cv2.RETR_EXTERNAL: Only extreme outer flags. All child contours are left behind.
		# CHAIN_APPROX_SIMPLE: Removes all redundant points and compresses the contour.
		thresh = cv2.dilate(thresh, None, iterations=2)
		motion = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		motion = imutils.grab_contours(motion)

		# only proceed if at least one contour was found
		if len(motion) > 0:
			c = max(motion, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			self.objectX = int(x)
			self.objectY = int(y)

		# Show the frames
		key = cv2.waitKey(1) & 0xFF
		cv2.imshow('Frame', frame)
		cv2.imshow('Laser', mask)
		cv2.imshow('Motion', thresh)

	def stopCamera(self):
		# Clear connections
		self.cam.release()


def main():
	# Connect to webcam
	v = video()
	v.startCamera()

	T = int(input("Enter time to run program: "))
	startTime = time.time()
	count = 0

	while(time.time() < (startTime + T)):
		v.findObject()
		print(count, v.laserX, v.laserY, v.objectX, v.objectY)
		count += 1

	print("Frames per second: ", int(count / (time.time()-startTime)))

	# Close all connections on the pi
	v.stopCamera()


if __name__ == '__main__':
	main()
