import numpy as np
import cv2
from matplotlib import pyplot as plt

orig = cv2.imread("4.jpg")
cv2.imshow('Original Image', orig)
cv2.waitKey(0)

img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
kernel_size = 3
cv2.GaussianBlur(img, (kernel_size,kernel_size), 0)
cv2.imshow('Apply Blur', img)
cv2.waitKey(0)

edges = cv2.Canny(img, 255/3, 255, apertureSize = 3)
cv2.imshow('Apply Canny Edge Detection', edges)
cv2.waitKey(0)

lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
print(lines)
for inter_array in lines:
    for rho, theta in inter_array:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(orig,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.imshow('Hough Lines', orig)
        cv2.waitKey(0)

cv2.imshow('Hough Lines', orig)
cv2.waitKey(0)




