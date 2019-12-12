'''
outputs a "subtracted" image
literal pixel subtraction ~= pixel by pixel comparison
'''
import cv2

img1 = cv2.imread("nobat2.jpg")
img2 = cv2.imread("darkbat1.jpg")
img3 = cv2.subtract(img2, img1)
img4 = cv2.resize(img3, (960, 540))   
cv2.imshow("image", img4)
cv2.waitKey(0)
