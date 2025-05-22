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
    json = """
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
    print(json)

def get_project_json():
    """"""

    json = """
        "projects": [
        {
            "alias": "comparative-analysis",
            "name": "Made up Human Gut Microbiota Study",
            "title": "Exploration of the diversity human gastric microbiota",
            "description": "The genome sequences of gut microbes were obtained using...",
            "sequencingProject": {},
            "attributes": [
                {
                    "tag": "testTag",
                    "value": "testValue"
                }
            ],
            "project_links": [
                {
                    "xrefLink": {
                        "db": "PUBMED",
                        "id": "25035323"
                    }
                }
            ]
        }
    ],
    """
    print (json)

def get_sample_json():
    """"""
    json = """
    "samples": "samples": [
        {
            "alias": "stomach_microbiota",
            "title": "madeup human gastric microbiota, mucosal",
            "organism": {
                "taxonId": "1284369"
            },
            "attributes": [
                {
                    "tag": "investigation type",
                    "value": "mimarks-survey"
                },
                {
                    "tag": "sequencing method",
                    "value": "pyrosequencing"
                },
                {
                    "tag": "collection date",
                    "value": "2010-01-20"
                },
                {
                    "tag": "host body site",
                    "value": "Mucosa of stomach"
                },
                {
                    "tag": "human-associated environmental package",
                    "value": "human-associated"
                },
                {
                    "tag": "geographic location (latitude)",
                    "value": "1.81",
                    "unit": "DD"
                },
                {
                    "tag": "geographic location (longitude)",
                    "value": "-78.76",
                    "unit": "DD"
                },
                {
                    "tag": "geographic location (country and/or sea)",
                    "value": "Colombia"
                },
                {
                    "tag": "geographic location (region and locality)",
                    "value": "Tumaco"
                },
                {
                    "tag": "environment (biome)",
                    "value": "coast"
                },
                {
                "tag": "environment (feature)",
                "value": "human-associated habitat"
                },
                {
                    "tag": "project name",
                    "value": "Human microbiota"
                },
                {
                    "tag": "environment (material)",
                    "value": "gastric biopsy"
                },
                {
                    "tag": "ena-checklist",
                    "value": "ERC000014"
                }
            ]
        }
    ]
    """

def main():
    get_submission_json()
    get_project_json()

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(message)s')
    main()
