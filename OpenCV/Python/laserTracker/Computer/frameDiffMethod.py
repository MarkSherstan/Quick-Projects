# Import the necessary packages
import numpy as np
import cv2
import imutils

# Set webcam properties
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_FFMPEG, True)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 10)

# Get rid of initial garbo frames
for ii in range(10):
	_, frame = cam.read()

# Get a good first frame for mask
_, frame = cam.read()
frame = cv2.GaussianBlur(frame, (5, 5), 0)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
firstFrame = gray


while True:
	# Read a frame
	_, frame = cam.read()

	# Removes high frequency components and converts to HSV color space
	frame = cv2.GaussianBlur(frame, (5, 5), 0)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# compute the absolute difference between the current frame and first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 55, 255, cv2.THRESH_BINARY)[1]

	kernel = np.ones((5,5), np.uint8)
	thresh = cv2.erode(thresh, kernel, iterations=1)
	thresh = cv2.dilate(thresh, kernel, iterations=1)

	motion = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	motion = imutils.grab_contours(motion)

	# only proceed if at least one contour was found
	if len(motion) > 0:
		c = max(motion, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 1)


	# # dilate the thresholded image to fill in holes, then find contours on thresholded image
	# # cv2.RETR_EXTERNAL: Only extreme outer flags. All child contours are left behind.
	# # CHAIN_APPROX_SIMPLE: Removes all redundant points and compresses the contour.
	# thresh = cv2.dilate(thresh, None, iterations=2)
	# motion = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# motion = imutils.grab_contours(motion)

	# cv2.imshow("Frame", frame)
	cv2.imshow("Thresh", thresh)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

cam.release()
cv2.destroyAllWindows()
