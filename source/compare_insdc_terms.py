#!/usr/bin/env python3
"""Script of compare_insdc_terms.py is to compare_insdc_terms.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2024-05-24
__docformat___ = 'reStructuredText'
chmod a+x compare_insdc_terms.py
"""
import sys

import os
import argparse
import pandas as pd
import logging
import coloredlogs
import numpy as np
import re
from analyse_mixs import *
import string

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

my_coloredFormatter = coloredlogs.ColoredFormatter(
    fmt='[%(name)s] %(asctime)s %(funcName)s %(lineno)-3d  %(message)s',
    level_styles=dict(
        debug=dict(color='white'),
        info=dict(color='green'),
        warning=dict(color='yellow', bright=True),
        error=dict(color='red', bold=True, bright=True),
        critical=dict(color='black', bold=True, background='red'),
    ),
    field_styles=dict(
        name=dict(color='white'),
        asctime=dict(color='white'),
        funcName=dict(color='white'),
        lineno=dict(color='white'),
    )
)

def checklist_field_stats(site, df):
    logging.info(site)
    logging.info(f"Total number of terms = {len(df)}")

def get_data_files_dict():
    data_files_dict = {
        'ENA': {"packages": "EBI - Package", "fields": 'ENA - Attribute'},
        'DDBJ': {"packages": 'DDBJ - Package', "fields": 'DDBJ - Attribute'},
        'NCBI': {"packages": 'NCBI - Package', "fields": 'NCBI - Attribute'}
    }
    return data_files_dict

def get_attribute_dfs(combined_xlsx_file, data_files_dict):
    logging.info(msg="get_attribute_dfs")
    for site in data_files_dict:

        df = pd.read_excel(open(combined_xlsx_file, 'rb'),
                      sheet_name = data_files_dict[site]["fields"])
        print(f"{site} total of fields(attributes): {len(df)}")
        data_files_dict[site]["fields_df"] = df
    return data_files_dict


def print_simple_dict(ena_term_matches_dict, filter_field):
        df = pd.DataFrame.from_dict(ena_term_matches_dict, orient='index')

        logger.info(f"print_simple_dict before, note counts {df['note'].value_counts()}")
        if len(filter_field) <= 2:
           logger.info(f"print_simple_dict\n{df.head(5).to_string()}")
        else:
            logger.info(f"\tbefore filter df= {len(df)} filter_field -->{filter_field}<--")
            df = df.query('note == @filter_field')
            logger.info(f"\tafter filter df= {len(df)}")
            logger.info(f"print_simple_dict with filter_field -->{filter_field}<--\n{df.head(5).to_string()}")

def populate_input_data_structure():
    """

    :return:
    """
    logging.info(msg="populate_input_data_structure")
    combined_xlsx_file = '/Users/woollard/projects/ChecklistReviews/data/INSDC_WORK/package_or_checklist_attributes_INSDC-2.xlsx'
    data_files_dict = get_data_files_dict()
    data_files_dict = get_attribute_dfs(combined_xlsx_file, data_files_dict)
    return data_files_dict


def add_in_easy_mappings(df, source_mapped_name, target_mapped_name, mapping_set):
    logging.info(f"add_in_easy_mappings for {source_mapped_name} and {target_mapped_name}")
    count = 0
    for name in mapping_set:
       #logging.info(f"{name}")
       df.loc[df[source_mapped_name] == name, target_mapped_name] = name

       count = count + 1

    # taking one off for the empty sets
    logging.info(f"now {target_mapped_name} has this many mapped in harmonised {len(set(df[target_mapped_name].to_list())) - 1 }")
    logging.info(f"now {source_mapped_name} has this many mapped in harmonised {len(set(df[source_mapped_name].to_list())) - 1}")

    return df



def prefix_name2columns(formatted_prefix, df):
    logging.info(df.columns)
    native_columns = df.columns.tolist()
    append_str = formatted_prefix
    new_name_list = [append_str + sub for sub in native_columns]
    rename_dict = dict(zip(native_columns, new_name_list))
    logging.info(rename_dict)
    df = df.rename(columns=rename_dict)

    return df

