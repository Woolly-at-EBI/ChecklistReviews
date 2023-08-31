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
from rapidfuzz import process

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pio.renderers.default = "browser"
# from fuzzywuzzy import process


image_dir = "../docs/images/"


def get_data():
    """

    :return:
    """
    ic()
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


def print_mixs_review_dict_stats(mixs_review_dict):
    """

    :param mixs_review_dict:
    :return:
    """
    print(f"Count of top_level MIX-S checklists={len(mixs_review_dict['by_package'])}")
    for checklist_name in mixs_review_dict['by_package']:
        print(f"{checklist_name} field_count={mixs_review_dict['by_package'][checklist_name]['count']}")


def process_mixs_dict(my_dict, linkml_dict):
    """
    /used for mixs5 at least

    :param my_dict:
    :param linkml_dict:
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

    MIXS_review_dict = {"by_package": {}, "by_term": {}}

    def get_long_name(short_term_name, linkml_dict):
        if short_term_name in linkml_dict["slots"]:
            return linkml_dict["slots"][short_term_name]['title']
        return short_term_name

    for top_def in my_dict["$defs"]:
        # print(top_def)
        package_name = top_def
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

                    term_name = get_long_name(third_def, linkml_dict)
                    MIXS_review_dict["by_package"][top_def]["field"][term_name] = {}

                MIXS_review_dict["by_package"][package_name]["count"] = len(
                    MIXS_review_dict["by_package"][package_name]["field"])
            else:
                pass
    # ic(MIXS_review_dict)
    MIXS_review_dict = add_term_package_count(MIXS_review_dict)
    # print_mixs_review_dict_stats(MIXS_review_dict)
    return MIXS_review_dict


def url2file(url):
    # url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/mixs/jsonschema/mixs.schema.json"
    ic(url)
    r = requests.get(url)
    r_json = r.text


def process_ena_cl(my_dict, linkml_mixs_dict):
    """
    function to parse the ena_cl in a similar way to how the mixs versions have been parsed

    :param my_dict:
    :return:
    """
    # print(my_dict)
    # print(my_dict.keys())
    # print(my_dict["CHECKLIST_SET"].keys())
    MIXS_review_dict = {"by_package": {}, "by_term": {}}

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

                if field_name in linkml_mixs_dict['slots']:
                    # ic(linkml_mixs_dict['slots'][field_name])
                    long_field_name = linkml_mixs_dict['slots'][field_name]['title']  # ENA uses the long_field_name
                    # ic(field_name)
                    # ic(long_field_name)
                    # sys.exit()
                else:
                    long_field_name = field_name

                if field_name not in MIXS_review_dict["by_term"]:
                    MIXS_review_dict["by_term"][long_field_name] = {}
                if field_name not in MIXS_review_dict["by_package"][checklist_name]['field']:
                    MIXS_review_dict["by_package"][checklist_name]['field'][long_field_name] = {}
                # MIXS_review_dict["by_package"][checklist_name][field_name]['name'] = field_name

                description = "no_description"
                if "DESCRIPTION" in field:
                    description = field["DESCRIPTION"]
                else:
                    # print(f"no DESCRIPTION, so using LABEL for {field_name}")
                    if 'LABEL' in field:
                        description = field["LABEL"]
                        # print(f"no description so using label={description}")

                MIXS_review_dict["by_term"][long_field_name]['DESCRIPTION'] = description
                MIXS_review_dict["by_package"][checklist_name]['field'][long_field_name]["DESCRIPTION"] = description
                # ic(MIXS_review_dict["by_package"][checklist_name]['field'][field_name])

            # end of for field_group
            # ic(MIXS_review_dict["by_package"])
            # ic(MIXS_review_dict["by_term"])
            # sys.exit()
            for checklist_name in MIXS_review_dict["by_package"]:
                # ic(checklist_name)
                # ic(MIXS_review_dict["by_package"][checklist_name])
                if 'field' in MIXS_review_dict["by_package"][checklist_name]:
                    MIXS_review_dict["by_package"][checklist_name]['count'] = len(
                        MIXS_review_dict["by_package"][checklist_name]['field'].keys())
                # else:
                # ic("WARNING: package seems to be missing any fields!", checklist_name)

        # print()
        # end of for each checklist
        # sys.exit()

    MIXS_review_dict = add_term_package_count(MIXS_review_dict)

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
        self.my_dict = process_ena_cl(self.my_dict_raw, self.linkml_mixs_dict)

    def __init__(self, my_dict, type, linkml_mixs_dict):
        # type could be  "mixs_v5" or "mixs_v6"
        self.type = type

        if type == "ena_cl":
            print(f"type = {type}")
            self.my_dict_raw = my_dict
            self.linkml_mixs_dict = linkml_mixs_dict
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

    def get_terms_with_freq(self):
        """
                :return:  {'Food_Product_type': 12,
                                        'Food_source': 12,
                                        'HACCP_term': 36,
        """
        self.get_terms_by_freq()
        return self.term_with_freq

    def get_terms_by_freq(self):
        """

        :return:  40: {'term_count_with_freq': 2,
                        'terms': dict_keys(['collection date', 'geographic location (country and/or sea)'])}}
        """
        ic()
        if hasattr(self, 'my_just_freq'):
            return self.my_just_freq

        my_just_freq = {}
        if "by_term_count" not in self.my_dict:
            add_term_package_count(self.my_dict)

        self.term_with_freq = {}

        freq_keys = sorted(self.my_dict["by_term_count"].keys(), reverse = True)
        # ic("KEYS=+++++++++++++++++++++++++")
        # ic(freq_keys)
        # ic(self.my_dict["by_term_count"][40].keys())
        for freq_key in freq_keys:
            my_just_freq[freq_key] = {}
            my_just_freq[freq_key]["terms"] = list(self.my_dict["by_term_count"][freq_key].keys())
            my_just_freq[freq_key]["term_count_with_freq"] = len(my_just_freq[freq_key]["terms"])
            for term in my_just_freq[freq_key]["terms"]:
                self.term_with_freq[term] = freq_key
        # ic(my_just_freq)
        # sys.exit()

        self.my_just_freq = my_just_freq
        return self.my_just_freq

        #
        #
        # total_count =0
        # # my_dict["by_term_count"]
        # ic(self.my_dict["by_term_count"].keys())
        # ic(self.my_dict["by_term_count"])
        #
        # return (self.my_dict["by_term_count"])

    def get_term_top(self, first_number):
        """
        get_term_top - get the first 10, or whatever in terms of frequency
        :param first_number:
        :return:
        """
        my_just_freq = self.get_terms_by_freq()
        total_found_so_far = 0
        top_terms = []
        for freq_key in my_just_freq:
            ic(my_just_freq[freq_key]["terms"])
            top_terms.extend(list(my_just_freq[freq_key]["terms"]))
            if len(top_terms) >= first_number:
                return top_terms[0:first_number - 1]
        return top_terms

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


# **********************************************************************************

class COMPARISONS:
    """ not yet a proper or even rich object...
        if more development, need to improve this.
        (still it served a purpose and broke up an excessively long routine)
    """

    def __init__(self, comparisonStats, comparison_source):
        ic()
        ic(comparison_source)
        self.source_list = []
        self.source_list = comparison_source.split('::')
        self.comparisonStats = comparisonStats
        ic("---------------------------")
        self.ingest()

    def left_source(self):
        return self.source_list[0]

    def right_source(self):
        return self.source_list[1]

    def put_reorg_df(self, df):
        self.reorg_df = df
        self.reorg_df['short_ena'] = df['ena'].str.extract(r"([A-Za-z]+ [A-Za-z]+ [A-Za-z]+)")
        self.reorg_df['short_mixs_v6'] = df['mixs_v6'].str.extract(r"([A-Z][a-z]+)")

    def process_max_intersection_len(self):
        """

        :return:
        """
        # for each ENA checklist, get the maximum length of intersections
        # sources = source_list  # ['ena', 'mixs_v6']
        for source in self.source_list:
            ic(source)
            if source == 'ena':
                target_cols = [source, 'length_clean_intersection']
            else:
                target_cols = [source, 'length_clean_intersection', 'short_mixs_v6']
            new_df = self.reorg_df[target_cols].drop_duplicates()
            ic(new_df.head().to_string(index=False))

            # for each ENA or Mixs checklist, get the checklists with >= 20% overlap with at least one GSC MIx
            new_df = self.reorg_df
            target_cols = [source]
            if source == 'short_mixs_v6':
                target_cols.append('short_mixs_v6')
            alltarget_cols = target_cols
            alltarget_cols.append('pc_left_of_right')

            max_df = new_df[alltarget_cols].groupby(target_cols).max().reset_index()
            # print(max_df.to_string(index = False))

            if source == 'mixs_v6':
                mixs6_matches_plots(self.reorg_df, new_df)
            print(f"each {source} checklist with >= 20% overlap with at least one GSC MIx")
            tmp_df = max_df.query('pc_left_of_right >= 0.2')
            # print(tmp_df.to_string(index = False))
            # print(f"{tmp_df[source].unique()} \ntotal={len(tmp_df[source].unique())}")
            print("each {source} checklist with a maximum < 20% overlap with any GSC MIx")
            tmp_df = max_df.query('pc_left_of_right < 0.2')
            # print(tmp_df.to_string(index = False))
            # print(f"{tmp_df[source].unique()} \ntotal={len(tmp_df[source].unique())}")
            # end of process_max_intersection_len

    def ingest(self):
        # ic("start of ingest================================================"+ "\n")
        # ic()
        reorg_dict = { self.left_source(): [], self.right_source(): [], "left_source": [], "right_source": [], "pair": []}
        sub_dict_elements = ['length_clean_intersection', 'pc_left_of_right']
        for element in sub_dict_elements:
            reorg_dict[element] = []
        comparison_source = 'ena::mixs_v6'
        comparisonStats = self.comparisonStats
        # ic(comparisonStats)
        count =0

        if comparison_source not in comparisonStats:
            ic(f"ERROR {comparison_source} not in comparisonStats")
            ic(comparisonStats)
            sys.exit()
        #else:
        #    ic(f"{comparison_source} is in comparisonStats")

        for pair in comparisonStats[comparison_source]['by_package']:
            # ic(pair)
            pair_list = pair.split('::')
            # ic(pair_list)

            # ic(comparisonStats[comparison_source]['by_package'][pair])
            sub_dict = comparisonStats[comparison_source]['by_package'][pair]
            # ic(sub_dict)
            reorg_dict[self.left_source()].append(pair_list[0])
            reorg_dict[self.right_source()].append(pair_list[1])
            reorg_dict['left_source'].append(self.left_source())
            reorg_dict['right_source'].append(self.right_source())
            reorg_dict['pair'].append(pair)
            for element in sub_dict_elements:
                # ic(sub_dict[element])
                reorg_dict[element].append(sub_dict[element])
            if count > 3:
                break
            else:
                count += 1
        #ic(reorg_dict)
        self.put_reorg_df(pd.DataFrame.from_dict(reorg_dict))
        df = self.reorg_df
        ic(df.head(5))
        # ic(df['short_ena'].unique())
        # ic(df['short_mixs_v6'].unique())
        self.process_max_intersection_len()
        # ic("-------end of ingest------")
        #sys.exit()


# **********************************************************************************

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


def generate_clean_dict(my_list):
    """
    re-uses the clean_list to keep it consistent
    :param my_list:
    :return: clean_dict, raw_dict
    a hash of clean term as the index, and original term as the value and vice versa
    """
    my_clean_list = clean_list(my_list)
    clean_dict = {}
    raw_dict = {}
    pos = 0
    for clean_term in my_clean_list:
        clean_dict[clean_term] = my_list[pos]
        raw_dict[my_list[pos]] = clean_term
        pos += 1
    # print(clean_dict)
    # print(raw_dict)
    return clean_dict, raw_dict


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
                      title = "Comparisons of Different Versions of Checklist by Counts of Matching Terms", barmode="group")
    # fig.show()
    out_file = image_dir + "matches_table_plot.png"
    fig.write_image(out_file)
    #sys.exit()
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
        fuzzy = True

        comparisonStatsPackage = {}
        package_comparisonStatsPackage = compare2termLists(left_obj.get_term_list_for_package(left_package_name),
                                                           right_obj.get_term_list_for_package(right_package_name),
                                                           comparisonStatsPackage)
        core_comparisonStatsPackage = compare2termLists(left_obj.get_term_list_for_package(left_package_name),
                                                        right_obj.get_term_list_for_package("Core"),
                                                        comparisonStatsPackage)

        my_dict = {}
        left_list = sorted(left_obj.get_term_list_for_package(left_package_name))
        left_clean_dict, left_raw_dict = generate_clean_dict(left_list)
        right_term_list = right_obj.get_term_list_for_package(right_package_name)
        right_clean_dict, right_raw_dict = generate_clean_dict(right_term_list)
        core_term_list = right_obj.get_term_list_for_package("Core")
        core_clean_dict, core_raw_dict = generate_clean_dict(core_term_list)
        # ic(right_term_list)
        combined_right_term_list = (right_term_list)
        combined_right_term_list.extend(core_term_list)
        fuzzy_threshold = 85
        for left_term in left_list:
            my_dict[left_term] = {"match_type": "none", "fuzzy_score": 100}
            left_clean = left_raw_dict[left_term]
            # print(f"{left_term} - {left_clean}")
            if left_clean in package_comparisonStatsPackage["intersection_set"] or left_clean in \
                    package_comparisonStatsPackage["clean_intersection_set"]:
                if left_term in right_term_list:
                    my_dict[left_term]["match_type"] = "exact"
                    my_dict[left_term]["match"] = right_clean_dict[left_clean]
                elif left_clean in package_comparisonStatsPackage["clean_intersection_set"]:
                    my_dict[left_term]["match_type"] = "harmonised"
                    my_dict[left_term]["match"] = right_clean_dict[left_clean]
            elif left_term in core_comparisonStatsPackage["intersection_set"] or left_clean in \
                    core_comparisonStatsPackage["clean_intersection_set"]:
                if left_term in core_term_list:
                    my_dict[left_term]["match_type"] = "exact"
                    my_dict[left_term]["match"] = core_clean_dict[left_clean]
                elif left_clean in core_comparisonStatsPackage["clean_intersection_set"]:
                    my_dict[left_term]["match_type"] = "harmonised"
                    my_dict[left_term]["match"] = core_clean_dict[left_clean]
            if my_dict[left_term]["match_type"] == "none":
                # searches combined list as want the highest scoring!
                resp_match = process.extractOne(left_term, combined_right_term_list)
                if resp_match[1] > fuzzy_threshold:
                    my_dict[left_term]["match_type"] = "fuzzy"
                    my_dict[left_term]["fuzzy_score"] = resp_match[1]
                    my_dict[left_term]["match"] = resp_match[0]
                else:
                    my_dict[left_term]["fuzzy_score"] = 0

        df = pd.DataFrame.from_dict(my_dict, orient = 'index')
        df["left_term"] = df.index
        df = df[["left_term", "match_type", "match", "fuzzy_score"]]
        df["fuzzy_score"] = df["fuzzy_score"].astype(int)

        return df

    #main stream compare2packages aspects
    # building  comparisonStats[comparison]['by_package'][com_package_names]  = {}
    #ic(comparison)
    com_package_names = left_package_name + "::" + right_package_name
    # ic(com_package_names)
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
    # sys.exit()
    # report.write("### ====" + left_obj.type + "====" + "\n")
    # report.write(', '.join(left_obj.get_term_list_for_package(left_package_name))+ "\n")
    # report.write("### ====" + right_obj.type + "====" + "\n")
    # report.write(', '.join(right_obj.get_term_list_for_package(right_package_name)) + "\n")
    print_minimal_stats(comparisonStatsPackage, report)
    # report.write(f"Intersection = {comparisonStatsPackage['clean_intersection_set']}"+ "\n")
    # report.write("### ====" + right_obj.type + " Core" + "====" + "\n")
    # report.write(', '.join(right_obj.get_term_list_for_package("Core"))+ "\n")
    comparisonStatsPackage = comparisonStats[comparison]['by_package'][com_package_names]
    comparisonStatsPackage = compare2termLists(left_obj.get_term_list_for_package(left_package_name),
                                               right_obj.get_term_list_for_package("Core"), comparisonStatsPackage)
    report.write(f"Intersection = {comparisonStatsPackage['clean_intersection_set']}" + "\n")

    term_comparison_df = create_term_comparison_df(left_obj, right_obj, left_package_name, right_package_name, report)
    # report.write(term_comparison_df.to_string(justify = 'left', index = False))
    # report.write(f"right_diff={', '.join(sorted(comparisonStatsPackage['right_diff_set']))}" + "\n")
    # ic(comparisonStatsPackage)

    #ic("about to exit compare2packages")
    return comparisonStatsPackage


def cleanList2set(term_list):
    clean_term_list = clean_list(term_list)
    return (set(clean_term_list))


def plot_pair_df(df):
    """

    :param df:
    :return:
    """
    # import dash_bio

    #fig = px.scatter(df, x = "pc_left_of_right", y = "length_intersection", color = "short_mixs_v6", size = 'length_left', hover_data = 'pair')
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
    new_df = df_pc.pivot(index='ena', columns='mixs_v6')['pc_left_of_right']
    # ic(new_df)
    image_file = image_dir + "ena_checklist_match_heatmap.jpg"
    fig = px.imshow(new_df)
    ic(image_file)
    fig.write_image(image_file)
    # fig.show()
    #sys.exit()


def mixs6_matches_plots(df, new_df):
    """
    :param df:
    :param new_df:
    :return:
    """

    # print(max_df.head(20).to_string(index = False))
    # print("max")
    max_df = new_df[['short_mixs_v6', 'pc_left_of_right']].groupby('short_mixs_v6').max().reset_index().sort_values(
        by = 'pc_left_of_right')
    max_df.rename(columns = {"pc_left_of_right": "maxPC_intersection"}, inplace = True)
    # print(max_df.head(20).to_string(index = False))
    # print("average(mean)")
    mean_pc_df = new_df[['short_mixs_v6', 'pc_left_of_right']].groupby(
        'short_mixs_v6').mean().reset_index().sort_values(by = 'pc_left_of_right')  # average().reset_index()
    mean_pc_df.rename(columns = {"pc_left_of_right": "MeanPC_intersection"}, inplace = True)
    # print(mean_pc_df.head(20).to_string(index = False))
    mean_ints_df = df[['short_mixs_v6', 'length_clean_intersection']].groupby(
        'short_mixs_v6').mean().reset_index().sort_values(by = 'length_clean_intersection')  # average().reset_index()
    mean_ints_df.rename(columns = {"length_clean_intersection": "MeanLen_intersection"}, inplace = True)
    # print(mean_ints_df.head(20).to_string(index = False))
    # print("Count of rows")
    tmp_df = df[['mixs_v6', 'short_mixs_v6']].drop_duplicates()
    package_count_df = tmp_df.groupby('short_mixs_v6').count().reset_index()
    package_count_df.rename(columns = {"mixs_v6": "package_count"}, inplace = True)
    # print(package_count_df.head(20).to_string(index = False))
    stats_df = max_df.merge(mean_pc_df, on = 'short_mixs_v6').merge(package_count_df, on = 'short_mixs_v6')

    title = "Statistics of the MIXS v6 packages with matches from the ENA checklists"
    print(title)
    title += "<BR><sub>size=packages count for each collection</sub>"

    stats_df["maxPC_intersection"] = stats_df["maxPC_intersection"] * 100
    stats_df = stats_df.astype({'maxPC_intersection': 'int'})

    stats_df["MeanPC_intersection"] = stats_df["MeanPC_intersection"] * 100
    print(stats_df.head(20).to_string(index = False))
    fig = px.scatter(stats_df, title = title, x = 'maxPC_intersection', y = 'MeanPC_intersection',
                     size = 'package_count',
                     color = 'package_count', text = 'short_mixs_v6',
                     color_continuous_scale = px.colors.sequential.Viridis)
    fig.update_traces(textposition = 'top center')
    # fig.show()
    fig.write_image("/Users/woollard/projects/ChecklistReviews/docs/ENAvsMIXSv6_ScatterPlot.jpg")


def processComparisonStats(comparisonStats, pair):
    """ processComparisonStats

    :param comparisonStats:
    :return: comparison_obj
    """
    ic("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    ic()
    ic(pair)
    comparison_obj = COMPARISONS(comparisonStats, pair)
    return comparison_obj


def compareChecklists(ena_cl_obj, mixs_v6_obj, report):
    """
    Comparing all possible pairs of checklists
    :param ena_cl_obj:
    :param mixs_v6_obj:
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
    pair_string = 'ena::mixs_v6'
    comparisonStats = {pair_string: {'by_package': {}}}

    #ic(ena_cl_obj.get_all_package_list())
    #ic(mixs_v6_obj.get_all_package_list())
    ic(len(ena_cl_obj.get_all_package_list()))
    left_package_count = 0
    count = 0
    for left_package_name in ena_cl_obj.get_all_package_list():

        ic(str(left_package_count) + "\t" + left_package_name)
        left_package_count += 1
        if left_package_count > 10:
            break

        for right_package_name in mixs_v6_obj.get_all_package_list():
            # PMW
            com_package_names = '::'.join([left_package_name, right_package_name])
            # ic(right_package_name)
            comparisonStats[pair_string]['by_package'][com_package_names] = compare2packages(pair_string, left_package_name, right_package_name, ena_cl_obj, mixs_v6_obj,
                             comparisonStats, report)

            count += 1
    # ic(comparisonStats)
    # ic()
    # sys.exit()
    comparison_obj = processComparisonStats(comparisonStats, pair_string)

    return comparison_obj


