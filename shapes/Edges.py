import cv2
import numpy as np

# Moments
img = cv2.imread("1.jpg", cv2.IMREAD_GRAYSCALE)
ret, thresh = cv2. threshold(img, 127, 255, cv2.THRESH_BINARY)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt = contours[0]
m = cv2.moments(cnt)
'''
print(m)

cx = int(m['m10']/m['m00'])
cy = int(m['m01']/m['m00'])

print (cx)
print (cy)
'''
'''
# Contour Area
print (cv2.contourArea(cnt))
'''
'''
# Contour Perimeter
print (cv2.arcLength(cnt, True))
'''

'''
# Contour Approximation
# Less no. of Vertices
epsilon = 0.1*cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
#x, y, w, h = cv2.boundingRect(cnt)
#cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Contour Approximation", img)

cv2.waitKey(0)
'''
# Convex Hull
for con in contours:
    hull = cv2.convexHull(con)
    x, y, w, h = cv2.boundingRect(hull)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Contour Approximation", img)
    cv2.waitKey(0)

cv2.imshow("Contour Approximation", img)
cv2.waitKey(0)