def add_in_site_specific_names(mapped_df, site_only_set, site_df, site_df_name2index, site_df_mapped_name):
    """

    :param mapped_df:
    :param site_only_set:
    :param site_df:
    :return: mapped_df
    """
    # print("=========================================================")
    logger.info(f"add_in_site_specific_names site_df_mapped_name={site_df_mapped_name}<---,site_df_name2index={site_df_name2index}<---")
    logging.info(f"before  {site_df_mapped_name} has this many mapped in harmonised {len(set(mapped_df[site_df_mapped_name].to_list())) - 1 }")
    site_df['my_index'] = site_df[site_df_name2index]
    site_df = site_df.set_index('my_index')
    site_only_list = list(site_only_set)
    tmp_df = site_df.loc[site_only_list]
    # print("=========================================================")
    # logger.info(f"columns = {tmp_df.columns}")
    # logger.info(f"tmp_df {tmp_df.head()}")
    # print("=========================================================")
    # logger.info(site_df[site_df_name2index])
    # logger.info(site_df[site_df_name2index].value_counts())
    # print("=========================================================")
    tmp_df[site_df_mapped_name] = tmp_df[site_df_name2index]
    logger.info(f"{site_df_mapped_name} len of site_only_set  {len(site_only_set)}")
    logger.info(f"{site_df_mapped_name} len of df to merge in {len(tmp_df)}")
    mapped_df = pd.concat([mapped_df, tmp_df], join='outer').reset_index()
    print_mapped_3_head(mapped_df)
    logger.info(mapped_df.columns)

    logging.info(f"after {site_df_mapped_name} has this many mapped in harmonised {len(set(mapped_df[site_df_mapped_name].to_list())) - 1 }")
    logging.info(f"\tlen mapped_df: {len(mapped_df)}")


    return mapped_df

def generate_syn_dict(df_ena_working,synonym_col,field_name_col):
        """
        generate simple syn dict, with the keys being the synonyms and ENA field value being the value

        :param df_ena_working:
        :return: ena_synonym_dict
        """
        # logger.info(f"df_ena_working len {len(df_ena_working)}")
        ena_synonym_dict = dict(zip(df_ena_working[synonym_col], df_ena_working[field_name_col]))
        # logger.info(f"ena_synonym_dict len {ena_synonym_dict}")
        ena_synonym_dict.pop('\n', None)

        ena_synonym_set = set(ena_synonym_dict.keys())
        # logger.info(f"ena_synonym_set len {len(ena_synonym_set)}")

        clean_syn_dict = {}
        #deal with multiple synonyms i.e. separated by a ;
        for ena_synonym in ena_synonym_dict:
            split_ena_synonym = ena_synonym.split(';')
            if len(split_ena_synonym) > 1:
                # logger.info(f"split_ena_synonym  {split_ena_synonym}")
                for individual_ena_synonym in split_ena_synonym:
                    clean_syn_dict[individual_ena_synonym] = ena_synonym_dict[ena_synonym]
            else:
                clean_syn_dict[ena_synonym] = ena_synonym_dict[ena_synonym]
        # logger.info(f"ena_synonym_dict len {len(clean_syn_dict)}")
        return clean_syn_dict
def ena_synonym2fieldname_dict(synonym2fieldname_dict, synonym_hit_list):
    """
         is for ENA!
            gives it back in synonym_hit_list order
    :param synonym2fieldname_dict:
    :param synonym_hit_list:
    :return: checklist_field_name_list
    """
    checklist_field_name_list = []
    for ena_syn in synonym_hit_list:
        if ena_syn in synonym2fieldname_dict:
            # logger.info(f"-->{ena_syn}<-- matching-->{synonym2fieldname_dict[ena_syn]}<--")
            checklist_field_name_list.append(synonym2fieldname_dict[ena_syn])
    logger.info(f"fieldname_syn_intersection_list len = {len(fieldname_syn_intersection_list)}")

    return checklist_field_name_list

def clean_ncbi_syn(ncbi_synonym_set):
    logging.debug(ncbi_synonym_set)

    clean_set = set()
    for synonym_line in ncbi_synonym_set:
        synonym_line = str(synonym_line)
        for synonym in synonym_line.split(','):
            clean_set.add(synonym.strip())
    return clean_set

def get_fuzzy_matches(left_name, right_name, left_list, right_list):
        pair_string = names2pair_string(left_name, right_name )
        pairwise_obj = pairwise_term_matches(pair_string, left_list, right_list)
        # left_conf_set = pairwise_obj.get_left_confident_matched_list()
        # return left_conf_set
        # logger.info(left_conf_set)

        return pairwise_obj.get_medium_confidence_dict()

def run_process_fuzzy_matches(df_ena, df_ena_working, left_name, right_name, left_list, right_list):
        logger.info(f"run_process_fuzzy_matches {left_name} {right_name}")
        fuzzy_medium_confidence_dict = get_fuzzy_matches(left_name, right_name, left_list, right_list)
        logger.debug(fuzzy_medium_confidence_dict)
        ena_long_name_set = set(df_ena['CHECKLIST_FIELD_NAME'])
        left_terms_matched_list = []
        right_terms_matched_list = []
        left_terms_matched_already_set = set()
        for left_term in fuzzy_medium_confidence_dict.keys():
            right_term, fuzzy_score = fuzzy_medium_confidence_dict[left_term]
            logger.debug(f"Fuzzy match for -->{left_term}<-- -->{right_term}<-- with {fuzzy_score}")
            if right_term in ena_long_name_set:
                logger.debug(f"\tright_term is already in ENA list: {right_term}")
                left_terms_matched_already_set.add(right_term)
            else:
                left_terms_matched_list.append(left_term)
                right_terms_matched_list.append(right_term)
        logger.info(f"total left_terms_matched_set len = {len(left_terms_matched_already_set)} all= {left_terms_matched_list}")
        logger.info(f"\tIgnoring len={len(left_terms_matched_already_set)}  left_terms_matched_set already known {left_terms_matched_already_set}")

        return left_terms_matched_list, right_terms_matched_list

