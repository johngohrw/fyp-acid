import copy

def rightshift(dist_arr):
    new_dist_arr = copy.deepcopy(dist_arr)
    for row in range(len(dist_arr)):
        for col in range(len(dist_arr[0])):
            if ((col + row) % 2 == 0 ):
                if (col != 0):
                    new_dist_arr[row][col] = dist_arr[row][col-1]
                else:
                    new_dist_arr[row][col] = dist_arr[row][col+1]
    return new_dist_arr

def bottomshift(dist_arr):
    new_dist_arr = copy.deepcopy(dist_arr)
    for row in range(len(dist_arr)):
        for col in range(len(dist_arr[0])):
            if ((col + row) % 2 == 0 ):
                if (row != 0):
                    new_dist_arr[row][col] = dist_arr[row-1][col]
                else:
                    new_dist_arr[row][col] = dist_arr[row+1][col]
    return new_dist_arr