# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/3
# @Author  : Yingke Ding
# @File    : dataset_IO.py
# @Software: PyCharm

import csv
import operator


def get_transactions_db_from_dataset(csv_file_path):
    """
    Get data from csv file. And redirect names to indices for less computing in the algorithm.
    :param csv_file_path: string
    :return: name2index, index2name, transactions
    """
    transactions_strings = []
    transactions = []
    name2index = dict()
    current_count = 0

    with open(csv_file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            transactions_strings.append(row[1][1:-1])  # 1:-1 to delete bracket in the file

    transactions_strings = transactions_strings[1:]  # delete 0-th string (title)
    transactions_data = [transaction_string.split(",") for transaction_string in transactions_strings]

    for transaction in transactions_data:
        for item in transaction:
            if item not in name2index.keys():
                name2index[item] = current_count
                current_count += 1
    index2name = {value: key for key, value in name2index.items()}  # reverse

    for transaction in transactions_data:
        itemset = [name2index[item] for item in transaction]
        transactions.append(itemset)

    return name2index, index2name, transactions


def save_frequent_itemsets_to_file(frequent_itemsets, result_file_path):
    """
    Set the result into a csv file.
    :param frequent_itemsets: result in type of dict.
    :param result_file_path: string
    :return:
    """
    with open(result_file_path, "w") as csv_file:
        csv_file.write("%s, %s\n" % ("itemsets", "count"))
        for key in frequent_itemsets.keys():
            csv_file.write("%s, %s\n" % ("\"" + key + "\"", frequent_itemsets[key]))