def update_mapping_dict(ena_term_matches_dict, left_list, right_list, note_list):
    logging.info(f"before ena_term_matches_dict len {len(ena_term_matches_dict)} and input is of len={len(left_list)}")
    list_len = len(left_list)
    for i in range(0, list_len - 1):
        ena_term_matches_dict[left_list[i]] = {"match": right_list[i], "note": note_list[i] }

    logging.info(f"after ena_term_matches_dict len {len(ena_term_matches_dict)}")
    return ena_term_matches_dict

def create_note4all_list(note, length):
    note_list = []
    for i in range(length):
        note_list.append(note)
    return note_list

def make_ncbi_multiname_dict(df_ncbi):
    """
    make a dictionary keyed of both harmonised or long name and synonyms, all link to harmonised
    keys = {'harmonised_name' , 'name', 'synonym'}
    for synonyms does both the single and mult
    :param df_ncbi:
    :return:
    """
    ncbi_multi_name_dict = {}
    harmonised2long = dict(zip(df_ncbi['Harmonized name'], df_ncbi['Name']))
    long2harmonised = dict(zip(df_ncbi['Name'], df_ncbi['Harmonized name']))
    tmp_syns2harmonised = dict(zip(df_ncbi['Synonyms'], df_ncbi['Harmonized name'])) # n.b. is the multi as well the singular
    syns2harmonised = tmp_syns2harmonised.copy()
    for orig_syns in tmp_syns2harmonised:
        syns = str(orig_syns)
        # syns = ''.join([str(char) for char in syns_string if char in string.printable])     #making sure no strange chars...
        for syn in syns.split(','):
            syn = syn.strip()
            syns2harmonised[syn] = syns2harmonised[orig_syns]      # if synonym twice, will only keep the last one.
    #         if "geog" in syn:
    #             logger.info("-->" + syn + "<--")
    #             logger.info("WTTTTTTTT")
    # sys.exit()

    ncbi_multi_name_dict = {'harmonised_name': harmonised2long, 'name': long2harmonised, 'synonym': syns2harmonised}
    ic(ncbi_multi_name_dict.keys())
    return ncbi_multi_name_dict

def get_name_centric_matches(match_type, synonym_dict, syn_list):
    """
    Expecting the direct value of synonym_dict to be the checklist_field_name or the NCBI harmonised name
    :param synonym_dict:
    :param syn_list:
    :return:
    """

    if match_type == 'ena_synonym':

        #logger.info(f"syn_list len {len(syn_list)}")
        lc_synonym_dict = {}
        for syn in synonym_dict:
            lc_syn = str(syn).lower
            lc_synonym_dict[lc_syn] = synonym_dict[syn]

        checkfield_names = []
        for synonym in syn_list:
            if synonym_dict.get(synonym) is not None:
               checkfield_names.append(synonym_dict[synonym])
            else:
                lc_synonym = str(synonym).lower()
                #logger.info(f"lc_synonym={lc_synonym} ")
                if lc_synonym_dict.get(lc_synonym) is not None:
                    checkfield_names.append(lc_synonym_dict[lc_synonym])
                else:
                    logger.warning(f"synonym {synonym} not in synonym_dict")
        #logger.info(f"checkfield_names len {len(checkfield_names)}")
    return checkfield_names


