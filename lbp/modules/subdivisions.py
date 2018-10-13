import math
import cv2
import numpy as np
from scipy.spatial import distance

# prints warning if blocksize is not optimal.
def sizeCheck(width, height, blocksize_x, blocksize_y):
    if (width % blocksize_x != 0):
        print('warning! image width ({}px) does not conform with blocksize, <{} rightmost pixels will not be processed.'.format(width, blocksize_x))
    if (height % blocksize_y != 0):
        print('warning! image height ({}px) does not conform with blocksize, <{} bottommost pixels will not be processed.'.format(height, blocksize_y))
    
# rounding up integers to the nearest hundred
def roundup(val):
    return int(math.ceil(val / 100.0)) * 100

# quantizePixel: takes in a pixel value & a max pixel value (corresponds to 255)
# returns the quantized pixel intensity value (0-255) based on the given max.
def quantizePixel(val, maxPixelValue):
    return round((val/maxPixelValue)*255)

# subdivides the input image with a LocalBinaryPattern instance
# according to the blocksize, returns a checkered distance matrix.
def subdivide_checkeredLBP(image, blocksize, lbp):

    blocksize_x = blocksize
    blocksize_y = blocksize

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # get image dimensions
    dimensions = image.shape 
    img_height = dimensions[0]
    img_width = dimensions[1]

    # round up image dimensions for resizing
    new_height = roundup(img_height) 
    new_width = roundup(img_width)

    # resize image dimensions to nearest hundred
    scaled = cv2.resize(gray, (new_width, new_height))

    # sizeCheck. prints warning if blocksize is not optimal.
    sizeCheck(new_width, new_height, blocksize_x, blocksize_y)

    # get number of divisions on each axis
    divisions_x = new_width // blocksize_x
    divisions_y = new_height // blocksize_y

    # initialising histograms array
    histograms = []

    # iterate through image subdivision blocks, describing each
    # subdivision's lbp histogram and saving it into an array
    for row in range(divisions_y):
        subarray = []
        for col in range(divisions_x):
            x_start = col * blocksize_x
            x_end = x_start + blocksize_x
            y_start = row * blocksize_y
            y_end = y_start + blocksize_y
            # print(x_start, x_end, y_start, y_end)
            current_block = scaled[y_start:y_end, x_start:x_end]
            # describe texture of subregion histograms
            hist = lbp.describe(current_block)
            subarray.append(hist)
    
        # save histogram in histograms array
        histograms.append(subarray)
    
    # initialise array storing neighbouring histograms' Euclidean distances
    dist_array = np.zeros(shape=((divisions_y * 2)-1,(divisions_x * 2)-1))

    # calculating left-neighbour Euclidean distances, storing in dist_array
    for row in range(divisions_y):
        for col in range(divisions_x-1):
            eDist = distance.euclidean(histograms[row][col],histograms[row][col+1])
            dist_array[row*2][(col*2)+1] = eDist
    
    # calculating bottom-neighbour Euclidean distances, storing in dist_array
    for row in range(divisions_y-1):
        for col in range(divisions_x):
            eDist = distance.euclidean(histograms[row][col], histograms[row+1][col])
            dist_array[(row*2)+1][col*2] = eDist
    
    # find maximum Euclidean distance value in dist_array
    # this value will be used as the maximum intensity value (255)
    # when quantizing distances to pixel values.
    maxDist = 0
    for row in dist_array: 
        maxRow = max(row)
        if (maxRow > maxDist):
            maxDist = maxRow
    
    # quantizing each distance value to pixels
    for y in range(len(dist_array)):
        for x in range(len(dist_array[0])):
            dist_array[y][x] = quantizePixel(dist_array[y][x], maxDist)
    
    return dist_array
    
    
# subdivides the input image into divisions based on the blocksize.
# nice and simple. no retarded stuff going on.
def divisions(image, blocksize):

    # how many pixels per block (square blocks only for now lul)
    blocksize_x = blocksize 
    blocksize_y = blocksize

    # get image dimensions
    dimensions = image.shape 
    img_height = dimensions[0]
    img_width = dimensions[1]

    # round up image dimensions for resizing
    new_height = roundup(img_height) 
    new_width = roundup(img_width)

    # resize image dimensions to nearest hundred
    scaled = cv2.resize(image, (new_width, new_height))

    # sizeCheck. prints warning if blocksize is not optimal.
    sizeCheck(new_width, new_height, blocksize_x, blocksize_y)

    # get number of divisions on each axis
    divisions_x = new_width // blocksize_x
    divisions_y = new_height // blocksize_y

    # initialising histograms array
    divisions = []

    # iterate through image subdivision blocks, describing each
    # subdivision's lbp histogram and saving it into an array
    for row in range(divisions_y):
        subarray = []
        for col in range(divisions_x):
            x_start = col * blocksize_x
            x_end = x_start + blocksize_x
            y_start = row * blocksize_y
            y_end = y_start + blocksize_y
            # print(x_start, x_end, y_start, y_end)
            current_block = scaled[y_start:y_end, x_start:x_end]

            subarray.append(current_block)
    
        # save histogram in histograms array
        divisions.append(subarray)
    
    return divisions
    