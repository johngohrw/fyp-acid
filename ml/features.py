import os
import math
import argparse

import cv2
import numpy as np

import sys
sys.path.append("../ocr/");
sys.path.append("../shapes/");
sys.path.append("../lbp/");

from modules.lbp import LocalBinaryPatterns
from modules.subdivisions import subdivide_checkeredLBP, divisions
from modules.shifting import rightshift, bottomshift
from lbp2 import getLBPHistogram
from Method2 import Shapes
from ocr import OCR


def getFeatures(imgNames, imgDir, lbp, shape, ocr, dataFile, labelsFile, label_value, limit = None):
    imgLimit = limit;
    if limit == None:
        imgLimit = len(imgNames);

    if label_value == 1:
        class_name = "COMP";
    else:
        class_name = "NOCOMP";

    for i in range(imgLimit):
        print("i = {}".format(i));
        img = imgNames[i];
        print("{} = {}".format(class_name, img));
        imgPath = os.path.join(imgDir, img);

        # LBP features
        img = cv2.imread(imgPath);
        lbpHist = getLBPHistogram(lbp, img);
        lbpHistStr = np.array2string(lbpHist, max_line_width=math.inf, precision=5, threshold=100000,formatter={'float_kind':lambda x: "%.5f" % x}, separator=',', suppress_small=False)[1:-1];

        # Shape features
        shapeFeatures = shape.boxFeatures(img);

        # OCR feature
        _, frequency = ocr.recognize(img);

        features = lbpHistStr;
        for area in shapeFeatures:
            features += ",{:.5f}".format(area);

        features = "{},{}\n".format(features, frequency);
        print(features);
        dataFile.write(features);
        labelsFile.write("{}\n".format(label_value));


if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    parser.add_argument("comp_size", type=int, help="Number of compound images");
    parser.add_argument("nocomp_size", type=int, help="Number of non-compound images");

    args = parser.parse_args();
    comp_size = args.comp_size;
    nocomp_size = args.nocomp_size;

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
        shape = Shapes();
        ocr = OCR();

        with open(dataFilename, "w") as dataFile, open(labelFilename, "w") as labelsFile:
            getFeatures(compImgs, compPath, lbp, shape, ocr, dataFile, labelsFile, 1, limit = comp_size);
            getFeatures(noCompImgs, noCompPath, lbp, shape, ocr, dataFile, labelsFile, 0, limit = nocomp_size);

