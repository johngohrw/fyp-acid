import os
import cv2
import glob
import matplotlib.pyplot as plt
from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide
from modules.shifting import rightshift, bottomshift

class LBP:
    def __init__(self):
        print("Hello from LBP!");
        currentDir = os.path.dirname(os.path.realpath(__file__));

    def preprocess(self, image):
        # read current image
        img = image

        # get image dimensions
        dimensions = img.shape 
        img_height = dimensions[0]
        img_width = dimensions[1]
        # resize image
        img = cv2.resize(img, (img_width * 2, img_height * 2))

        print('preprocess!')

        return img







if __name__ == "__main__":
    
    print('running main code!')

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

        # get image dimensions
        dimensions = img.shape 
        img_height = dimensions[0]
        img_width = dimensions[1]
        # resize image
        img = cv2.resize(img, (img_width * 2, img_height * 2))

        # compute distance array via LBP (checkerboard format)
        dist_array = subdivide(img, blocksize, lbp)

        rightshifted = rightshift(dist_array)
        bottomshifted = bottomshift(dist_array)

        # plt.subplot(1, 4, 1)
        # plt.imshow(img)
        # plt.axis('off')
        # plt.subplot(1, 4, 2)``
        # plt.imshow(dist_array)
        # plt.axis('off')
        # plt.subplot(1, 4, 3)
        # plt.imshow(rightshifted)
        # plt.axis('off')
        # plt.subplot(1, 4, 4)
        # plt.imshow(bottomshifted)
        # plt.axis('off')
        # plt.show()
