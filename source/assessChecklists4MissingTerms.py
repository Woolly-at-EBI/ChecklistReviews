#!/usr/bin/env python3
"""Script of assessChecklists4MissingTerms.py is to script to compare ENA and GSC
      checklist field_lists methods such as get_gsc_package_name_specific_fields_list
___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-11-10
__docformat___ = 'reStructuredText'
chmod a+x assessChecklists4MissingTerms.py
"""
import sys

from icecream import ic
import os
import argparse
import pandas as pd
from mixs import mixs, generate_mixs6_object, generate_ena_object, get_ena_dict

out_dir = "/Users/woollard/projects/ChecklistReviews/data/output/"

def find_substrings(input_string, string_list):
    matches = [element for element in string_list if input_string.lower() in element.lower()]
    return matches

def getENA_Cls(ena_cl_obj, cl_hl):
    """
    get ENA checklsits corresponding to the parameter.
    :param cl_hl:
    :return:
    """
    ic()
    all_gsc_packages = ena_cl_obj.get_gsc_packages()

    results_list = find_substrings(cl_hl, all_gsc_packages)

    if results_list:
        ic(f"yippee: \"{cl_hl}\" matches {results_list}")
    else:
        print(f"\"{cl_hl}\" was not found in {all_gsc_packages}")
    return results_list

def get_matching_ena_terms(checklist_synonym_dict, mixs_list):
    """

    :param checklist_synonym_dict:
    :param mixs_list:
    :return:
    """

