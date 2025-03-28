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
from ena_info import EnaInfo

def get_out_dir():
    return "../data/"

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
        logger.info(f"in get_target_fields_df target={target}===")
        if target in self.sheet_mapping_dict:
            my_df_name = self.sheet_mapping_dict[target]['name']
        else:
            my_df_name = target
        # logger.info(f"all targets = {sorted(self.df_dict)}")
        # print(self.df_dict[my_df_name])
        # logger.info(f"columns={sorted(self.df_dict[my_df_name].columns)}")
        # logger.info(type(my_df_name))

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

    def get_bcdm_field_list(self):
        return sorted(self.get_target_field_list(target='bcdm'))

    def print_stats(self):
        print("BGE_sample_mapping - print_stats")
        sheet_name_list = sorted(self.df_dict)
        print(f"sheet_names: {sheet_name_list}")
        # print(f"bcdm terms: {self.get_bcdm_field_list()}")


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
        logger.info(f"match_type={match_type}\n{filter_df.head(100).to_markdown(index=False)}")

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

def BCDM_iBOL_comparison(BGE_sample_mapping_obj):
    print("-------------------------------------------------------------------------")
    out_data_dir = get_out_dir()
    out_file = os.path.join(out_data_dir, f"{'bcdm_ibol_comparison.txt'}")
    new_bge_ibol_field_list =  sorted(get_bge_ibol_field_list())

    print(f"bcdm_list={BGE_sample_mapping_obj.get_bcdm_field_list()}")
    print()
    print(f"new_bge_ibol_field_list={new_bge_ibol_field_list}")
    fuzzy_compare2lists(BGE_sample_mapping_obj.get_bcdm_field_list(), new_bge_ibol_field_list, 50, out_file)


def generate_SSOM(mapped_sheet, BGE_sample_mapping_obj):
    print("-----------------------------------------------------------------------------------------")
    #f 'BCDM-BGE_iBOL'
    out_file = os.path.join(f"{get_out_dir()}{mapped_sheet}_SSSOM.tsv")
    unmatched_list = ["unmatched"]
    close_subject_list = []
    if mapped_sheet == 'BCDM-BGE_iBOL':
        BGE_sample_mapping_obj.print_stats()
        my_df = BGE_sample_mapping_obj.get_target_fields_df(mapped_sheet)
        new_df = my_df[['field','BGE iBOL metadata sheet']]
        new_df = new_df.rename(columns={'field': 'subject_label', 'BGE iBOL metadata sheet': 'object_label'})

        new_df['mapping_date'] = '2024-04-24'
        narrow_subject_list = ["bcdm:coord", "bcdm:insdc_acs"]
        broader_subject_list = ["bcdm:specimen_linkout"]
        new_df['subject_source'] = 'https://github.com/boldsystems-central/BCDM/blob/main/field_definitions.tsv'
        new_df['subject_source_version'] = '2024-08-31'
        new_df['object_source'] = 'iBOL-EU spreadsheet'
        new_df['object_source_version'] = '2024-O8'
        new_df['subject_label'] = new_df['subject_label'].apply(lambda x: f"bcdm:{x}" if pd.notna(x) and x else x)
        new_df['object_label'] = new_df['object_label'].apply(lambda x: f"iboleu:{x}" if pd.notna(x) and x else x)
    elif  mapped_sheet == 'ENA-iBOL':
        my_df = BGE_sample_mapping_obj.get_target_fields_df(mapped_sheet)

        logger.info(my_df.head())
        my_df = my_df.rename(columns = {'ENA': 'subject_label', 'BIOSCAN single sample (BOLD)': 'object_label'})
        new_df = my_df[['subject_label', 'object_label']]
        logger.info(new_df.head())
        narrow_subject_list = [""]
        broader_subject_list = ["ena:taxon_id", "ena:scientific_name", "ena:organism part"]
        close_subject_list = ['ena:sample collection method', 'ena:identified_by', 'ena:collected_by']
        new_df['mapping_date'] = '2024-04-24'
        new_df['subject_source'] = ''
        new_df['subject_source_version'] = '2024-08-31'
        new_df['object_source'] = 'ENA-iBOL spreadsheet'
        new_df['object_source_version'] = '2024-O8'
        new_df['subject_label'] = new_df['subject_label'].apply(lambda x: f"ena:{x}" if pd.notna(x) and x and x != "unmatched" else x)
        new_df['object_label'] = new_df['object_label'].apply(lambda x: f"iboleu:{x}" if pd.notna(x) and x and x != "unmatched" else x)

    else:
        logger.error(f"mapped_sheet {mapped_sheet} not in BGE_sample_mapping_obj")

    new_df['subject_id'] = new_df['subject_label']
    new_df['object_id'] = new_df['object_label']
    # https://academic.oup.com/database/article/doi/10.1093/database/baac035/6591806
    new_df['predicate_id'] = new_df.apply( lambda row: f"skos:exactMatch"  if pd.notna(row['object_label']) and pd.notna(row['subject_label']) else f"notApplicable",  axis=1)
    new_df['predicate_id'] = new_df.apply(lambda row: f"skos:narrowMatch" if row['subject_label'] in narrow_subject_list else row['predicate_id'], axis = 1)
    new_df['predicate_id'] = new_df.apply(
        lambda row: f"skos:broaderMatch" if row['subject_label'] in broader_subject_list else row['predicate_id'],
        axis = 1)
    new_df['predicate_id'] = new_df.apply(
        lambda row: f"skos:closeMatch" if row['subject_label'] in close_subject_list else row['predicate_id'],
        axis = 1)
    new_df['predicate_id'] = new_df.apply(
        lambda row: f"notApplicable" if row['subject_label'] in unmatched_list or  row['object_label'] in unmatched_list else row['predicate_id'],
        axis = 1)


    new_df['mapping_justification'] = 'semapv:ManualMappingCuration'

    for my_col in ['author_id', 'confidence', 'comment',	'examples']:
        new_df[my_col] = ""

    new_df = new_df[['subject_id', 'subject_label', 'predicate_id', 'object_id', 'object_label',
                     'mapping_justification', 'mapping_date', 'author_id', 'subject_source', 'subject_source_version',
                     'object_source', 'object_source_version', 'confidence', 'comment',	'examples']]

    print(new_df.head(10))
    logger.info(f"writing to {out_file}")
    new_df.to_csv(out_file,sep="\t", index=False)


