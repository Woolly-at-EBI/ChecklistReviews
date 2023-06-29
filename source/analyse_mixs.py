#!/usr/bin/env python3
"""Script of 'analyse_mixs.py' is to analyse the mixs

convert to JSON, not quite...
cat o | sed -E "s/: \"/: '/g" | sed -E "s/([A-Za-z])'([A-Za-z])/\1\2/g" |  tr "'" '"'  | sed 's/: nan,/: "",/g'  | head -c 157625


___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-16
__docformat___ = 'reStructuredText'

"""

from icecream import ic
import requests
import json
import sys
import os
import os.path
import pickle
import pandas

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
            json.dump(r_json, f, indent=4)
        ic(f"Created {json_file}")
    return r_json


def get_mixs_dict():
    """

    :return:
    """
    pickle_file = '../data/v6_mixs.schema.json.pickle'
    if os.path.isfile(pickle_file):
        with open(pickle_file, 'rb') as handle:
            my_dict = pickle.load(handle)
    else:
        my_dict = json.loads(get_data())
        with open(pickle_file, 'wb') as handle:
             pickle.dump(my_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)
    return my_dict

def print_MIXS_review_dict_stats(MIXS_review_dict):
    """

    :param MIXS_review_dict:
    :return:
    """
    print(f"Count of top_level MIX-S checklists={len(MIXS_review_dict)}")
    for checklist_name in MIXS_review_dict:
        print(f"{checklist_name} field_count={MIXS_review_dict[checklist_name]['count']}")

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

    for top_def in my_dict["$defs"]:
        # print(top_def)
        printed_top = False
        for second_def in my_dict["$defs"][top_def]:
            if not printed_top and second_def == 'properties':
                MIXS_review_dict[top_def] = {}
                MIXS_review_dict[top_def]["count"] = 0
                MIXS_review_dict[top_def]["field"] = {}
                #print("") #
                #print(top_def, end = ": ")
                printed_top = True
            #print(f"\t{second_def}")
            # print(f"\t\tsub_dict={my_dict['$defs'][top_def][second_def]}")
            # sub_dict = my_dict["$defs"][top_def][second_def]
            # print(f"\t\tsub={sub_dict}")
            if second_def == 'properties':
                 #print(f"\t\t{second_def} property_count={len(my_dict['$defs'][top_def][second_def])}", end = " properties: ")
                 for third_def in my_dict["$defs"][top_def][second_def]:
                     #print(f"{third_def}", end = ", ")
                     MIXS_review_dict[top_def]["field"][third_def] = {}
                     #sys.exit()
                 MIXS_review_dict[top_def]["count"] = len(MIXS_review_dict[top_def]["field"])
            else:
                pass
    print()
    #ic(MIXS_review_dict)

    print_MIXS_review_dict_stats(MIXS_review_dict)

def url2file(url):
    url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/mixs/jsonschema/mixs.schema.json"
    ic(url)
    r = requests.get(url)
    r_json = r.text

class mixs_v5:
    def __init__(self,my_dict):
        self.my_dict = my_dict

    def get_all_term_list(self):
        return list(self.my_dict['by_term'].keys())

    def get_all_term_count(self):
        return(len(self.my_dict['by_term'].keys()))

    def get_all_package_list(self):
        return list(self.my_dict['by_package'].keys())

    def get_all_package_count(self):
        return(len(self.my_dict['by_package'].keys()))


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

        df_mixs5 = pandas.read_excel(xlsx_file, sheet_name = 'environmental_packages')
        print(df_mixs5.head(5))
        # print(df_mixs5.head(5).to_dict(orient = 'records'))
        mixs_v5_simple_dict = df_mixs5.to_dict(orient = 'index')
        mixs_v5_dict = {}
        mixs_v5_dict['by_package'] = {}
        mixs_v5_dict['by_term'] = {}
        # print ("==============================================")
        for index in mixs_v5_simple_dict:
            #print("___________________________________________")
            checklist_env_package_name = mixs_v5_simple_dict[index]['Environmental package']
            package_item = mixs_v5_simple_dict[index]['Package item']
            if checklist_env_package_name in mixs_v5_dict:
                #print("YIPPEE")
                # sys.exit()
                pass
            else:
                #print(f"not hasattr: -->{checklist_env_package_name}<--")
                #print(mixs_v5_dict)
                mixs_v5_dict['by_package'][checklist_env_package_name] = {}

                #print(mixs_v5_dict)
            #print(package_item)
            mixs_v5_dict['by_package'][checklist_env_package_name][package_item] = {}
            mixs_v5_dict['by_term'][package_item] = {}
            for key in mixs_v5_simple_dict[index]:
                if key == 'Environmental package' or key == 'Package item':
                    continue
                else:
                    mixs_v5_dict['by_package'][checklist_env_package_name][package_item][key] = mixs_v5_simple_dict[index][key]
                    mixs_v5_dict['by_term'][package_item][key] = mixs_v5_simple_dict[index][key]
            #print(mixs_v5_dict)
        #sys.exit()
        # print(json.dumps(mixs_v5_dict, indent=4))
        with open(pickle_file, 'wb') as handle:
            pickle.dump(mixs_v5_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)



    return mixs_v5_dict


def main():
    mixs_v5_dict = get_mixs_v5_dict()
    mixs_v5_obj = mixs_v5(mixs_v5_dict )
    print(f"term_count={mixs_v5_obj.get_all_term_count()}  terms={mixs_v5_obj.get_all_term_list()}")
    print(f"package_count={mixs_v5_obj.get_all_package_count()} packages={mixs_v5_obj.get_all_package_list()}")
    sys.exit()
    my_dict_v6 = get_mixs_dict()
    ic(len(my_dict_v6))
    process_dict(my_dict_v6)


if __name__ == '__main__':
    ic()
    main()
