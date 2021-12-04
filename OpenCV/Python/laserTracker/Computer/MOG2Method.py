import cv2
import numpy as np
import imutils

# Set webcam properties
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_FFMPEG, True)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 10)

subtractor = cv2.createBackgroundSubtractorMOG2(history=600, varThreshold=100, detectShadows=True)

while True:
	# Read a frame
	_, frame = cam.read()

	mask = subtractor.apply(frame)

	kernel = np.ones((5,5), np.uint8)
	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=1)

	motion = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	motion = imutils.grab_contours(motion)

	# only proceed if at least one contour was found
	if len(motion) > 0:
		c = max(motion, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 1)

	# cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

cam.release()
cv2.destroyAllWindows()
