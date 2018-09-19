import string
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from text_detection import pivotingTextDetection
from min_coverage import getMinCoverage
from img_utils import *
from recognition import *


class OCR:

    def __init__(self):
        print("Hello from OCR!");
        currentDir = os.path.dirname(os.path.realpath(__file__));

        lettersPath = os.path.join(currentDir, "templates/letters.png");
        upperPath = os.path.join(currentDir, "templates/letters_upper.png");
        digitsPath = os.path.join(currentDir, "templates/digits.png");

        lettersImg = cv2.imread(lettersPath);
        upperImg = cv2.imread(upperPath);
        digitsImg = cv2.imread(digitsPath);

        fixedRows = lettersImg.shape[0];

        upperDimensions = (upperImg.shape[1], fixedRows);
        upperImg = cv2.resize(upperImg, upperDimensions);
        digitsDimensions = (digitsImg.shape[1], fixedRows);
        digitsImg = cv2.resize(digitsImg, digitsDimensions);

        # Concatenate the template images in a row
        templateImg = np.concatenate((lettersImg, np.concatenate((upperImg, digitsImg), axis=1)), axis=1);

        self.chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits);
        self.chars.insert(9, "-");
        self.chars.insert(11, "-");
        charRects, templateBinImg = processTemplateImg(templateImg);
        self.charRects = charRects;
        self.templateBinImg = templateBinImg;


    def preprocess(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

        KERNEL_SIZE = 9;
        sigmaX = 10;
        blurred = cv2.GaussianBlur(gray, (KERNEL_SIZE, KERNEL_SIZE), sigmaX);

        unsharped = unsharp(gray, blurred);
        binarized = cv2.threshold(unsharped, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1];

        minTh = 100;
        maxTh = 200;
        edges = cv2.Canny(unsharped, minTh, maxTh, L2gradient = True);

        linesCoords, linesImg = detectLines(edges);
        removedLines = cv2.subtract(edges, linesImg);

        return (removedLines, binarized);


    def recognize(self, img, edges, binarized):
        imgCopy = img.copy();
        regions, isTextRegion = pivotingTextDetection(edges, img);

        for r in range(len(regions)):
            if isTextRegion[r]:
                current = regions[r];
                #minCoveredRegion = getMinCoverage(edges, current);

                #(top, bottom, left, right) = minCoveredRegion;
                (top, bottom, left, right) = current;
                binTextRegion = binarized[top:bottom+1, left:right+1];
                charRects = getBoundingBoxOfChars(binTextRegion);

                recognizedText = self.__template_match(binTextRegion, charRects);
                print(recognizedText);
                font = cv2.FONT_HERSHEY_SIMPLEX;
                origin = (right, bottom);   # origin of the text is bottom-left
                fontScale = 0.5;
                fontColor = (255, 0, 0);
                lineType = 2;

                # Putting recognized text near their detected region
                cv2.putText(imgCopy, recognizedText,
                        origin, font, fontScale, fontColor, lineType);

                #colBounds = minCoveredRegion[2:];
                #rowBounds = minCoveredRegion[:2];
                colBounds = current[2:];
                rowBounds = current[:2];
                drawBoundingBox(imgCopy, colBounds, rowBounds);

        return imgCopy;


    # This is python's way for defining a private method, Pfffft"
    def __template_match(self, binTextRegion, charRects):
        dimensionsToMatch = (57, 88);
        recognizedText = "";
        for rect in charRects:
            (x, y, w, h) = rect;
            roi = binTextRegion[y:y + h, x:x + w];
            roi = cv2.resize(roi, dimensionsToMatch);

            maxLetterScore, maxLetterIndex = matchTemplate(roi, self.lowerLetters, self.lowerRects, self.lowerBinImg);
            maxUpperScore, maxUpperIndex = matchTemplate(roi, self.upperLetters, self.upperRects, self.upperBinImg);
            maxDigitsScore, maxDigitsIndex = matchTemplate(roi, self.digits, self.digitsRects, self.digitsBinImg);

            if maxLetterScore > maxUpperScore and maxLetterScore > maxDigitsScore:
                recognizedText += self.lowerLetters[maxLetterIndex];
            elif maxUpperScore > maxLetterScore and maxUpperScore > maxDigitsScore:
                recognizedText += self.upperLetters[maxUpperIndex];
            else:
                recognizedText += self.digits[maxDigitsIndex];

        return recognizedText;


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.realpath(__file__));
    imgPath = os.path.join(currentDir, "imgs/example3.jpg");
    img = cv2.imread(imgPath);

    ocr = OCR();
    """
    edges, binImg = ocr.preprocess(img);
    result = ocr.recognize(img, edges, binImg);

    imagesToShow = [];
    imagesToShow.append(("Original", img));
    imagesToShow.append(("Detected Texts", result));
    showImages(1, 2, imagesToShow);
    """


