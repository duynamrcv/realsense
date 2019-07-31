import numpy as np

def nearestFace(list_dist_obj):
    min_obj =  list_dist_obj[0]
    for i in range(len(list_dist_obj)):
        if list_dist_obj[i][3] < min_obj[3]:
            min_obj = list_dist_obj[i]
    return min_obj

arr = np.array([[1, 2, 3, 2],
                [3, 2, 10, 4],
                [11, 2, 3, 6],
                [0, 0, 0, 0],
                [0, 0, 0, 1]])
ls = nearestFace(arr)
print ls