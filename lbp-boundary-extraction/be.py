import cv2
import glob
import matplotlib.pyplot as plt
from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide

# initialise LocalBinaryPattern instance
lbp = LocalBinaryPatterns(24, 8, "uniform") #number of points, radius

# deciding approximate size of subdivision blocks.
# best to keep it a factor of 100 as image dimensions 
# will first be resized to a factor of 100.
blocksize = 10

# get list of image in folder
images = glob.glob("images/*")

# for each image in folder:
for i in range(len(images)):
    
    # read current image
    img = cv2.imread(images[i])

    # compute distance array via LBP (checkerboard format)
    dist_array = subdivide(img, blocksize, lbp)

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.subplot(1, 2, 2)
    plt.imshow(dist_array)
    plt.show()
