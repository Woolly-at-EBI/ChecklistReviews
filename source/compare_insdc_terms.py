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
    site_df = site_df.set_index(site_df_name2index)
    site_only_list = list(site_only_set)
    tmp_df = site_df.loc[site_only_list]
    #print("=========================================================")
    logger.info(f"{site_df_mapped_name} len of site_only_set  {len(site_only_set)}")
    logger.info(f"{site_df_mapped_name} len of df to merge in {len(tmp_df)}")
    mapped_df = pd.concat([mapped_df, tmp_df])
    logger.info(mapped_df.head())

    return mapped_df

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
    mapped_df = add_in_site_specific_names(mapped_df, ddbj_only_set, ddbj_df, 'DDBJ:Name', 'DDBJ_mapped_name')


    data_files_dict = add_mapping_corrections(data_files_dict, 'DDBJ')
    logging.info(ddbj_df.head())

    data_files_dict['mapped_df'] = mapped_df
    return data_files_dict

def map_field_names(data_files_dict):
    logging.warning(msg = "************ map_field_names *************")
    mapped_df = data_files_dict['NCBI']['fields_df'].copy()
    logging.info(mapped_df.columns)

    mapped_df.rename(columns={'Name': 'NCBI:Name', 'Harmonized name': 'NCBI:Harmonized name', 'Synonyms': 'NCBI:Synonyms',
                              'Description': 'NCBI:Description', 'Rule': 'NCBI:Rule',
                              'Format': 'NCBI:Format'}, inplace=True)
    mapped_df['NCBI_mapped_name'] = mapped_df['NCBI:Harmonized name']
    mapped_df['ENA_mapped_name'] = ""
    mapped_df['DDBJ_mapped_name'] = ""
#
    data_files_dict['mapped_df'] = mapped_df

    data_files_dict = process_NCBI_DDBJ(data_files_dict)
    logging.info(msg = "map NCBI and DDBJ")
    print(mapped_df[['NCBI_mapped_name', 'ENA_mapped_name', 'DDBJ_mapped_name']].head())
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



def main():
    logger.warning(msg='in main (should be yellow)')
    logger.info(msg = '          (should be green)')
    data_files_dict = populate_input_data_structure()
    logging.info(msg= (data_files_dict.keys()))
    data_files_dict = map_field_names(data_files_dict)


    logger.info("finished......")

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(name = 'mylogger')
    coloredlogs.install(logger = logger)
    logger.propagate = False
    ch = logging.StreamHandler(stream = sys.stdout)
    ch.setFormatter(fmt = my_coloredFormatter)
    logger.addHandler(hdlr = ch)
    logger.setLevel(level = logging.DEBUG)

    logger.warning('colors')
    logger.info(msg="testing, should be green")

    logging.debug("inside main")

    main()
