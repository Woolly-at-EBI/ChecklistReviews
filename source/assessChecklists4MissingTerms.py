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
log_file = out_dir + ena_mixs_logfile_Nov2022.txt

def find_substrings(input_string, string_list):
    matches = [element for element in string_list if input_string.lower() in element.lower()]
    return matches

def find_starting_substrings(input_string, string_list):
    matches = []
    for element in string_list:
        input_lower = input_string.lower()
        element_lower = element.lower()
        if input_lower == element or element_lower.startswith(input_lower):
            matches.append(element)
    return matches

def find_ending_substrings(input_string, string_list):
    matches = []
    for element in string_list:
        input_lower = input_string.lower()
        element_lower = element.lower()
        if input_lower == element or element_lower.endswith(input_lower):
            matches.append(element)
    return matches
def remove_word(results_list, remove_word_list):
    results_set = set(results_list)
    ic(results_list)
    for rm_word in remove_word_list:
        ic(rm_word)
        for element in results_list:
            if rm_word.lower() in element:
                results_set.remove(element)
                print(f"INFO rm {element} from: {', '.join(results_list)}")

    return list(results_set)
def getENA_Cls(ena_cl_obj, cl_hl):
    """
    get ENA checklists corresponding to the parameter.
    :param cl_hl:
    :return:  results_list of 0 or more terms...


    ic| ','.join(ena_cl_obj.get_all_package_list()): ('COMPARE-ECDC-EFSA pilot food-associated reporting standard,COMPARE-ECDC-EFSA '
                                                  'pilot human-associated reporting standard,ENA Crop Plant sample enhanced '
                                                  'annotation checklist,ENA Global Microbial Identifier Proficiency Test (GMI '
                                                  'PT) checklist,ENA Global Microbial Identifier reporting standard checklist '
                                                  'GMI_MDM:1.1,ENA Influenza virus reporting standard checklist,ENA Marine '
                                                  'Microalgae Checklist,ENA Micro B3,ENA Plant Sample Checklist,ENA Shellfish '
                                                  'Checklist,ENA Tara Oceans,ENA UniEuk_EukBank Checklist,ENA binned '
                                                  'metagenome,ENA default sample checklist,ENA mutagenesis by carcinogen '
                                                  'treatment checklist,ENA parasite sample checklist,ENA prokaryotic pathogen '
                                                  'minimal sample checklist,ENA sewage checklist,ENA virus pathogen reporting '
                                                  'standard checklist,GSC MIMAGS,GSC MISAGS,GSC MIUVIGS,GSC MIxS air,GSC MIxS '
                                                  'built environment,GSC MIxS host associated,GSC MIxS human associated,GSC '
                                                  'MIxS human gut,GSC MIxS human oral,GSC MIxS human skin,GSC MIxS human '
                                                  'vaginal,GSC MIxS microbial mat biolfilm,GSC MIxS miscellaneous natural or '
                                                  'artificial environment,GSC MIxS plant associated,GSC MIxS sediment,GSC MIxS '
                                                  'soil,GSC MIxS wastewater sludge,GSC MIxS water,HoloFood Checklist,PDX '
                                                  'Checklist,Tree of Life Checklist')
    """
    ic()
    all_gsc_packages = ena_cl_obj.get_gsc_packages()

    # these are the non-straightforward ones  echo $ena_packages | tr "'" ' ' | sed 's/^ *//' | tr '\t' ' ' | tr '\n' ' ' | sed -e 's/ */ /g' | tr ',' '\n'
    MIXS_CorePackages2ena = {'host': 'host associated',
                             'builtenvironment': 'built environment',
                             'microbialmatbiofilm': 'microbial mat biolfilm',
                             'humanassociated': 'human associated',
                             'human-gut': 'human gut',
                             'human-oral': 'human oral',
                             'human-skin': 'human skin',
                             'human-vaginal': 'human vaginal',
                             'human-associated': 'human associated',
                             'plant-associated': 'plant associated',
                             'wastewatersludge': 'wastewater sludge',
                             'miscellaneousnaturalorartificialenvironment': 'miscellaneous natural or artificial environment'
                         }
    ic(cl_hl)
    if cl_hl in MIXS_CorePackages2ena:
        tmp_cl_hl = MIXS_CorePackages2ena[cl_hl]
    else:
        tmp_cl_hl = cl_hl
    results_list = find_substrings(tmp_cl_hl, all_gsc_packages)
    if tmp_cl_hl == 'water':
        ic()
        results_list = remove_word(results_list, ['Waste'])
        # if cl_hl == 'water':
        #     results_list = ['GSC MIxS water']
    if results_list:
        ic(f"INFO: \"{cl_hl}\" matches {results_list}")
    else:
        print(f"WARNING: \"{cl_hl}\" was not found in {all_gsc_packages}")
        if cl_hl in ['agriculture', 'core', 'food', 'hydrocarbon','symbiont']:
            pass
        else:
            sys.exit()

    return results_list

