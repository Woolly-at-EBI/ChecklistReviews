# !/usr/bin/env python3
"""Script of 'analyse_mixs.py' is to analyse the mixs

convert to JSON, not quite...
cat o| sed -E "s/: \"/: '/g"|sed -E "s/([A-Za-z])'([A-Za-z])/\1\2/g" | tr "'" '"'|sed 's/: nan,/: "",/g'|head -c 157625


___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-16
__docformat___ = 'reStructuredText'

"""
from icecream import ic
import math
import requests
import json
import sys
import os
import os.path
import pickle
import pandas as pd

import plotly.express as px
# import numpy as np
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud

import plotly.io as pio

# project objects etc. being imported
from pairwise_term_matches import pairwise_term_matches, compareAllTerms
from COMPARISONS import COMPARISONS, pair_string2names
from source_package_name_comparisons import source_package_name_comparisons
import mixs
from mixs import mixs, parse_new_linkml, get_ena_dict, get_mixs_dict, process_mixs_dict
from clean_terms import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pio.renderers.default = "browser"
# from fuzzywuzzy import process

docs_dir = "../docs/"
image_dir = docs_dir + "images/"


def get_data(source_name):
    """

    :return:
    """
    ic()
    if source_name == "mixs_v6":
        json_file = "../data/v6_mixs.schema.json"
    # cat ../data/mixs.schema.json | sed 's/\\"/"/g;s/\\n/\n/g;s/^"//;s/"$//' | sed 's/\\\\"//g'  | jq
    ic(json_file)
    # r_text = '{ "test": "test_val"}'
    if os.path.isfile(json_file):
        ic(f"about to open {json_file}")
        with open(json_file) as f:
            r_json = json.load(f)
            ic(r_json)
    else:
        json_url = ("https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/mixs/jsonschema/mixs"
                    ".schema.json")
        ic(json_url)
        r = requests.get(json_url)
        r_json = r.text

        with open(json_file, 'w') as f:
            json.dump(r_json, f, indent = 4)
        ic(f"Created {json_file}")
    return r_json







def print_mixs_review_dict_stats(mixs_review_dict):
    """

    :param mixs_review_dict:
    :return:
    """
    print(f"Count of top_level MIX-S checklists={len(mixs_review_dict['by_package'])}")
    for checklist_name in mixs_review_dict['by_package']:
        print(f"{checklist_name} field_count={mixs_review_dict['by_package'][checklist_name]['count']}")




# this is the mixs.py too, need to work out how to only have one copy!
def add_term_package_count(my_dict):
    """
    for all the term_name's add the package_name and count.
    slightly verbose, being careful in case the dictionary has already been partially populated.

    :param my_dict:
    :return: my_dict
    """

    for package_name in my_dict["by_package"]:
        for term_name in my_dict["by_package"][package_name]["field"]:
            if term_name in my_dict["by_term"] and 'packages' in my_dict["by_term"][term_name]:
                my_dict["by_term"][term_name]['packages'].append(package_name)
                my_dict["by_term"][term_name]['count'] += 1
            else:
                if term_name not in my_dict["by_term"]:
                    my_dict["by_term"][term_name] = {}
                my_dict["by_term"][term_name]['packages'] = [package_name]
                my_dict["by_term"][term_name]['count'] = 1
    my_dict["by_term_count"] = {}

    # now to add by_term_count
    for term_name in my_dict["by_term"]:
        my_total = my_dict["by_term"][term_name]['count']
        if my_total not in my_dict["by_term_count"]:
            my_dict["by_term_count"][my_total] = {}
        my_dict["by_term_count"][my_total][term_name] = {}
        my_dict["by_term_count"][my_total][term_name]['packages'] = my_dict["by_term"][term_name]['packages']

    # ic(my_dict["by_term_count"])
    # sys.exit()
    return my_dict


def url2file(url):
    # url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/mixs/jsonschema/mixs.schema.json"
    ic(url)
    r = requests.get(url)
    r_json = r.text


def get_ena_cl_details(ena_cl_dict):
    """get_ena_cl_details
    is actually a simplification
    is designed to be consumed by the "class mixs object)
    :param ena_cl_dict:
    :return:
    """
    ena_simplified_cl_dict = {}
    # ic(ena_cl_dict)
    count = 0
    for checklist in ena_cl_dict["CHECKLIST_SET"]["CHECKLIST"]:
        # ic(count)
        count += 1
        # ic(checklist["@accession"])
        # ic(checklist["DESCRIPTOR"]["NAME"])
        cl_name = checklist["DESCRIPTOR"]["NAME"]
        ena_simplified_cl_dict[cl_name] = {}
        ena_simplified_cl_dict[cl_name]["field_name"] = {}
        for field_group in checklist["DESCRIPTOR"]["FIELD_GROUP"]:
            # ic(field_group["NAME"])
            # ic(field_group)
            # ic(field_group["NAME"])
            for sp_field in field_group["FIELD"]:
                if isinstance(sp_field, dict):
                    # ic(sp_field)
                    # ic(sp_field["NAME"])
                    ena_simplified_cl_dict[cl_name]["field_name"][sp_field["NAME"]] = "PRESENT"
        # ic(ena_simplified_cl_dict)   # 'GSC MIxS microbial mat biolfilm': {'field_name': {'adapters': 'PRESENT',
    return ena_simplified_cl_dict




# **********************************************************************************