def compareSelectChecklists(ena_cl_obj, mixs_v6_obj, report):
    """

    :param ena_cl_obj:
    :param mixs_v6_obj:
    :param report:
    :return:
    """
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
        # ic(mixs_v6_res)

        # get the first off the list
        if len(ena_res) > 0 and len(mixs_v6_res) > 0:
            test_ena_cl_name = ' '.join([ena_res[0]])
            test_mixs_v6_cl_name = ' '.join([mixs_v6_res[0]])
            print(f"test_ena_cl_name={test_ena_cl_name} test_mixs_v6_cl_name={test_mixs_v6_cl_name}")
        else:
            ic("ERROR: no matching checklists found in at least one of ENA or mixs_v6")
            continue
        ic("==================================================================" + "\n")

        compare2packages('ena::mixs_v6', test_ena_cl_name, test_mixs_v6_cl_name, ena_cl_obj, mixs_v6_obj,
                         comparisonStats, report)
    # other tests
    compare2packages('ena::mixs_v6', 'GSC MIxS human skin', 'Human-skin', ena_cl_obj, mixs_v6_obj,
                     comparisonStats, report)

    compare2packages('ena::mixs_v6', 'GSC MIxS soil', 'Soil', ena_cl_obj, mixs_v6_obj,
                     comparisonStats, report)

    compare2packages('ena::mixs_v6', 'GSC MIxS soil', 'Core', ena_cl_obj, mixs_v6_obj,
                     comparisonStats, report)


