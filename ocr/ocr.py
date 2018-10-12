import string
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

from PIL import Image
import pytesseract

from text_detection import pivotingTextDetection
from img_utils import *
from recognition import *
from thinning import zhangSuen


class OCR:

    def __init__(self, templateMatching = False):
        print("Hello from OCR!");

        if templateMatching:
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

        """
        linesCoords, linesImg = detectLines(edges);
        removedLines = cv2.subtract(edges, linesImg);
        """

        return (unsharped, edges, binarized);


    def recognize(self, img):
        results = [];
        texts = {};

        currentDir = os.path.dirname(os.path.realpath(__file__));
        for angle in np.arange(0, 360, 90):
            rotated = imutils.rotate_bound(img, angle);
            preprocessedImg, edges, binImg = self.preprocess(rotated);
            txtRegions = pivotingTextDetection(edges, img);

            for (top, bottom, left, right) in txtRegions:
                targetRegion = preprocessedImg[top:bottom+1, left:right+1];

                if 0 in targetRegion.shape:
                    continue;

                filename = "{}.jpg".format(os.getpid());
                imgPath = os.path.join(currentDir, filename);
                cv2.imwrite(imgPath, targetRegion);
                config = ("-l eng --oem 1 --psm 7");
                recognizedText = pytesseract.image_to_string(Image.open(imgPath), config=config);
                os.remove(imgPath);

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

        return results, texts;


    def __placeText(self, img, text):
        font = cv2.FONT_HERSHEY_SIMPLEX;
        origin = (right, bottom);   # origin of the text is bottom-left
        fontScale = 0.5;
        fontColor = (255, 0, 0);
        lineType = 2;

        # Putting recognized text near their detected region
        cv2.putText(img, text,
                origin, font, fontScale, fontColor, lineType);


    # This is python's way for defining a private method, Pfffft"
    def __template_match(self, binTextRegion, currentRegionChars):
        dimensionsToMatch = (57, 88);
        recognizedText = "";
        # Attempt to match each segmented chars in the text region with
        # all the chars in our alphabet
        for (x, y, w, h) in currentRegionChars:
            roi = binTextRegion[y:y + h, x:x + w];
            roi = cv2.resize(roi, dimensionsToMatch);

            _, maxLetterIndex = matchTemplate(roi, self.chars, self.charRects, self.templateBinImg);
            recognizedText += self.chars[maxLetterIndex];

        return recognizedText;


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.realpath(__file__));
    imgPath = os.path.join(currentDir, "imgs/example3.jpg");
    img = cv2.imread(imgPath);

    ocr = OCR();
    results, texts = ocr.recognize(img);

    """
    imagesToShow = [];
    imagesToShow.append(("Original", img));
    imagesToShow.append(("Detected Texts", result));
    showImages(1, 2, imagesToShow);
    """

