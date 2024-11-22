#!/usr/bin/env python3
"""Script of BGE_sample_mapping.py is to BGE_sample_mapping.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2024-11-21
__docformat___ = 'reStructuredText'

"""


import logging
logger = logging.getLogger(__name__)
import os
import pandas as pd
from pairwise_term_matches import compareAllTerms

class BGE_sample_mapping:

    def parse_bg_mapping_file(self):
        # file_name = "../data/BGE_sample_metadata_mapping.xlsx" - old one
        file_name = "../data/BGE_sample_metadata_mapping_v2.xlsx"
        logger.info(f"file={file_name}")
        xls_obj = pd.ExcelFile(file_name)
        logger.info(f"sheets{xls_obj.sheet_names}")

        df_dict  = {}

        for sheet_name in xls_obj.sheet_names:

            my_df = pd.read_excel(file_name, sheet_name=sheet_name)
            if sheet_name in self.sheet_mapping_dict:
                my_df_name = self.sheet_mapping_dict[sheet_name]['name']
            else:
                my_df_name = sheet_name
            logger.info(f"sheet=>{sheet_name}<= key_now =>{my_df_name}<=")
            df_dict[my_df_name] = my_df
        return df_dict


    def __init__(self):
        self.sheet_mapping_dict = {
        'BCDM fields_April24': { 'name': 'bcdm_old'},
        'BCDM fields_Nov24': {'name': 'bcdm'},
        'bcdm': { 'name': 'bcdm', 'field_name_column': 'field', 'description': 'definition', 'data_type': 'data_type' },
        'bcdm_old': {'name': 'bcdm_old', 'field_name_column': 'field', 'description': 'definition',
                     'data_type': 'data_type'},

        }
        self.df_dict = self.parse_bg_mapping_file()

    def get_target_fields_df(self, target):
        if target in self.sheet_mapping_dict:
            my_df_name = self.sheet_mapping_dict[target]['name']
        else:
            my_df_name = target
        return self.df_dict[my_df_name]

    def get_target_field_list(self, target):
        my_df = self.get_target_fields_df(target)
        target_column = self.sheet_mapping_dict[target]['field_name_column']
        logger.info(f"target_column={target_column}")

        field_list = sorted(my_df[target_column].unique())
        logger.debug(f"field_list={field_list}")
        return field_list

    def get_target_field_dict(self, target):
        my_df = self.get_target_fields_df(target)
        target_column = self.sheet_mapping_dict[target]['field_name_column']
        logger.info(f"target_column={target_column}")

        return my_df.to_dict(orient='records')


    def print_stats(self):
        print("BGE_sample_mapping - print_stats")


def exact_compare2lists(source_list, target_list, outfile):
    """

    :param outfile:
    :param source_list:
    :param target_list:
    :return:   df: # left_term match_type        match  fuzzy_score  match_term_duplicated
    """
    logger.info(f"source_list total={len(source_list)} target_list total={len(target_list)}")

    source_set = set(source_list)
    target_set = set(target_list)
    print(f"common to both source and target set(total={len(source_set.intersection(target_set))}) ={sorted(source_set.intersection(target_set))}")
    print(f"unique to source set={sorted(source_set.difference(target_set))}")
    print(f"unique to target set={sorted(target_set.difference(source_set))}")


def fuzzy_compare2lists(source_list, target_list, fuzzy_threshold, outfile):
    """

    :param outfile:
    :param source_list:
    :param target_list:
    :return:   df: # left_term match_type        match  fuzzy_score  match_term_duplicated
    """
    df = compareAllTerms(source_list, target_list, fuzzy_threshold)
    logger.info(f"write to {outfile}")
    df.to_csv(outfile, index=False, sep="\t")

    for match_type in ['exact', 'fuzzy']:
        filter_df = df.query('match_type == @match_type')
        logger.info(f"match_type=\n{filter_df.head(100).to_markdown(index=False)}")

def get_ena_field_names():
    """

    :return: sorted(field_names_set)
    """
    file_name = '/Users/woollard/projects/eDNAaquaPlan/wp2/ena_in/ena_checklists_mandatory_or_not.tsv'
    df = pd.read_csv(file_name, sep='\t', index_col=0)
    logger.debug(df.head())
    field_names_set = set(df['CHECKLIST_FIELD_NAME'].to_list())
    logger.debug(f"field_names_set length: {len(field_names_set)}")

    return sorted(field_names_set)

def main():
    BGE_sample_mapping_obj = BGE_sample_mapping()
    BGE_sample_mapping_obj.print_stats()
    out_data_dir = "../data/out_files"

    field_list_dict = {}

    for target in ['bcdm', 'bcdm_old']:

        field_list_dict[target] = BGE_sample_mapping_obj.get_target_field_list(target)
        logger.debug(f"{target}={field_list_dict[target]}")


    ena_field_names_list = get_ena_field_names()
    logger.info(f"ena_field_names_list total={len(ena_field_names_list)}")

    for target in ['bcdm']:
        out_file = os.path.join(out_data_dir, f"{target}_ena_field_list.txt")

        fuzzy_compare2lists(field_list_dict['bcdm'], ena_field_names_list, 75, out_file)

        print("\n--------Comparison of source=bcdm of new(Nov 2024) and target=old(April 2024))---------")
        exact_compare2lists(field_list_dict['bcdm'], field_list_dict['bcdm_old'], out_file)


if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format = '%(levelname)s - %(message)s')
    main()
