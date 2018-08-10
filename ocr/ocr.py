import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from text_detection import pivotingTextDetection


def unsharp(img, blurred):
    # Unsharped filter by subtracting the blurred image from the original
    # in a weighted way
    # Formula:
    # dst = src1*alpha + src2*beta + gamma;
    alpha = 1.5;
    beta = -0.5;
    gamma = 0;
    unsharped = cv2.addWeighted(img, alpha, blurred, beta, gamma);

    return unsharped;


def sharpen(img):
    sharpening_mask = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]);
    sharpened = cv2.filter2D(img, -1, sharpening_mask);
    return sharpened;


def detectLines(edges):
    linesCoords = [];
    linesImg = np.zeros(edges.shape, dtype=np.uint8);

    MIN_LENGTH = 100;
    MAX_GAP = 20;
    Th = 125;
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, Th, minLineLength=MIN_LENGTH, maxLineGap=MAX_GAP);
    for x in range(len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            endpoint1 = (x1, y1);
            endpoint2 = (x2, y2);
            linePoints = endpoint1 + endpoint2;
            linesCoords.append(linePoints);

            drawLine(linesImg, linePoints, thick=3);

    return (linesCoords, linesImg);


def drawLine(img, coords, color = (255, 255, 255), thick = 1):
    x1 = coords[0];
    y1 = coords[1];
    x2 = coords[2];
    y2 = coords[3];

    cv2.line(img, (x1, y1), (x2, y2), color, thick);


def drawBoundingBox(img, colBounds, rowBounds):
    left = colBounds[0];
    right = colBounds[1];
    top = rowBounds[0];
    bottom = rowBounds[1];

    thickness = 1;
    color = (255, 0, 0);
    cv2.rectangle(img, (left, top), (right, bottom), color, thickness);


def showImages(m, n, images):
    for i in range(1, len(images)+1):
        plt.subplot(m, n, i),plt.imshow(images[i-1][1], 'gray');
        plt.title(images[i-1][0]);
        plt.xticks([]),plt.yticks([]);

    plt.show();


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
            colBounds = current[2:];
            rowBounds = current[:2];
            drawBoundingBox(img2, colBounds, rowBounds);

    imagesToShow = [];
    imagesToShow.append(("Original", img));
    imagesToShow.append(("Sharpened", unsharped));
    imagesToShow.append(("Edges with detected lines removed", removedLines));
    imagesToShow.append(("Detected Texts", img2));
    showImages(2, 2, imagesToShow);

