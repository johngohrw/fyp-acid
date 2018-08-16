import numpy as np


def filterSegments(bin_seq):
    #Filter out segments which are less than 3 pixels wide
    segment_len = 0;
    segment_indexes = [];
    segment_boundaries = [];
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


def pivotingTextDetection(edges):
    rows = edges.shape[0];
    cols = edges.shape[1];
    # Region represented as (top, bottom, left, right)
    initRegion = (0, rows) + (0, cols);
    # Active Local Image Region Collection - possible candidates for text regions
    # would be added to this collection
    ALIRC = [initRegion];
    isTextRegion = [False];

    for index, regionBounds in enumerate(ALIRC):
        top = regionBounds[0]; bottom = regionBounds[1];
        left = regionBounds[2]; right = regionBounds[3];
        region = edges[top:bottom+1, left:right+1];
        col_bounds = getColBounds(region);

        # A region is considered to be a true text region when it could not be
        # be further subdivided into subregions
        if len(col_bounds) == 0:
            isTextRegion[index] = True;

        for col_bound in col_bounds:
            left = col_bound[0];
            right = col_bound[1];
            subregion = edges[:, left:right+1];
            row_bounds = getRowBounds(subregion);
            for row_bound in row_bounds:
                detectedRegion = row_bound + col_bound;
                ALIRC.append(detectedRegion);
                isTextRegion.append(False);

    return (ALIRC, isTextRegion);