def get_mixs_v5_dict():
    """
        mixs_v5_dict['by_package'][checklist_env_package_name][package_item][key] = mixs_v5_simple_dict[index][key]
        mixs_v5_dict['by_term'][package_item][key] = mixs_v5_simple_dict[index][key]
    :return:
    """
    pickle_file = "../data/mixs_v5.dict.pickle"

    if os.path.isfile(pickle_file):
        ic(f"found {pickle_file}")
        with open(pickle_file, 'rb') as handle:
            mixs_v5_dict = pickle.load(handle)
    else:

        # https://github.com/GenomicsStandardsConsortium/mixs-legacy/blob/master/mixs5/mixs_v5.xlsx
        xlsx_file = '../data/mixs_v5.xlsx'

        df_mixs5 = pd.read_excel(xlsx_file, sheet_name = 'environmental_packages')
        # print(df_mixs5.head(5))
        # print(df_mixs5.head(5).to_dict(orient = 'records'))
        mixs_v5_simple_dict = df_mixs5.to_dict(orient = 'index')
        mixs_v5_dict = {}
        mixs_v5_dict['by_package'] = {}
        mixs_v5_dict['by_term'] = {}
        # print ("==============================================")
        for index in mixs_v5_simple_dict:
            # print("___________________________________________")
            checklist_env_package_name = mixs_v5_simple_dict[index]['Environmental package']
            package_item = mixs_v5_simple_dict[index]['Package item']
            if checklist_env_package_name in mixs_v5_dict:
                # print("YIPPEE")
                # sys.exit()
                pass
            else:
                # print(f"not hasattr: -->{checklist_env_package_name}<--")
                # print(mixs_v5_dict)
                mixs_v5_dict['by_package'][checklist_env_package_name] = {}

                # print(mixs_v5_dict)
            # print(package_item)
            mixs_v5_dict['by_package'][checklist_env_package_name][package_item] = {}
            mixs_v5_dict['by_term'][package_item] = {}
            for key in mixs_v5_simple_dict[index]:
                if key == 'Environmental package' or key == 'Package item':
                    continue
                else:
                    mixs_v5_dict['by_package'][checklist_env_package_name][package_item][key] = \
                        mixs_v5_simple_dict[index][key]
                    mixs_v5_dict['by_term'][package_item][key] = mixs_v5_simple_dict[index][key]
            # print(mixs_v5_dict)
        # sys.exit()
        # print(json.dumps(mixs_v5_dict, indent=4))
        with open(pickle_file, 'wb') as handle:
            pickle.dump(mixs_v5_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)

    return mixs_v5_dict


def unique_elements_left(left_list, term_matches):
    left_list_set = set(left_list)
    difference = left_list_set.difference(set(term_matches))
    difference = list(difference)
    difference.sort()

    return difference


def do_stats(ena_cl_obj, mixs_v5_obj, mixs_v6_obj):
    def list2file(my_list, file_name):
        # print(f"{file_name}")
        with open(file_name, "w") as f:
            f.write("\n".join(my_list))
        return file_name

    def various(left, right, stats_dict):
        """
        function to print out the statistics for the lists of terms in the left and right objects,
        is an interlude to allow the print_exact_term_stats to be more simple to just process lists
        :param left: MIXs object
        :param right: MIXs object
        :return: dict
        """
        message = ""
        (left_diff, right_diff) = get_unmatched(left.get_all_term_list(), right.get_all_term_list())

        print_exact_term_stats(left.get_all_term_list(), left_diff, left.type, right.get_all_term_list(), right_diff,
                               right.type, message, stats_dict)
        print()
        print_cleaned_term_stats(left.get_all_term_list(), left.type, right.get_all_term_list(), right.type, message,
                                 stats_dict)

    def print_exact_term_stats(left_list, left_unmatched, left_type, right_list, right_unmatched, right_type, message,
                               stats_dict):
        """

        :param left_list:
        :param left_unmatched:
        :param left_type: name of the left type
        :param right_list:
        :param right_unmatched:
        :param right_type: name of the right type
        :param message: This allows other functions to reuse this code, but still "know: where
              currently: "harmonised" and "exact"
        :return:
        """
        # print(left_list)
        # print(right_list)

        if message == "":
            message = "exact"
        left_set = set(left_list)
        right_set = set(right_list)
        top_num = 10
        term_matches = list(left_set.intersection(right_set))
        print(f"{message} term_match_count={len(term_matches)}")
        print(f"first {top_num}  matches={term_matches[0:top_num]}")
        if left_type not in stats_dict:
            stats_dict[left_type] = {}
        if right_type not in stats_dict[left_type]:
            stats_dict[left_type][right_type] = {}
        stats_dict[left_type][right_type][message] = {}
        stats_dict[left_type][right_type][message]["matches"] = len(term_matches)
        pair = left_type + right_type
        pair = pair.replace("mixs_", "").replace("ena_cl", "_vs_ena").replace("v5v6", "v5_vs_v6")
        stats_dict[left_type][right_type][message]["pair"] = pair

        print(f"PAIR-{pair}")

        difference = unique_elements_left(left_list, term_matches)
        print(
            f"unique={left_type} ({message} terms):  count={len(difference)} first {top_num} terms={difference[0:top_num]}")
        outfile = list2file(difference, message + "_" + left_type + "_vs_" + right_type + "_unique.txt")
        stats_dict[left_type][right_type][message]["uniq_left"] = len(difference)
        stats_dict[left_type][right_type][message]["left_pc_matched"] = int(
            len(term_matches) * 100 / (len(term_matches) + len(difference)))
        print(f"output to: {outfile}")
        difference = unique_elements_left(right_list, term_matches)
        print(
            f"unique={right_type} ({message} terms):  count={len(difference)} first {top_num} terms={difference[0:top_num]}")
        outfile = list2file(difference, message + "_" + right_type + "_vs_" + left_type + "_unique.txt")
        print(f"output to: {outfile}")
        stats_dict[left_type][right_type][message]["uniq_right"] = len(difference)
        stats_dict[left_type][right_type][message]["right_pc_matched"] = int(
            len(term_matches) * 100 / (len(term_matches) + len(difference)))
        stats_dict[left_type][right_type][message]["left_unmatched_count"] = int(len(left_unmatched))
        # stats_dict[left_type][right_type][message]["left_unmatched_names"] = left_unmatched
        stats_dict[left_type][right_type][message]["right_unmatched_count"] = int(len(right_unmatched))
        # stats_dict[left_type][right_type][message]["right_unmatched_names"] = right_unmatched

    def get_unmatched(left_list, right_list):
        left_set = set(left_list)
        right_set = set(right_list)
        term_matches = list(left_set.difference(right_set))
        # print(f"left_non_matched count:  {len(term_matches)}")
        # print(term_matches)

        term_matches = list(right_set.difference(left_set))
        # print(f"right_non_matched count:  {len(term_matches)}")
        # print(term_matches)
        return list(left_set.difference(right_set)), list(right_set.difference(left_set))

    def print_cleaned_term_stats(left_list, left_type, right_list, right_type, message, stats_dict):
        left_clean_term_list = clean_list(left_list)
        right_clean_term_list = clean_list(right_list)
        message = "harmonised"
        (left_diff, right_diff) = get_unmatched(left_clean_term_list, right_clean_term_list)
        print_exact_term_stats(left_clean_term_list, left_diff, left_type, right_clean_term_list, right_diff,
                               right_type, message, stats_dict)

    stats_dict = {}
    clean_des = "lower case + underscoring spaces and hyphens"
    print(f"Cleaning is: {clean_des}")

    print("\n======MIXS v5 verses ENA=========" + "\n")
    print(f"mixs_v5 term count={mixs_v5_obj.get_all_term_count()}" + "\n")
    print(f"ena_cl term count={ena_cl_obj.get_all_term_count()}\n" + "\n")
    various(mixs_v5_obj, ena_cl_obj, stats_dict)

    print("\n======MIXS v6 verses ENA=========" + "\n")
    print(f"mixs_v6 term count={mixs_v6_obj.get_all_term_count()}" + "\n")
    print(f" ena_cl term count={ena_cl_obj.get_all_term_count()}\n" + "\n")
    various(mixs_v6_obj, ena_cl_obj, stats_dict)

    #
    print("\n======MIXS v5 verses v6=========")
    print(f"mixs_v5 term count={mixs_v5_obj.get_all_term_count()}" + "\n")
    print(f"mixs_v6 term count={mixs_v6_obj.get_all_term_count()}\n" + "\n")
    various(mixs_v5_obj, mixs_v6_obj, stats_dict)

    print(stats_dict)
    return stats_dict


