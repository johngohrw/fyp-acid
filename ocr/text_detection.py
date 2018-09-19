import numpy as np
from matplotlib import pyplot as plt
from img_utils import drawBoundingBox;
from min_coverage import getMinCoverage


def filterSegments(bin_seq):
    ones = [];
    segmentBounds = [];
    for coord, x in np.ndenumerate(bin_seq):
        if x == 1:
            ones.append(x);
        else:
            segmentLen = len(ones);
            currentIndex = coord[0];
            if segmentLen > 3:
                start = currentIndex - segmentLen;
                end = currentIndex - 1;
                segmentBounds.append((start, end));
            ones = [];

    return segmentBounds;


def getColBounds(region, Th = 10):
    COL_AXIS = 0;
    # Count the number of edge pixels in each column of the region
    horizHist = np.count_nonzero(region, axis=COL_AXIS);
    # Obtain a binary sequence from the histogram
    bin_seq = np.array(list(map(lambda x: int(x >= Th), horizHist)));
    col_boundaries = filterSegments(bin_seq);

    return col_boundaries;


def getRowBounds(region, Th = 10):
    ROW_AXIS = 1;
    # Count the number of edge pixels in each row of the region
    vertHist = np.count_nonzero(region, axis=ROW_AXIS);
    binSeqVert = np.array(list(map(lambda x: int(x >= Th), vertHist)));
    row_boundaries = filterSegments(binSeqVert);

    return row_boundaries;


def pivotingTextDetection(edges, orig, debug = False):
    rows = edges.shape[0];
    cols = edges.shape[1];
    # Region represented as (top, bottom, left, right)
    initRegion = (0, rows) + (0, cols);
    # Active Local Image Region Collection - possible candidates for text regions
    # would be added to this collection
    ALIRC = [initRegion];
    txtRegions = [];

    for index, regionBounds in enumerate(ALIRC):
        top, bottom, left, right = regionBounds;
        region = edges[top:bottom+1, left:right+1];

        col_bounds = getColBounds(region);

        # A region is considered to be a true text region when it could not be
        # be further subdivided into subregions
        if len(col_bounds) == 0:
            if debug:
                referenceImg = orig[top:bottom+1, left:right+1];
                plt.imshow(referenceImg, 'gray');
                plt.show();
            txtRegions.append(regionBounds);

        for col_bound in col_bounds:
            # Column boundaries is relative to the subregion,
            # but we want their actual position in the original image
            segment_left = left + col_bound[0];
            segment_right = left + col_bound[1];

            subregion = edges[:, segment_left:segment_right+1];
            row_bounds = getRowBounds(subregion);

            for row_bound in row_bounds:
                # Again the row boundaries are relative to the subregion
                segment_top = top + row_bound[0];
                segment_bottom = top + row_bound[1];
                detectedRegion = (segment_top, segment_bottom, segment_left, segment_right);

                minCoveredRegion = getMinCoverage(edges, detectedRegion);
                if debug:
                    regionImg = edges[segment_top:segment_bottom+1, segment_left:segment_right+1];
                    minTop, minBot, minLeft, minRight = minCoveredRegion;
                    minRegionImg = edges[minTop:minBot+1, minLeft:minRight+1];

                    plt.subplot(1, 2, 1), plt.imshow(regionImg, 'gray');
                    plt.subplot(1, 2, 2), plt.imshow(minRegionImg, 'gray');
                    plt.show();

                ALIRC.append(minCoveredRegion);

    return txtRegions;