def add_ena_notes(data_files_dict):
    logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    logger.info(f"add_ena_notes keys={data_files_dict.keys()}")
    mapped_df = data_files_dict['mapped_df']
    ena_term_matches_dict = data_files_dict['ena_term_matches_dict']
    logger.info(f"mapped_df keys={mapped_df.keys()}")

    #logger.info(f"ena_term_matches_dict keys={ena_term_matches_dict.keys()}")
    #print_simple_dict(ena_term_matches_dict,'')
    df_ena_term_matches = pd.DataFrame.from_dict(ena_term_matches_dict, orient='index')
    logger.info(f"df_ena_term_matches notes={df_ena_term_matches['note'].value_counts()}")
    df_ena_term_matches['ENA_mapped_name'] = df_ena_term_matches.index
    df_2_map = df_ena_term_matches[['ENA_mapped_name', 'match', 'note']]
    df_2_map = df_2_map.rename(columns={'match': 'NCBI_mapped_name', 'note': 'EBI_mapped_note'})
    logger.info(f"len(df_ena_term_matches)={len(df_2_map)}")
    ENA_NCBI_mapped_names = set(df_2_map['NCBI_mapped_name'].to_list())
    logger.info(f"NCBI_mapped_names total={len(ENA_NCBI_mapped_names)}")
    logger.info(f"df_2_map notes={df_2_map.head(3)}")

    MAPPED_DF_NCBI_mapped_names = set(mapped_df['NCBI_mapped_name'].to_list())
    logger.info(f"MAPPED_DF_NCBI_mapped_names total={len(MAPPED_DF_NCBI_mapped_names)}")
    NCBI_mapped_names_intersection = MAPPED_DF_NCBI_mapped_names.intersection(ENA_NCBI_mapped_names)
    logger.info(f"MAPPED_DF_NCBI_mapped_names intersection total={len(NCBI_mapped_names_intersection)}")

    mapped_df = mapped_df.drop(columns=['ENA_mapped_name'])
    mapped_df = pd.merge(mapped_df, df_2_map, how="left", on='NCBI_mapped_name')
    mapped_df = mapped_df.fillna('')
    # logger.info(f"mapped_df =\n{mapped_df.head(10).to_string(index=False)}")
    logger.info(mapped_df.columns)
    mapped_df_slim = mapped_df[['ENA_mapped_name', 'NCBI_mapped_name', 'NCBI:Harmonized_name', 'DDBJ_mapped_name']]
    logger.info(f"mapped_df =\n{mapped_df_slim.head(10).to_string(index = False)}")
    data_files_dict['mapped_df'] = mapped_df

    generate_stats(data_files_dict)
    sys.exit()