def process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, ena_results_list):
    """

    :param ena_cl_obj:
    :param mixs_v6_obj:
    :param cl_hl:
    :param ena_results_list:
    :return: mixs_list_missing, ena_list_missing
    """
    ic()

    #ic(mixs_v6_obj.get_gsc_packages())
    mixs_cat_packages_set = set(find_substrings(cl_hl, mixs_v6_obj.get_gsc_packages()))
    ic(mixs_cat_packages_set)
    ic(mixs_v6_obj.corePackageSet)
    ic(mixs_cat_packages_set.intersection(mixs_v6_obj.corePackageSet))
    ic(mixs_v6_obj.print_summaries())
    sys.exit()
    mixs_core_package_set = mixs_cat_packages_set.intersection(mixs_v6_obj.corePackageSet)
    ic(mixs_core_package_set)
    if len(mixs_core_package_set) < 1:
        ic("ERROR len(mixs_core_package_set) < 1")
        sys.exit()

    ic()
    mixs_core_package = list(mixs_core_package_set)[0]
    print(f"Total ENA checklists matching: {len(ena_results_list)}")

    checklist_synonym_dict = get_checklist_synonym_dict()
    # ic(checklist_synonym_dict)

    def get_syn_matches_dict(checklist_synonym_dict, mixs_difference_terms):
        """

        :param checklist_synonym_dict:
        :param mixs_difference_terms:
        :return:
        """
        if len(checklist_synonym_dict) == 0:
            ic("needed to re-input checklist_synonym_dict")
            checklist_synonym_dict = get_checklist_synonym_dict()


        syn_matches = {}
        for mixs_term in mixs_difference_terms:
            for mixs_term in mixs_difference_terms:
                if mixs_term in checklist_synonym_dict:
                    syn_matches[checklist_synonym_dict[mixs_term]] = mixs_term
        return syn_matches

    def get_syn_matching_ena_terms_dict(checklist_synonym_dict, ena_difference_terms, mixs_difference_terms):
        """
            only finds those terms that are in both the mixs_diff and have the ena term
        :param checklist_synonym_dict:
        :param ena_difference_terms:
        :param mixs_difference_terms:
        :return: syn_matches_filtered_dict, ena_syn_matches_set, mixs_syn_matches_set
          a dictionary with the key of the ENA term and the synonym as the value
        """

        ena_difference_set = set(ena_difference_terms)
        mixs_difference_set = set(mixs_difference_terms)
        syn_matches_dict = get_syn_matches_dict(checklist_synonym_dict, mixs_difference_set)
        synonym_set = set(syn_matches_dict.keys())
        ena_mixs_matching_syn_set = synonym_set.intersection(syn_matches_dict)
        #ic(ena_mixs_matching_syn_set)
        in_both_ena_and_mixs_diff_set = ena_mixs_matching_syn_set.intersection(ena_difference_set)
        #ic(in_both_ena_and_mixs_diff_set)

        syn_matches_filtered_dict = {key: syn_matches_dict[key] for key in in_both_ena_and_mixs_diff_set}
        ena_syn_matches_set = set(syn_matches_filtered_dict.keys())
        mixs_syn_matches_set = set()
        for ena_term in syn_matches_filtered_dict:
            mixs_syn_matches_set.add(syn_matches_filtered_dict[ena_term])
        #ic(syn_matches_filtered_dict)
        return syn_matches_filtered_dict, ena_syn_matches_set, mixs_syn_matches_set

    mixs_list_missing_set = set()
    ena_list_missing_set = set()

    #if len(ena_results_list) > 1:
    #    printf(f"WARNING there are multiple ena_results: {ena_results_list} - this means ")

    for ena_checklist in ena_results_list:
        ic(ena_checklist)
        ena_term_set = set(ena_cl_obj.get_gsc_package_name_specific_fields_list(ena_checklist))
        ic(len(ena_term_set))
        # ic(ena_term_set)
        ic(mixs_core_package_set)
        combined_MIXS_term_set = set(mixs_v6_obj.get_combined_MIXS_term_list(mixs_core_package, mixs_cat_packages_set))
        ic(len(combined_MIXS_term_set))
        intersection_terms = ena_term_set.intersection(combined_MIXS_term_set)
        ic(len(intersection_terms))
        ena_difference_terms = ena_term_set.difference(combined_MIXS_term_set)
        ic(len(ena_difference_terms))
        ic(ena_difference_terms)
        mixs_difference_terms = combined_MIXS_term_set.difference(ena_term_set)
        ic(len(mixs_difference_terms))

        ena_syn_matches_dict, ena_syn_matches_set, mixs_syn_matches_set = get_syn_matching_ena_terms_dict(checklist_synonym_dict, ena_difference_terms, mixs_difference_terms)
        intersection_terms = intersection_terms.union(ena_syn_matches_set)
        ic(len(intersection_terms))
        ena_difference_terms = ena_term_set.difference(intersection_terms)
        ic(len(ena_difference_terms))
        ic(ena_difference_terms)
        ic(mixs_syn_matches_set)
        mixs_difference_terms = mixs_difference_terms.difference(mixs_syn_matches_set)
        ic(len(mixs_difference_terms))
        #ic(mixs_difference_terms)
        mixs_list_missing_set = mixs_list_missing_set.union(mixs_difference_terms)
        ena_list_missing_set = ena_list_missing_set.union()

    return mixs_list_missing_set, ena_list_missing_set

def get_checklist_synonym_dict():
    """

    :return: a dictionary of synonyms linked to the checklist_term
       {'16S recovery software': 'x 16S recovery software',
               'API gravity': 'api gravity',
               'Depth': 'depth',
               'Event Date/Time': 'collection date',
               'Food harvesting process': 'food harvesting process',
    """
    # -- get all sample terms synonyms and their matching checklist term
    # select CV_CHECKLIST_SYNONYM.CHECKLIST_FIELD_ID, CV_CHECKLIST_FIELD.CHECKLIST_FIELD_NAME, CV_CHECKLIST_SYNONYM.CHECKLIST_SYNONYM
    # join CV_CHECKLIST_FIELD
    # on CV_CHECKLIST_FIELD.CHECKLIST_FIELD_ID = CV_CHECKLIST_SYNONYM.CHECKLIST_FIELD_ID
    # where CV_CHECKLIST_SYNONYM.CHECKLIST_TYPE = 'Sample'
    # at some point have as a live SQL read
    syn_file = '/Users/woollard/projects/ChecklistReviews/data/output/ena_checklists_terms_synonyms.txt'

    df_syn = pd.read_csv(syn_file, sep="\t")
    df_syn = df_syn[['CHECKLIST_FIELD_NAME', 'CHECKLIST_SYNONYM']]
    df_syn = df_syn.set_index('CHECKLIST_SYNONYM')
    #ic(df_syn)
    #ic(df_syn.head(5).to_dict())
    df_syn_tmp_dict = df_syn.to_dict()
    df_syn_dict = df_syn_tmp_dict['CHECKLIST_FIELD_NAME']
    return df_syn_dict

