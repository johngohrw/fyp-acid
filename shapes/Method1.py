import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt

'''======================================= METHOD   1 ============================================='''

def detectCorners():
    filename = 'extractedLines.jpg'
    img = cv.imread(filename)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray,2,3,0.04)
    #dst = cv.cornerHarris(gray,2,3,1)
            
    #result is dilated for marking the corners, not important
    dst = cv.dilate(dst,None)
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]
    #cv.imshow('dst',img)

    ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)

    #find centroids
    ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)

    #define the criteria to stop and refine the corners
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
    #here u can get corners
    print (corners)

    #Now draw them
    res = np.hstack((centroids,corners)) 
    res = np.int0(res) 
    img[res[:,1],res[:,0]]=[0,0,255] 
    img[res[:,3],res[:,2]] = [0,255,0]

    print("Going In =======================================================")
    for i in (res): 
        print("====================================>>>>>>>   ")
        print (i)

    cv.imshow('wee', img)

    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()


def method_one(image):
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
        o Try To eliminate as much noise as possible
        o Try to use erosion and dilation method to smoothen the line for better accuracy.
        o Then Use the Hough lines again
        o Harris Corner Detection, to detect the edge of the box


    """

    orig = cv2.imread("14.jpg")
    cv2.imshow('Original Image', orig)
    cv2.waitKey(0)

    img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    '''
    kernel_size = 3
    gausBlur = cv2.GaussianBlur(img, (kernel_size,kernel_size), 0)
    cv2.imshow('Apply Blur', gausBlur)
    cv2.waitKey(0)
    '''
    kernel_size = 3
    medianBlur = cv2.medianBlur(img, kernel_size)
    cv2.imshow('Median Blur', medianBlur)
    cv2.waitKey(0)

    edges = cv2.Canny(medianBlur, 800/3, 800, apertureSize = 3)
    cv2.imshow('Apply Canny Edge Detection', edges)
    cv2.waitKey(0)
    '''
    image, contours, hier = cv2.findContours(edges, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        epsilon = 0.1*cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(x, y, w, h)

    cv2.imshow('Find Contour', orig)
    '''
    '''

    edges1 = cv2.Canny(medianBlur, 255/3, 255, apertureSize = 3)
    cv2.imshow('Apply Canny Edge Detection1', edges1)
    cv2.waitKey(0)
    '''

    lines = cv2.HoughLines(edges, 1, np.pi/180, 120)
    print(lines)
    height, width = orig.shape[:2]
    blank_image = np.zeros((height,width,3), np.uint8)
    cv2.imshow('Hough Lines', blank_image)
    cv2.waitKey(0)

    try:
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

                cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.imshow('Hough Lines', blank_image)
                cv2.waitKey(0)

        #cv2.imshow('Hough Lines', orig)
        print("There is Lines")
        cv2.imwrite('extractedLines.jpg',blank_image)

    except TypeError:
        pass


    '''
    dilate_kernel = np.ones((5,5),np.uint8)
    edges = cv2.dilate(edges, dilate_kernel, iterations = 1 )
    cv2.imshow('Apply Canny Edge Detection', edges)
    cv2.waitKey(0)

    lines = cv2.HoughLinesP(edges, rho =1, theta = np.pi/180, lines= np.array([]), threshold = 15 ,minLineLength = 80,maxLineGap = 0)
    print(lines)

    for coordinates in lines:
        for x1,y1,x2,y2 in coordinates:
            cv2.line(orig, (x1,y1) , (x2,y2) ,(0,255,0),4)
            cv2.imshow("Hough Lines Prob", orig)
            cv2.waitKey(0)

    cv2.imshow("Hough Lines Prob", orig)
    '''
    cv2.waitKey(0)
    detectCorners()
