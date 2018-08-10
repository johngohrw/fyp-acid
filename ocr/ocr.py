import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

from text_detection import pivotingTextDetection


def detectLines(edges):
    linesCoords = [];
    linesImg = np.zeros(edges.shape);

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

            drawLine(linesImg, linePoints);

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
    imgPath = os.path.join(currentDir, "imgs/example4.jpg");
    img = cv2.imread(imgPath);
    rows = img.shape[0];
    cols = img.shape[1];
    print("Image: Rows = %d, Cols = %d" % (rows, cols));
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

    img2 = img.copy();
    KERNEL_SIZE = 3;
    #blurred = cv2.medianBlur(gray, KERNEL_SIZE);
    blurred = cv2.GaussianBlur(gray, (KERNEL_SIZE, KERNEL_SIZE), 0);

    minTh = 100;
    maxTh = 200;
    edges = cv2.Canny(blurred, minTh, maxTh, L2gradient = True);

    linesCoords, linesImg = detectLines(edges);
    for coords in linesCoords:
        drawLine(img2, coords, (0, 0, 255), 2);
    """
    regions, isTextRegion = pivotingTextDetection(edges);

    for r in range(len(regions)):
        if isTextRegion[r]:
            current = regions[r];
            print(current);
            colBounds = current[2:];
            rowBounds = current[:2];
            drawBoundingBox(img2, colBounds, rowBounds);
    """
    imagesToShow = [];
    imagesToShow.append(("Original", img));
    imagesToShow.append(("Edges", edges));
    imagesToShow.append(("Detected Texts", linesImg));
    showImages(1, 3, imagesToShow);

