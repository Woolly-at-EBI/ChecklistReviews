#!/usr/bin/env python3
"""Script of 'analyse_mixs.py' is to analyse the mixs

convert to JSON, not quite...
cat o | sed -E "s/: \"/: '/g" | sed -E "s/([A-Za-z])'([A-Za-z])/\1\2/g" |  tr "'" '"'  | sed 's/: nan,/: "",/g'  | head -c 157625


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

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import plotly.express as px
import numpy as np

import plotly.io as pio

pio.renderers.default = "browser"

import plotly.express as px

def get_data():
    """

    :return:
    """
    ic()
    json_file = "../data/v6_mixs.schema.json"
    # cat ../data/mixs.schema.json | sed 's/\\"/"/g;s/\\n/\n/g;s/^"//;s/"$//' | sed 's/\\\\"//g'  | jq
    ic(json_file)
    r_text = '{ "test": "test_val"}'
    if os.path.isfile(json_file):
        ic(f"about to open {json_file}")
        with open(json_file) as f:
            r_json = json.load(f)
            ic(r_json)
    else:
        json_url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/mixs/jsonschema/mixs.schema.json"
        ic(json_url)
        r = requests.get(json_url)
        r_json = r.text
        # r_text = '{ "test": "test_val"}'
        with open(json_file, 'w') as f:
            json.dump(r_json, f, indent = 4)
        ic(f"Created {json_file}")
    return r_json


def get_mixs_dict():
    """

    :return:
    """
    pickle_file = '../data/v6_mixs.schema.json.pickle'

    if not os.path.isfile(pickle_file):
        my_dict = json.loads(get_data())
        with open(pickle_file, 'wb') as handle:
            pickle.dump(my_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)

    if os.path.isfile(pickle_file):
        with open(pickle_file, 'rb') as handle:
            my_dict = pickle.load(handle)
    else:
        print(f"ERROR no {pickle_file}")
        sys.exit()

    return my_dict


def print_MIXS_review_dict_stats(MIXS_review_dict):
    """

    :param MIXS_review_dict:
    :return:
    """
    print(f"Count of top_level MIX-S checklists={len(MIXS_review_dict['by_package'])}")
    for checklist_name in MIXS_review_dict['by_package']:
        print(f"{checklist_name} field_count={MIXS_review_dict['by_package'][checklist_name]['count']}")


def process_dict(my_dict):
    """

    :param my_dict:
    :return:
    """
    # for top in my_dict:
    #     print(top)

    #
    # for top_defs in my_dict["$defs"]:
    #     # ic(top_defs)
    #     pass
    #
    # for agr_defs in my_dict["$defs"]["Agriculture"]:
    #     ic(agr_defs)
    #
    # for agr_prop_defs in my_dict["$defs"]["Agriculture"]["properties"]:
    #     ic(agr_prop_defs)

    MIXS_review_dict = {}
    MIXS_review_dict["by_package"] = {}
    MIXS_review_dict["by_term"] = {}

    for top_def in my_dict["$defs"]:
        # print(top_def)
        printed_top = False
        for second_def in my_dict["$defs"][top_def]:
            if not printed_top and second_def == 'properties':
                MIXS_review_dict["by_package"][top_def] = {}
                MIXS_review_dict["by_package"][top_def]["count"] = 0
                MIXS_review_dict["by_package"][top_def]["field"] = {}

                # print("") #
                # print(top_def, end = ": ")
                printed_top = True
            # print(f"\t{second_def}")
            # print(f"\t\tsub_dict={my_dict['$defs'][top_def][second_def]}")
            # sub_dict = my_dict["$defs"][top_def][second_def]
            # print(f"\t\tsub={sub_dict}")
            if second_def == 'properties':
                # print(f"\t\t{second_def} property_count={len(my_dict['$defs'][top_def][second_def])}", end = " properties: ")
                for third_def in my_dict["$defs"][top_def][second_def]:
                    # print(f"{third_def}", end = ", ")
                    MIXS_review_dict["by_package"][top_def]["field"][third_def] = {}
                    # sys.exit()
                    MIXS_review_dict["by_term"][third_def] = ""
                MIXS_review_dict["by_package"][top_def]["count"] = len(MIXS_review_dict["by_package"][top_def]["field"])
            else:
                pass
    print()
    # ic(MIXS_review_dict)

    # print_MIXS_review_dict_stats(MIXS_review_dict)
    return MIXS_review_dict


def url2file(url):
    url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/mixs/jsonschema/mixs.schema.json"
    ic(url)
    r = requests.get(url)
    r_json = r.text


def process_ena_cl(my_dict):
    """
    function to parse the ena_cl in a similar way to how the mixs versions have been parsed

    :param my_dict:
    :return:
    """
    # print(my_dict)
    # print(my_dict.keys())
    # print(my_dict["CHECKLIST_SET"].keys())
    MIXS_review_dict = {}
    MIXS_review_dict["by_package"] = {}
    MIXS_review_dict["by_term"] = {}

    # print("----------------------------------")
    for checklist in my_dict["CHECKLIST_SET"]["CHECKLIST"]:
        # print(checklist)
        # print(checklist["@accession"])
        # print(checklist["@checklistType"])
        # print(f"name={checklist['DESCRIPTOR']['NAME']} DESCRIPTION={checklist['DESCRIPTOR']['DESCRIPTION']}")
        checklist_name = checklist['DESCRIPTOR']['NAME']
        # ic(checklist_name)
        if not hasattr(MIXS_review_dict["by_package"], checklist_name):
            MIXS_review_dict["by_package"][checklist_name] = {'field': {}}

        for field_group in checklist['DESCRIPTOR']["FIELD_GROUP"]:
            # print(field_group)
            # print(f"\tname={field_group['NAME']} DESCRIPTION={field_group['DESCRIPTION']}")
            for field in field_group["FIELD"]:
                # print(f"\t\tfield={field}")
                # ic(field)
                if field in ["LABEL", "NAME", "DESCRIPTION", "FIELD_TYPE", "MANDATORY", "MULTIPLICITY", "SYNONYM",
                             "UNITS"]:
                    continue
                field_name = field['NAME']
                # ic(field_name)

                if not hasattr(MIXS_review_dict["by_term"], field_name):
                    MIXS_review_dict["by_term"][field_name] = {}
                if not hasattr(MIXS_review_dict["by_package"][checklist_name]['field'], field_name):
                    MIXS_review_dict["by_package"][checklist_name]['field'][field_name] = {}
                # MIXS_review_dict["by_package"][checklist_name][field_name]['name'] = field_name

                description = "no_description"
                if "DESCRIPTION" in field:
                    description = field["DESCRIPTION"]
                else:
                    # print(f"no DESCRIPTION, so using LABEL for {field_name}")
                    if 'LABEL' in field:
                        description = field["LABEL"]
                        # print(f"no description so using label={description}")

                MIXS_review_dict["by_term"][field_name]['DESCRIPTION'] = description
                MIXS_review_dict["by_package"][checklist_name]['field'][field_name]["DESCRIPTION"] = description
                # ic(MIXS_review_dict["by_package"][checklist_name]['field'][field_name])

            # end of for field_group
            # ic(MIXS_review_dict["by_package"])
            # ic(MIXS_review_dict["by_term"])
            # sys.exit()
            for checklist_name in MIXS_review_dict["by_package"]:
                #ic(checklist_name)
                # ic(MIXS_review_dict["by_package"][checklist_name])
                if hasattr(MIXS_review_dict["by_package"][checklist_name], 'field'):
                    MIXS_review_dict["by_package"][checklist_name]['count'] = len(
                        MIXS_review_dict["by_package"][checklist_name]['field'].keys())
                #else:
                #ic("WARNING: package seems to be missing any fields!", checklist_name)

        # print()
        # end of for each checklist
        # sys.exit()
    return MIXS_review_dict


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


class mixs:
    def ingest_ena_cl(self):
        self.my_dict = process_ena_cl(self.my_dict_raw)

    def __init__(self, my_dict, type):
        # type could be  "mixs_v5" or "mixs_v6"
        self.type = type

        if type == "ena_cl":
            print(f"type = {type}")
            self.my_dict_raw = my_dict
            self.ingest_ena_cl()
            # self.cl_details_dict = get_ena_cl_details(self.my_dict_raw)
        else:
            self.my_dict = my_dict

    def get_type(self):
        return self.type

    def get_all_term_list(self):
        my_list = list(self.my_dict['by_term'].keys())
        my_list.sort()
        return my_list

    def get_all_term_count(self):
        return (len(self.my_dict['by_term'].keys()))

    def print_term_summary(self, top):
        """

        :param top: = top # number to print, if "", print all
        :return:
        """
        if top == "":
            print(f"term_count={self.get_all_term_count()}  terms={self.get_all_term_list()}")
        else:
            print(f"term_count={self.get_all_term_count()} first {top} terms={self.get_all_term_list()[0:top]}")

    def get_all_package_list(self):
        my_list = list(self.my_dict['by_package'].keys())
        my_list.sort()
        return my_list

    def get_all_package_count(self):
        return (len(self.my_dict['by_package'].keys()))

    def print_package_summary(self):
        print(f"package_count={self.get_all_package_count()} packages={self.get_all_package_list()}")

    def print_summaries(self):
        self.print_term_summary(10)
        self.print_package_summary()

    # def get_all_checklists(self):
    #     self.cl_details_dict

    def get_term_list_for_package(self, package_cl_name):
        # ic("inside get_term_list_for_package", package_cl_name)
        # ic(self.my_dict['by_package'][package_cl_name])
        return list(self.my_dict['by_package'][package_cl_name]['field'].keys())


def get_ena_dict():
    # curl https://www.ebi.ac.uk/ena/browser/api/xml/ERC000001-ERC000999 | xq >  ENA_checklists.json
    json_file = "../data/ENA/ENA_checklists.json"
    pickle_file = json_file + ".pickle"

    if os.path.isfile(pickle_file):
        with open(pickle_file, 'rb') as handle:
            my_dict = pickle.load(handle)
    elif os.path.isfile(json_file):
        ic(f"about to open {json_file}")
        with open(json_file) as f:
            my_dict = json.load(f)
            # ic(my_dict)
            with open(pickle_file, 'wb') as handle:
                pickle.dump(my_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)
    else:
        print("ERROR: unable to find file: {json_file}")
        print(
            "Run: curl https://www.ebi.ac.uk/ena/browser/api/xml/ERC000001-ERC000999 | xq >  ..data/ENA/ENA_checklists.json")
        sys.exit()

    return my_dict


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


def clean_list(my_list):
    """
    function to do some simple cleaning on textual lists.
    e.g. make lower case and use underscore as the main delimiter.
    :param my_list:
    :return: clean_list
    """
    term_list_clean = list(map(str.lower, my_list))
    term_list_clean = [s.replace(' ', '_') for s in term_list_clean]
    term_list_clean = [s.replace('-', '_') for s in term_list_clean]
    term_list_clean = [s.replace('/', '_') for s in term_list_clean]
    term_list_clean = [s.removesuffix("_") for s in term_list_clean]
    return term_list_clean


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

    print("\n======MIXS v5 verses ENA=========")
    print(f"mixs_v5 term count={mixs_v5_obj.get_all_term_count()}")
    print(f"ena_cl term count={ena_cl_obj.get_all_term_count()}\n")
    various(mixs_v5_obj, ena_cl_obj, stats_dict)

    print("\n======MIXS v6 verses ENA=========")
    print(f"mixs_v6 term count={mixs_v6_obj.get_all_term_count()}")
    print(f" ena_cl term count={ena_cl_obj.get_all_term_count()}\n")
    various(mixs_v6_obj, ena_cl_obj, stats_dict)

    #
    print("\n======MIXS v5 verses v6=========")
    print(f"mixs_v5 term count={mixs_v5_obj.get_all_term_count()}")
    print(f"mixs_v6 term count={mixs_v6_obj.get_all_term_count()}\n")
    various(mixs_v5_obj, mixs_v6_obj, stats_dict)

    print(stats_dict)
    return stats_dict


def unpack(stats_dict):
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
    print(df)
    return df


def plot_df(df, image_dir):
    import plotly.io as pio
    pd.options.plotting.backend = "plotly"
    pio.renderers.default = "browser"
    print(df)

    fig = df.plot.bar(x = "pair", y = "right_pc_matched", color = "match_type", text = "pair",
                      title = "Comparisons of Different Versions of Checklist by Counts of Matching Terms")
    fig.show()
    out_file = image_dir + "matches_table_plot.png"
    fig.write_image(out_file)
    return out_file


def compare2termLists(left_term_list, right_term_list, comparisonStatsPackage):
    """
    does comparison of two term lets, including some simple harmonisation(cleaning)
    The results are going into the relevant part of a dictionary collecting statistics.
    currently much is commented out, as did not want to load up the stats dictionary with excessive terms.
    :param left_term_list:
    :param right_term_list:
    :param comparisonStatsPackage:
    :return:
    """
    # ic("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    clean_left_set = cleanList2set(left_term_list)
    # comparisonStatsPackage['left_term_list'] = clean_left_set
    clean_right_set = cleanList2set(right_term_list)
    # comparisonStatsPackage['right_term_list'] = clean_right_set
    union = clean_right_set.union(clean_left_set)
    # comparisonStatsPackage['union_term_list'] = union

    intersection = clean_right_set.intersection(clean_left_set)
    # comparisonStatsPackage['intersection_term_list'] = intersection
    # ic(intersection)
    left_diff = clean_left_set.difference(clean_right_set)
    # comparisonStatsPackage['left_diff_list'] = left_diff

    # ic(left_diff)
    right_diff = clean_right_set.difference(clean_left_set)
    # ic(right_diff)
    pc_left_of_right = math.floor(
        (len(intersection) * 100) / len(clean_right_set)) / 100  # get it as a 2 dp decimal fraction
    comparisonStatsPackage['pc_left_of_right'] = pc_left_of_right
    # ic(f"{len(clean_left_set)} {len(clean_right_set)} union:{len(union)} intersection:{len(intersection)}  pc_left_of_right:{pc_left_of_right}")
    comparisonStatsPackage['length_left'] = len(clean_left_set)
    comparisonStatsPackage['length_union'] = len(union)
    comparisonStatsPackage['length_intersection'] = len(intersection)
    return comparisonStatsPackage


def compare2packages(comparison, left_package_name, right_package_name, left_obj, right_obj, comparisonStats):
    # ic(comparison)
    com_package_names = left_package_name + "::" + right_package_name
    comparisonStats[comparison]['by_package'][com_package_names] = {}
    comparisonStatsPackage = comparisonStats[comparison]['by_package'][com_package_names]
    compare2termLists(left_obj.get_term_list_for_package(left_package_name),
                      right_obj.get_term_list_for_package(right_package_name), comparisonStatsPackage)
    # ic(ena_cl_obj.get_term_list_for_package(test_ena_cl_name))
    # ic(mixs_v6_obj.get_term_list_for_package(test_mixs_v6_cl_name))

def cleanList2set(term_list):
    clean_term_list = clean_list(term_list)
    return (set(clean_term_list))

def plot_pair_df(df):
    """

    :param df:
    :return:
    """
    #import dash_bio

    #fig = px.scatter(df, x = "pc_left_of_right", y = "length_intersection", color = "short_mixs_v6", size = 'length_left', hover_data = 'pair')
    # fig.show()
    cut_off = 0.2
    title = "Heatmap of Fraction of ENA Checklists Terms in Different MIXS v6 packages"
    subtitle = '<br><sup>The terms are lightly harmonised before matching e.g. lower cased</sup>'
    title += subtitle
    df_pc = df[['pc_left_of_right', 'ena','mixs_v6']]
    # df_pc = df_pc.loc[(df_pc['pc_left_of_right'] >= cut_off)]
    new_df = df_pc.pivot(index='ena', columns='mixs_v6')['pc_left_of_right']
    ic(new_df)
    fig = px.imshow(new_df, color_continuous_scale='Greens', width=2000, height=1000, aspect='auto', title=title)
    fig.update_layout(yaxis=dict(title_text="ENA Checklists",
         tickfont=dict(size=8)),
                      xaxis = dict(title_text = "MIXs v6 Packages",
                                  tickfont = dict(size = 8))
                      )
    fig.update_layout(title_text = title, title_x = 0.5)
    fig.update_xaxes(tickangle = 45)
    fig.update_yaxes(tickangle = 45)
    fig.show()
    fig.write_image("/Users/woollard/projects/ChecklistReviews/docs/ENAvsMIXSv6_heatmap.jpg")


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


    sys.exit()

    # df_pc = df_pc.loc[(df_pc['pc_left_of_right'] < 0.3)]
    # new_df = df_pc.pivot(index='ena', columns='mixs_v6')['pc_left_of_right']
    # ic(new_df)
    # fig = px.imshow(new_df)
    # fig.show()


def processComparisonStats(comparisonStats):
    """ processComparisonStats

    :param comparisonStats:
    :return:
    """

    reorg_dict = []
    comparison_source = 'ena::mixs_v6'
    source_list = comparison_source.split('::')

    for pair in comparisonStats[comparison_source]['by_package']:
        # ic(pair)
        sub_dict = comparisonStats[comparison_source]['by_package'][pair]
        pair_list = pair.split('::')
        sub_dict[source_list[0]] = pair_list[0]
        sub_dict[source_list[1]] = pair_list[1]
        sub_dict['left_source'] = source_list[0]
        sub_dict['right_source'] = source_list[1]
        sub_dict['pair'] = pair
        # ic(sub_dict)
        reorg_dict.append(sub_dict)

    df = pd.DataFrame.from_dict(reorg_dict)
    df['short_ena'] = df['ena'].str.extract(r"([A-Za-z]+ [A-Za-z]+ [A-Za-z]+)")
    df['short_mixs_v6'] = df['mixs_v6'].str.extract(r"([A-Z][a-z]+)")
    ic(df.head(10))



    ic(df['short_ena'].unique())
    ic(df['short_mixs_v6'].unique())
    # ic(df['mixs_v6'].unique())

    # for each ENA checklist, get the maximum length of intersections
    new_df = df[['ena', 'length_intersection']].drop_duplicates()
    ic(new_df.head().to_string(index=False))
    idx = new_df.groupby(['ena'])['length_intersection'].transform(max) == new_df['length_intersection']
    print(new_df[idx].to_string(index = False))

    # for each ENA checklist, get the checklists with >= 20% overlap with at least one GSC MIx
    new_df = df[['ena', 'pc_left_of_right']].drop_duplicates()
    ic(new_df.head().to_string(index=False))
    idx = new_df.groupby(['ena'])['pc_left_of_right'].transform(max) == new_df['pc_left_of_right']

    print("each ENA checklist with >= 20% overlap with at least one GSC MIx")
    tmp_df = new_df[idx].query('pc_left_of_right >= 0.2')
    print(tmp_df.to_string(index = False))
    print(f"{tmp_df['ena'].unique()} \ntotal={len(tmp_df['ena'].unique())}")

    print("each ENA checklist with a maximum < 20% overlap with any GSC MIx")
    tmp_df = new_df[idx].query('pc_left_of_right < 0.2')
    print(tmp_df.to_string(index = False))
    print(f"{tmp_df['ena'].unique()} \ntotal={len(tmp_df['ena'].unique())}")



    sys.exit()
    plot_pair_df(df)


def compareChecklists(ena_cl_obj, mixs_v6_obj):
    """
    Comparing all possible pairs of checklists
    :param ena_cl_obj:
    :param mixs_v6_obj:
    :return:
    """
    comparisonStats = {'ena::mixs_v6': {'by_package': {}}}

    # ic(ena_cl_obj.get_all_package_list())
    # ic(mixs_v6_obj.get_all_package_list())

    count = 0
    for left_package_name in ena_cl_obj.get_all_package_list():
        #ic(left_package_name)
        for right_package_name in mixs_v6_obj.get_all_package_list():
            # if count > 10:
            #     break
            # ic(right_package_name)
            compare2packages('ena::mixs_v6', left_package_name, right_package_name, ena_cl_obj, mixs_v6_obj,
                         comparisonStats)
            count += 1
    # ic(comparisonStats)
    processComparisonStats(comparisonStats)
    sys.exit()
    return comparisonStats




def compareSelectChecklists(ena_cl_obj, mixs_v6_obj):
    comparisonStats = {'ena::mixs_v6': {'by_package': {}}}

    # ic(ena_cl_obj.get_all_package_list())
    # ic(mixs_v6_obj.get_all_package_list())



    targets = ["AIR"]
    for target in targets:
        ic(target)
        target_lower = target.lower()
        # for target in ena_cl_obj.get_all_package_list():
        ena_res = [i for i in ena_cl_obj.get_all_package_list() if target_lower in i.lower()]
        ic(ena_res)

        mixs_v6_res = [i for i in mixs_v6_obj.get_all_package_list() if target_lower in i.lower()]
        ic(mixs_v6_res)

        # get the first off the list
        if len(ena_res) > 0 and len(mixs_v6_res) > 0:
            test_ena_cl_name = ' '.join([ena_res[0]])
            test_mixs_v6_cl_name = ' '.join([mixs_v6_res[0]])
            print(f"test_ena_cl_name={test_ena_cl_name} test_mixs_v6_cl_name={test_mixs_v6_cl_name}")
        else:
            ic("ERROR: no matching checklists found in at least one of ENA or mixs_v6")
            continue
        ic("==================================================================")

        compare2packages('ena::mixs_v6', test_ena_cl_name, test_mixs_v6_cl_name, ena_cl_obj, mixs_v6_obj,
                         comparisonStats)



def main():
    report_file = "../docs/report.md"
    image_dir = "../docs/images/"
    report = open(report_file, "w")
    print(report.write("# Review of the MIX-S checklists proposed by GSC\n"))

    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl")
    # ena_cl_obj.get_all_checklists()
    # ena_cl_obj.print_summaries()

    # get_ena_cl_details(ena_cl_dict)

    my_dict_v6 = get_mixs_dict()
    mixs_v6_dict = process_dict(my_dict_v6)
    mixs_v6_obj = mixs(mixs_v6_dict, "mixs_v6")

    # get_v6_cl_details

    # compareSelectChecklists(ena_cl_obj, mixs_v6_obj)
    compareChecklists(ena_cl_obj, mixs_v6_obj)


    ic("early exit")
    sys.exit()

    mixs_v5_dict = get_mixs_v5_dict()
    mixs_v5_obj = mixs(mixs_v5_dict, "mixs_v5")
    # mixs_v5_obj.print_summaries()

    # mixs_v6_obj.print_summaries()

    stats_dict = do_stats(ena_cl_obj, mixs_v5_obj, mixs_v6_obj)
    df = unpack(stats_dict)

    outfilename = plot_df(df, image_dir)
    print(report.write('![Table comparisons](' + outfilename + ')\n\n'))
    print(report.write(df.to_markdown()))

    print(f"closing {report_file}")
    report.close()


if __name__ == '__main__':
    ic()
    main()
