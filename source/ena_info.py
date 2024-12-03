#!/usr/bin/env python3
"""Script of ena_info.py is to ena_info.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2024-12-03
__docformat___ = 'reStructuredText'

"""


import logging
logger = logging.getLogger(__name__)
import pandas as pd

class EnaInfo:
    def __init__(self):
        print("inside EnaInfo")
        inf_file = "../data/all_checklists_fields_by_checklist.tsv"
        self.df = pd.read_csv(inf_file, sep="\t")
        self.all_checklist_field_names_list = self.get_all_checklist_field_names()

    def get_all_checklist_field_names(self):
        all_field_names_set = set(self.df['CHECKLIST_FIELD_NAME'].to_list())
        return list(all_field_names_set) # will not let me sort.


def main():
    ena_info = EnaInfo()
    print(f"checklist_field_names (total={len(ena_info.all_checklist_field_names_list)}): {ena_info.all_checklist_field_names_list}")

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(message)s')
    main()
