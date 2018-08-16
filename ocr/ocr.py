import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from text_detection import pivotingTextDetection
from min_coverage import getMinCoverage
from img_utils import *

if __name__ == "__main__":
    #img = cv2.imread('compound.jpg', cv2.IMREAD_GRAYSCALE);

    currentDir = os.path.dirname(os.path.realpath(__file__));
    imgPath = os.path.join(currentDir, "imgs/example3.jpg");
    img = cv2.imread(imgPath);
    rows = img.shape[0];
    cols = img.shape[1];
    print("Image: Rows = %d, Cols = %d" % (rows, cols));
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

    img2 = img.copy();
    KERNEL_SIZE = 9;
    sigmaX = 10;
    blurred = cv2.GaussianBlur(gray, (KERNEL_SIZE, KERNEL_SIZE), sigmaX);

    unsharped = unsharp(gray, blurred);

    minTh = 100;
    maxTh = 200;
    edges = cv2.Canny(unsharped, minTh, maxTh, L2gradient = True);

    linesCoords, linesImg = detectLines(edges);
    removedLines = cv2.subtract(edges, linesImg);

    regions, isTextRegion = pivotingTextDetection(removedLines);

    for r in range(len(regions)):
        if isTextRegion[r]:
            current = regions[r];
            minCoveredRegion = getMinCoverage(edges, current);
            colBounds = minCoveredRegion[2:];
            rowBounds = minCoveredRegion[:2];
            drawBoundingBox(img2, colBounds, rowBounds);

    imagesToShow = [];
    imagesToShow.append(("Edges with removed detected Lines", removedLines));
    imagesToShow.append(("Detected Texts", img2));
    showImages(1, 2, imagesToShow);

