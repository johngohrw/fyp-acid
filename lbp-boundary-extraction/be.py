from skimage import *
import cv2
import glob
import numpy
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided as ast
from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import roundup

# initialise LocalBinaryPattern instance
lbp = LocalBinaryPatterns(24, 8, "uniform") #number of points, radius

# deciding approximate size of subdivision blocks.
# best to keep it a factor of 100 as image dimensions 
# will first be resized to a factor of 100.
blockSize_x = 20
blockSize_y = 20

# get list of image in folder
images = glob.glob("images/*")

# for each image in folder:
# for i in range(len(images)):
for i in range(0,1):
    
    # read current image
    img = cv2.imread(images[i])

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # get image dimensions
    dimensions = img.shape 
    imgHeight = dimensions[0]
    imgWidth = dimensions[1]
    # rounding up image dimensions for resizing
    newHeight = roundup(imgHeight) 
    newWidth = roundup(imgWidth)
    # resizing image
    scaled = cv2.resize(gray, (newWidth, newHeight))

    # sizeCheck
    if (newWidth % blockSize_x != 0):
        print('warning! [i={}] image width ({}px) does not conform with blocksize, <{} rightmost pixels will not be processed.'.format(i, newWidth, blockSize_x))
    if (newHeight % blockSize_y != 0):
        print('warning! [i={}] image height ({}px) does not conform with blocksize, <{} bottommost pixels will not be processed.'.format(i, newHeight, blockSize_y))
    
    # getting number of divisions on each axis
    divisions_x = newWidth//blockSize_x
    divisions_y = newHeight//blockSize_y

    # initialising histograms array
    histograms = []

    # iterate through image subdivision blocks, describing each
    # subdivision's lbp histogram and saving it into an array
    for row in range(divisions_y):
        subarray = []
        for col in range(divisions_x):
            x_start = col * blockSize_x
            y_start = row * blockSize_y
            x_end = x_start + blockSize_x
            y_end = y_start + blockSize_y
            currentBlock = scaled[x_start:x_end, y_start:y_end]
            # describe texture of subregion histograms
            hist = lbp.describe(currentBlock)
            subarray.append(hist)

        # save histogram in histograms array
        histograms.append(subarray)
