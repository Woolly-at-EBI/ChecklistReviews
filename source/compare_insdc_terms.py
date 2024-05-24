#!/usr/bin/env python3
"""Script of compare_insdc_terms.py is to compare_insdc_terms.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2024-05-24
__docformat___ = 'reStructuredText'
chmod a+x compare_insdc_terms.py
"""
import sys

from icecream import ic
import os
import argparse
import pandas as pd


def checklist_field_stats(site, df):
    ic(site)
    ic(f"Total number of terms = {len(df)}")

def get_data_files_dict():
    data_files_dict = {
        'ENA': {"packages": "EBI - Package", "fields": 'ENA - Attribute'},
        'DDBJ': {"packages": 'DDBJ - Package', "fields": 'DDBJ - Attribute'},
        'NCBI': {"packages": 'NCBI - Package', "fields": 'NCBI - Attribute'}
    }
    return data_files_dict

def get_attribute_dfs(combined_xlsx_file, data_files_dict):
    ic()
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
    ic()
    combined_xlsx_file = '/Users/woollard/projects/ChecklistReviews/data/INSDC_WORK/package_or_checklist_attributes_INSDC-2.xlsx'
    data_files_dict = get_data_files_dict()
    data_files_dict = get_attribute_dfs(combined_xlsx_file, data_files_dict)
    return data_files_dict

def map_field_names(data_files_dict):
    ic("map NCBI and DDJB")
    df_ncbi = data_files_dict['NCBI']['fields_df']
    df_ddjb = data_files_dict['DDBJ']['fields_df']
    ic(df_ncbi.head())
    ic(df_ncbi.columns)
    ncbi_harmonised_name_set = set(df_ncbi['Harmonized name'].to_list())
    ic(len(ncbi_harmonised_name_set))
    ic(df_ddjb.head())
    ic(df_ddjb.columns)
    ddbj_name_set = set(df_ddjb['Name'].to_list())
    ic(len(ddbj_name_set))
    ddbj_ncbi_intersect_set = ddbj_name_set.intersection(ncbi_harmonised_name_set)
    print(f"intersect of ddbj and ncbi count={len(ddbj_ncbi_intersect_set)}")
    ddbj_only_set = ddbj_name_set.difference(ncbi_harmonised_name_set)
    ic(ddbj_only_set)





def main():
    data_files_dict = populate_input_data_structure()
    ic(data_files_dict.keys())
    map_field_names(data_files_dict)


if __name__ == '__main__':
    ic()
    main()
