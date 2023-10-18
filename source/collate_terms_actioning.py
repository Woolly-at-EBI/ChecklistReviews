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
import sys
import re
datadir = "/Users/woollard/projects/ChecklistReviews/data/"

def get_input_data():
    """"""
    ic()
    input_spreadsheet = datadir + "all_terms_matches_ena2mixs.xlsx"
    #all_terms_matches_mixs2ena
    df_ena2mixs = pd.read_excel(input_spreadsheet, sheet_name="all_terms_matches_ena2mixs")
    #ic(df_ena2mixs.head())

    df_mixs2ena = pd.read_excel(input_spreadsheet, sheet_name='all_terms_matches_mixs2ena')
    #ic(df_mixs2ena.head())
    return df_ena2mixs, df_mixs2ena

def process_straight_forward_terms(df_ena2mixs, df_mixs2ena):
    """

    :param df_ena2mixs:
    :param df_mixs2ena:
    :return: the same dataframes, but removed the easy to process terms,
             + stats
    """
    stats_dict = {}
    #ic(df_ena2mixs)
    stats_dict['total_ena'] = len(df_ena2mixs)
    stats_dict['total_mixs'] = len(df_mixs2ena)

    stats_dict['exact_matches'] = df_ena2mixs.query('match_type == "exact"')['left_term'].tolist()
    stats_dict['uniq2ena'] = df_ena2mixs.query('match_type == "none"')['left_term'].tolist()
    stats_dict['harmonised_ena'] = df_ena2mixs.query('match_type == "harmonised"')['left_term'].tolist()
    stats_dict['harmonised_mixs'] = df_ena2mixs.query('match_type == "harmonised"')['match in MIXS'].tolist()
    df_ena2mixs = df_ena2mixs.query('match_type not in  ["exact", "harmonised", "none"]')
    #ic(df_ena2mixs)
    df_mixs2ena = df_mixs2ena.query('match_type not in  ["exact", "harmonised"]')
    #ic(df_mixs2ena)
    return df_ena2mixs, df_mixs2ena, stats_dict
def process_fuzzy_terms(df_ena2mixs, df_mixs2ena, stats_dict):
    """

    :param df_ena2mixs:
    :param df_mixs2ena:
    :param stats_dict:
    :return:
    """
    #ic(len(df_ena2mixs))


    ic(df_ena2mixs['mapping_recommend'].value_counts())
    #ic(df_ena2mixs.query('mapping_recommend == False').head(5))
    stats_dict['uniq2ena'].extend(df_ena2mixs.query('mapping_recommend == False')['left_term'].tolist())
    #ic(stats_dict['uniq2ena'])
    df_ena2mixs = df_ena2mixs.query('mapping_recommend != False')
    ic(len(df_ena2mixs))
    stats_dict['harmonised_ena'].extend(df_ena2mixs.query('mapping_recommend == True')['left_term'].tolist())
    stats_dict['harmonised_mixs'].extend(df_ena2mixs.query('mapping_recommend == True')['match in MIXS'].tolist())
    df_ena2mixs = df_ena2mixs.query('mapping_recommend != True')
    df_mixs2ena = df_mixs2ena.query('mapping_recommend != True')

    stats_dict['unsure_ena'] = df_ena2mixs.query('mapping_recommend in ["PARTIAL","UNSURE"]')['left_term'].tolist()
    stats_dict['unsure_mixs'] = df_ena2mixs.query('mapping_recommend in ["PARTIAL","UNSURE"]')['match in MIXS'].tolist()
    stats_dict['unsure_mixs_set'] = set(stats_dict['unsure_mixs'])
    ic(stats_dict['unsure_mixs_set'])
    df_ena2mixs = df_ena2mixs.query('mapping_recommend not in ["PARTIAL","UNSURE"]')
    ic(len(df_ena2mixs))
    tmp_set = set(df_mixs2ena['left_term'].tolist())  # this is what is left
    tmp_set.discard(set(stats_dict['unsure_mixs']))
    stats_dict['uniq2mixs']  = list(tmp_set)

    return df_ena2mixs, df_mixs2ena, stats_dict

def create_annotated_list(list_length,annotation):
        my_list = []
        for i in range(list_length):
            my_list.append(annotation)

        return my_list

def assess2lists4left_rules(left_list, right_list, action_list):
    """
    asssumes that all the lists are the same length!
    :param left_list:
    :param right_list:
    :param action_list:
    :return:
    """
    for i in range(len(left_list)):
        found_US = False
        if "_" in left_list[i]:
            ic(f"{left_list[i]} contains '_'")
            action_list[i] = "remove '_' from the ENA term name and then map them"
            found_US = True
        if bool(re.match(r'[A-Z]', left_list[i])):
            ic(f"{left_list[i]} contains upper case chars")
            if found_US:
               action_list[i] = "remove '_' from the ENA term name, make lower case; then map them"
            else:
                action_list[i] = "make ENA term lower case; then map them"

    return action_list

def generatePrioritisingSpreadsheet(stats_dict,prioritised_xlsx_filename):
    """
    Adding the terms to a dataframe and then write the dataframe to a spreadsheet


    :param stats_dict:
    :param prioritised_xlsx_filename:
    :return: the data frame
    """

    #improved changes to ENA terms to start with
    priority_list = create_annotated_list(len(stats_dict['harmonised_ena']),"high")
    action_list = create_annotated_list(len(stats_dict['harmonised_ena']), "map the terms")
    comment_list = create_annotated_list(len(stats_dict['harmonised_ena']), "")
    assess2lists4left_rules(stats_dict['harmonised_ena'], stats_dict['harmonised_mixs'], action_list)

    df = pd.DataFrame({'ENA_term': stats_dict['harmonised_ena'], 'MIXSv6_term': stats_dict['harmonised_mixs'],
                       'priority': priority_list, 'comment': comment_list})
    ic(df)
    # mapping "harmonised"



    # actions for the unsures


    # actions for uniq 2 mixs terms




def printStats(stats_dict):
    ic()
    ic(stats_dict['total_ena'])
    ic(stats_dict['total_mixs'])
    ic(len(stats_dict['exact_matches']))
    ic(len(stats_dict['uniq2ena']))
    ic(len(stats_dict['uniq2mixs']))
    ic(len(stats_dict['harmonised_ena']))
    ic(len(stats_dict['harmonised_mixs']))
    ic(len(stats_dict['unsure_ena'] ))
    ic(len(set(stats_dict['unsure_mixs'])))

def main():
    df_ena2mixs, df_mixs2ena = get_input_data()
    ic(len(df_ena2mixs))
    ic(len(df_mixs2ena))
    df_ena2mixs, df_mixs2ena, stats_dict = process_straight_forward_terms(df_ena2mixs, df_mixs2ena)
    ic(len(df_ena2mixs))
    df_ena2mixs, df_mixs2ena, stats_dict = process_fuzzy_terms(df_ena2mixs, df_mixs2ena, stats_dict)
    ic(len(df_ena2mixs))
    ic(len(df_mixs2ena))
    printStats(stats_dict)

    prioritised_xlsx_filename = datadir + "ena_mixs_mapping_prioritised.xlsx"
    generatePrioritisingSpreadsheet(stats_dict,prioritised_xlsx_filename)

if __name__ == '__main__':
    ic()
    main()