def unpack_dict(stats_dict):
    """
    left term is ENA and right term is MIXS
    :param stats_dict:
    :return:
    """
    df = pd.DataFrame(
        columns = ['left_repo', 'right_repo', 'match_type', 'matches', 'uniq_left', 'left_pc_matched', 'uniq_right',
                   'right_pc_matched'])
    df = df.astype({'matches': 'int', 'uniq_left': 'int', 'left_pc_matched': 'int', 'uniq_right': 'int',
                    'right_pc_matched': 'int'})
    for left_term in stats_dict:
        print(f"{left_term}")
        for right_term in stats_dict[left_term]:
            print(f"\t{right_term}")

            for match_type in stats_dict[left_term][right_term]:
                print(f"\t\t{match_type}")
                temp_dict = {'left_repo': [left_term], 'right_repo': [right_term], 'match_type': [match_type],
                             'matches': [0], 'uniq_left': [0], 'uniq_right': [0]}
                for matches in stats_dict[left_term][right_term][match_type]:
                    print(f"\t\t\t{matches} total={stats_dict[left_term][right_term][match_type][matches]}")
                    temp_dict[matches] = stats_dict[left_term][right_term][match_type][matches]
                # df = df.append(temp_dict, ignore_index=True)
                df_temp = pd.DataFrame.from_dict(temp_dict, orient = 'columns')
                # df_temp.reset_index(inplace = True)
                # df.reset_index(inplace = True, drop = True)
                df = pd.concat([df, df_temp])
                # df = df.loc[~df.index.duplicated(keep = 'first')]

    ic(stats_dict)
    return df


def plot_pair_counts_df(df, image_dir):
    import plotly.io as pio
    pd.options.plotting.backend = "plotly"
    pio.renderers.default = "browser"
    print(df)

    fig = df.plot.bar(x = "pair", y = "right_pc_matched", color = "match_type", text = "pair",
                      title = "Comparisons of Different Versions of Checklist by Counts of Matching Terms",
                      barmode = "group")
    # fig.show()
    out_file = image_dir + "matches_table_plot.png"
    fig.write_image(out_file)
    # sys.exit()
    return out_file


def compare2termLists(left_term_list, right_term_list, comparisonStatsPackage):
    """
    does comparison of two term lets, including some simple harmonisation(cleaning)
    The results are going into the relevant part of a dictionary collecting statistics.
    currently much is commented out, as did not want to load up the stats dictionary with excessive terms.
    :param left_term_list:
    :param right_term_list:
    :param comparisonStatsPackage:  # is optional
    :return:

    comparisonStatsPackage['length_union']
    comparisonStatsPackage['length_intersection']
    comparisonStatsPackage['clean_intersection_set']
    comparisonStatsPackage['intersection_set']
    comparisonStatsPackage['clean_left_diff_set'] = clean_left_diff
    comparisonStatsPackage['clean_right_diff_set'] = clean_right_diff
    comparisonStatsPackage['left_diff_set']
    comparisonStatsPackage['right_diff_set']
    comparisonStatsPackage['pc_left_of_right']
    comparisonStatsPackage['length_left']
    comparisonStatsPackage['length_right']

    """
    # ic("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    if not comparisonStatsPackage:
        comparisonStatsPackage = {}

    clean_left_set = cleanList2set(left_term_list)
    # comparisonStatsPackage['left_term_list'] = clean_left_set
    clean_right_set = cleanList2set(right_term_list)
    # comparisonStatsPackage['right_term_list'] = clean_right_set
    union = clean_right_set.union(clean_left_set)
    # comparisonStatsPackage['union_term_list'] = union

    left_set = set(left_term_list)
    right_set = set(right_term_list)

    clean_intersection = clean_right_set.intersection(clean_left_set)
    # comparisonStatsPackage['intersection_term_list'] = intersection
    clean_left_diff = clean_left_set.difference(clean_right_set)
    # comparisonStatsPackage['left_diff_list'] = left_diff

    # ic(left_diff)
    clean_right_diff = clean_right_set.difference(clean_left_set)
    # ic(right_diff)
    pc_left_of_right = math.floor(
        (len(clean_intersection) * 100) / len(clean_right_set)) / 100  # get it as a 2 dp decimal fraction
    comparisonStatsPackage['pc_left_of_right'] = pc_left_of_right
    # ic(f"{len(clean_left_set)} {len(clean_right_set)} union:{len(union)} intersection:{len(intersection)}  pc_left_of_right:{pc_left_of_right}")
    comparisonStatsPackage['length_left'] = len(clean_left_set)
    comparisonStatsPackage['length_right'] = len(clean_right_set)
    comparisonStatsPackage['length_union'] = len(union)
    comparisonStatsPackage['length_clean_intersection'] = len(clean_intersection)
    comparisonStatsPackage['clean_intersection_set'] = clean_intersection
    comparisonStatsPackage['clean_left_diff_set'] = clean_left_diff
    comparisonStatsPackage['clean_right_diff_set'] = clean_right_diff
    comparisonStatsPackage['left_diff_set'] = left_set.difference(right_set)
    comparisonStatsPackage['right_diff_set'] = right_set.difference(left_set)
    comparisonStatsPackage['intersection_set'] = left_set.intersection(right_set)
    return comparisonStatsPackage

def names2pair_string(left_name, right_name):
        return '::'.join([left_name, right_name])


