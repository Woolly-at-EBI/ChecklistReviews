#!/usr/bin/env python3
"""Script of my_utils.py is to my_utils.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-10-24
__docformat___ = 'reStructuredText'
chmod a+x my_utils.py
"""


from icecream import ic
import os
import argparse
from collections import Counter


def find_list_duplicates(in_list):
    """

    :param in_list:
    :return:
    """
    counts = dict(Counter(in_list))
    duplicates = {key: value for key, value in counts.items() if value > 1}
    #ic(duplicates.keys())
    return list(duplicates.keys())

def main():
    in_list = ['a','b','c','a','b']
    find_list_duplicates(in_list)

if __name__ == '__main__':
    ic()
    main()
