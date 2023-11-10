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
from mixs import mixs, generate_mixs6_object, generate_ena_object, get_ena_dict


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

def process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, ena_results_list):
    ic()

    ic(mixs_v6_obj.get_gsc_packages())
    mixs_results_set = set(find_substrings(cl_hl, mixs_v6_obj.get_gsc_packages()))
    ic(mixs_results_set)
    ic(mixs_v6_obj.corePackageSet)
    ic(mixs_results_set.intersection(mixs_v6_obj.corePackageSet))
    mixs_core_package_set = mixs_results_set.intersection(mixs_v6_obj.corePackageSet)
    if len(mixs_core_package_set) < 1:
        ic("ERROR len(mixs_core_package_set) < 1")
        sys.exit()

    print(f"Total ENA checklists matching: {len(ena_results_list)}")
    for ena_checklist in ena_results_list:
        ic(ena_checklist)
        ena_term_list = ena_cl_obj.get_gsc_package_name_specific_fields_list(ena_checklist)
        ic(len(ena_term_list))

        ic(mixs_core_package_set)
        mixs_core_package = list(mixs_core_package_set)[0]
        mixs_term_list = mixs_v6_obj.get_gsc_package_name_specific_fields_list(mixs_core_package)
        ic(len(mixs_term_list))



def main():

    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)

    cl_hl = 'built'
    results_list = getENA_Cls(ena_cl_obj, cl_hl)
    process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, results_list)

if __name__ == '__main__':
    ic()
    main()