def compare2packages(comparison, left_package_name, right_package_name, left_obj, right_obj, comparisonStats, report):
    def print_minimal_stats(comparisonStatsPackage, report):
        report.write(f"## Minimal_stats:\n\tlength_intersection={comparisonStatsPackage['length_clean_intersection']}")
        report.write(f"\n\tlength_union={comparisonStatsPackage['length_union']}")
        report.write(f"\n\tlength_left={comparisonStatsPackage['length_left']}")
        report.write(f"\n\tlength_right={comparisonStatsPackage['length_right']}")
        report.write(f"\n\tpc_left_of_right={comparisonStatsPackage['pc_left_of_right'] * 100}%" + "\n")



    def create_term_comparison_df(left_obj, right_obj, left_package_name, right_package_name, report):
        """
        given the above objects, runs the comparison functions for the desired 2 packages
        returns a dataframe summarising any matches. The match_type can be exact or harmonised.
        Harmonised is a very simple clean of the terms, it is not doing abbreviations etc. yet.
        :param left_obj:
        :param right_obj:
        :param left_package_name:
        :param right_package_name:
        :return:  df[["left_term", "match_type", "match"]]
        """
        # report.write("\n###
        # report.write("\n=============================================================================\n")
        # # ic()
        # report.write("====" + left_obj.type + "====" +"\n")
        # report.write(', '.join(left_obj.get_term_list_for_package(left_package_name)) + "\n")
        # report.write("====" + right_obj.type + "====" + "\n")
        # report.write(', '.join(right_obj.get_term_list_for_package(right_package_name)) + "\n")
        #
        # report.write('------++++++++---------' + "\n")

        # ic(left_package_name)
        # ic(right_package_name)
        left_term_list = left_obj.get_term_list_for_package(left_package_name)
        right_term_list = right_obj.get_term_list_for_package(right_package_name)
        right_term_list.extend(right_obj.get_term_list_for_package("Core"))
        df = compareAllTerms(left_term_list,right_term_list)

        return df

    # main stream compare2packages aspects
    # ic()
    # building  comparisonStats[comparison]['by_package'][com_package_names]  = {}
    # ic(comparison)
    com_package_names = names2pair_string(left_package_name,right_package_name)
    if comparison not in comparisonStats:  # added on 30 Aug
        comparisonStats[comparison] = {}
        comparisonStats[comparison]['by_package'] = {}
    if com_package_names not in comparisonStats[comparison]['by_package']:
        comparisonStats[comparison]['by_package'][com_package_names] = {}
    comparisonStatsPackage = comparisonStats[comparison]['by_package'][com_package_names]
    comparisonStatsPackage = compare2termLists(left_obj.get_term_list_for_package(left_package_name),
                                               right_obj.get_term_list_for_package(right_package_name),
                                               comparisonStatsPackage)
    comparisonStats[comparison]['by_package'][com_package_names] = comparisonStatsPackage
    # ic(comparisonStatsPackage)
    # ic(comparisonStats)
    report.write('## Comparison of ' + left_package_name + " and " + right_package_name + "\n")
    # sys.exit()
    # report.write("### ====" + left_obj.type + "====" + "\n")
    # report.write(', '.join(left_obj.get_term_list_for_package(left_package_name))+ "\n")
    # report.write("### ====" + right_obj.type + "====" + "\n")
    # report.write(', '.join(right_obj.get_term_list_for_package(right_package_name)) + "\n")
    # print_minimal_stats(comparisonStatsPackage, report)
    # report.write(f"Intersection = {comparisonStatsPackage['clean_intersection_set']}"+ "\n")
    # report.write("### ====" + right_obj.type + " Core" + "====" + "\n")
    # report.write(', '.join(right_obj.get_term_list_for_package("Core"))+ "\n")
    comparisonStatsPackage = comparisonStats[comparison]['by_package'][com_package_names]
    comparisonStatsPackage = compare2termLists(left_obj.get_term_list_for_package(left_package_name),
                                               right_obj.get_term_list_for_package("Core"), comparisonStatsPackage)
    # report.write(f"Intersection = {comparisonStatsPackage['clean_intersection_set']}" + "\n")

    term_comparison_df = create_term_comparison_df(left_obj, right_obj, left_package_name, right_package_name, report)
    # report.write(term_comparison_df.to_string(justify = 'left', index = False))
    # report.write(f"right_diff={', '.join(sorted(comparisonStatsPackage['right_diff_set']))}" + "\n")
    # ic(comparisonStatsPackage)

    report.write("\n" + term_comparison_df.to_markdown(index=False) + "\n")

    # ic("about to exit compare2packages")
    return comparisonStatsPackage


def plot_pair_df(df):
    """

    :param df:
    :return:
    """
    # import dash_bio

    # fig = px.scatter(df, x = "pc_left_of_right", y = "length_intersection", color = "short_mixs_v6", size = 'length_left', hover_data = 'pair')
    # fig.show()
    cut_off = 0.2
    title = "Heatmap of Fraction of ENA Checklists Terms in Different MIXS v6 packages"
    subtitle = '<br><sup>The terms are lightly harmonised before matching e.g. lower cased</sup>'
    title += subtitle
    df_pc = df[['pc_left_of_right', 'ena', 'mixs_v6']]
    # df_pc = df_pc.loc[(df_pc['pc_left_of_right'] >= cut_off)]
    new_df = df_pc.pivot(index = 'ena', columns = 'mixs_v6')['pc_left_of_right']
    # ic(new_df)
    fig = px.imshow(new_df, color_continuous_scale = 'Greens', width = 2000, height = 1000, aspect = 'auto',
                    title = title)
    fig.update_layout(yaxis = dict(title_text = "ENA Checklists",
                                   tickfont = dict(size = 8)),
                      xaxis = dict(title_text = "MIXs v6 Packages",
                                   tickfont = dict(size = 8))
                      )
    fig.update_layout(title_text = title, title_x = 0.5)
    fig.update_xaxes(tickangle = 45)
    fig.update_yaxes(tickangle = 45)
    fig.show()
    image_file = image_dir + "ENAvsMIXSv6_heatmap.jpg"
    ic(f"creating: {image_file}")
    fig.write_image(image_file)

    ic(len(df['ena'].unique()))

    # dash_bio.Clustergram(
    #     data = new_df,
    #     column_labels = list(new_df.columns.values),
    #     row_labels = list(new_df.index),
    #     height = 800,
    #     width = 700,
    #     color_list = {
    #         'row': ['#636EFA', '#00CC96', '#19D3F3'],
    #         'col': ['#AB63FA', '#EF553B'],
    #         'bg': '#506784'
    #     },
    #     line_width = 2
    # )

    df_pc = df_pc.loc[(df_pc['pc_left_of_right'] < 0.3)]
    new_df = df_pc.pivot(index = 'ena', columns = 'mixs_v6')['pc_left_of_right']
    # ic(new_df)
    image_file = image_dir + "ena_checklist_match_heatmap.jpg"
    fig = px.imshow(new_df)
    ic(image_file)
    fig.write_image(image_file)
    # fig.show()
    # sys.exit()




