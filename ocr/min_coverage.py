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
    top = regionBounds[0]; bottom = regionBounds[1];
    left = regionBounds[2]; right = regionBounds[3];

    height = edges.shape[0];
    width = edges.shape[1];

    if top > 0:
        top = detectEdgesOutsideTopAndBottom(edges, top, left, right, -1);
    if bottom < height-1:
        bottom = detectEdgesOutsideTopAndBottom(edges, bottom, left, right, 1);

    if left > 0:
        left = detectEdgesOutsideLeftAndRight(edges, left, top, bottom, -1);
    if right < width-1:
        right = detectEdgesOutsideLeftAndRight(edges, right, top, bottom, 1);

    newRegionBounds = (top, bottom, left, right);
    return newRegionBounds;


def detectEdgesOutsideTopAndBottom(edges, targetBound, left, right, step):
    EDGE_PIXEL = 255;

    noEdgeDetected = False;
    current = targetBound;
    # Keep expanding the boundary until there is no more edge pixels that
    # connect with an edge pixel within a region
    while not noEdgeDetected:
        for col in range(left, right+1):
            noEdgeDetected = True;
            currentPixel = edges[current, col];
            if currentPixel == EDGE_PIXEL:
                neighbour1 = edges[current+step, col-1];
                neighbour2 = edges[current+step, col];
                neighbour3 = edges[current+step, col+1];
                if neighbour1 == EDGE_PIXEL or neighbour2 == EDGE_PIXEL or neighbour3 == EDGE_PIXEL:
                    noEdgeDetected = False;
                    current += step;
                    break;

    return current;


def detectEdgesOutsideLeftAndRight(edges, targetBound, top, bottom, step):
    EDGE_PIXEL = 255;

    noEdgeDetected = False;
    current = targetBound;
    # Keep expanding the boundary until there is no more edge pixels that
    # connect with an edge pixel within a region
    while not noEdgeDetected:
        for row in range(top, bottom+1):
            noEdgeDetected = True;
            currentPixel = edges[row, current];
            if currentPixel == EDGE_PIXEL:
                neighbour1 = edges[row-1, current+step];
                neighbour2 = edges[row, current+step];
                neighbour3 = edges[row+1, current+step];
                if neighbour1 == EDGE_PIXEL or neighbour2 == EDGE_PIXEL or neighbour3 == EDGE_PIXEL:
                    noEdgeDetected = False;
                    current += step;
                    break;

    return current;


def maxShrinking(edges, regionBounds):
    top = regionBounds[0]; bottom = regionBounds[1];
    left = regionBounds[2]; right = regionBounds[3];

    top = shrinkRowBounds(edges, top, left, right, 1);
    bottom = shrinkRowBounds(edges, bottom, left, right, -1);

    left = shrinkColBounds(edges, left, top, bottom, 1);
    right = shrinkColBounds(edges, right, top, bottom, -1);

    newRegionBounds = (top, bottom, left, right);
    return newRegionBounds;


def shrinkRowBounds(edges, rowBound, left, right, step):
    EDGE_PIXEL = 255;

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

    return current;


def shrinkColBounds(edges, colBound, top, bottom, step):
    EDGE_PIXEL = 255;

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

    return current;

