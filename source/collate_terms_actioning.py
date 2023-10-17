#!/usr/bin/env python3
"""Script of collate_terms_actioning.py is to collate terms for further actioning

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-10-17
__docformat___ = 'reStructuredText'
chmod a+x collated_terms_actioning.py
"""


from icecream import ic
import os
import argparse
import pandas as pd
datadir = "/Users/woollard/projects/ChecklistReviews/data/"

def get_input_data():
    """"""
    ic()
    input_spreadsheet = datadir + "all_terms_matches_ena2mixs.xlsx"
    #all_terms_matches_mixs2ena
    df_ena2mixs = pd.read_excel(input_spreadsheet, sheet_name="all_terms_matches_ena2mixs")
    ic(df_ena2mixs.head())

    df_mixs2ena = pd.read_excel(input_spreadsheet, sheet_name='all_terms_matches_mixs2ena')
    ic(df_mixs2ena.head())
    return df_ena2mixs, df_mixs2ena

def process_straight_forward_terms(df_ena2mixs, df_mixs2ena):
    """

    :param df_ena2mixs:
    :param df_mixs2ena:
    :return: the same dataframes, but removed the easy to process terms,
             + stats
    """
    stats_dict = {}
    ic(df_ena2mixs)

    stats_dict['exact_matches'] = df_ena2mixs.query('match_type == "exact"')['left_term'].tolist()
    stats_dict['harmonised_ena'] = df_ena2mixs.query('match_type == "harmonised"')['left_term'].tolist()
    stats_dict['harmonised_mixs'] = df_ena2mixs.query('match_type == "harmonised"')['match in MIXS'].tolist()
    df_ena2mixs = df_ena2mixs.query('match_type not in  ["exact", "harmonised"]')
    ic(df_ena2mixs)
    df_mixs2ena = df_mixs2ena.query('match_type not in  ["exact", "harmonised"]')
    ic(df_mixs2ena)
    return df_ena2mixs, df_mixs2ena, stats_dict
def process_fuzzy_terms(df_ena2mixs, df_mixs2ena, stats_dict):
    """

    :param df_ena2mixs:
    :param df_mixs2ena:
    :param stats_dict:
    :return:
    """
    ic(len(df_ena2mixs))


    return df_ena2mixs, df_mixs2ena, stats_dict



def main():
    df_ena2mixs, df_mixs2ena = get_input_data()
    df_ena2mixs, df_mixs2ena, stats_dict = process_straight_forward_terms(df_ena2mixs, df_mixs2ena)
    df_ena2mixs, df_mixs2ena, stats_dict = process_fuzzy_terms(df_ena2mixs, df_mixs2ena, stats_dict)

if __name__ == '__main__':
    ic()
    main()
