import cv2
import numpy as np
from ar_markers import detect_markers

#################################################################
				Image Read			#
#################################################################

image = cv2.imread('IMG_1250.JPG')
image1 = cv2.imread('IMG_1250.JPG', cv2.IMREAD_GRAYSCALE)



#################################################################
				Image Write			#
#################################################################

cv2.imwrite('mask.jpg', image)


#################################################################
				Threading			#
#################################################################

retval, threshold = cv2.threshold(image, 110, 255, cv2.THRESH_BINARY)

methods = [
	("THRESH_BINARY", cv2.THRESH_BINARY),
	("THRESH_BINARY_INV", cv2.THRESH_BINARY_INV),
	("THRESH_TRUNC", cv2.THRESH_TRUNC),
	("THRESH_TOZERO", cv2.THRESH_TOZERO),
	("THRESH_TOZERO_INV", cv2.THRESH_TOZERO_INV)]



#################################################################
				Blur(Smoothing)			#
#################################################################

image = cv2.GaussianBlur(image, (3, 3), 0)


#################################################################
				Conversion of colors		#
#################################################################

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


#################################################################
				Color Mask			#
#################################################################

lower_color = np.array([0, 0, 0])
upper_color = np.array([180, 255, 110])

mask = cv2.inRange(hsv, lower_color, upper_color)
res = cv2.bitwise_and(image, image, mask=mask)


#################################################################
				Color Mask			#
#################################################################

gray = cv2.bilateralFilter(image1, 11, 250, 17)
edged = cv2.Canny(gray, 30, 200)