# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:09:00 2020

@author: YH Zhao
"""


import numpy as np

float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind': float_formatter})


def TimeSeriesSimilarity(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    paths = np.full((l1 + 1, l2 + 1), np.inf)  # 全部赋予无穷大
    paths[0, 0] = 0
    for i in range(l1):
        for j in range(l2):
            d = s1[i] - s2[j]
            cost = d ** 2
            paths[i + 1, j + 1] = cost + min(paths[i, j + 1], paths[i + 1, j], paths[i, j])

    paths = np.sqrt(paths)
    s = paths[l1, l2]
    return s, paths.T


if __name__ == '__main__':
    s1 = [1, 2, 0]
    s2 = [1, 0, 1]

    distance, paths = TimeSeriesSimilarity(s1, s2)
    print(paths)
    print("=" * 40)
    print(distance)