def processComparisonStats(comparisonStats, pair):
    """ processComparisonStats

    :param comparisonStats:
    :return: comparison_obj
    """
    ic("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    ic()
    ic(pair)
    print()
    comparison_obj = COMPARISONS(comparisonStats, pair)
    return comparison_obj


def compareChecklists(left_obj, right_obj, report):
    """
    Comparing all possible pairs of checklists
    :param left_obj:
    :param right_obj:
    :param report:
    :return:

    comparisonStats[comparison]['by_package'][com_package_names]  = {} e.g.

    {'ena::mixs_v6':
       {'by_package':
         {'COMPARE-ECDC-EFSA pilot food-associated reporting standard::Agriculture':
            {'pc_left_of_right': 0.0, 'length_left': 7, 'length_union': 173,
            'length_intersection': 1, 'ena': 'COMPARE-ECDC-EFSA pilot food-associated reporting standard',
            'mixs_v6': 'Agriculture',
            'left_source': 'ena', 'right_source': 'mixs_v6',
            'pair': 'COMPARE-ECDC-EFSA pilot food-associated reporting standard::Agriculture'},

    """
    ic()
    ic(left_obj.type)
    ic(right_obj.type)
    pair_string = names2pair_string(left_obj.type, right_obj.type)
    comparisonStats = {pair_string: {'by_package': {}}}
    ic(comparisonStats)

    # ic(left_obj.get_all_package_list())
    # ic(right.get_all_package_list())
    ic(len(left_obj.get_all_package_list()))
    left_package_count = 0
    count = 0
    for left_package_name in left_obj.get_all_package_list():
        ic(str(left_package_count) + "\t" + left_package_name)
        left_package_count += 1
        if left_package_count > 2:
            break
        for right_package_name in right_obj.get_all_package_list():
            com_package_names = names2pair_string(left_package_name, right_package_name)
            comparisonStats[pair_string]['by_package'][com_package_names] = compare2packages(pair_string, left_package_name,\
                     right_package_name, left_obj, right_obj, comparisonStats, report)
            count += 1
    comparison_obj = processComparisonStats(comparisonStats, pair_string)
    return comparison_obj

def source_objs_to_pair_string(left_obj, right_obj):
    """
    trivial method, but wanted to ensure it was standard
    :param left_obj:
    :param right_obj:
    :return: pair_string
    """
    return '::'.join([left_obj.type, right_obj.type])

def compareSelectChecklists(left_obj, right_obj, report):
    """

    :param left_obj:
    :param right_obj:
    :param report:
    :return:
    """
    ic()
    pair_string = source_objs_to_pair_string(left_obj, right_obj)
    comparisonStats = {pair_string: {'by_package': {}}}

    # ic(left_obj.get_all_package_list())
    # ic(right_obj.get_all_package_list())

    targets = ["AIR"]
    for target in targets:
        ic(target)
        target_lower = target.lower()
        # for target in left_obj.get_all_package_list():
        left_res = [i for i in left_obj.get_all_package_list() if target_lower in i.lower()]
        ic(left_res)

        right_res = [i for i in right_obj.get_all_package_list() if target_lower in i.lower()]
        # ic(mixs_v6_res)

        # get the first off the list
        if len(left_res) > 0 and len(right_res) > 0:
            test_left_name = ' '.join([left_res[0]])
            test_right_name = ' '.join([right_res[0]])
            print(f"test_left_name={test_left_name} test_right_name={test_right_name}")
        else:
            ic(f"ERROR: no matching checklists found in at least one of {left_obj.type} or {right_obj.type}")
            continue
        ic("==================================================================" + "\n")

        compare2packages(pair_string, test_left_name, test_right_name, left_obj, right_obj,
                         comparisonStats, report)
    # other tests
    compare2packages(pair_string, 'GSC MIxS human skin', 'Human-skin', left_obj, right_obj,
                     comparisonStats, report)

    compare2packages(pair_string, 'GSC MIxS soil', 'Soil', left_obj, right_obj,
                     comparisonStats, report)

    compare2packages(pair_string, 'GSC MIxS soil', 'Core', left_obj, right_obj,
                     comparisonStats, report)

def do_textWordCloud(df, title):
    # in pycharm WordCloud not installing, although installed via pip3
    # import WordCloud
    # # doing wordcloud for the text
    # text_freq_dict = df.to_dict()
    # ic()
    # ic(text_freq_dict)
    #
    # wordcloud = WordCloud(min_word_length = 3, width = 1200, height = 1000,
    #                       background_color = 'white')
    # wordcloud.generate_from_frequencies(frequencies = text_freq_dict['frequency'])
    # plt.imshow(wordcloud, interpolation = 'bilinear')
    # plt.axis('off')
    # plt.title(title)
    # # plt.rcParams['figure.figsize'] = [15, 15]  # for square canvas
    # # plt.rcParams['figure.subplot.left'] = 0
    # plt.rcParams['figure.subplot.bottom'] = 0
    # plt.rcParams['figure.subplot.right'] = 1
    # plt.rcParams['figure.subplot.top'] = 1
    # # plt.show()
    # plt.savefig(image_dir + "mixsv6_wordcloud.png")
    pass

def create_pairwise_confidence_summary(pairwise_obj):
        """
        called from do_pairwise_term_matches
        :param pairwise_obj:
        :return:
        """

        left_obj = pairwise_obj.left_obj
        right_obj = pairwise_obj.right_obj
        # ic(pairwise_matches)
        ic(len(pairwise_obj.left_term_list))
        ic(len(pairwise_obj.left_exact_matched_set))
        ic(len(pairwise_obj.left_harmonised_matched_set))
        ic(len(pairwise_obj.left_not_matched_set))

        ic(len(pairwise_obj.right_term_list))
        ic(len(pairwise_obj.right_exact_matched_set))
        ic(len(pairwise_obj.right_harmonised_matched_set))
        ic(len(pairwise_obj.right_not_matched_set))
        complete_matches_df = pairwise_obj.get_complete_matches_df()
        ic(len(complete_matches_df))
        pairwise_obj.get_harmonised_and_exact_match_df()
        pairwise_obj.get_vlow_confidence_mapping_match_df()

        summary_dict = {}
        cumulative_left_total = len(pairwise_obj.left_exact_matched_set)
        summary_dict['exact'] = [left_obj.type, right_obj.type, len(pairwise_obj.left_exact_matched_set),\
            len(pairwise_obj.left_term_list), len(pairwise_obj.right_exact_matched_set),\
                                 len(pairwise_obj.right_term_list), cumulative_left_total, ""]
        cumulative_left_total += len(pairwise_obj.left_high_confident_matched_list)
        summary_dict['high_confident_matched'] = [left_obj.type, right_obj.type, len(pairwise_obj.left_high_confident_matched_list),\
                                 len(pairwise_obj.left_term_list), len(set(pairwise_obj.right_high_confident_matched_list)),\
                                 len(pairwise_obj.right_term_list), cumulative_left_total, ""]
        cumulative_left_total += len(pairwise_obj.left_medium_confident_matched_list)
        summary_dict['medium_confident_matched'] = [left_obj.type, right_obj.type, len(pairwise_obj.left_medium_confident_matched_list ), \
                                 len(pairwise_obj.left_term_list), len(set(pairwise_obj.right_medium_confident_matched_list)),\
                                 len(pairwise_obj.right_term_list), cumulative_left_total, ""]
        cumulative_left_total += len(pairwise_obj.left_low_confident_matched_list)
        summary_dict['low_confident_matched'] = [left_obj.type, right_obj.type, len(set(pairwise_obj.left_low_confident_matched_list)), \
                                 len(pairwise_obj.left_term_list),  len(set(pairwise_obj.right_low_confident_matched_list)),\
                                 len(pairwise_obj.right_term_list), cumulative_left_total, ""]
        cumulative_left_total += len(pairwise_obj.left_vlow_confident_matched_list)
        summary_dict['vlow_confident_matched'] = [left_obj.type, right_obj.type, len(set(pairwise_obj.left_vlow_confident_matched_list)), \
                                 len(pairwise_obj.left_term_list), len(set(pairwise_obj.right_vlow_confident_matched_list)),\
                                 len(pairwise_obj.right_term_list), cumulative_left_total, ""]
        cumulative_left_total += len(pairwise_obj.left_not_matched_set)
        summary_dict['not_matched'] = [left_obj.type, right_obj.type, len(pairwise_obj.left_not_matched_set),\
                                 len(pairwise_obj.left_term_list), len(pairwise_obj.right_not_matched_set),\
                                 len(pairwise_obj.right_term_list), cumulative_left_total, ""]
        summary_df = pd.DataFrame.from_dict(summary_dict, orient = 'index',
                                            columns = ['left_source', 'right_source', 'left_count', 'left_total',
                                                       'right_count', 'right_total', 'cumulative_left', 'comment'])
        # ic(summary_dict)
        ic(summary_df)
        return summary_df

def do_matching_and_summarisation(pair_string, left_term_list, right_term_list, left_obj, right_obj):
    """

    :param pair_string:
    :param left_term_list:
    :param right_term_list:
    :param left_obj:
    :param right_obj:
    :return: summary_df, pairwise_obj
    """
    pairwise_obj = pairwise_term_matches(pair_string, left_term_list, right_term_list)
    pairwise_obj.put_right_obj(right_obj)
    pairwise_obj.put_left_obj(left_obj)
    summary_df = create_pairwise_confidence_summary(pairwise_obj)
    all_pairwise_df = pairwise_obj.get_complete_matches_df()
    all_pairwise_df = pairwise_obj.assess_likely_map_accuracy(all_pairwise_df)
    outfile = docs_dir + "all_terms_matches_" + pair_string + ".tsv"
    all_pairwise_df.to_csv(outfile, sep="\t", index = False)
    ic(outfile)
    return summary_df, pairwise_obj

def do_pairwise_term_matches(pair_string, left_term_list, right_term_list, left_obj, right_obj, report):
    """
    making use of sets as sets don't allow duplicates
    :param pair_string:  # left_list_name '::' right_list_name
    :param left_term_list:
    :param right_term_list:
    :param right_obj:
    :param report:
    :return: pairwise_obj:
    """
    ic()
    ic(pair_string)
    # grep '#' report.md | sed 's/[#]* //'  | awk -F"," '{print "["$1"](#"$1")" }' | cat -n | tr '\t' ' ' | sed 's/^[ ]*//'
    report.write("## Table of Contents\n")
    toc = """
1 Review of the MIX-S checklists proposed by GSC  
2 Summary of Matches  
3 Exact Matches  
4 mixs_v6Terms without exact matches  
5 Frequency  
6 Harmonised Matches  
           """
    toc.replace("\n","\n")
    report.write(f"\n{toc}\n\n")

    # ic(left_term_list)
    # ic(right_term_list)
    summary_df, pairwise_obj = do_matching_and_summarisation(pair_string, left_term_list, right_term_list, left_obj, right_obj)

    report.write(f'\n\n## Summary of Matches <a name="ReviewoftheMIX-SchecklistsproposedbyGSC"></a>\n')
    report.write(summary_df.to_markdown(index = True))
    left_total = len(pairwise_obj.left_exact_matched_set) + len(pairwise_obj.left_not_matched_set) + \
                  len(pairwise_obj.left_high_confident_matched_list) + len(pairwise_obj.left_medium_confident_matched_list) + \
                  len(pairwise_obj.left_low_confident_matched_list) + len(set(pairwise_obj.left_vlow_confident_matched_list))
    ic(f"left sum: {left_total} out of { len(set(pairwise_obj.left_term_list))} terms are being captured")
    report.write(f"\nleft sum: {left_total} out of { len(set(pairwise_obj.left_term_list))}  \n")
    left_total_to_map = len(set(pairwise_obj.left_term_list)) - len(pairwise_obj.left_exact_matched_set)
    report.write(f"\nMaximal total of mappings(changes to make) without adding new terms to ENA: {left_total_to_map}  out of { len(set(pairwise_obj.left_term_list))}\n")

    right_total = len(pairwise_obj.right_exact_matched_set) + len(pairwise_obj.right_not_matched_set) + \
                 len(set(pairwise_obj.right_high_confident_matched_list)) + len(
        set(pairwise_obj.right_medium_confident_matched_list)) + \
                 len(set(pairwise_obj.right_low_confident_matched_list)) + len(
        set(pairwise_obj.right_vlow_confident_matched_list))
    ic(f"right sum: {right_total} out of {len(pairwise_obj.right_term_list)}, expecting a higher than total score as often an many to 1 match of terms in MIXS match")
    report.write(f"right sum: {right_total} out of {len(pairwise_obj.right_term_list)} terms are being captured, expecting a higher than total score as often an many to 1 match of terms in MIXS match\n")

    right_total_to_map = len(set(pairwise_obj.right_term_list)) - len(pairwise_obj.left_exact_matched_set)
    report.write(
        f"\nMaximal total of mappings(changes to make) without adding new terms to ENA: {right_total_to_map}  out of {len(set(pairwise_obj.right_term_list))}\n")

    report.write(f"\n\n## Different types of Non-exact matches\n <BR>")
    report.write(f"\n\n### High confidence matches\n<BR> This is mainly simple format differences, a no brainer to change?\n <BR>")
    report.write(f"ENA count={len(pairwise_obj.left_high_confident_matched_list)}\n <BR>")
    report.write(f"ENA: {pairwise_obj.left_high_confident_matched_list}\n <BR>")
    report.write(f"MIXS: {pairwise_obj.right_high_confident_matched_list}\n <BR>")
    report.write( f"\n\n### Medium confidence matches\n These are probably minor differences, a no brainer to change?\n <BR>")
    report.write(f"ENA count={len(pairwise_obj.left_medium_confident_matched_list)}\n <BR>")
    report.write(f"ENA: {pairwise_obj.left_medium_confident_matched_list}\n <BR>")
    report.write(f"MIXS: {pairwise_obj.right_medium_confident_matched_list}\n <BR>")
    report.write(f"\n\n### Low confidence matches\n These are higher risk, will need checking to change\n <BR>")
    report.write(f"ENA count= {len(pairwise_obj.left_low_confident_matched_list)}\n <BR>")
    report.write(f"ENA: {pairwise_obj.left_low_confident_matched_list}\n <BR>")
    report.write(f"MIXS: {pairwise_obj.right_low_confident_matched_list}\n <BR>")

    report.write('\n\n## Exact Matches of ENA <a name="ExactMatches"></a>\n')
    report.write(', '.join(list(pairwise_obj.left_exact_matched_set)))
    # ic(right_obj.type)

    report.write('\n\n[Spreadsheets for having all matches and none ENA vs MIXS5 and vice versa](https://docs.google.com/spreadsheets/d/1fYgle5VqF36F2AZXaCfAklzEs_vLPPyLWkcroymaojU/edit?usp=sharing)\n\n')

    report.write(f'\n\n## {pairwise_obj.right_name}Terms without exact matches, these are the most frequent <a name="mixs_v6Termswithoutexactmatches"></a>\n')
    # ic(mixs_v6_obj.get_terms_by_freq())
    right_all_match_freq = right_obj.get_terms_with_freq()

    right_no_match_freq = pairwise_obj.get_right_no_match_freq_dict()

    #ic(right_no_match_freq["by_term"])


    df = pd.DataFrame.from_dict(right_no_match_freq["by_term"], orient = 'index', columns = ["frequency"])
    df["term"] = df.index
    df = df.sort_values("frequency", ascending = False)
    df = df[["term", "frequency"]]
    # report.write(df.head(100).to_string(justify = 'left', index = False))
    report.write('\n\n### Table of Frequency on unexact GSC MIXS terms<a name="Frequency"></a>\n')
    report.write(df.to_markdown(index = False) + "\n")

    title = f"Terms in {pairwise_obj.right_name} not matching {pairwise_obj.left_name} \
          terms,\n( sized by the number of packages they occur in )"
    # do_textWordCloud(df, title)
    report.write('\n\n## Harmonised Matches <a name="HarmonisedMatches"></a>\n')
    pairwise_df = pairwise_obj.get_harmonised_and_exact_match_df()
    report.write(pairwise_df.to_markdown(index = False) + "\n")

    #pairwise_df = pairwise_obj.get_just_harmonised_df()
    print(pairwise_df.head(10).to_markdown(index = False))
    ic(len(pairwise_df))
    ic("do the mapping the other way around")
    left_name, right_name = pair_string2names(pair_string)
    pair_string = names2pair_string(right_name, left_name)
    other_summary_df, other_pairwise_obj = do_matching_and_summarisation(pair_string,  right_term_list, left_term_list,
                                                             right_obj, left_obj)

    return pairwise_obj


def analyse_term_matches(ena_cl_obj, mixs_v6_obj, report):
    """
    badly named.
    Actually analysing the term frequencies.

    :param ena_cl_obj:
    :param mixs_v6_obj:
    :param report:
    :return:
    """

    def get_df(obj):
        df = pd.DataFrame.from_dict(obj.get_terms_by_freq(), orient = 'index')
        df["term_freq"] = df.index
        df = df.sort_values(by = ["term_freq"], ascending = False)
        df = df[["term_freq", "term_count_with_freq", "terms"]]
        # print(df.head(10).to_string(index=False))
        blankIndex = [''] * len(df)
        df.index = blankIndex
        print(df.head(10))
        return df

    def do_hist(df, source):
        df['term_frequency'] = df.index
        ic(df.head())
        title = "Frequency of terms in the " + source + " Checklist"
        fig = px.histogram(df, x = 'term_freq', y = 'term_count_with_freq', nbins = 50, title = title)
        image_file = image_dir + 'term_frequency_hist_' + source + '.jpg'
        ic(f"writing to {image_file}")
        fig.write_image(image_file)

    pair_string = ena_cl_obj.type + "::" + mixs_v6_obj.type
    pairwise_obj = do_pairwise_term_matches(pair_string, ena_cl_obj.get_all_term_list(), mixs_v6_obj.get_all_term_list(), \
                                            ena_cl_obj, mixs_v6_obj, report)
    ic("just ran do_pairwise_term_matches")
    sys.exit()
    print(f"left_not_matched_set={pairwise_obj.left_not_matched_set}")
    ic(f"right_not_matched_set={pairwise_obj.right_not_matched_set}")
    ic()
    sys.exit()

    ena_df = get_df(ena_cl_obj)
    do_hist(ena_df, 'ENA')

    mixs_v6_df = get_df(mixs_v6_obj)
    do_hist(mixs_v6_df, 'MIXS_v6')




def compareAndReport(left_obj, right_obj, report):
    pair_string = names2pair_string(left_obj.type, right_obj.type)
    pairwise_obj = pairwise_term_matches(pair_string, left_obj.get_all_term_list(), right_obj.get_all_term_list())

    df = pairwise_obj.comparison_df

    report.write("\n" + "## Comparison of " + left_obj.type + " and " + right_obj.type + "\n")
    report.write("\n" + "### Table of all terms and their matches for " + left_obj.type\
                 + " and " + right_obj.type + "\n")
    report.write(pairwise_obj.comparison_df.to_markdown(index = False) + "\n")

    report.write("\n" + "### Basic stats of " + left_obj.type + " and " + right_obj.type + "\n")
    print(pairwise_obj.print_stats())
    report.write("\n" + pairwise_obj.print_stats())

    report.write("\n" + "### Fuzzy matches of " + left_obj.type + " and " + right_obj.type + "\n")
    fuzzy_df = df.query('match_type == "fuzzy"')
    report.write(fuzzy_df.to_markdown(index = False) + "\n")

    report.write("\n" + f"### {left_obj.type} without a match:\n " +\
                  ", ".join(pairwise_obj.get_left_not_matched_list()) + "\n")
    report.write("\n\n" + f"### {right_obj.type} without a match:\n " +\
                  ", ".join(pairwise_obj.get_right_not_matched_list()) + "\n")

def getPackageNameInfo(obj):
    # ic(obj.type)
    # ic(len(obj.get_all_package_list()))
    # #ic(obj.get_all_package_list())
    # ic(obj.get_gsc_packages())
    # ic(obj.get_gsc_packages_mixs_style_nomenclature_list())
    # #ic(obj.get_gsc_package_name_dict())
    # ic(obj.get_not_gsc_packages())
    pass


def compareChecklistsByName(ena_obj, mixs_obj):

    ic("For ena_obj")
    ic(len(ena_obj.get_not_gsc_packages()))
    ic(sorted(ena_obj.get_not_gsc_packages()))

    source_p_n_comp_obj = source_package_name_comparisons(ena_obj.get_gsc_packages_mixs_style_nomenclature_list(), mixs_obj.get_gsc_packages_mixs_style_nomenclature_list())

    ic(f"matching source1 packages seen in source2: {sorted(source_p_n_comp_obj.get_matching_s1_set())}")
    ic(f"Not matching source1 packages not seen in source2: {sorted(source_p_n_comp_obj.get_non_matching_s1_set())}")

    ic(f"source2 matched total {len(source_p_n_comp_obj.get_source2_matched_set())}")
    ic(f"source2 matched {sorted(source_p_n_comp_obj.get_source2_matched_set())}")
    ic(f"source2 not matched total {len(source_p_n_comp_obj.get_source2_not_matched_set())}")
    ic(f"source2 not matched {sorted(source_p_n_comp_obj.get_source2_not_matched_set())}")

    sys.exit()


def do_extra_check(mixs_v6_obj):
    ic()
    extra_mixs_list = ['tot_car', 'sample true vertical depth subsea', 'pooling of DNA extracts (if done)', 'sampling room ID or name', 'organism count qPCR information', 'non_mineral_nutr_regm', 'microbial starter NCBI taxonomy ID', 'texture_meth', 'soil_text_measure', 'previous_land_use_meth', 'samp_salinity', 'sample_collec_method', 'has_numeric_value', 'samp_stor_loc', 'has_unit', 'timepoint', 'time-course duration', 'samp_collec_device', 'single_cell_lysis_prot', 'x_16s_recover', 'host_infra_specific_name', 'tot_n_meth', 'presence of pets or farm animals', 'nitrogen', 'samp_collec_method', 'tot_phos', 'samp_stor_dur', 'single_cell_lysis_appr', 'x_16s_recover_software', 'texture', 'samp_stor_temp', 'soil horizon', 'additional info', 'sample_name', 'salinity_meth', 'sample transport temperature', 'spike in organism', 'microbial_biomass_meth']
        #['air_particulate_matter_concentration', 'host_family_relation', 'has_unit', 'has_numeric_value', 'previous_land_use_meth', 'food distribution point geographic location (city)', 'Food_Product_type', 'geographic location (country and/or sea,region)', 'host of the symbiotic host environemental medium', 'additional info', 'room architectural elements', 'depth (TVDSS) of hydrocarbon resource temperature', 'Hazard Analysis Critical Control Points (HACCP) guide food safety term', 'assembly_quality', 'window open frequency', 'spike in organism', 'time-course duration', 'food product origin geographic location', 'Interagency Food Safety Analytics Collaboration (IFSAC) category', 'depth (TVDSS) of hydrocarbon resource pressure', 'sample_name', 'geographic location (latitude and longitude)', 'food distribution point geographic location', 'fermentation pH', 'organism count qPCR information', 'API gravity', 'microbial starter NCBI taxonomy ID', 'sampling room ID or name', 'Food harvesting process']

    term_dict = mixs_v6_obj.get_term_dict()
    for term in extra_mixs_list:
        print(f"{term}={term_dict[term]['description']}")
        print(f"\n\n--------------------------------------------------------")

def main():
    linkml_mixs_dict = parse_new_linkml()

    report_file = "../docs/report.md"
    report = open(report_file, "w")
    print(report.write("# Review of the MIX-S checklists proposed by GSC\n"))
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)
    my_dict_v6 = get_mixs_dict("my_dict_v6")
    mixs_v6_dict = process_mixs_dict(my_dict_v6, linkml_mixs_dict)
    mixs_v6_obj = mixs(mixs_v6_dict, "mixs_v6", linkml_mixs_dict)

    do_extra_check(mixs_v6_obj)
    sys.exit()

    out_file = '../data/output/v6_term_list.txt'
    with open(out_file, 'w') as f:
        f.write('\n'.join(map(str, mixs_v6_obj.get_all_term_list())))
    ic(f"created {out_file}")
    print (mixs_v6_obj.get_all_term_list())
    # compareChecklistsByName(ena_cl_obj, mixs_v6_obj)


    sys.exit()

    ic("do ena_cl and mix_v6")
    ic(ena_cl_obj.type)
    # comparison_obj = compareChecklists(ena_cl_obj, mixs_v6_obj, report)
    # compareSelectChecklists(ena_cl_obj, mixs_v6_obj, report)

    # print(comparison_obj.comparisonStats)

    analyse_term_matches(ena_cl_obj, mixs_v6_obj, report)

    ic("early exit")
    sys.exit()

    mixs_v5_dict = get_mixs_v5_dict()
    mixs_v5_obj = mixs(mixs_v5_dict, "mixs_v5", linkml_mixs_dict)
    ic(mixs_v5_obj.type)

    ic("do mix_v5 and mix_v6")
    comparison_obj = compareAndReport(mixs_v5_obj, mixs_v6_obj, report)

    mixs_v5_dict = get_mixs_v5_dict()
    mixs_v5_obj = mixs(mixs_v5_dict, "mixs_v5", linkml_mixs_dict)
    # mixs_v5_obj.print_summaries()

    # mixs_v6_obj.print_summaries()

    stats_dict = do_stats(ena_cl_obj, mixs_v5_obj, mixs_v6_obj)
    df = unpack_dict(stats_dict)
    ic(df)

    outfilename = plot_pair_counts_df(df, image_dir)
    print(report.write('## Table of pair_count comparisons'))
    print(report.write('![Table comparisons](' + outfilename + ')\n\n'))
    print(report.write(df.to_markdown(index = False)))

    print(f"closing {report_file}")
    report.close()


if __name__ == '__main__':
    ic()
    main()
