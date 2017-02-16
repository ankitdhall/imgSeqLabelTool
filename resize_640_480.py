import cv2
import numpy as np
import os

height = 480
width = 640

for filename in os.listdir('.'):
	if filename.endswith('.png'):
		print filename
		img = cv2.imread(filename)
		
		res = cv2.resize(img, (width, height))#, interpolation = cv2.INTER_CUBIC)
		cv2.imwrite(filename, res)
