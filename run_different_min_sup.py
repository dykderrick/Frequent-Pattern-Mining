# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/14
# @Author  : Yingke Ding
# @File    : run_different_min_sup.py
# @Software: PyCharm

import apriori
import fp_growth
from time import time

if __name__ == '__main__':
    minimum_supports = [10, 20, 50, 100, 150, 300, 500]
    for min_sup in minimum_supports:
        start_time = time()
        print("BEGIN FP GROWTH WITH MIN_SUP: " + str(min_sup))
        fp_growth.main(min_sup, is_save_results=False)
        stop_time = time()
        print("END FP GROWTH IN " + "%.2f" % (stop_time - start_time) + "s\n")

    for min_sup in minimum_supports:
        start_time = time()
        print("BEGIN APRIORI WITH MIN_SUP: " + str(min_sup))
        apriori.main(min_sup, is_save_results=False)
        stop_time = time()
        print("END APRIORI IN " + "%.2f" % (stop_time - start_time) + "s\n")