def removeNaN_from_list(my_list):
    return [x for x in my_list if x == x]

def compare_ena_ibol(ena_info, BGE_sample_mapping_obj):
    print(f"checklist_field_names (total={len(ena_info.all_checklist_field_names_list)})")
    print()

    mapped_sheet = 'ENA-iBOL'
    my_df = BGE_sample_mapping_obj.get_target_fields_df(mapped_sheet)
    logger.info(f"my_df={my_df}")
    ena_field_name = 'ENA Tree of Life Checklist (ERC000053)'
    ena_field_name = 'ENA'
    ibol_field_name = 'BIOSCAN single sample (BOLD)'
    logger.info(f"left_field_name={ena_field_name}  values={my_df[ena_field_name].to_list()}")
    logger.info(f"right_field_name={ibol_field_name}  values={my_df[ibol_field_name].to_list()}")
    my_left_dict = dict(zip(my_df[ena_field_name], my_df[ibol_field_name]))
    logger.info(f"my_left_dict={my_left_dict}")
    my_right_dict = dict(zip(my_df[ibol_field_name], my_df[ena_field_name]))
    logger.info(f"my_right_dict={my_right_dict}")

    my_new_dict = {}
    ibol_remaining_set = set(my_df[ibol_field_name])
    ena_unmatched_set = set()
    unmatched_pattern_list = ["", "unmatched"]
    for ena_field_name in ena_info.all_checklist_field_names_list:

        if ena_field_name in my_left_dict and  my_left_dict[ena_field_name] not in unmatched_pattern_list:
            my_new_dict[ena_field_name] = my_left_dict[ena_field_name]
            if my_left_dict[ena_field_name] in ibol_remaining_set:
                ibol_remaining_set.remove(my_left_dict[ena_field_name])
        else:
            my_new_dict[ena_field_name] = "unmatched"
            ena_unmatched_set.add(ena_field_name)
    logger.info(f"remaining_set={ibol_remaining_set}")
    new_df = pd.DataFrame.from_dict(my_new_dict, orient='index')
    logger.info(f"new_df={new_df.head(1000)}")
    # logger.info(f"going in ena_unmatched_set={ena_unmatched_set}")
    ena_unmatched_set = set(removeNaN_from_list(ena_unmatched_set))
    logger.info(f"ena_unmatched_set={ena_unmatched_set}")
    ibol_remaining_set = set(removeNaN_from_list(ibol_remaining_set))
    logger.info(f"ibol_remaining_set={ibol_remaining_set}")

    mapped_df = compareAllTerms(list(ena_unmatched_set), list(ibol_remaining_set), 50)
    logger.info(f"mapped_df match_type(s)={mapped_df['match_type'].value_counts()}")
    # logger.info(f"mapped_df={mapped_df.head(30).to_markdown()}")
    exact_df = mapped_df.query('match_type == "harmonised"')
    logger.info(f"exact_df={exact_df.to_markdown(index=False)}")
    exact_dict = exact_df.to_dict(orient='records')
    logger.info(exact_dict)

    def process_matches(my_matching_dict):
        for my_record in my_matching_dict:
            logger.info(f"my_record={my_record}")
            left_term = my_record['left_term']
            right_term = my_record['match']
            logger.info(f"left_term={left_term} right_term={right_term}")
            my_new_dict[left_term] = right_term
            ena_unmatched_set.remove(left_term)
            ibol_remaining_set.remove(right_term)

    process_matches(exact_dict)

    fuzzy_df = mapped_df.query('match_type == "fuzzy"')
    logger.info(f"fuzzy_df={fuzzy_df.to_markdown(index=False)}")

    for ibol_field_name in ibol_remaining_set:
        my_new_dict[ibol_field_name] = "unmatched"

    # logger.info(my_new_dict)
    new_df = pd.DataFrame.from_dict(my_new_dict, orient='index')
    new_df['left_term'] = new_df.index
    new_df.columns = ['right_term', 'left_term']
    new_df = new_df[['left_term', 'right_term']]
    new_df = new_df.sort_values(by='left_term', key=lambda col: col.str.lower())
    logger.info(f"new_df=\n{new_df.sample(n=10)}")
    outfile = f"{get_out_dir()}/new_ena_ibol.tsv"
    logger.info(f"writing to {outfile}")
    new_df.to_csv(outfile, sep="\t", index=False)

    outfile = f"{get_out_dir()}/ena_ibol_sssom.tsv"
    generate_SSOM(mapped_sheet, BGE_sample_mapping_obj)


def main():
    compare_ibol_lists()

    BGE_sample_mapping_obj = BGE_sample_mapping()
    BGE_sample_mapping_obj.print_stats()

    BCDM_iBOL_comparison(BGE_sample_mapping_obj)

    out_data_dir = get_out_dir()

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

    BCDM_iBOL_comparison(BGE_sample_mapping_obj)
    generate_SSOM('BCDM-BGE_iBOL', BGE_sample_mapping_obj)

    ena_info = EnaInfo()
    compare_ena_ibol(ena_info, BGE_sample_mapping_obj)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format = '%(levelname)s - %(message)s')
    main()