def get_matching_ena_terms(checklist_synonym_dict, mixs_list):
    """

    :param checklist_synonym_dict:
    :param mixs_list:
    :return:
    """
    pass

#--------------------------------------------------------------------------------
def process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, ena_results_list):
    """

    :param ena_cl_obj:
    :param mixs_v6_obj:
    :param cl_hl:
    :param ena_results_list:
    :return: mixs_list_missing, ena_list_missing
    """
    ic()
    ic(ena_cl_obj.type)
    ic(mixs_v6_obj.type)

    def remove_exceptions(cl_hl, package_set):
        """
        Human food related checklists were being incorrectly assigned, so removing them here
        :param cl_hl:
        :param package_set:
        :return:
        """
        ic()
        #ic(', '.join(package_set))
        remove_set = set()
        if cl_hl == 'human':
             remove_set = set(find_substrings('food', package_set))

        if len(remove_set) > 0:
            ic(remove_set)
            for key in remove_set:
                package_set.remove(key)
            # package_set.remove(remove_set)
            ic("removed")
            ic(package_set)

        # if cl_hl == 'human':
        #     sys.exit()

        return package_set

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

    ic("start of process_matching_ena_checklists function proper")
    #ic(mixs_v6_obj.get_gsc_packages())
    mixs_cat_packages_set = remove_exceptions(cl_hl, set(find_starting_substrings(cl_hl, mixs_v6_obj.get_gsc_packages())))
    ic(', '.join(list(mixs_cat_packages_set)))
    #ic(mixs_v6_obj.corePackageSet)
    ic(', '.join(mixs_cat_packages_set.intersection(mixs_v6_obj.corePackageSet)))
    mixs_core_package_set = mixs_cat_packages_set.intersection(mixs_v6_obj.corePackageSet)
    ic(', '.join(list(mixs_core_package_set)))

    MIXS_package_mapping_dict = mixs_v6_obj.get_MIXS_package_mapping_dict()
    ic(cl_hl)
    ic(MIXS_package_mapping_dict)
    if cl_hl in MIXS_package_mapping_dict:
        ic()
        mixs_core_package_set.add(MIXS_package_mapping_dict[cl_hl]['core'])
        ic(mixs_core_package_set)

    if len(mixs_core_package_set) < 1:
        ic(f"ERROR {len(mixs_core_package_set)} < 1")
        #sys.exit()
        ic(', '.join(list(mixs_v6_obj.corePackageSet)))
        lc_mixs_core_set = set(x.lower() for x in mixs_v6_obj.corePackageSet)
        ic(f"{cl_hl} core set={lc_mixs_core_set}")
        for core_value in lc_mixs_core_set:
           if cl_hl in core_value:
            ic(f"core_value {core_value}")
    else:
        mixs_core_package = list(mixs_core_package_set)[0]

    ic()
    print(f"Total ENA checklists matching: {len(ena_results_list)}")
    mixs_list_missing_set = set()
    ena_list_missing_set = set()
    combined_MIXS_term_set = set(mixs_v6_obj.get_combined_MIXS_term_list(mixs_core_package, mixs_cat_packages_set))
    #ic(', '.join(combined_MIXS_term_set))
    ena_list_missing_set
    if len(ena_results_list) == 0:
        mixs_list_missing_set = combined_MIXS_term_set
    elif len(ena_results_list) > 0:
        checklist_synonym_dict = get_checklist_synonym_dict()
        # ic(checklist_synonym_dict)

        #if len(ena_results_list) > 1:
        #    printf(f"WARNING there are multiple ena_results: {ena_results_list} - this means ")

        ic(','.join(ena_results_list))
        for ena_checklist in ena_results_list:
            ic(ena_checklist)
            ena_term_set = set(ena_cl_obj.get_gsc_package_name_specific_fields_list(ena_checklist))
            ic(len(ena_term_set))
            # ic(ena_term_set)
            ic()
            ic(mixs_core_package_set)
            # combined_MIXS_term_set = set(mixs_v6_obj.get_combined_MIXS_term_list(mixs_core_package, mixs_cat_packages_set))
            #ic(len(combined_MIXS_term_set))
            intersection_terms = ena_term_set.intersection(combined_MIXS_term_set)
            #ic(len(intersection_terms))
            ena_difference_terms = ena_term_set.difference(combined_MIXS_term_set)
            #ic(len(ena_difference_terms))
            #ic(', '.join(list(ena_difference_terms)))
            mixs_difference_terms = combined_MIXS_term_set.difference(ena_term_set)
            #ic(len(mixs_difference_terms))

            #test for synonyms
            ena_syn_matches_dict, ena_syn_matches_set, mixs_syn_matches_set = get_syn_matching_ena_terms_dict(checklist_synonym_dict, ena_difference_terms, mixs_difference_terms)
            intersection_terms = intersection_terms.union(ena_syn_matches_set)
            ic(len(intersection_terms))
            ena_difference_terms = ena_term_set.difference(intersection_terms)
            ic(len(ena_difference_terms))
            ic(', '.join(list(ena_difference_terms)))
            ic(', '.join(list(mixs_syn_matches_set)))
            mixs_difference_terms = mixs_difference_terms.difference(mixs_syn_matches_set)
            #ic(len(mixs_difference_terms))
            #ic(mixs_difference_terms)
            mixs_list_missing_set = mixs_list_missing_set.union(mixs_difference_terms)
            ena_list_missing_set = ena_list_missing_set.union()
    # END OF if len(ena_results_list) > 0:


    return mixs_list_missing_set, ena_list_missing_set
