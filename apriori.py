# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/2
# @Author  : Yingke Ding
# @File    : apriori.py
# @Software: PyCharm

from dataset_IO import *

test_transactions = [["I1", "I2", "I5"], ["I2", "I4"], ["I2", "I3"], ["I1", "I2", "I4"], ["I1", "I3"], ["I2", "I3"],
                     ["I1", "I3"], ["I1", "I2", "I3", "I5"], ["I1", "I2", "I3"]]


def apriori_algorithm(transactions_db, min_sup):
    """
    Core part for Apriori algorithm.
    :param transactions_db: a list of list of items (transaction).
    :param min_sup: minimum support for the program.
    :return: frequent itemsets for the database.
    """
    frequent_one_itemsets = get_frequent_one_itemsets_and_counts(transactions_db, min_sup)
    frequent_one_itemsets_tuple = {tuple([key]): frequent_one_itemsets[key] for key in frequent_one_itemsets.keys()}

    _frequent_itemsets = []
    for key in frequent_one_itemsets.keys():
        _frequent_itemsets.append([key])
    _frequent_itemsets.sort()

    _final_results = []
    while len(_frequent_itemsets) != 0:
        candidate_k_itemsets = apriori_gen(_frequent_itemsets)
        candidate_k_itemsets_counts = [0 for i in range(len(candidate_k_itemsets))]  # record occurrences (support)

        for transaction in transactions_db:
            for index, candidate_k_itemset in enumerate(candidate_k_itemsets):
                if is_subset(candidate_k_itemset, transaction):
                    candidate_k_itemsets_counts[index] += 1  # update counts

        # pruning based on counts (should be no less than min_sup)
        _frequent_itemsets = [candidate_k_itemset for index, candidate_k_itemset in enumerate(candidate_k_itemsets) if
                              candidate_k_itemsets_counts[index] >= min_sup]

        # also pruning the count record for saving into dictionary
        frequent_itemsets_counts = [candidate_k_itemset_count
                                    for candidate_k_itemset_count in candidate_k_itemsets_counts if
                                    candidate_k_itemset_count >= min_sup]

        # saving results
        frequent_itemsets_dict = dict()
        for index, itemset in enumerate(_frequent_itemsets):
            frequent_itemsets_dict[tuple(itemset)] = frequent_itemsets_counts[index]  # use tuple because of hashable
        _final_results.append(frequent_itemsets_dict)

    del _final_results[-1]  # delete the last one which is null
    _final_results.append(frequent_one_itemsets_tuple)  # unite the frequent 1-itemset for final results
    return _final_results


def apriori_gen(frequent_k_minus_one_itemsets):
    """
    Generate candidate k-itemsets from frequent (k-1)-itemsets.
    :param frequent_k_minus_one_itemsets: L_(k-1)
    :return: C_k
    """
    candidate_k_itemsets = []
    for itemset_a in frequent_k_minus_one_itemsets:
        for itemset_b in frequent_k_minus_one_itemsets:
            # 1. for the process L1 to C2, the two elements should be different.
            # 2. for the process L_(k-1) to C_k, all first k-2 elements should be the same,
            # and the (k-1)-th element should be different.
            if (len(itemset_a) == 1 and itemset_a != itemset_b) or \
                    (itemset_a[:-1] == itemset_b[:-1] and itemset_a[-1] != itemset_b[-1]):
                # join step: generate candidates
                new_candidate = itemset_a.copy()  # copy() in case we modify the raw data simultaneously
                new_candidate.append(itemset_b[-1])
                new_candidate.sort()

                # pruning (only record fruitful candidate)
                if not has_infrequent_subset(new_candidate, frequent_k_minus_one_itemsets) and \
                        new_candidate not in candidate_k_itemsets:
                    candidate_k_itemsets.append(new_candidate)

    return candidate_k_itemsets


def has_infrequent_subset(candidate, frequent_itemsets):
    """
    Determine if an itemset has infrequent subset.
    :param candidate: list of k items
    :param frequent_itemsets: list of frequent (k-1)-itemsets
    :return: boolean type
    """
    for i in range(len(candidate)):
        k_minus_one_subset = candidate[0:i] + candidate[i + 1:]  # 把某一项给除掉
        if k_minus_one_subset not in frequent_itemsets:
            return True
    return False


def is_subset(candidate, transaction):
    """
    Determine if a probable candidate is part of a transaction.
    :param candidate: an itemset in type of a list.
    :param transaction: a tuple of a list of items in db.
    :return: boolean type
    """
    return set(candidate).issubset(transaction)


def get_frequent_one_itemsets_and_counts(transactions_db, min_sup):
    """
    Get frequent 1-itemsets and their occurrences from a transactions database.
    :param transactions_db: all transactions in a list of list of numbers.
    :return: frequent 1-itemsets (in dictionary showing their occurrences).
    """
    _one_itemsets_and_counts = dict()  # item: count

    # Compute candidate 1-itemsets (C1)
    for transaction in transactions_db:
        for item in transaction:
            if item in _one_itemsets_and_counts.keys():
                _one_itemsets_and_counts[item] = _one_itemsets_and_counts[item] + 1
            else:
                _one_itemsets_and_counts.update({item: 1})

    # delete infrequent (support < min_sup) items to get L1
    infrequent_one_items = [key for key in _one_itemsets_and_counts.keys() if _one_itemsets_and_counts[key] < min_sup]
    for item in infrequent_one_items:
        del _one_itemsets_and_counts[item]  # C1 becomes L1 here

    return _one_itemsets_and_counts


def post_process_frequent_itemsets(frequent_itemsets, index2name):
    """
    Convert number use of database to the original name database.
    :param frequent_itemsets: computed results in apriori_algorithm.
    :param index2name: a dict indicating which name corresponds to a specific number.
    :return: final_result in type of a name to number dictionary.
    """
    final_results = {}
    for dict_value in frequent_itemsets:
        final_results = {**final_results, **dict_value}

    final_results_dict = dict()
    for itemset, count in final_results.items():
        item_strings = [index2name[item] for item in itemset]
        itemset_string = ','.join(map(str, item_strings))
        final_results_dict[itemset_string] = count

    return final_results_dict


def main(min_sup=100):
    """
    Driver to the program.
    """
    # get data and use the index for computing
    name2index, index2name, transactions = get_transactions_db_from_dataset("./dataset/Groceries.csv")

    # run
    frequent_itemsets = apriori_algorithm(transactions, min_sup)
    # frequent_itemsets = apriori_algorithm(test_transactions, min_sup=2)
    # print(frequent_itemsets)

    # turn back to the name-number pairs
    final_results_dict = post_process_frequent_itemsets(frequent_itemsets, index2name)
    sorted_final_results_dict = {k: v for k, v in sorted(final_results_dict.items(), key=lambda item: item[1], reverse=True)}

    # save result to a csv file
    save_frequent_itemsets_to_file(sorted_final_results_dict, "./results/apriori_results.csv")