def clean_term(term):
    # ic(term)
    clean = term.lower().replace(' ', '_').replace('-', '_').replace('/', '_').removesuffix("_")
    return clean


class pairwise_term_matches:
    """pairwise_term_matches object as simple object orientated to reduce complexity and saves passing a big hash.

    """

    def process_names(self, pair_string):
        self.pair_string = pair_string
        ic(pair_string)
        pair_source = pair_string.split('::')
        self.left_name = pair_source[0]
        self.right_name = pair_source[1]

    def __init__(self, pair_string, left_term_list, right_term_list):
        self.process_names(pair_string)

        self.left_term_list = left_term_list
        self.right_term_list = right_term_list
        clean_hash = self.get_clean_hash()

        pairwise_matches = {'left': {"exact": {}, "harmonised": {}, "no_matches": {}}, 'right': {"no_matches": {}}}
        self.pairwise_matches = pairwise_matches
        left_pairwise_matches = pairwise_matches["left"]
        right_pairwise_matches = pairwise_matches["right"]
        self.right_exact_matched_set = set()
        self.left_exact_matched_set = set()
        self.right_harmonised_matched_set = set()
        self.left_harmonised_matched_set = set()
        self.right_not_matched_set = set()
        self.left_not_matched_set = set()

        for left in left_term_list:
            exact_matches_found = False
            harmonised_matches_found = False
            left_pairwise_matches["exact"][left] = {}
            left_pairwise_matches["harmonised"][left] = {}
            first_right_harmonised = ""
            local_right_harmonised_list = []
            right_count = 0
            for right in right_term_list:
                right_match_found = False
                right_count += 1
                if left == right:
                    left_pairwise_matches["exact"][left][right] = ""
                    exact_matches_found = True
                    self.right_exact_matched_set.add(right)
                    self.left_exact_matched_set.add(left)
                    break
                elif clean_hash[left] == clean_hash[right]:
                    # only add them if no exact matches, so have to do it later
                    left_pairwise_matches["harmonised"][left][right] = ""
                    harmonised_matches_found = True
                    local_right_harmonised_list.append(right)
            if exact_matches_found:
                del left_pairwise_matches["harmonised"][left]
            elif harmonised_matches_found:
                del left_pairwise_matches["exact"][left]
                self.left_harmonised_matched_set.add(left)
                self.right_harmonised_matched_set.add(local_right_harmonised_list[0])
            else:
                # if not exact_matches_found and not harmonised_matches_found:
                left_pairwise_matches["no_matches"][left] = ""
                self.left_not_matched_set.add(left)
                del left_pairwise_matches["harmonised"][left]
                del left_pairwise_matches["exact"][left]

        # some terms may still possibly be classified as harmonised as well as exact, so resolving that.
        self.left_harmonised_matched_set.difference_update(self.left_exact_matched_set)
        self.right_harmonised_matched_set.difference_update(self.right_exact_matched_set)

        self.right_not_matched_set = set(right_term_list)
        self.right_not_matched_set.difference_update(self.right_exact_matched_set)
        self.right_not_matched_set.difference_update(self.right_harmonised_matched_set)

        # left_pairwise_matches["exact"][left] = {}
        # left_pairwise_matches["harmonised"][left] = {}
        self.set_harmonised_matches()

    def set_harmonised_matches(self):
        ic()
        left_ordered_list = []
        right_ordered_list = []
        for left in self.left_harmonised_matched_set:
            left_ordered_list.append(left)
            right = ', '.join(list(self.pairwise_matches["left"]["harmonised"][left].keys()))
            right_ordered_list.append(right)
            self.left_harmonised_matching_list = left_ordered_list
            self.right_harmonised_matching_list = right_ordered_list
        # ic(self.left_harmonised_matching_list)
        # ic(self.right_harmonised_matching_list)

        self.right_all_matches_set = self.right_exact_matched_set
        self.right_all_matches_set.union(self.left_harmonised_matched_set)
        return


    def get_clean_hash(self):
        clean_hash = {}
        pairwise_matches = {}
        for left in self.left_term_list:
            clean_hash[left] = clean_term(left)
        for right in self.right_term_list:
            clean_hash[right] = clean_term(right)
        self.clean_hash = clean_hash
        return self.clean_hash

    def get_harmonised_match_df(self):
        df = pd.DataFrame(list(zip(self.left_harmonised_matching_list, self.right_harmonised_matching_list)),
                          columns = [self.left_name, self.right_name]).sort_values(self.left_name)

        return df


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


