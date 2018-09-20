import numpy as np

"""
Calculates the minimum coverage bounding box.

This is done in a two stage expansion and shrinking process.

Minimum Expansion
=================
Minimally expand the region such that it covers all edge pixels outside
of the region that connects to any edge pixels along the boundaries of
the region

Maximum Shrinking
=================
Shrink the region as much as possible without excluding the edge pixels
already in the region
"""

def getMinCoverage(edges, regionBounds):
    expandedRegion = minExpansion(edges, regionBounds);
    shrinkedRegion = maxShrinking(edges, expandedRegion);
    return shrinkedRegion;


def minExpansion(edges, regionBounds):
    top, bottom, left, right  = regionBounds;

    height = edges.shape[0];
    width = edges.shape[1];

    lookaheadVal = 3;
    if top > 0:
        top = detectEdgesOutsideTopAndBottom(edges, top, left, right, -1, -lookaheadVal);
    if bottom < height-1:
        bottom = detectEdgesOutsideTopAndBottom(edges, bottom, left, right, 1, lookaheadVal);

    if left > 0:
        left = detectEdgesOutsideLeftAndRight(edges, left, top, bottom, -1, -lookaheadVal);
    if right < width-1:
        right = detectEdgesOutsideLeftAndRight(edges, right, top, bottom, 1, lookaheadVal);

    newRegionBounds = (top, bottom, left, right);
    return newRegionBounds;


def detectEdgesOutsideTopAndBottom(edges, targetBound, left, right, step, lookahead):
    EDGE_PIXEL = 255;

    rows = edges.shape[0];
    edgeDetected = True;
    current = targetBound;
    # Keep expanding the boundary until there is no more edge pixels that
    # connect with an edge pixel within a region
    while edgeDetected and (current > 0 and current < rows-1):
        for col in range(left, right+1):
            edgeDetected = False;
            currentPixel = edges[current, col];
            if currentPixel == EDGE_PIXEL:
                neighbour1 = edges[current+step, col-1];
                neighbour2 = edges[current+step, col];
                neighbour3 = edges[current+step, col+1];
                # There is a neighbouring edge pixel at the boundaries
                # of the region, move to next row
                if neighbour1 == EDGE_PIXEL or neighbour2 == EDGE_PIXEL or neighbour3 == EDGE_PIXEL:
                    edgeDetected = True;
                    current += step;
                    break;

                # Allow some gaps in between
                lookaheadRow = current + lookahead;
                if lookaheadRow > 0 or lookaheadRow < rows:
                    n1 = edges[lookaheadRow, col-1];
                    n2 = edges[lookaheadRow, col];
                    n3 = edges[lookaheadRow, col+1];
                    if n1 == EDGE_PIXEL or n2 == EDGE_PIXEL or n3 == EDGE_PIXEL:
                        edgeDetected = True;
                        current += lookahead;
                        break;

    return current;


def detectEdgesOutsideLeftAndRight(edges, targetBound, top, bottom, step, lookahead):
    EDGE_PIXEL = 255;

    cols = edges.shape[1];
    edgeDetected = True;
    current = targetBound;
    # Keep expanding the boundary until there is no more edge pixels that
    # connect with an edge pixel within a region
    while edgeDetected and (current > 0 and current < cols-1):
        for row in range(top, bottom+1):
            edgeDetected = False;
            currentPixel = edges[row, current];
            if currentPixel == EDGE_PIXEL:
                neighbour1 = edges[row-1, current+step];
                neighbour2 = edges[row, current+step];
                neighbour3 = edges[row+1, current+step];
                # There is a neighbouring edge pixel at the boundaries
                # of the region, move to next column
                if neighbour1 == EDGE_PIXEL or neighbour2 == EDGE_PIXEL or neighbour3 == EDGE_PIXEL:
                    edgeDetected = True;
                    current += step;
                    break;

                # Allows some gaps in between
                lookaheadCol = current + lookahead;
                if lookaheadCol > 0 or lookaheadCol < cols:
                    n1 = edges[row-1, lookaheadCol];
                    n2 = edges[row, lookaheadCol];
                    n3 = edges[row+1, lookaheadCol];
                    if n1 == EDGE_PIXEL or n2 == EDGE_PIXEL or n3 == EDGE_PIXEL:
                        edgeDetected = True;
                        current += lookahead;
                        break;

    return current;


def maxShrinking(edges, regionBounds):
    top, bottom, left, right = regionBounds;

    top = shrinkRowBounds(edges, top, left, right, 1);
    bottom = shrinkRowBounds(edges, bottom, left, right, -1);

    left = shrinkColBounds(edges, left, top, bottom, 1);
    right = shrinkColBounds(edges, right, top, bottom, -1);

    newRegionBounds = (top, bottom, left, right);
    return newRegionBounds;


def shrinkRowBounds(edges, rowBound, left, right, step):
    EDGE_PIXEL = 255;

    rows = edges.shape[0];
    current = rowBound;
    edgeDetected = False;
    while not edgeDetected:
        for col in range(left, right+1):
            currentPixel = edges[current, col];
            if currentPixel == EDGE_PIXEL:
                edgeDetected = True;
                break;
        if not edgeDetected:
            current += step;
        if current < 0 or current >= rows:
            current = rowBound;
            break;

    return current;


def shrinkColBounds(edges, colBound, top, bottom, step):
    EDGE_PIXEL = 255;

    cols = edges.shape[1];
    current = colBound;
    edgeDetected = False;
    while not edgeDetected:
        for row in range(top, bottom+1):
            currentPixel = edges[row, current];
            if currentPixel == EDGE_PIXEL:
                edgeDetected = True;
                break;
        if not edgeDetected:
            current += step;
        if current < 0 or current >= cols:
            current = colBound;
            break;

    return current;