def process_ENA_terms_to_map(data_files_dict):
    """
    map to the NCBI_harmonized
    :param data_files_dict:
    :return:
    """
    logging.info(data_files_dict.keys())
    logger.info(f"process_ENA_terms_to_map ")
    ena_term_matches_dict = {} # format  { CHECKLIST_FIELD_NAME: { match: right_term, ena_mapping_note: ""} #
    df_ncbi = data_files_dict['NCBI']['fields_df']

    ncbi_multi_name_dict = make_ncbi_multiname_dict(df_ncbi)
    logger.info(f"ncbi_multi_name_dict keys {ncbi_multi_name_dict.keys()}")

    logging.info(df_ncbi.head())
    logger.info(data_files_dict['ENA'].keys())
    df_ena = data_files_dict['ENA']['fields_df']
    df_ena_working = df_ena.copy()
    logging.info(df_ena.head())
    logging.info(df_ena.columns)
    #harmonised name

    def get_df_lists(df_left, left_set, left_col, right_col):
        """
        need to them back in the right order
        :param df_left:
        :param left_set:
        :param left_col:
        :param right_col:
        :return:
        """
        logger.info("WTF")

    def get_ncbi_harmonised_mapped_list(ncbi_multi_name_dict, name_key, sorted_names):
        """
        This is to allow one to get the 'NCBI harmonised name"
        :param ncbi_multi_name_dict:
        :param name_key:
        :param sorted_names:
        :return:
        """
        ncbi_harmonised_list = []
        if name_key not in ncbi_multi_name_dict:
            logger.error(
                f"ERROR: get_ncbi_harmonised_mapped_list  key-->{name_key}<-- not present ncbi_multi_name_dict, contact Peter and get the code fixed")
            sys.exit(-1)
        # logger.info(sorted_names)
        for name in sorted_names:
           logger.debug(f"-->{name}<--")
           if name == '':
               continue
           elif name in ncbi_multi_name_dict[name_key]:
               logger.debug(f"-->name<--")
               ncbi_harmonised_list.append(ncbi_multi_name_dict[name_key][name])
           else:
               logger.error(f"ERROR: get_ncbi_harmonised_mapped_list  -->{name}<-- not present in name_key={name_key}, contact Peter and get the code fixed")
               logger.debug(ncbi_multi_name_dict[name_key])
               # ERROR: get_ncbi_harmonised_mapped_list  -->geographic location (country and/or sea)<-- not present in name_key=synonym, contact Peter and get the code fixed

               sys.exit(-1)
        return ncbi_harmonised_list

    def remove_ena_rows_now_matched(df_ena_working, ena_field, ena_field_list):
        """
        ena_field for example CHECKLIST_FIELD_NAME
        :param df_ena_working:
        :param ena_field_list:
        :return:
        """
        logger.info(f"inside remove_ena_rows_now_matched for {ena_field} and list of len= {len(ena_field_list)} examples: {ena_field_list[0:5]}")
        logger.debug(df_ena_working.head(2))
        logger.debug(f"df_ena_working[ena_field].head(5) = \n{df_ena_working[ena_field].head(3)}")
        if ena_field == 'CHECKLIST_FIELD_NAME':
            df_ena_working = df_ena_working.query('CHECKLIST_FIELD_NAME not in @ena_field_list')
        elif ena_field == 'SHORT_FIELD_NAME_FROM_MIXS_LINKML':
            df_ena_working = df_ena_working.query('SHORT_FIELD_NAME_FROM_MIXS_LINKML not in @ena_field_list')
        else:
            logger.error(f"not recognising {ena_field} in remove_ena_rows_now_matched")
            sys.error()
        logger.info(f"\tafter updated df_ena_working len {len(df_ena_working)}")
        return df_ena_working

    ena_long_name_set = set(df_ena['CHECKLIST_FIELD_NAME'])
    logger.info(f"ena initial name total = {len(ena_long_name_set)}")
    ncbi_short_name_set = set(df_ncbi['Name'])
    logger.info(f"NCBI initial name total = {len(ncbi_short_name_set)}")

    logger.info("-----Matching ENA CHECKLIST_FIELD_NAME with NCBI harmonised name")
    ncbi_harmonised_name_set = set(df_ncbi['Harmonized name'])
    ena_long_name_set = set(df_ena_working['CHECKLIST_FIELD_NAME'])
    ena_long_ncbi_harmonised_intersection_set = ena_long_name_set.intersection(ncbi_harmonised_name_set)
    logger.info(f"ena_long_ncbi_harmonised_intersection_set len = {len(ena_long_ncbi_harmonised_intersection_set)}")
    note_text = "exact_match_2_ncbi_harmonised_name"
    note_list = create_note4all_list(note_text, len(ena_long_ncbi_harmonised_intersection_set))
    sorted_list = sorted(ena_long_ncbi_harmonised_intersection_set)
    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, sorted_list, sorted_list, note_list)
    df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'CHECKLIST_FIELD_NAME', list(ena_long_ncbi_harmonised_intersection_set))
    print_simple_dict(ena_term_matches_dict, note_text)

    print('-----------------------------------------------------------------------------------------------------')
    logger.info("-----Matching ENA CHECKLIST_FIELD_NAME with NCBI short name")
    ena_long_ncbi_short_intersection_set = ena_long_name_set.intersection(ncbi_short_name_set)
    logger.info(f"ena_long_ncbi_short_intersection_set {len(ena_long_ncbi_short_intersection_set)}")
    note_text = "exact_match_2_ncbi_name"
    note_list = create_note4all_list(note_text, len(ena_long_ncbi_short_intersection_set))
    sorted_list = sorted(ena_long_ncbi_short_intersection_set)
    sorted_ncbi_harmonised_list = get_ncbi_harmonised_mapped_list(ncbi_multi_name_dict, 'name', sorted_list)
    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, sorted_list, sorted_ncbi_harmonised_list, note_list)
    logging.info(f"len(ena_term_matches_dict) {len(ena_term_matches_dict)}")
    df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'CHECKLIST_FIELD_NAME', list(ena_long_ncbi_short_intersection_set))
    print_simple_dict(ena_term_matches_dict, note_text)
    #
    logger.info("-----Matching ENA short name(via MIXS_LINKML) with NCBI harmonised name")
    ena_short_name_set = set(df_ena_working['SHORT_FIELD_NAME_FROM_MIXS_LINKML'])
    ena_short_ncbi_harmonised_intersection_set = ena_short_name_set.intersection(ncbi_harmonised_name_set)
    logger.info(f"ena_short_ncbi_harmonised_intersection_set len= {len(ena_short_ncbi_harmonised_intersection_set)}")
    df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'SHORT_FIELD_NAME_FROM_MIXS_LINKML',
                                                 list(ena_short_ncbi_harmonised_intersection_set))
    note_list = create_note4all_list("exact_match_ena_short_2_ncbi_harmonised_name", len(ena_short_ncbi_harmonised_intersection_set))
    sorted_list = list(ena_short_ncbi_harmonised_intersection_set)

    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, list(ena_short_ncbi_harmonised_intersection_set),
                                                sorted_list, note_list)

    logger.info("-------Matching ENA synonyms with NCBI (short)Name---------")
    ena_synonym_dict = generate_syn_dict(df_ena_working, "SYNONYMS", "CHECKLIST_FIELD_NAME")
    ena_synonym_set = set(ena_synonym_dict.keys())
    ena_syn_ncbi_short_intersection_list = sorted(ena_synonym_set.intersection(ncbi_short_name_set))
    ena_fieldname_syn_intersection_list = get_name_centric_matches('ena_synonym',  ena_synonym_dict,
                                                                   ena_syn_ncbi_short_intersection_list)
    logger.info(f"ena_syn_ncbi_short_intersection_list len = {len(ena_syn_ncbi_short_intersection_list)}")
    logger.info("Adding info to ena_term_matches_dict ---------")
    df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'CHECKLIST_FIELD_NAME', ena_fieldname_syn_intersection_list)
    note_list = create_note4all_list("exact_match_ena_syn_ncbi_short_name", len(ena_fieldname_syn_intersection_list))
    # logger.info(f"ena_term_matches_dict keys = {ena_term_matches_dict.keys()}")
    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, ena_fieldname_syn_intersection_list,
                                                get_ncbi_harmonised_mapped_list(ncbi_multi_name_dict,'name', ena_syn_ncbi_short_intersection_list), note_list)

    logger.info("-------Matching ENA synonyms with NCBI Harmonised Name---------")
    ena_synonym_dict = generate_syn_dict(df_ena_working, "SYNONYMS", "CHECKLIST_FIELD_NAME")
    ena_synonym_set = set(ena_synonym_dict.keys())
    ena_syn_ncbi_harmonised_intersection_list = sorted(ena_synonym_set.intersection(ncbi_harmonised_name_set))
    logger.info(f"ena_syn_ncbi_harmonised_intersection_list: {ena_syn_ncbi_harmonised_intersection_list}")
    ena_fieldname_ncbi_harmonised_intersection_list = get_name_centric_matches('ena_synonym', ena_synonym_dict,
                                                                     ena_syn_ncbi_harmonised_intersection_list)
    logger.info(f"ena_fieldname_ncbi_harmonised_intersection_list {len(ena_fieldname_ncbi_harmonised_intersection_list)}")

    logger.info("Adding info to ena_term_matches_dict ---------")
    note_text = 'exact_match_ena_syn_ncbi_harmonised_name'
    note_list = create_note4all_list(note_text, len(ena_fieldname_ncbi_harmonised_intersection_list))
    df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'CHECKLIST_FIELD_NAME',
                                                 list(ena_fieldname_ncbi_harmonised_intersection_list))
    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, ena_fieldname_ncbi_harmonised_intersection_list,
                                                ena_syn_ncbi_harmonised_intersection_list, note_list)
    print_simple_dict(ena_term_matches_dict, note_text)

    logger.info("-------------------------------------------------------------")
    logger.info("-------Matching ENA synonyms with NCBI synonyms---------")
    ncbi_synonym_set = clean_ncbi_syn(set(df_ncbi['Synonyms']))
    logger.info(df_ena_working.columns)
    ena_synonym_set = clean_ncbi_syn(set(df_ena_working['SYNONYMS']))
    ena_syn_ncbi_syn_list = sorted(ena_synonym_set.intersection(ncbi_synonym_set))
    logger.info(f"ena_syn_ncbi_syn_list matching syn len= {len(ena_syn_ncbi_syn_list)}")
    logger.debug(f"ena_synonym_dict keys------{ena_synonym_dict.keys()}")
    ncbi_harmonised_name_set = get_ncbi_harmonised_mapped_list(ncbi_multi_name_dict, 'synonym', ena_syn_ncbi_syn_list)
    ena_fieldnames_ncbi_syn_by_checklist_name_list = get_name_centric_matches('ena_synonym', ena_synonym_dict, ena_syn_ncbi_syn_list)
    logger.info(f"++++++++++ena_fieldnames_ncbi_syn_by_checklist_name_set len={len(ena_fieldnames_ncbi_syn_by_checklist_name_list)} examples {ena_fieldnames_ncbi_syn_by_checklist_name_list[0:3]}")
    note_text = 'exact_match_ena_syn_ncbi_syns'
    note_list = create_note4all_list(note_text, len(ena_fieldnames_ncbi_syn_by_checklist_name_list))
    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, ena_fieldnames_ncbi_syn_by_checklist_name_list,
                                                ncbi_harmonised_name_set, note_list)
    print_simple_dict(ena_term_matches_dict, note_text)
    df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'CHECKLIST_FIELD_NAME', ena_fieldnames_ncbi_syn_by_checklist_name_list)
    logger.info(f"df_ena_working len = {len(df_ena_working)}")

    ena_long_name_set = set(df_ena_working['CHECKLIST_FIELD_NAME'])
    logger.info(f"ena_long_name_set len = {len(ena_long_name_set)}")
    logger.info(f"ena_term_matches_dict keys len------{len(ena_term_matches_dict.keys())}")


    logger.info("------------Fuzzy matching with 'NCBI_name'")
    ena_terms_matched_sorted, ncbi_name_matched_sorted = run_process_fuzzy_matches(df_ena, df_ena_working,'ENA_long_name', 'ncbi_short_name', list(ena_long_name_set), list(ncbi_short_name_set))
    df_ena_working = remove_ena_rows_now_matched(df_ena_working,'CHECKLIST_FIELD_NAME', ena_terms_matched_sorted)
    logger.info(f"df_ena_working len = {len(df_ena_working)}")
    ncbi_harmonised_name_list = get_ncbi_harmonised_mapped_list(ncbi_multi_name_dict, 'name', ncbi_name_matched_sorted)
    note_text = 'fuzzy_match_ena_ncbi_name'
    note_list = create_note4all_list(note_text, len(ena_terms_matched_sorted))
    logger.info(f"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, ena_terms_matched_sorted,
                                                ncbi_harmonised_name_list, note_list)
    print_simple_dict(ena_term_matches_dict, note_text)


    logger.info("------------Fuzzy matching with 'NCBI_harmonised_name'")
    ena_long_name_set = set(df_ena_working['CHECKLIST_FIELD_NAME'])
    ena_terms_matched_sorted, ncbi_harmonised_name_matched_sorted = run_process_fuzzy_matches(df_ena, df_ena_working,'ENA_long_name', 'NCBI_harmonised_name', list(ena_long_name_set), list(ncbi_short_name_set))

    if len(ena_terms_matched_sorted) > 0:
        df_ena_working = remove_ena_rows_now_matched(df_ena_working, 'CHECKLIST_FIELD_NAME', ena_terms_matched_sorted)
        logger.info(f"df_ena_working len = {len(df_ena_working)}")
        note_text = 'fuzzy_match_ena_ncbi_harmonised_name'
        note_list = create_note4all_list(note_text, len(ena_terms_matched_sorted))
        ena_term_matches_dict = update_mapping_dict(ena_term_matches_dict, ena_terms_matched_sorted,
                                                ncbi_harmonised_name_matched_sorted, note_list)
        print_simple_dict(ena_term_matches_dict, note_text)
    else:
        logger.info(f"No valid extra fuzzy hits, so skipping")
        print_simple_dict(ena_term_matches_dict, '')

    logger.info(f"phew got process_ENA_terms_to_map function pretty much working")
    data_files_dict['ena_term_matches_dict'] = ena_term_matches_dict

    add_ena_notes(data_files_dict)

    return data_files_dict



