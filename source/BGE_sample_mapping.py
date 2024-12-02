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
import sys

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

def get_bge_ibol_field_list():
    return ['2D Barcode ID DNA','2D Barcode ID Tissue','Additional ID','Associated Specimens','Associated Taxa','Biobanked tissue type','Class','Collection Code','Collection Date Accuracy','Collection End Date','Collection Event ID','Collection Notes','Collection Start Date','Collectors','Coordinate Accuracy','Country/ Ocean','DNA Biobank ID','DNA Biobank Name','DNA Concentration [ng/µL]','DNA Volume [µL]','Depth','Depth Precision','ENA Sample Accession','ENA_BIOSAMPLE_ID','ENA_PROJECT_ID','Elev','Elevation Precision','Event Time','Exact Site','External URLs','Extra Info','Extraction Date','Extraction Method','Extraction Staff or Lab','Family','Field ID','GGBN Upload Mechanism','GPS Source','Genus','Habitat','Identification Date','Identification Method','Identifier','Identifier Email','Identifier ORCID','Institution Storing','Lab status','Lat','Life Stage','Lon','Museum ID','NCBI Tax ID','Notes','Order','Permits','Phylum','Plate ID','Preparation Type (DNA)','Preparation type (Tissue)','Preservation history','Quantification Date','Quantification Method','Region','Relation To Voucher','Reproduction','Sample Alias','Sample ID','Sampling Protocol','Sector','Sex','Site Code','Species','State/ Province','Subfamily','Subspecies','Taxonomy Notes','Tissue Biobank ID','Tissue Biobank Name','Tissue Descriptor','Tissue biobanked?','Tribe','Type Status','Type of Additional ID','Voucher Status','Voucher preservation','Well Position','institution ID']


def get_old_bge_ibol_field_list():
    return ['Associated Specimens','Associated Taxa','Class','Collection Date','Collection End Date','Collection Event ID','Collection Notes','Collection code','Collectors','Coordinate Accuracy','Country/Ocean','Depth','Depth Precision','Elev','Elevation Precision','Event Time','Exact Site','External URLs','Family','Field ID','GPS source','Genus','Habitat','Identification Method','Identifier','Identifier Email','Institution storing','Lat','Life Stage','Long','Museum ID','Notes','Order','Phylum','Region','Reproduction','Sample ID','Sampling Protocol','Sector','Sex','Site Code','Species','State/Province','Subfamily','Subspecies','Taxonomy Notes','Tissue Descriptor','Tribe','Voucher Status']

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

    :param fuzzy_threshold:
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


def compare_ibol_lists():
    new_bge_ibol_field_set =  set(get_bge_ibol_field_list())
    old_bge_ibol_field_set =  set(get_old_bge_ibol_field_list())
    print(f"new_bge_ibol_field_set total={len(new_bge_ibol_field_set)}")
    print(f"old_bge_ibol_field_set total={len(old_bge_ibol_field_set)}")
    intersection_set = new_bge_ibol_field_set & old_bge_ibol_field_set
    print(f"intersection total={len(intersection_set)}")
    print(f"unique to old_bge_ibol_field_set={sorted(old_bge_ibol_field_set.difference(new_bge_ibol_field_set))}")
    print(f"unique to new_bge_ibol_field_set={sorted(new_bge_ibol_field_set.difference(old_bge_ibol_field_set))}")


def main():
    compare_ibol_lists()
    sys.exit()

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