#--------------------------------------------------------------------------------

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
        return df_ena_dict

def get_filtered_dict(my_dict, keep_keys):
    return {key: my_dict[key] for key in keep_keys}


def create_ena_existing_terms(cl_hl, ena_obj, ena_sp_package_term_list):
    ic(type(ena_obj))
    filtered_dict = get_filtered_dict(ena_obj.get_term_dict(), ena_sp_package_term_list)
    # ic(filtered_dict)
    df = term_dict_2_df(filtered_dict)
    df_to_print = df[['term_name', 'description']].sort_values('term_name')
    #ic(df_to_print.head())
    out_file = out_dir + cl_hl.lower()  + '_old_terms.tsv'
    ic(f"creating {out_file}")
    df_to_print.to_csv(out_file, sep='\t', index=False)

def term_dict_2_df(filtered_dict):
    """
    In_dict                   'water current': {'count': 3,
                                      'description': 'measurement of magnitude and direction of '
                                                     'flow within a fluid',
                                      'package_category_set': {'G', 'E'},
                                      'packages': ['GSC MIxS water',
                                                   'GSC MIxS miscellaneous natural or artificial '
                                                   'environment',
                                                   'ENA Micro B3']}}"
    return:
      df.columns: Index(['description', 'type', 'packages', 'count', 'package_category_set',
                       'term_name']
    """
    #ic(filtered_dict)
    df = pd.DataFrame.from_dict(filtered_dict, orient='index')
    #df = df.drop('packages', axis = 1)
    df['term_name'] = df.index
    # #print(df.to_markdown(index = False))
    #ic(df.columns)
    #ic(df.head())
    #sys.exit()
    return df.sort_values('term_name')

