#!/usr/bin/env python3
"""Script of simple_ena_checklist_comparison.pl is to simple_ena_checklist_comparison.pl

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2024-10-24
__docformat___ = 'reStructuredText'

"""


import logging
logger = logging.getLogger(__name__)
import argparse
import pandas as pd


def readin_ena_checklist_file():

   """
        CHECKLIST_ID  CHECKLIST_FIELD_ID CHECKLIST_FIELD_MANDATORY  CHECKLIST_NAME CHECKLIST_FIELD_NAME
   """
   infile="/Users/woollard/projects/eDNAaquaPlan/wp2/ena_in/ena_checklists_mandatory_or_not.tsv"
   df = pd.read_csv(infile, sep='\t')
   # Using DataFrame.reindex() to change columns order
   change_column = ['CHECKLIST_FIELD_NAME','CHECKLIST_FIELD_ID', 'CHECKLIST_FIELD_MANDATORY', 'CHECKLIST_ID' , 'CHECKLIST_NAME']
   df = df.reindex(columns=change_column)
   df = df[['CHECKLIST_FIELD_NAME', 'CHECKLIST_ID' , 'CHECKLIST_NAME']]
   logger.debug(df.head())
   return df


def first_func():
    """"""
    df = readin_ena_checklist_file()
    # Group by 'CHECKLIST_FIELD_NAME', concatenate 'CHECKLIST_ID' and 'CHECKLIST_NAME', count the number of 'CHECKLIST_ID's, and sort by 'CHECKLIST_FIELD_NAME'
    # Group by 'CHECKLIST_FIELD_NAME' and concatenate 'CHECKLIST_ID' and 'CHECKLIST_NAME'
    df_grouped = df.groupby('CHECKLIST_FIELD_NAME').agg({
    'CHECKLIST_ID': lambda x: ', '.join(x),
    'CHECKLIST_NAME': lambda x: ', '.join(x)
    }).reset_index()

    # Calculate the count of 'CHECKLIST_ID' per group
    checklist_id_count = df.groupby('CHECKLIST_FIELD_NAME')['CHECKLIST_ID'].size().reset_index(name='CHECKLIST_ID_count')

    # Merge the count into the grouped DataFrame
    df_grouped = pd.merge(df_grouped, checklist_id_count, on='CHECKLIST_FIELD_NAME')

    # Sort by 'CHECKLIST_FIELD_NAME'
    df_grouped = df_grouped.sort_values('CHECKLIST_FIELD_NAME')
    logger.debug(df_grouped.head(100))

    outfile="../data/ena_only_checklist_terms_and_checklists.tsv"
    df_grouped.to_csv(outfile, sep="\t", index=False)
    logger.info(f"wrote output to {outfile}")


def main():
    first_func()

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(message)s')
    main()