def get_all_ena_term_dict():
        """
        select CHECKLIST_FIELD_ID, CHECKLIST_FIELD_NAME, CHECKLIST_FIELD_DESCRIPTION from CV_CHECKLIST_FIELD
        :return: dict keyed by ENA term and one value: the description
        """
        #ic("------------------------------------------------------------")
        ena_term_file = '/Users/woollard/projects/ChecklistReviews/data/output/ena_checklists_terms.txt'

        df_ena = pd.read_csv(ena_term_file, sep="\t")
        #ic(df_ena.head(5))
        df_ena = df_ena[['CHECKLIST_FIELD_NAME', 'CHECKLIST_FIELD_DESCRIPTION']]
        df_ena = df_ena.set_index('CHECKLIST_FIELD_NAME')
        # ic(df_ena.to_dict())
        df_ena_tmp_dict = df_ena.to_dict()
        ic(df_ena_tmp_dict.keys())
        df_ena_dict = df_ena_tmp_dict['CHECKLIST_FIELD_DESCRIPTION']
        #ic(df_ena_dict)

        # tmp_dict = {k: df_ena_dict[k] for k in
        #             df_ena_dict.keys() & {'potassium', 'pregnancy', 'soil type'}}
        # for key in tmp_dict:
        #     ic(f"key=\"{key}\" description={tmp_dict[key]}")
        #
        # sys.exit()
        return df_ena_dict

def create_ena_style_terms_to_add(mixs_v6_obj, cl_hl, mixs_list_missing):
    ic()

    all_ena_term_dict = get_all_ena_term_dict()


    by_term_dict = mixs_v6_obj.get_term_dict()
    ic(len(by_term_dict))
    filtered_dict = {key: by_term_dict[key] for key in mixs_list_missing}
    ic(len(filtered_dict))

    tmp_dict = {k: filtered_dict[k] for k in filtered_dict.keys() & {'assembly quality', 'geographic location (country and/or sea,region)','temperature'}}
    # for key in tmp_dict:
    #     ic(f"key=\"{key}\" description={tmp_dict[key]['description']}")

    #ic(tmp_dict)
    df = pd.DataFrame.from_dict(tmp_dict, orient='index')
    df = df.drop('packages', axis = 1)
    df['term_name'] = df.index
    # #ic(df)
    # #print(df.to_markdown(index = False))
    # ic(len(tmp_dict))
    # ic(df.columns)
    # ic(out_dir)
    df_to_print = df[['term_name', 'description']].sort_values('term_name')
    #ic(df_to_print.head())
    out_file = out_dir + cl_hl + '_new_terms.tsv'
    ic(f"creating {out_file}")
    df_to_print.to_csv(out_file, sep='\t')


def main():

    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)

    ch_hl_list = ['built', 'air']
    for cl_hl in ch_hl_list:
        ic(cl_hl)
        results_list = getENA_Cls(ena_cl_obj, cl_hl)
        mixs_list_missing, ena_list_missing = process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, results_list)
        ic(len(mixs_list_missing))
        create_ena_style_terms_to_add(mixs_v6_obj, cl_hl, mixs_list_missing)
        ic("--------------------------------------------------------------\n")

if __name__ == '__main__':
    ic()
    main()
