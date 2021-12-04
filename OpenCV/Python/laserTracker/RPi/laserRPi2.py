# import the necessary packages
import RPi.GPIO as GPIO
import numpy as np
import cv2
import imutils
import time


class video:
	def __init__(self):
		# Video properties
		self.width = 720
		self.height = 480
		self.FPS = 30

		# Define location of object and laser
		self.objectX = 0
		self.objectY = 0
		self.laserPos = 0

	def startCamera(self):
		# Create video capture object and configure settings
		self.cam = cv2.VideoCapture(0)
		self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
		self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
		self.cam.set(cv2.CAP_PROP_FPS, self.FPS)

		# Get rid of initial garbo frames
		for ii in range(10):
			_, frame = self.cam.read()

		# Get a good first Frame for mask
		_, frame = self.cam.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		self.firstFrame = gray

	def findObject(self):
		# Read a frame
		_, frame = self.cam.read()

		# Removes high frequency components and converts to HSV and gray color space
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0) # To track lazer --> gray = cv2.GaussianBlur(gray, (3, 3), 0)

		# Find the laser dot
		(minVal, maxVal, minLoc, self.laserPos) = cv2.minMaxLoc(gray)

		# compute the absolute difference between the current frame and
		# first frame\
		frameDelta = cv2.absdiff(self.firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			self.objectX = int(x)
			self.objectY = int(y)

	def stopCamera(self):
		# Clear connections
		self.cam.release()


class hardware:
	def __init__(self):
		# Microsecond range for servos
		self.joint1Range = [1300,1750]
		self.joint2Range = [500,2500]

		# Servo joint value
		self.joint1value = 1500
		self.joint2value = 1500

		# percentage / (20 ms * unit conversion)
		self.dutyCycleScale = 100 / (20*1000)

		# Laser state
		self.laserState = False

		# Gains for tracking
		self.gainX = 0.5
		self.gainY = 0.5

	def startControl(self):
		# Disable GPIO warnings
		GPIO.setwarnings(True)

		# Run `pinout` to see the numbers for pins
		GPIO.setmode(GPIO.BOARD)

		# Set up pins for laser and servos
		GPIO.setup(5, GPIO.OUT)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(16, GPIO.OUT)

		# Initialize all servos and write start position
		self.joint1 = GPIO.PWM(12, 50)
		self.joint2 = GPIO.PWM(16, 50)

		self.joint1.start(self.joint1value * self.dutyCycleScale)
		self.joint2.start(self.joint2value * self.dutyCycleScale)

		# Turn on laser
		if (self.laserState is False):
			GPIO.output(5, GPIO.HIGH)
			self.laserState = True

	def track(self, xLaser, yLaser, xObject, yObject):

		self.joint1value = int(np.interp(xObject, [0, 720], self.joint1Range))
		print(xObject, xLaser, self.joint1value)
		# controlX = (xObject - xLaser) * self.gainX
		# self.joint1value += controlX

		self.joint1.start(self.joint1value * self.dutyCycleScale)
		# self.joint2.start(self.joint2value * self.dutyCycleScale)


	def endControl(self):
		# Stop writing PWM signal to servos
		self.joint1.stop()
		self.joint2.stop()

		# Turn on laser
		if (self.laserState is True):
			GPIO.output(5, GPIO.LOW)
			self.laserState = False

		# Clean up ports used
		GPIO.cleanup()


def main():
	# Connect to video
	v = video()
	v.startCamera()

	# Connect to hardware
	h = hardware()
	h.startControl()

	T = int(input("Enter time to run program: "))
	startTime = time.time()
	count = 0

	while(time.time() < (startTime + T)):
		v.findObject()
		count += 1
		# print(count, v.laserPos[0], v.laserPos[1], v.objectX, v.objectY)
		h.track(v.laserPos[0], v.laserPos[1], v.objectX, v.objectY)

	print("Frames per second: ", int(count / (time.time()-startTime)))

	# Close all connections on the pi
	h.endControl()
	v.stopCamera()



if __name__ == '__main__':
	main()
