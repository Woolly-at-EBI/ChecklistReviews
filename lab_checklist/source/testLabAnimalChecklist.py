#!/usr/bin/env python3
"""Script of testLabAnimalChecklist.py is to testLabAnimalChecklist.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2025-06-24
__docformat___ = 'reStructuredText'

"""


import logging
import sys
import requests
import pandas as pd
import json
sys.path.append("/Users/woollard/projects/ChecklistReviews/source/")
from pairwise_term_matches import compareAllTerms

logger = logging.getLogger(__name__)


def get_lab_animals_checklist_speadsheet_df():
    # URL to CSV export
    url = "https://docs.google.com/spreadsheets/d/1VsbjEYVLA5oOlp9cZmcTqFvTnBTc0ApmmDkCV_YOTkM/export?format=csv&gid=0"

    # Read the sheet into a DataFrame
    df = pd.read_csv(url)
    # Display column names to d the one you want

    logger.info(f"Available columns: {df.columns.tolist()}")

    return df

def getSpreadsheetCol(col_name):
    df = get_lab_animals_checklist_speadsheet_df()

    column_values = df[col_name].dropna().tolist()

    # Output the list
    logger.info(f"{col_name} values:{column_values}")
    return column_values

def getENAChecklist(checklist_id):
    """

    :param checklist_id:
    :return: json
    """
    url = f"https://wwwdev.ebi.ac.uk/biosamples/schema-store/registry/schemas/{checklist_id}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Step 2: Parse the JSON
    return response.json()

def getENAChecklistTerms(checklist_id):
    """"""
    logger.info(f"getChecklistTerms(checklist_id: {checklist_id})")
    checklistTerms = {}
    data = getENAChecklist(checklist_id)

    try:
        characteristics_properties = data['properties']['characteristics']['properties']

        # Step 4: Get the keys
        checklistTerms = list(characteristics_properties.keys())

    except KeyError as e:
        print(f"Key not found in JSON: {e}")
    logger.debug(f"getChecklistTerms(data: {checklistTerms})")
    return checklistTerms

def do_comparison_check(SS_terms, ENAChecklistTerms):
    print("---------------------------------------------------------")
    # logger.info(f"SS_terms:{SS_terms}")
    # logger.info(f"ENAChecklistTerms:{ENAChecklistTerms}")
    SS_terms_set = set(SS_terms)
    ENAChecklistTerms_set = set(ENAChecklistTerms)
    logger.info(f"Terms that are identical in all: {len(SS_terms_set.intersection(ENAChecklistTerms_set))}")
    logger.info(f"Terms that are unique in the spreadsheet: total={len(SS_terms_set.difference(ENAChecklistTerms_set))} fields={SS_terms_set.difference(ENAChecklistTerms_set)}")
    logger.info(
        f"Terms that are unique in the ENA checklist: total={len(ENAChecklistTerms_set.difference(SS_terms_set))} fields={ENAChecklistTerms_set.difference(SS_terms_set)}")

    df_comparison = compareAllTerms(SS_terms, ENAChecklistTerms, 75)
    logger.info(f"df_comparison:{df_comparison}")


def  getENAChecklist_df(checklist_id):
    data = getENAChecklist(checklist_id)
    logger.debug(f"ENAChecklist_df:{json.dumps(data,indent=4)}")

    # Step 2: Navigate to characteristics properties
    characteristics = data['properties']['characteristics']['properties']

    # Step 3: Get list of required fields inside characteristics
    # These are usually defined under characteristics['required'] (if present)
    required_fields = set(data['properties']['characteristics'].get('required', []))

    # Step 4: Build DataFrame
    rows = []
    for key, value in characteristics.items():
        is_required = key in required_fields
        rows.append({
            'property': key,
            'required': is_required
        })

    df = pd.DataFrame(rows)

    # Optional: sort or inspect
    df = df.sort_values(by = 'required', ascending = False).reset_index(drop = True)
    logger.debug(df)
    return df

def exploreMandatoryNess(checklist_id):
    ena_df = getENAChecklist_df(checklist_id)
    logger.debug(f"ena_df:{ena_df.head(6)}")
    tmp_df = ena_df[ena_df['required']]
    ena_checklist_mandatory_properties_set = set(tmp_df['property'])
    logger.info(f"ENA checklist mandatory_fields={sorted(ena_checklist_mandatory_properties_set)}")

    lab_ss_df = get_lab_animals_checklist_speadsheet_df()
    logger.info(f"lab_ss_df:{lab_ss_df.head(6)}")
    logger.info(f"columns: {lab_ss_df.columns.tolist()}")

    print("+++++++++---------------------------------------------------")
    tmp_df = lab_ss_df[['field_name: ENA_suggested','requirement']]
    tmp_df = tmp_df[tmp_df['requirement'] == "mandatory"]
    logger.info(f"lab_ss_df:{tmp_df.head(6)}")
    ss_mandatory_properties_set = set(tmp_df['field_name: ENA_suggested'])
    logger.info(f"ss_mandatory_properties: {sorted(ss_mandatory_properties_set)}")

    print(f"Mandatory properties on both sets: {ss_mandatory_properties_set.intersection(ena_checklist_mandatory_properties_set)}")
    print(f"Mandatory properties unique to ss_mandatory_properties_set: {ss_mandatory_properties_set.difference(ena_checklist_mandatory_properties_set)}")
    print(
        f"Mandatory properties unique to ena_checklist_mandatory_properties_set: {ena_checklist_mandatory_properties_set.difference(ss_mandatory_properties_set)}")



def main():
    checklist_id = 'ERC000059'
    ENAChecklistTerms = getENAChecklistTerms(checklist_id)
    SS_terms = getSpreadsheetCol(col_name = 'field_name: ENA_suggested')
    do_comparison_check(SS_terms, ENAChecklistTerms)

    exploreMandatoryNess(checklist_id)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format = '%(levelname)s - %(message)s')
    main()
