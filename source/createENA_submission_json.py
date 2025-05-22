#!/usr/bin/env python3
"""Script of createENA_submission_json.py is to createENA_submission_json.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2025-05-22
__docformat___ = 'reStructuredText'

"""


import logging
logger = logging.getLogger(__name__)
import argparse

def get_submission_json():
    """"""
    submission_json = """
    "submission": {
        "alias": "PeterTestAliasName",
        "accession": "",
        "actions": [
            {
                "type": "ADD"
            },
            {
                "type": "RELEASE"
            }
        ],
        "attributes": [
            {
                "tag": "test_tag",
                "value": "test_val"
            },
            {
                "tag": "test_tag_1",
                "value": "test_val_1"
            }
        ]
    }
    """


    print(submission_json)

def main():
    get_submission_json()

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(message)s')
    main()