def process_NCBI_DDBJ(data_files_dict):
    logging.info(msg="process_NCBI_DDBJ================================================")
    df_ncbi = data_files_dict['NCBI']['fields_df']
    logging.info(df_ncbi.head())
    df_ddjb = data_files_dict['DDBJ']['fields_df']
    logging.info(df_ncbi.head())
    logging.info(df_ncbi.columns)
    ncbi_harmonised_name_set = set(df_ncbi['Harmonized name'].to_list())
    logging.info(msg = len(ncbi_harmonised_name_set))
    logging.info(msg = df_ddjb.head())
    logging.info(msg = df_ddjb.columns)
    ddbj_name_set = set(df_ddjb['Name'].to_list())
    logging.info(msg = len(ddbj_name_set))
    ddbj_ncbi_intersect_set = ddbj_name_set.intersection(ncbi_harmonised_name_set)
    print(f"intersect of ddbj and ncbi count={len(ddbj_ncbi_intersect_set)}")
    ddbj_only_set = ddbj_name_set.difference(ncbi_harmonised_name_set)
    logging.info(ddbj_only_set)

    mapped_df = data_files_dict['mapped_df']
    mapped_df = add_in_easy_mappings(mapped_df, 'NCBI_mapped_name', 'DDBJ_mapped_name', ddbj_ncbi_intersect_set)

    ddbj_df = prefix_name2columns('DDBJ:', data_files_dict['DDBJ']['fields_df'])
    data_files_dict['mapped_df'] = add_in_site_specific_names(mapped_df, ddbj_only_set, ddbj_df, 'DDBJ:Name', 'DDBJ_mapped_name')
    data_files_dict = add_mapping_corrections(data_files_dict, 'DDBJ')
    logging.info(data_files_dict['mapped_df'].head())

    logging.info(data_files_dict['mapped_df'].columns)
    mapped_df = data_files_dict['mapped_df']
    logger.info(mapped_df['DDBJ_mapped_note'].value_counts())
    generate_stats(data_files_dict)


    return data_files_dict

