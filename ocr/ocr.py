import string
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

from io import StringIO
from PIL import Image
import pytesseract

from text_detection import pivotingTextDetection
from img_utils import *
from thinning import zhangSuen


class OCR:

    def __init__(self):
        print("Hello from OCR!");


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

        return (unsharped, edges, binarized);


    def recognize(self, img):
        results = [];
        texts = {};

        currentDir = os.path.dirname(os.path.realpath(__file__));
        for angle in [0, 90, 270]:
            rotated = imutils.rotate_bound(img, angle);
            preprocessedImg, edges, binImg = self.preprocess(rotated);
            txtRegions = pivotingTextDetection(edges, img);

            for (top, bottom, left, right) in txtRegions:
                targetRegion = preprocessedImg[top:bottom+1, left:right+1];

                if 0 in targetRegion.shape:
                    continue;

                in_memory = Image.fromarray(targetRegion);
                config = ("-l eng --oem 1 --psm 7");
                recognizedText = pytesseract.image_to_string(in_memory, config=config);

                tokens = recognizedText.split(" ");
                for token in tokens:
                    try:
                        texts[token] += 1;
                    except KeyError:
                        texts[token] = 1;

                colBounds = (left, right);
                rowBounds = (top, bottom);
                drawBoundingBox(rotated, colBounds, rowBounds);

            results.append(rotated);

        frequency = self.__summarizeOccurences(texts);
        return results, frequency;


    def __placeText(self, img, text):
        font = cv2.FONT_HERSHEY_SIMPLEX;
        origin = (right, bottom);   # origin of the text is bottom-left
        fontScale = 0.5;
        fontColor = (255, 0, 0);
        lineType = 2;

        # Putting recognized text near their detected region
        cv2.putText(img, text,
                origin, font, fontScale, fontColor, lineType);


    def __summarizeOccurences(self, texts):
        frequency = 0;
        total = 0;
        for key, value in texts.items():
            if len(key) == 0:
                continue;
            if value > 1:
                frequency += value;
            total += value;

        if total == 0:
            return "{:.5f}".format(float(total));
        else:
            frequency /= total;
            return "{:.5f}".format(frequency);


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.realpath(__file__));
    imgPath = os.path.join(currentDir, "imgs/example3.jpg");
    img = cv2.imread(imgPath);

    ocr = OCR();
    results, frequency = ocr.recognize(img);
    print(frequency);

