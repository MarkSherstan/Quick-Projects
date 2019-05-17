# import the necessary packages
import cv2
import numpy as np

# Set webcam properties
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_FFMPEG, True)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Dummy function
def nothing(x):
	pass

# Creating a window for later use
cv2.namedWindow('result')

# Start with 100's to prevent error while masking
h_l,s_l,v_l = 100,100,100
h_u,s_u,v_u = 100,100,100

# Creating track bar(s)
cv2.createTrackbar('h_l', 'result', 0, 180, nothing)
cv2.createTrackbar('s_l', 'result', 0, 255, nothing)
cv2.createTrackbar('v_l', 'result', 0, 255, nothing)

cv2.createTrackbar('h_u', 'result', 0, 180, nothing)
cv2.createTrackbar('s_u', 'result', 0, 255, nothing)
cv2.createTrackbar('v_u', 'result', 0, 255, nothing)

cv2.setTrackbarPos('h_u', 'result', 180)
cv2.setTrackbarPos('s_u', 'result', 255)
cv2.setTrackbarPos('v_u', 'result', 255)

while(True):
	# Get frame
	_, frame = cap.read()

	# Convert to HSV
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	# Get info from tracking bar(s)
	h_l = cv2.getTrackbarPos('h_l', 'result')
	s_l = cv2.getTrackbarPos('s_l', 'result')
	v_l = cv2.getTrackbarPos('v_l', 'result')

	h_u = cv2.getTrackbarPos('h_u', 'result')
	s_u = cv2.getTrackbarPos('s_u', 'result')
	v_u = cv2.getTrackbarPos('v_u', 'result')

	# Masking and result
	lower = np.array([h_l,s_l,v_l])
	upper = np.array([h_u,s_u,v_u])
	mask = cv2.inRange(hsv, lower, upper)

	result = cv2.bitwise_and(frame,frame,mask = mask)

	# Show result
	cv2.imshow('result', result)

	# Exit commands
	key = cv2.waitKey(5) & 0xFF
	if key == ord("q"):
		break

# Release cam and close windows
cap.release()
cv2.destroyAllWindows()
