import string
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from text_detection import pivotingTextDetection
from min_coverage import getMinCoverage
from img_utils import *
from recognition import processTemplateImg, getBoundingBoxOfChars, matchTemplate


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.realpath(__file__));

    letters = list(string.ascii_lowercase);
    letters.insert(9, "-");
    letters.insert(11, "-");
    lettersPath = os.path.join(currentDir, "templates/letters.png");
    lettersRects, lettersBinImg = processTemplateImg(lettersPath);

    upper = list(string.ascii_uppercase);
    upperPath = os.path.join(currentDir, "templates/letters_upper.png");
    upperRects, upperBinImg = processTemplateImg(upperPath);

    digits = list(string.digits);
    digitsPath = os.path.join(currentDir, "templates/digits.png");
    digitsRects, digitsBinImg = processTemplateImg(digitsPath);



    #imgPath = os.path.join(currentDir, "sample.bmp");
    imgPath = os.path.join(currentDir, "imgs/example3.jpg");
    img = cv2.imread(imgPath);
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

    binarized = cv2.threshold(unsharped, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1];

    dimensionsToMatch = (57, 88);
    for r in range(len(regions)):
        if isTextRegion[r]:
            current = regions[r];
            minCoveredRegion = getMinCoverage(edges, current);

            (top, bottom, left, right) = minCoveredRegion;
            binTextRegion = binarized[top:bottom+1, left:right+1];
            charRects = getBoundingBoxOfChars(binTextRegion);

            recognizedStr = "";
            for rect in charRects:
                (x, y, w, h) = rect;
                roi = binTextRegion[y:y + h, x:x + w];
                roi = cv2.resize(roi, dimensionsToMatch);

                maxLetterScore, maxLetterIndex = matchTemplate(roi, letters, lettersRects, lettersBinImg);
                maxUpperScore, maxUpperIndex = matchTemplate(roi, upper, upperRects, upperBinImg);
                maxDigitsScore, maxDigitsIndex = matchTemplate(roi, digits, digitsRects, digitsBinImg);

                if maxLetterScore > maxUpperScore and maxLetterScore > maxDigitsScore:
                    recognizedStr += letters[maxLetterIndex];
                elif maxUpperScore > maxLetterScore and maxUpperScore > maxDigitsScore:
                    recognizedStr += upper[maxUpperIndex];
                else:
                    recognizedStr += digits[maxDigitsIndex];

            print(recognizedStr);

            colBounds = minCoveredRegion[2:];
            rowBounds = minCoveredRegion[:2];
            drawBoundingBox(img2, colBounds, rowBounds);

    #expectedPath = os.path.join(currentDir, "result.bmp");
    #expected = cv2.imread(expectedPath);

    imagesToShow = [];
    #imagesToShow.append(("Expected", expected));
    imagesToShow.append(("Detected Texts", img2));
    showImages(1, 1, imagesToShow);

