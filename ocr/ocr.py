import numpy as np
import cv2
from matplotlib import pyplot as plt


def filterSegments(bin_seq):
    segment_len = 0;
    segment_indexes = [];
    segment_boundaries = [];
    # Eliminate segments that are less than 3 pixels wide
    for coord, x in np.ndenumerate(bin_seq):
        if x == 1:
            segment_len += 1;
            x_coord = coord[0];
            segment_indexes.append(x_coord);
        else:
            if segment_len > 0 and segment_len < 3:
                for i in segment_indexes:
                    bin_seq[i] = 0;
                segment_len = 0;
                segment_indexes = [];
            else:
                if segment_len > 0:
                    segment_boundaries.append((segment_indexes[0], segment_indexes[-1]));
                    segment_len = 0;
                    segment_indexes = [];

    return segment_boundaries;


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
    COL_AXIS = 0;
    ROW_AXIS = 1;

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

    # Count the number of edge pixels in each column to get a horizontal histogram
    horizHist = np.count_nonzero(edges, axis=COL_AXIS);
    print("Horizontal Hist Size: %d" % (horizHist.shape[0]));


    Th = 10;
    bin_seq = np.array(list(map(lambda x: int(x > Th), horizHist)));
    col_segment_boundaries = filterSegments(bin_seq);


    Tv = 2;
    row_segment_boundaries = [];
    # For each region bounded by the segments identified
    for r in range(len(col_segment_boundaries)):
        col_bounds = col_segment_boundaries[r];
        left = col_bounds[0];
        right = col_bounds[1];
        region = edges[:, left:right+1];
        # Obtain a vertical histogram for each of the region
        vertHist = np.count_nonzero(region, axis=ROW_AXIS);
        binSeqVert = np.array(list(map(lambda x: int(x > Tv), vertHist)));
        row_boundaries = filterSegments(binSeqVert);

        for row_bounds in row_boundaries:
            drawBoundingBox(img2, col_bounds, row_bounds);

    imagesToShow = [];
    imagesToShow.append(("Original", img));
    #imagesToShow.append(("Edges", edges));
    imagesToShow.append(("Detected Texts", img2));
    showImages(1, 2, imagesToShow);

