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

def getENAChecklistTerms(checklist_id):
    """"""
    logger.info(f"getChecklistTerms(checklist_id: {checklist_id})")
    checklistTerms = {}
    url = f"https://wwwdev.ebi.ac.uk/biosamples/schema-store/registry/schemas/{checklist_id}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Step 2: Parse the JSON
    data = response.json()
    try:
        characteristics_properties = data['properties']['characteristics']['properties']

        # Step 4: Get the keys
        checklistTerms = list(characteristics_properties.keys())

    except KeyError as e:
        print(f"Key not found in JSON: {e}")
    logger.info(f"getChecklistTerms(data: {checklistTerms})")
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

def main():
    checklist_id = 'ERC000059'
    ENAChecklistTerms = getENAChecklistTerms(checklist_id)
    SS_terms = getSpreadsheetCol(col_name = 'field_name: ENA_suggested')
    do_comparison_check(SS_terms, ENAChecklistTerms)

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(message)s')
    main()
