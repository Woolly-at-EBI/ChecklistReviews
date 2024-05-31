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
    return mapped_df

def generate_syn_dict(df_ena_working,synonym_col,field_name_col):
        """ generate_syn_dict

        :param df_ena_working:
        :return: ena_synonym_dict
        """
        logger.info(f"df_ena_working len {len(df_ena_working)}")
        ena_synonym_dict = dict(zip(df_ena_working[synonym_col], df_ena_working[field_name_col]))
        logger.info(f"ena_synonym_dict len {ena_synonym_dict}")
        ena_synonym_dict.pop('\n', None)

        ena_synonym_set = set(ena_synonym_dict.keys())
        logger.info(f"ena_synonym_set len {len(ena_synonym_set)}")

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
        logger.info(f"ena_synonym_dict len {len(clean_syn_dict)}")
        return clean_syn_dict
def get_name_centric_matches(synonym2fieldname_dict, synonym_hit_set):
    """
            # need to add ENA_mapping_note: "mapped_on_synonyms"
    :param synonym2fieldname_dict:
    :param synonym_hit_set:
    :return:
    """
    fieldname_syn_intersection_set = set()
    for ena_syn in synonym_hit_set:
        if ena_syn in synonym2fieldname_dict:
            # logger.info(f"-->{ena_syn}<-- matching-->{synonym2fieldname_dict[ena_syn]}<--")
            fieldname_syn_intersection_set.add(synonym2fieldname_dict[ena_syn])
    logger.info(f"fieldname_syn_intersection_set len = {len(fieldname_syn_intersection_set)}")

    return fieldname_syn_intersection_set

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
        fuzzy_medium_confidence_dict = get_fuzzy_matches(left_name, right_name, left_list, right_list)
        logger.info(fuzzy_medium_confidence_dict)
        ena_long_name_set = set(df_ena['CHECKLIST_FIELD_NAME'])
        left_terms_matched_set = set()
        for left_term in fuzzy_medium_confidence_dict.keys():
            right_term, fuzzy_score = fuzzy_medium_confidence_dict[left_term]
            logger.info(f"Fuzzy match for -->{left_term}<-- -->{right_term}<-- with {fuzzy_score}")
            if right_term in ena_long_name_set:
                logger.info(f"\tright_term is already in ENA list: {right_term}")
            else:
                left_terms_matched_set.add(left_term)
        return left_terms_matched_set

def process_ENA_terms_to_map(data_files_dict):
    logging.info(data_files_dict.keys())
    logger.info(f"process_ENA_terms_to_map ")
    df_ncbi = data_files_dict['NCBI']['fields_df']
    logging.info(df_ncbi.head())
    logger.info(data_files_dict['ENA'].keys())
    df_ena = data_files_dict['ENA']['fields_df']
    logging.info(df_ena.head())
    logging.info(df_ena.columns)
    #harmonised name

    ena_long_name_set = set(df_ena['CHECKLIST_FIELD_NAME'])
    logger.info(f"ena initial name total = {len(ena_long_name_set)}")
    ncbi_long_name_set = set(df_ncbi['Name'])
    logger.info(f"NCBI initial name total = {len(ncbi_long_name_set)}")
    ncbi_harmonised_name_set = set(df_ncbi['Harmonized name'])
    ena_long_ncbi_long_intersection_set = ena_long_name_set.intersection(ncbi_long_name_set)
    logger.info(f"ena_long_ncbi_long_intersection_set {len(ena_long_ncbi_long_intersection_set)}")

    df_ena_working = df_ena.query('CHECKLIST_FIELD_NAME not in @ena_long_ncbi_long_intersection_set')
    logger.info(f"df_ena_working len {len(df_ena_working)}")
    ena_long_name_set = set(df_ena_working['CHECKLIST_FIELD_NAME'])
    ena_long_ncbi_harmonised_intersection_set = ena_long_name_set.intersection(ncbi_harmonised_name_set)
    logger.info(f"ena_long_ncbi_harmonised_intersection_set len = {len(ena_long_ncbi_harmonised_intersection_set)}")
    df_ena_working = df_ena_working.query('CHECKLIST_FIELD_NAME not in @ena_long_ncbi_harmonised_intersection_set')

    ena_short_name_set = set(df_ena_working['SHORT_FIELD_NAME_FROM_MIXS_LINKML'])
    ena_short_ncbi_harmonised_intersection_set = ena_short_name_set.intersection(ncbi_harmonised_name_set)
    logger.info(f"ena_short_ncbi_harmonised_intersection_set len= {len(ena_short_ncbi_harmonised_intersection_set)}")
    df_ena_working = df_ena_working.query('SHORT_FIELD_NAME_FROM_MIXS_LINKML not in @ena_short_ncbi_harmonised_intersection_set')

    ena_synonym_dict = generate_syn_dict(df_ena_working, "SYNONYMS", "CHECKLIST_FIELD_NAME")
    ena_synonym_set = set(ena_synonym_dict.keys())
    ena_syn_ncbi_long_intersection_set = ena_synonym_set.intersection(ncbi_long_name_set)
    logger.info(f"ena_syn_ncbi_long_intersection_set len = {len(ena_syn_ncbi_long_intersection_set)}")
    ena_syn_ncbi_harmonised_intersection_set = ena_synonym_set.intersection(ncbi_long_name_set)
    logger.info(f"ena_syn_ncbi_harmonised_intersection_set len = {len(ena_syn_ncbi_harmonised_intersection_set)}")
    ena_syn_ncbi_long_or_harmonised_intersection_set = ena_syn_ncbi_harmonised_intersection_set.union(ena_syn_ncbi_long_intersection_set)
    logger.info(f"ena_syn_ncbi_long_or_harmonised_intersection_set len = {len(ena_syn_ncbi_long_or_harmonised_intersection_set)}")

    ena_fieldname_syn_intersection_set = get_name_centric_matches(ena_synonym_dict, ena_syn_ncbi_long_or_harmonised_intersection_set)
    df_ena_working = df_ena_working.query('CHECKLIST_FIELD_NAME not in @ena_fieldname_syn_intersection_set')
    logger.info(f"df_ena_working len = {len(df_ena_working)}")

    ncbi_synonym_set = clean_ncbi_syn(set(df_ncbi['Synonyms']))
    logger.debug(ncbi_synonym_set)

    ena_long_ncbi_synonyms_intersection_set = ena_long_name_set.intersection(ncbi_synonym_set)
    logger.info(f"ena_long_ncbi_synonyms_intersection_set {len(ena_long_ncbi_synonyms_intersection_set)}")
    logger.info(f"ena_long_ncbi_synonyms_intersection_set = {ena_long_ncbi_synonyms_intersection_set}")
    df_ena_working = df_ena_working.query('CHECKLIST_FIELD_NAME not in @ena_long_ncbi_synonyms_intersection_set')
    logger.info(f"df_ena_working len = {len(df_ena_working)}")

    ena_long_ncbi_synonyms_intersection_set = ena_long_name_set.intersection(ncbi_synonym_set)
    logger.info(f"ena_long_ncbi_synonyms_intersection_set {len(ena_long_ncbi_synonyms_intersection_set)}")
    logger.info(f"ena_long_ncbi_synonyms_intersection_set = {ena_long_ncbi_synonyms_intersection_set}")
    df_ena_working = df_ena_working.query('CHECKLIST_FIELD_NAME not in @ena_long_ncbi_synonyms_intersection_set')
    logger.info(f"df_ena_working len = {len(df_ena_working)}")



    ena_long_name_set = df_ena_working['CHECKLIST_FIELD_NAME']
    logger.info(f"ena_long_name_set len = {len(ena_long_name_set)}")

    ena_terms_matched_set = run_process_fuzzy_matches(df_ena, df_ena_working,'ENA_long_name', 'NCBI_harmonised_name', list(ena_long_name_set), list(ncbi_harmonised_name_set))
    ena_long_name_set = df_ena_working['CHECKLIST_FIELD_NAME']
    logger.info(f"ena_long_name_set len = {len(ena_long_name_set)}")

    sys.exit()

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

    return data_files_dict

