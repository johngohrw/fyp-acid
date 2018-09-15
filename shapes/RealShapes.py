import numpy as np
import cv2
from matplotlib import pyplot as plt

"""
YOU NEED ROI YONG KIN! PLEASE FOR GODSAKE! THINK LA DIU! DONT NEED ME TO HELP YOU ALWAYS! FUCKING STUPID
So what do you need?
- You need the border of the image only right?
- So use that as your region of interest
- Then what function should i use?
- Well, you gonna have alot of ideas though

Idea 1
- Use Your research paper method
- Pre-process
    o Make it into Black and white
- Doing
    o First occurence of white pixel
    o Start tracing
    o 4 Direction compass like tracing method

Idea 2
- Using Canny Edge and Hough Line Probabilistic
- Pre-process

- Doing

"""

orig = cv2.imread("3.jpg")
cv2.imshow('Original Image', orig)
cv2.waitKey(0)

img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
kernel_size = 3
cv2.GaussianBlur(img, (kernel_size,kernel_size), 0)
cv2.imshow('Apply Blur', img)
cv2.waitKey(0)

'''
edges = cv2.Canny(img, 255/3, 255, apertureSize = 3)
cv2.imshow('Apply Canny Edge Detection', edges)
cv2.waitKey(0)
'''

edges = cv2.Canny(img, 800/3, 800, apertureSize = 3)
cv2.imshow('Apply Canny Edge Detection', edges)
cv2.waitKey(0)

ret, thres = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('Apply Binary', thres)
cv2.waitKey(0)

'''

edges1 = cv2.Canny(thres, 255/3, 255, apertureSize = 3)
cv2.imshow('Apply Canny Edge Detection1', edges1)
cv2.waitKey(0)
'''
'''
lines = cv2.HoughLines(edges, 1, np.pi/180, 290)
print(lines)



for inter_array in lines:
    print (inter_array)
    for rho, theta in inter_array:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        print(a, b, x0, y0, x1, x2, y1, y2)

        cv2.line(orig,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.imshow('Hough Lines', orig)
        cv2.waitKey(0)

cv2.imshow('Hough Lines', orig)

'''
lines = cv2.HoughLinesP(thres, rho =1, theta = np.pi/180, lines= np.array([]), threshold = 15 ,minLineLength = 50,maxLineGap = 10)
print(lines)

for coordinates in lines:
    for x1,y1,x2,y2 in coordinates:
        cv2.line(orig, (x1,y1) , (x2,y2) ,(0,255,0),4)
        cv2.imshow("Hough Lines Prob", orig)
        cv2.waitKey(0)

cv2.imshow("Hough Lines Prob", orig)

cv2.waitKey(0)




