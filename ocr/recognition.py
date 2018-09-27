from imutils import contours
import numpy as np
import imutils
import cv2
from matplotlib import pyplot as plt

from img_utils import showImages


def processTemplateImg(templateImg):
    img = cv2.cvtColor(templateImg, cv2.COLOR_BGR2GRAY);

    binarized = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1];

    rects = getBoundingBoxOfChars(binarized);
    return (rects, binarized);


def getBoundingBoxOfChars(binarized):
    contourRefs = cv2.findContours(binarized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1];
    contourRefs = contours.sort_contours(contourRefs, method="left-to-right")[0];

    return [cv2.boundingRect(contour) for contour in contourRefs];


def inspectTemplateChars(charRects, templateBinImg):
    imagesToShow = [];
    i = 0;
    for (x, y, w, h) in charRects:
        charImg = templateBinImg[y:y+h, x:x+w];
        imagesToShow.append((str(i), charImg));
        i += 1;
    showImages(7, 10, imagesToShow);


def matchTemplate(roi, chars, charRects, templateBinImg):
    dimensionsToMatch = (57, 88);
    scores = [];
    for c in range(len(chars)):
        (x, y, w, h) = charRects[c];
        currentTemplate = templateBinImg[y:y + h, x:x + w];
        currentTemplate = cv2.resize(currentTemplate, dimensionsToMatch);

        result = cv2.matchTemplate(roi, currentTemplate, cv2.TM_CCOEFF);
        (_, score, _, _) = cv2.minMaxLoc(result);
        scores.append(score);

    maxIndex = np.argmax(scores);

    return (scores[maxIndex], maxIndex);


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