def print_mapped_3_head(mapped_df):
    tmp_mapped_df = mapped_df[['DDBJ_mapped_name', 'ENA_mapped_name', 'NCBI_mapped_name']]
    logger.info("\n" + tmp_mapped_df.head().to_markdown(index=False))

def map_field_names(data_files_dict):
    """
    using the NCBI as the "master" and building from that, as the DDJB is very similar
    data_files_dict['mapped_df'] = mapped_df    # this is the core!
    :param data_files_dict:
    :return:
    """
    logging.warning(msg = "************ map_field_names *************")
    mapped_df = data_files_dict['NCBI']['fields_df'].copy()
    logger.info(mapped_df.columns)

    mapped_df.rename(columns={'Name': 'NCBI:Name', 'Harmonized name': 'NCBI:Harmonized_name', 'Synonyms': 'NCBI:Synonyms',
                              'Description': 'NCBI:Description', 'Rule': 'NCBI:Rule',
                              'Format': 'NCBI:Format'}, inplace=True)
    mapped_df['NCBI_mapped_name'] = mapped_df['NCBI:Harmonized_name']  # populating NCBI_mapped_name
    mapped_df['ENA_mapped_name'] = ""
    mapped_df['DDBJ_mapped_name'] = ""
    mapped_df = mapped_df[['DDBJ_mapped_name', 'ENA_mapped_name', 'NCBI_mapped_name',
     'NCBI:Name', 'NCBI:Harmonized_name', 'NCBI:Synonyms',
     'NCBI:Description', 'NCBI:Rule', 'NCBI:Format']]
    print_mapped_3_head(mapped_df)
    data_files_dict['mapped_df'] = mapped_df
    logger.info(mapped_df.columns)

    data_files_dict = process_NCBI_DDBJ(data_files_dict)
    logging.info(msg = "map NCBI and DDBJ")
    print(mapped_df[['NCBI_mapped_name', 'ENA_mapped_name', 'DDBJ_mapped_name']].head())

    data_files_dict = process_ENA_terms_to_map(data_files_dict)
    #     sys.exit()
    logger.info("leaving map_field_names")
    return data_files_dict


