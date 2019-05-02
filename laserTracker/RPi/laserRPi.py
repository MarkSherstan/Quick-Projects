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
		self.cam = cv2.VideoCapture(0)
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
        # Interpolate value for easy control
		self.joint1value = int(np.interp(xObject, [0, 720], self.joint1Range))
		self.joint1.start(self.joint1value * self.dutyCycleScale)
        print(xObject, xLaser, self.joint1value)

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

	# Run for a set amount of time
	T = int(input("Enter time to run program: "))
	startTime = time.time()
	count = 0

	while(time.time() < (startTime + T)):
		v.findObject()
		print(count, v.laserX, v.laserY, v.objectX, v.objectY)
		count += 1
		# h.track(v.laserPos[0], v.laserPos[1], v.objectX, v.objectY)

	# Print average frame rate
	print("Frames per second: ", int(count / (time.time()-startTime)))

	# Close all connections on the pi
	h.endControl()
	v.stopCamera()


if __name__ == '__main__':
	main()