def do_pairwise_term_matches(pair_string, left_term_list, right_term_list, mixs_v6_obj, report):
    """
    making use of sets as sets don't allow duplicates
    :param pair_string:  # left_list_name '::' right_list_name
    :param left_term_list:
    :param right_term_list:
    :param mixs_v6_obj:
    :param report:
    :return: pairwise_obj:
    """
    ic()
    ic(pair_string)
    # ic(left_term_list)
    # ic(right_term_list)
    pairwise_obj = pairwise_term_matches(pair_string, left_term_list, right_term_list)
    # ic(pairwise_matches)
    ic(len(left_term_list))
    ic(len(pairwise_obj.left_exact_matched_set))
    ic(len(pairwise_obj.left_harmonised_matched_set))
    ic(len(pairwise_obj.left_not_matched_set))

    ic(len(right_term_list))
    ic(len(pairwise_obj.right_exact_matched_set))
    ic(len(pairwise_obj.right_harmonised_matched_set))
    ic(len(pairwise_obj.right_not_matched_set))

    report.write("## Exact Matches")
    report.write(', '.join(list(pairwise_obj.left_exact_matched_set)))
    # ic(mixs_v6_obj.type)

    report.write("\n## mixs_v6 Terms without matches, these are the most frequent")
    # ic(mixs_v6_obj.get_terms_by_freq())
    mixsv6_all_match_freq = mixs_v6_obj.get_terms_with_freq()
    # df = pd.DataFrame(list(zip(self.left_harmonised_matching_list, self.right_harmonised_matching_list)),
    #                  columns = [self.left_name, self.right_name]).sort_values(self.left_name)

    mixsv6_no_match_freq = {"by_freq": {}, "by_term": {}}
    for right in pairwise_obj.right_not_matched_set:
        mixsv6_no_match_freq["by_term"][right] = mixsv6_all_match_freq[right]
        # ic(right)
        freq = mixsv6_all_match_freq[right]
        if freq not in mixsv6_no_match_freq["by_freq"]:
            mixsv6_no_match_freq["by_freq"][freq] = []
        # ic(type(mixsv6_no_match_freq["by_freq"][freq]))
        # ic(type(right))
        mixsv6_no_match_freq["by_freq"][freq].append(right)

    ic(mixsv6_no_match_freq["by_term"])

    df = pd.DataFrame.from_dict(mixsv6_no_match_freq["by_term"], orient = 'index', columns = ["frequency"])
    df["term"] = df.index
    df = df.sort_values("frequency", ascending = False)
    df = df[["term", "frequency"]]
    #report.write(df.head(100).to_string(justify = 'left', index = False))
    report.write("## Frequency" + "\n")
    report.write(df.to_markdown() + "\n")

    title = "Terms in MIXSv6 not matching ENA terms,\n( sized by the number of packages they occur in )"
    # do_textWordCloud(df, title)
    report.write("## Harmonised Matches"+ "\n")
    pairwise_df = pairwise_obj.get_harmonised_match_df()
    report.write(pairwise_df.to_markdown() + "\n")
    # report.write(pairwise_obj.get_harmonised_match_df().to_string(index = false)


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
    do_pairwise_term_matches(pair_string, ena_cl_obj.get_all_term_list(), mixs_v6_obj.get_all_term_list(), mixs_v6_obj,
                             report)

    ena_df = get_df(ena_cl_obj)
    do_hist(ena_df, 'ENA')

    mixs_v6_df = get_df(mixs_v6_obj)
    do_hist(mixs_v6_df, 'MIXS_v6')