def add_mapping_corrections(data_files_dict, INSDC_site):
    """
    This allows for not automated curations
    Currently this is fairly static, it needs one to manually create a data structure here. It could be read in.
    :param data_files_dict:
    :param INSDC_site:
    :return: data_files_dict
    """
    logging.info(msg="add_mapping_corrections")

    logging.info(data_files_dict.keys())

    ddbj_omics_note = 'DDBJ-only Omics package used for samples of GEA (counterpart of GEO/ArrayExpress) and MetaboBank (counterpart of MetaboLights). The Omics package consists of frequently used attributes (sample characteristics) of GEO and ArrayExpress when the package was created. So these attribues are used in NCBI/EBI BioSamples but not included in your packages/checklists because BioSamples are generated from GEO/ArrayExpress sample characteristics, on the other hand, BioSamples are pre-registered for GEA/MetaboBank submissions by using the Omics package.'
    notes_dict = {'DDBJ':
                      {'antibody': {'mapping_note': 'used in ChIPSeq.'},
                       'infection': {'mapping_note': ddbj_omics_note},
                       'stress': {'mapping_note': ddbj_omics_note},
                       'time': {'mapping_note': ddbj_omics_note}
                       }
                  }
    logger.info(data_files_dict[INSDC_site].keys())
    logger.info(notes_dict[INSDC_site].keys())
    logger.info(msg=notes_dict)
    df = data_files_dict['mapped_df']

    source_mapped_name = INSDC_site + "_mapped_name"
    target_mapped_name = INSDC_site + "_mapped_note"

    logger.info(f"source_mapped_name={source_mapped_name} and target_mapped_name={target_mapped_name}")
    count = 0
    for name in notes_dict[INSDC_site].keys():
           #logging.info(f"{name}")
           df.loc[df[source_mapped_name] == name, target_mapped_name] = notes_dict[INSDC_site][name]['mapping_note']

           count = count + 1

    data_files_dict['mapped_df'] = df
    return data_files_dict


def get_INSDC_site_names():
    return sorted(['NCBI', 'ENA', 'DDBJ'])

def generate_stats(data_files_dict):
    print("++++++++++++++ Generate Statistics ++++++++++++++")
    logger.info(data_files_dict.keys())
    mapped_df = data_files_dict['mapped_df']
    print(mapped_df.columns)
    mapped_df = mapped_df.fillna('')
    sites = get_INSDC_site_names()

    total_combined_entries = mapped_df.shape[0]
    print(f"total_combined_entries {total_combined_entries}")
    for site in sites:
        mapped_name = site + "_mapped_name"
        total_site_entries = mapped_df.loc[mapped_df[mapped_name] != ""].shape[0]
        print(f"total {site} entries {total_site_entries}")

    #df_tmp_ena = mapped_df['ENA_mapped_name']
    # slim_mapped_df = mapped_df[['ENA_mapped_name', 'NCBI_mapped_name', 'DDBJ_mapped_name']]


def main():
    logger.warning(msg='in main (should be yellow)')
    logger.info(msg = '          (should be green)')
    data_files_dict = populate_input_data_structure()
    logging.info(msg= (data_files_dict.keys()))
    data_files_dict = map_field_names(data_files_dict)
    generate_stats(data_files_dict)


    logger.info("finished......")

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(name = 'mylogger')
    coloredlogs.install(logger = logger)
    logger.propagate = False
    ch = logging.StreamHandler(stream = sys.stdout)
    ch.setFormatter(fmt = my_coloredFormatter)
    logger.addHandler(hdlr = ch)
    logger.setLevel(level = logging.INFO)

    logger.warning('colors')
    logger.info(msg="testing, should be green")

    logging.debug("inside main")

    main()
