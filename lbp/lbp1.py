import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide_checkeredLBP
from modules.shifting import rightshift, bottomshift

# initialise LocalBinaryPattern instances for testing
lbp1 = LocalBinaryPatterns(12, 2, "uniform") #number of points, radius
lbp2 = LocalBinaryPatterns(8, 2, "uniform") #number of points, radius
lbp3 = LocalBinaryPatterns(4, 2, "uniform") #number of points, radius
lbp4 = LocalBinaryPatterns(2, 2, "uniform") #number of points, radius
lbp5 = LocalBinaryPatterns(1, 2, "uniform") #number of points, radius

lbps = [lbp1,lbp2,lbp3,lbp4,lbp5]

# deciding approximate size of subdivision blocks.
# best to keep it a factor of 100 as image dimensions 
# will first be resized to a factor of 100.
blocksize = 10

# get list of image in folder
images = glob.glob("images/*")

# for each image in folder:
# len(images)
for i in range(len(images)):
    
    # read current image
    img = cv2.imread(images[i])

    # get image dimensions
    dimensions = img.shape 
    img_height = dimensions[0]
    img_width = dimensions[1]
    # resize image
    img = cv2.resize(img, (img_width * 3, img_height * 3))

    plt.subplot(1, 4, 1)
    plt.imshow(img)
    plt.axis('off')

    # compute distance array via LBP (checkerboard format)
    # for j in range(5):
    checkered = subdivide_checkeredLBP(img, blocksize, lbps[3])
    equ = cv2.equalizeHist(np.uint8(checkered)) # do histogram equalization
    # sub = cv2.bitwise_not(equ)
    # ret,thresh1 = cv2.threshold(sub,200,255,cv2.THRESH_TOZERO)
    # ret,thresh2 = cv2.threshold(sub,200,255,cv2.THRESH_BINARY)

    # kernel = np.ones((3,3),np.uint8)
    # erosion = cv2.erode(thresh2,kernel,iterations = 1)
    # edges = cv2.Canny(erosion,100,200,apertureSize = 7)


    # rho = 200  # distance resolution in pixels of the Hough grid
    # theta = np.pi / 2  # angular resolution in radians of the Hough grid
    # threshold = 30  # minimum number of votes (intersections in Hough grid cell)
    # min_line_length = 50  # minimum number of pixels making up a line
    # max_line_gap = 20  # maximum gap in pixels between connectable line segments
    # line_image = np.copy(edges) * 0  # creating a blank to draw lines on

    # # Run Hough on edge detected image
    # # Output "lines" is an array containing endpoints of detected line segments
    # lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
    #                     min_line_length, max_line_gap)

    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    #         cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),1)


    # plt.subplot(1, 4, 2)
    # plt.imshow(thresh2, cmap='gray')
    # plt.axis('off')

    # plt.subplot(1, 4, 3)
    # plt.imshow(edges, cmap='gray')
    # plt.axis('off')

    # plt.subplot(1, 4, 4)
    # plt.imshow(line_image)
    # plt.axis('off')

    # checkered1 = subdivide(img, blocksize, lbp1)
    # checkered2 = subdivide(img, blocksize, lbp2)
    # checkered3 = subdivide(img, blocksize, lbp3)
    # checkered4 = subdivide(img, blocksize, lbp4)
    # checkered5 = subdivide(img, blocksize, lbp5)

    # equ1 = cv2.equalizeHist(np.uint8(checkered1)) # do histogram equalization
    # equ2 = cv2.equalizeHist(np.uint8(checkered2)) # do histogram equalization
    # equ3 = cv2.equalizeHist(np.uint8(checkered3)) # do histogram equalization
    # equ4 = cv2.equalizeHist(np.uint8(checkered4)) # do histogram equalization
    # equ5 = cv2.equalizeHist(np.uint8(checkered5)) # do histogram equalization

    # sub1 = cv2.bitwise_not(equ1)
    # sub2 = cv2.bitwise_not(equ2)
    # sub3 = cv2.bitwise_not(equ3)
    # sub4 = cv2.bitwise_not(equ4)
    # sub5 = cv2.bitwise_not(equ5)

    # otsu's thresh
    # ret,thresh = cv2.threshold(equ,0,255,cv2.THRESH_OTSU)

    # gaussian thresh
    # adaptThresh = cv2.adaptiveThreshold(equ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    # rightshifted = rightshift(equ)  # do rightshift
    # rs_blur = cv2.GaussianBlur(rightshifted,(5,5),0)
    # rs_sobel_y = cv2.Sobel(rightshifted,cv2.CV_64F,1,0,ksize=5)

    # bottomshifted = bottomshift(equ) # do bottomshift
    # bs_blur = cv2.GaussianBlur(bottomshifted,(5,5),0)
    # bs_sobel_x = cv2.Sobel(bottomshifted,cv2.CV_64F,1,0,ksize=3)

    # bs_kernel = np.array([[-1,2,-1], [-1,2,-1], [-1,2,-1]])
    # sobelagain = cv2.filter2D(bs_sobel_x, -1, bs_kernel)

    # rs_canny = cv2.Canny(np.uint8(rs_blur),255,255)
    # bs_canny = cv2.Canny(np.uint8(bs_blur),255,255)
    # bottomshifted_edges = cv2.Canny(np.uint8(rightshifted),200,210)


    # plt.subplot(2, 3, 1)
    # plt.imshow(sub1, cmap='gray')
    # plt.axis('off')
    # plt.subplot(2, 3, 2)
    # plt.imshow(sub2, cmap='gray')
    # plt.axis('off')
    # plt.subplot(2, 3, 3)
    # plt.imshow(sub3, cmap='gray')
    # plt.axis('off')
    # plt.subplot(2, 3, 4)
    # plt.imshow(sub4, cmap='gray')
    # plt.axis('off')
    # plt.subplot(2, 3, 5)
    # plt.imshow(sub5, cmap='gray')
    # plt.axis('off')
    # plt.subplot(1, 5, 4)
    # plt.imshow(bs_sobel_x, cmap='gray')
    # plt.axis('off')
    # plt.subplot(1, 5, 5)
    # plt.imshow(sobelagain, cmap='gray')
    # plt.axis('off')
    plt.show()


