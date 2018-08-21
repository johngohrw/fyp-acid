import cv2
import numpy as np 

file_name = '8.jpg'

# =============================== READ FILE ===================================
# read and scale down image
#img = cv2.pyrDown(cv2.imread(file_name, cv2.IMREAD_UNCHANGED))

#img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

# ============================== Pre-process ==================================
noise_removal = cv2.GaussianBlur(img, (5, 5), 0)


# Gray scale image
#grayscaled = cv2.cvtColor(noise_removal, cv2.COLOR_BGR2GRAY)
#grayscaled = np.float32(grayscaled)
#grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold image
ret, threshed_img = cv2.threshold(noise_removal, 127, 255, cv2.THRESH_BINARY)

# find contours and get the external one
image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

#Gray to color
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# ============================ Get Contour / Box =============================
# Draw only contours i want
largest_area = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if (area > largest_area):
        largest_area = area
    epsilon = 0.1*cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if (area <largest_area):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(x, y, w, h)
    
    '''
    if (area >6000):
        #cv2.drawContours(img, contour, -1, (0, 255, 0), 3)
        x, y, w, h = cv2.boundingRect(contour)
        # draw a green rectangle to visualize the bounding rect
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(len(contours))
        #cv2.drawContours(img, contour, -1, (0, 255, 0), 10)
        print("============")
        print(contour)
        print("============")
        #break
    #Search among contours which the x points end at the same place
    '''




# with each contour, draw boundingRect in green
# a minAreaRect in red and
# a minEnclosingCircle in blue

'''
for c in contours:

# get the bounding rect
x, y, w, h = cv2.boundingRect(c)
# draw a green rectangle to visualize the bounding rect
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
'''
'''
# get the min area rect
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)

# convert all coordinates floating point values to int
box = np.int0(box)
# draw a red 'nghien' rectangle
cv2.drawContours(img, [box], 0, (0, 0, 255))
'''
'''
# finally, get the min enclosing circle
(x, y), radius = cv2.minEnclosingCircle(c)
# convert all values to int
center = (int(x), int(y))
radius = int(radius)
# and draw the circle in blue
img = cv2.circle(img, center, radius, (255, 0, 0), 2)
'''


#print(len(contours))
#cv2.drawContours(img, approx, -1, (255, 255, 0), 1)

#=============================== SHOWING WINDOWS ============================
cv2.imshow("contours", img)
#cv2.imshow("Threshold", threshed_img)
#cv2.imshow("GrayScaled", grayscaled)
#cv2.imshow("HSV", hsv)

#=============================== Interface for the program ==================
ESC = 27

cv2.waitKey(0)

cv2.destroyAllWindows()

