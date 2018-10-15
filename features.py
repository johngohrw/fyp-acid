import os
import math

import cv2
import numpy as np

import sys
sys.path.append("./ocr/");
sys.path.append("./lbp/");

from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide_checkeredLBP, divisions
from modules.shifting import rightshift, bottomshift
from lbp2 import getLBPHistogram
from ocr import OCR


def getFeatures(imgNames, imgDir, lbp, ocr, dataFile, labelsFile, label_value, limit = None):
    imgLimit = limit;
    if limit == None:
        imgLimit = len(imgNames);

    for i in range(imgLimit):
        img = imgNames[i];
        print(img);
        imgPath = os.path.join(imgDir, img);

        # LBP features
        img = cv2.imread(imgPath);
        lbpHist = getLBPHistogram(lbp, img);
        lbpHistStr = np.array2string(lbpHist, max_line_width=math.inf, precision=5, threshold=100000,formatter={'float_kind':lambda x: "%.5f" % x}, separator=',', suppress_small=False)[1:-1];
        # OCR feature
        _, frequency = ocr.recognize(img);

        features = "{},{}\n".format(lbpHistStr, frequency);
        print(features);
        dataFile.write(features);
        labelsFile.write("{}\n".format(label_value));


if __name__ == "__main__":
    dataFilename = "data.csv";
    labelFilename = "labels.txt";
    # Data or label file does not exist then just extract the features, give
    # label and write them to their respective files
    if not os.path.isfile(dataFilename) or not os.path.isfile(labelFilename):
        currentDir = os.path.dirname(os.path.realpath(__file__));
        compPath = os.path.join(currentDir, "dataset/COMP");
        noCompPath = os.path.join(currentDir, "dataset/NOCOMP");

        compImgs = os.listdir(compPath);
        noCompImgs = os.listdir(noCompPath);
        print(len(compImgs));
        print(len(noCompImgs));

        lbp = LocalBinaryPatterns(8, 24, "uniform") #number of points, radius
        ocr = OCR();

        with open(dataFilename, "w") as dataFile, open(labelFilename, "w") as labelsFile:
            compLimit = 15;
            getFeatures(compImgs, compPath, lbp, ocr, dataFile, labelsFile, 1, limit = compLimit);
            noCompLimit = 10;
            getFeatures(noCompImgs, noCompPath, lbp, ocr, dataFile, labelsFile, 0, limit = noCompLimit);

