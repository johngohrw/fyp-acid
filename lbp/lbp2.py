import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide, divisions
from modules.shifting import rightshift, bottomshift

# initialise LocalBinaryPattern instance
lbp = LocalBinaryPatterns(8, 24, "uniform") #number of points, radius

# get list of image in folder
images = glob.glob("images/*")

# for each image in folder:
for i in range(len(images)):
    
    # read current image
    img = cv2.imread(images[i])

    # get image dimensions
    dimensions = img.shape 
    img_height = dimensions[0]
    img_width = dimensions[1]

    # resize image
    img = cv2.resize(img, (600, 600))

    subdivided = divisions(img, 50)

    concatenatedHistograms = np.array([])
 
    for m in range(len(subdivided)):
        for n in range(len(subdivided[0])):

            # convert to grayscale
            gray = cv2.cvtColor(subdivided[m][n], cv2.COLOR_RGB2GRAY)
            hist = lbp.describe(gray)
            concatenatedHistograms = np.concatenate([concatenatedHistograms, hist])

            # plt.subplot(len(subdivided), len(subdivided[0]), ( m*len(subdivided[0]) + (n+1) ) )
            # plt.imshow(subdivided[m][n])
            # plt.axis('off')
    
    # plt.show()