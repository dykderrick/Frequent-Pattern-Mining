# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/14
# @Author  : Yingke Ding
# @File    : run_different_data_length.py
# @Software: PyCharm

import apriori
import fp_growth
from time import time

if __name__ == '__main__':
    data_lengths = [500, 1000, 1500, 2000, 3000, 5000, 7500, 9835]
    min_sup = 50

    for data_length in data_lengths:
        start_time = time()
        print("BEGIN FP GROWTH WITH DATA LENGTH: " + str(data_length))
        fp_growth.main(min_sup=min_sup, data_length=data_length, is_save_results=False)
        stop_time = time()
        print("END FP GROWTH IN " + "%.2f" % (stop_time - start_time) + "s\n")

    for data_length in data_lengths:
        start_time = time()
        print("BEGIN APRIORI WITH DATA LENGTH: " + str(data_length))
        apriori.main(min_sup=min_sup, data_length=data_length, is_save_results=False)
        stop_time = time()
        print("END APRIORI IN " + "%.2f" % (stop_time - start_time) + "s\n")
