import os
import cv2 as cv
import numpy as np

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def getImageHeightWidth (image):
    height, width = image.shape[:2]
    return height, width

def binarizeImages (image):
    (thresh, binarized) = cv.threshold(image, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)  # Thresholding the image
    return binarized

def invertImages (image):
    inv_img = 255 - image 
    return inv_img

def detectBoxes(img):

    img_binarized = binarizeImages(img)
    img_inverted = invertImages(img_binarized)

    cv.imwrite("Image_bin.jpg",img_inverted)
   
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//40
    
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernel_length))
    
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_length, 1))

    # A kernel of (3 X 3) ones.
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))

    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv.erode(img_inverted, verticle_kernel, iterations=3)
    verticle_lines_img = cv.dilate(img_temp1, verticle_kernel, iterations=3)
    cv.imwrite("verticle_lines.jpg",verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv.erode(img_inverted, hori_kernel, iterations=3)
    horizontal_lines_img = cv.dilate(img_temp2, hori_kernel, iterations=3)
    cv.imwrite("horizontal_lines.jpg",horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv.threshold(img_final_bin, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    cv.imwrite("img_final_bin.jpg",img_final_bin)
    
    # Find contours for image, which will detect all the boxes
    im2, contours, hierarchy = cv.findContours(
        img_final_bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    
    img_height, img_width = getImageHeightWidth(img)
    threshed_height = img_height *0.3
    threshed_width = img_width * 0.3
'''
    highest_height = img_height
    highest_width = img_width
'''
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv.boundingRect(c)

    # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
        #if (w > 80 and h > 20) and w > 3*h:
        if (w > threshed_width  and h > threshed_height):
            new_img = img[y:y+h, x:x+w]
            cv.imshow('cropped images', new_img)
            print(w*h) #area
            cv.waitKey(0)

currentDir = os.path.dirname(os.path.realpath(__file__));

for i in range (1, 32):
    img_name = "Images/" + str(i) + ".jpg"
    img_path = os.path.join(currentDir, img_name )
    image = cv.imread(img_path, 0)
    cv.imshow(img_name, image)
    detectBoxes(image)
    cv.destroyAllWindows()
