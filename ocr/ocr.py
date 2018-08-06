import cv2
from matplotlib import pyplot as plt

from text_detection import pivotingTextDetection


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

    img = cv2.imread('example.jpg');
    rows = img.shape[0];
    cols = img.shape[1];
    print("Image: Rows = %d, Cols = %d" % (rows, cols));
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

    img2 = img.copy();
    KERNEL_SIZE = 3;
    blurred = cv2.medianBlur(gray, KERNEL_SIZE);

    minTh = 100;
    maxTh = 200;
    edges = cv2.Canny(blurred, minTh, maxTh);

    regions, isTextRegion = pivotingTextDetection(edges);

    for r in range(len(regions)):
        if isTextRegion[r]:
            current = regions[r];
            colBounds = current[2:];
            rowBounds = current[:2];
            drawBoundingBox(img2, colBounds, rowBounds);

    imagesToShow = [];
    imagesToShow.append(("Original", img));
    imagesToShow.append(("Edges", edges));
    imagesToShow.append(("Detected Texts", img2));
    showImages(1, 3, imagesToShow);

