import string
import os

from imutils import contours
import numpy as np
import imutils
import cv2
from matplotlib import pyplot as plt

from img_utils import showImages


def getBoundingBoxOfChars(binarized):
    contourRefs = cv2.findContours(binarized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1];
    contourRefs = contours.sort_contours(contourRefs, method="left-to-right")[0];

    return [cv2.boundingRect(contour) for contour in contourRefs];


def processTemplateImg(imgName):
    img = cv2.imread(imgName);
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

    binarized = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1];

    rects = getBoundingBoxOfChars(binarized);
    return (rects, binarized);


def initDict():
    currentDir = os.path.dirname(os.path.realpath(__file__));

    letters = list(string.ascii_lowercase);
    letters.insert(9, "-");
    letters.insert(11, "-");
    lettersPath = os.path.join(currentDir, "templates/letters.png");
    lettersRects, binImg = processTemplateImg(lettersPath);

    upper = list(string.ascii_uppercase);
    upperPath = os.path.join(currentDir, "templates/letters_upper.png");
    upperRects, binImg2 = processTemplateImg(upperPath);

    digits = list(string.digits);
    digitsPath = os.path.join(currentDir, "templates/digits.png");
    digitsRects, binImg3 = processTemplateImg(digitsPath);

    chars = letters + upper + digits;
    charRects = lettersRects + upperRects + digitsRects;
    imgs = []; imgs.append(binImg); imgs.append(binImg2); imgs.append(binImg3);

    return (chars, charRects, imgs);


if __name__ == "__main__":
    #roi = binarized[y:y + h, x:x + w];
    #roi = cv2.resize(roi, (57, 88));
    (chars, rects, imgs) = initDict();
    (letterImg, upperImg, digitsImg) = imgs;

    imagesToShow = [];
    imagesToShow.append(("Lower", letterImg));
    imagesToShow.append(("Upper", upperImg));
    imagesToShow.append(("Digits", digitsImg));
    showImages(3, 1, imagesToShow);