def create_ena_style_terms_to_add(mixs_v6_obj, cl_hl, mixs_list_missing):
    ic()
    filtered_dict = get_filtered_dict(mixs_v6_obj.get_term_dict(), mixs_list_missing)
    # ic(len(#)

    #tmp_dict = {k: filtered_dict[k] for k in filtered_dict.keys() & {'assembly quality', 'geographic location (country and/or sea,region)','temperature'}}
    # for key in tmp_dict:
    #     ic(f"key=\"{key}\" description={tmp_dict[key]['description']}")

    #ic(tmp_dict)
    df = term_dict_2_df(filtered_dict)
    df_to_print = df[['term_name', 'description']].sort_values('term_name')
    #ic(df_to_print.head())
    out_file = out_dir  + cl_hl.lower() + '_new_terms.tsv'
    ic(f"creating {out_file}")
    df_to_print.to_csv(out_file, sep='\t', index=False)

def combined_comparision(cl_hl,mixs_list_missing,ena_sp_package_term_list):
    ic()
    combined_list = sorted(list(mixs_list_missing) + ena_sp_package_term_list)
    ena_sp_package_term_set = set(ena_sp_package_term_list)
    row_dict = {}
    row_num = 0
    for term in combined_list:
        if term in mixs_list_missing:  #i.e. missing from the ENA list
            row_dict[row_num] = {'mixs(missing_from_ENA)': term, 'ena': ''}
        elif term in ena_sp_package_term_list:
            row_dict[row_num] = {'mixs(missing_from_ENA)': '', 'ena': term}
        row_num = row_num + 1

    df = pd.DataFrame.from_dict(row_dict, orient = 'index')
    out_file = out_dir + cl_hl.lower() + '_missing_terms_context.tsv'
    ic(f"creating {out_file}")
    df.to_csv(out_file, sep = '\t', index = False)


def main():

    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)
    ic(','.join(ena_cl_obj.get_all_package_list()))

    # ch_hl_list = ['built', 'air']
    ch_hl_list = sorted(mixs_v6_obj.get_high_level_cat_list())
    ch_hl_list = [element.lower() for element in ch_hl_list];
    #ch_hl_list = ['Water', 'Agriculture', 'Food']
    #ch_hl_list = ['Agriculture']
    #ch_hl_list = ['miscellaneousnaturalorartificialenvironment']
    for cl_hl in ch_hl_list:
        ic("--------------------------------------------------------------\n")
        ic(cl_hl)

        results_list = getENA_Cls(ena_cl_obj, cl_hl)


        if len(results_list) == 0:
            ic(f"No ENA checklists corresponding to {cl_hl}")
            mixs_list_missing, ena_list_missing = process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, results_list)
            #ic(', '.join(mixs_list_missing))
            create_ena_style_terms_to_add(mixs_v6_obj, cl_hl, mixs_list_missing)
            # in future populate this  mixs_list_missing
        elif len(results_list) == 1:
          ena_sp_package_term_list = ena_cl_obj.get_gsc_package_name_specific_fields_list(results_list[0])
          # ic(', '.join(ena_sp_package_term_list))
          mixs_list_missing, ena_list_missing = process_matching_ena_checklists(ena_cl_obj, mixs_v6_obj, cl_hl, results_list)
          ic(len(mixs_list_missing))

          create_ena_style_terms_to_add(mixs_v6_obj, cl_hl, mixs_list_missing)
          create_ena_existing_terms(cl_hl, ena_cl_obj, ena_sp_package_term_list)
          combined_comparision(cl_hl, mixs_list_missing,ena_sp_package_term_list)
        else:
            print(f"ERROR Multiple ENA files {results_list} match {cl_hl}")
            sys.exit()
        ic('end of this iteration of ch_hl_list loop')

if __name__ == '__main__':
    ic()
    main()
