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


def getHorizontalHist(region, Th = 10):
    COL_AXIS = 0;
    # Count the number of edge pixels in each column of the region
    horizHist = np.count_nonzero(region, axis=COL_AXIS);
    print("Horizontal Hist Size: %d" % (horizHist.shape[0]));
    # Obtain a binary sequence from the histogram
    bin_seq = np.array(list(map(lambda x: int(x > Th), horizHist)));
    col_boundaries = filterSegments(bin_seq);

    return col_boundaries;


def getVerticalHist(region, Th = 2):
    ROW_AXIS = 1;
    # Count the number of edge pixels in each row of the region
    vertHist = np.count_nonzero(region, axis=ROW_AXIS);
    binSeqVert = np.array(list(map(lambda x: int(x > Th), vertHist)));
    row_boundaries = filterSegments(binSeqVert);

    return row_boundaries;


def pivotingTextDetection(edges):
    col_segment_boundaries = getHorizontalHist(edges);

    row_segment_boundaries = [];
    # For each region bounded by the segments identified
    for r in range(len(col_segment_boundaries)):
        col_bounds = col_segment_boundaries[r];
        left = col_bounds[0];
        right = col_bounds[1];
        region = edges[:, left:right+1];
        row_boundaries = getVerticalHist(region);
        row_segment_boundaries.append(row_boundaries);

    return (col_segment_boundaries, row_segment_boundaries);