def parse_new_linkml():
    """

    :return:
    mixs6_2_dict
        ["slots"][short_term_name]['description'] = "description"
        ["slots"][short_term_name]['title'] = "long_name_ena_uses"
    """
    json_file = "/Users/woollard/projects/GSC/code/mixs-6-2-release-candidate/schema-derivatives/mixs_6_2_rc.json"

    if os.path.isfile(json_file):
        ic(f"about to open {json_file}")
        with open(json_file) as f:
            r_json = json.load(f)

    # for slot in r_json["slots"]:
    #     print(slot)
    #     #title  id
    #     for tag in ('slot_uri', 'description', 'title'):
    #         if tag in r_json['slots'][slot]:
    #             print(f"\t{tag}=\t{r_json['slots'][slot][tag]}")
    #
    #     if slot == "alt":
    #         print(r_json['slots'][slot])

    return r_json


def main():
    linkml_mixs_dict = parse_new_linkml()

    report_file = "../docs/report.md"
    report = open(report_file, "w")
    print(report.write("# Review of the MIX-S checklists proposed by GSC\n"))
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)
    my_dict_v6 = get_mixs_dict()
    mixs_v6_dict = process_mixs_dict(my_dict_v6, linkml_mixs_dict)
    mixs_v6_obj = mixs(mixs_v6_dict, "mixs_v6", linkml_mixs_dict)

    compareSelectChecklists(ena_cl_obj, mixs_v6_obj, report)

    comparison_obj = compareChecklists(ena_cl_obj, mixs_v6_obj, report)
    # print(comparison_obj.comparisonStats)

    analyse_term_matches(ena_cl_obj, mixs_v6_obj, report)

    # ic("early exit")
    # sys.exit()

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
    print(report.write(df.to_markdown()))

    print(f"closing {report_file}")
    report.close()


if __name__ == '__main__':
    ic()
    main()
