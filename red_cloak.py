import time
import numpy as np
import cv2

capture_video = cv2.VideoCapture("video.mp4")
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (int(capture_video.get(3)), int(capture_video.get(4))) )

time.sleep(1)
background = 0

for i in range(50):
	return_val, background = capture_video.read()

background = np.flip(background, axis = 1)

while (capture_video.isOpened()):
	return_val, img = capture_video.read()
	if not return_val :
		break

	img = np.flip(img, axis = 1)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255]) # values is for red colour Cloth
	mask1 = cv2.inRange(hsv, lower_red,upper_red)

	lower_red = np.array([170,120,70])
	upper_red =  np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1 + mask2

	# Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations = 2)
	mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

	res1 = cv2.bitwise_and(background, background, mask = mask1)
	res2 = cv2.bitwise_and(img, img, mask = mask2)
	final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
	
	out.write(final_output)
	cv2.imshow("Izan", final_output)

	k = cv2.waitKey(10)
	if k == 27:
		break

