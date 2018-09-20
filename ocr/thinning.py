def neighbours(x,y,image):
    """
    Return 8-neighbours of image point P1(x,y), in a clockwise order

    The 8 neighbours are:
    [P9, P2, P3,
     P8, P1, P4,
     P7, P6, P5]
    """
    img = image;
    x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1;
            # P2,P3,P4,P5
    return [ img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],
            # P6, P7, P8, P9
            img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1] ];


def transitions(neighbours):
    """
    No. of white(BLACK) to black(WHITE) transitions(1) in the sequence
    P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> P9 -> P2
    which is just a clockwise cycle of the neighbour pixls of P1
    """
    # P2 at the end since its a cycle
    n = neighbours + neighbours[0:1];
    return sum( (n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]) )


def zhangSuen(image):
    """
    Zhang Suen's thinning algorithm. Credits to:
    https://rosettacode.org/wiki/Zhang-Suen_thinning_algorithm#Python

    Special values:
    A(P1) = the number of white to black transitions of P1's neighbours,
            see transitions() for more info
    B(P1) = the number of black pixels around P1
    """

    MAX_PX_VAL = 255;
    # Most information sources depict edge pixels as BLACK while background
    # is WHITE, thus to avoid confusion, we would assume the edge pixels to
    # be BLACK when in actuality they are WHITE. URGHHHH!!!
    #
    # Also, work with only 1s (BLACK) and 0s (WHITE) for convenience
    thinned = image.copy() / MAX_PX_VAL;

    # The pixels to be removed (set as 0)
    changing1 = changing2 = 1;
    # Iterate until no further changes occur in the image
    while changing1 or changing2:
        # Step 1
        changing1 = []
        rows, columns = thinned.shape;
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, thinned)
                # Condition 0: P1 is a black (WHITE) pixel
                if (thinned[x][y] == 1 and
                    # Condition 1: 2 <= B(P1) <= 6
                    2 <= sum(n) <= 6 and
                    # Condition 2: A(P1)=1
                    transitions(n) == 1 and
                    # Condition 3: One of P2, P4, P6 is white (BLACK)
                    P2 * P4 * P6 == 0  and
                    # Condition 4: One of P4, P6, P8 is white (BLACK)
                    P4 * P6 * P8 == 0):
                    changing1.append((x,y))

        for x, y in changing1:
            thinned[x][y] = 0;

        # Step 2
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, thinned)
                # Condition 0: Same as step 1
                if (thinned[x][y] == 1   and
                    # Condition 1: Same as step 1
                    2 <= sum(n) <= 6  and
                    # Condition 2: Same as step 1
                    transitions(n) == 1 and
                    # Condition 3: One of P2, P4, P8 is white (BLACK)
                    P2 * P4 * P8 == 0 and
                    # Condition 4: One of P2, P6, P8 is white (BLACK)
                    P2 * P6 * P8 == 0):
                    changing2.append((x,y))

        for x, y in changing2:
            thinned[x][y] = 0;

    return thinned * MAX_PX_VAL;

