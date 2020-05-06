# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5
# @Author  : Yingke Ding
# @File    : run.py
# @Software: PyCharm

import apriori
import fp_growth
from time import time


if __name__ == '__main__':
    start_time = time()
    print("BEGIN APRIORI...")
    apriori.main(min_sup=100)
    stop_time = time()
    print("APRIORI COMPLETED")
    print("APRIORI TIME: " + "%.2f" % (stop_time - start_time) + "s")
    print("\n")

    start_time = time()
    print("BEGIN FP_GROWTH")
    fp_growth.main(min_sup=100)
    print("FP_GROWTH COMPLETED")
    stop_time = time()
    print("FP_GROWTH TIME: " + "%.2f" % (stop_time - start_time) + "s")
