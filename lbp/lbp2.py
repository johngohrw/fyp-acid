import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
import math
from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide_checkeredLBP, divisions
from modules.shifting import rightshift, bottomshift


def getLBPHistogram(lbp, img):
    # Protect the original image
    imgCopy = img.copy();

    # get image dimensions
    dimensions = imgCopy.shape
    img_height = dimensions[0]
    img_width = dimensions[1]

    # resize image
    imgCopy = cv2.resize(imgCopy, (600, 600))

    subdivided = divisions(imgCopy, 200)

    concatenatedHistograms = np.array([])

    for m in range(len(subdivided)):
        for n in range(len(subdivided[0])):
            # convert to grayscale
            gray = cv2.cvtColor(subdivided[m][n], cv2.COLOR_RGB2GRAY)
            hist = lbp.describe(gray)
            concatenatedHistograms = np.concatenate([concatenatedHistograms, hist])
    return concatenatedHistograms;


if __name__ == "__main__":
    # initialise LocalBinaryPattern instance
    lbp = LocalBinaryPatterns(8, 24, "uniform") #number of points, radius

    # get list of image in folder
    images = glob.glob("images/*")

    # resultFile = open('results.txt', 'w')
    resultFileCsv = open('results.csv', 'w')

    # for each image in folder:
    for i in range(len(images)):
        # read current image
        img = cv2.imread(imgPath)
        lbpHist = getLBPHistogram(lbp, img);

        resultFileCsv.write(np.array2string(lbpHist, max_line_width=math.inf, precision=5, threshold=100000,formatter={'float_kind':lambda x: "%.5f" % x}, separator=',', suppress_small=False)[1:-1] + '\n')