def print_mapped_3_head(mapped_df):
    tmp_mapped_df = mapped_df[['DDBJ_mapped_name', 'ENA_mapped_name', 'NCBI_mapped_name']]
    logger.info("\n" + tmp_mapped_df.head().to_markdown(index=False))

def map_field_names(data_files_dict):
    logging.warning(msg = "************ map_field_names *************")
    mapped_df = data_files_dict['NCBI']['fields_df'].copy()
    logger.info(mapped_df.columns)

    mapped_df.rename(columns={'Name': 'NCBI:Name', 'Harmonized name': 'NCBI:Harmonized name', 'Synonyms': 'NCBI:Synonyms',
                              'Description': 'NCBI:Description', 'Rule': 'NCBI:Rule',
                              'Format': 'NCBI:Format'}, inplace=True)
    mapped_df['NCBI_mapped_name'] = mapped_df['NCBI:Harmonized name']
    mapped_df['ENA_mapped_name'] = ""
    mapped_df['DDBJ_mapped_name'] = ""
    mapped_df = mapped_df[['DDBJ_mapped_name', 'ENA_mapped_name', 'NCBI_mapped_name',
     'NCBI:Name', 'NCBI:Harmonized name', 'NCBI:Synonyms',
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

def generate_stats(data_files_dict):
    print("++++++++++++++ Generate Statistics ++++++++++++++")
    logger.info(type(data_files_dict))
    logger.info(data_files_dict.keys())
    mapped_df = data_files_dict['mapped_df']
    print(mapped_df.columns)
    total_combined_entries = mapped_df.shape[0]
    print(f"total_combined_entries {total_combined_entries}")
    total_ncbi_entries = mapped_df.loc[~mapped_df['NCBI_mapped_name'].isna()].shape[0]
    print(f"total_ncbi_entries {total_ncbi_entries}")
    total_ddbj_entries = mapped_df.loc[~mapped_df['DDBJ_mapped_name'].isna()].shape[0]
    print(f"total_ddbj_entries {total_ddbj_entries}")
    total_ena_entries = mapped_df.loc[~mapped_df['ENA_mapped_name'].isna()].shape[0]
    print(f"total_ena_entries {total_ena_entries}")
    slim_mapped_df = mapped_df[['ENA_mapped_name', 'NCBI_mapped_name', 'DDBJ_mapped_name']]
    print(slim_mapped_df.query('ENA_mapped_name != ""'))
    print(slim_mapped_df.query('ENA_mapped_name != ""').columns)

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
