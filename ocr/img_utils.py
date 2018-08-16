import cv2
import numpy as np
from matplotlib import pyplot as plt


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


