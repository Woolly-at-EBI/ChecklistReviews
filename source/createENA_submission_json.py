#!/usr/bin/env python3
"""Script of createENA_submission_json.py is to createENA_submission_json.py

https://ena-docs.readthedocs.io/en/latest/submit/general-guide/programmatic.html

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2025-05-22
__docformat___ = 'reStructuredText'

"""
import xml.etree.ElementTree as ET
import logging
import os.path
import json
import sys

logger = logging.getLogger(__name__)


def get_checklist(checklist_id):
    logger.debug(f"checklist_id={checklist_id}")

    my_checklist_dict = {"samples" : ""}

    logger.debug(f"my_checklist_dict={my_checklist_dict}")


    infile = f"/Users/woollard/projects/ChecklistReviews/data/checklist_versioning/{checklist_id}.xsd"
    logger.debug(f"infile={infile}")
    if os.path.isfile(infile):
        logger.debug(f"file exists: {infile}")
    else:
        logger.debug(f"file does not exist: {infile}")
        sys.exit()
    tree = ET.parse(infile)
    root = tree.getroot()
    logger.debug(f"root={root}")
    for child in root:
        print(child.tag, child.attrib)

    my_checklist_sample_set = set()
    for field in root.findall("./CHECKLIST/DESCRIPTOR/FIELD_GROUP/FIELD"):
        # logger.debug(f"field name={field.tag} attrib={field.attrib}")


        for name in field.findall("./NAME"):
            # print(f"\tname={name.tag} name--->{name.text}<--")
            tag = name.text
            my_checklist_sample_set.add(tag)


        # for field_child in field:
        #     print(f"\tfield name={field_child.tag} value={field_child.text}")
        # sys.exit()

    logger.debug(f"my_checklist_sample_set ={my_checklist_sample_set}")

    checklist_name_tag = root.find("./CHECKLIST/DESCRIPTOR/NAME")
    checklist_name = checklist_name_tag.text
    logger.debug(f"checklist_name_tag={checklist_name_tag.text}")

    return my_checklist_sample_set, checklist_name


def get_submission_json():
    """"""
    submission_json = {
        "submission": {
            "alias": "",
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
            ]
         }
     }

    logger.debug(f"submission_json={submission_json}")
    return submission_json

def get_submission_json_example():
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
    return submission_json

def get_project_json_template():
    project_json = {
            "projects": [
            {
                "alias": "",
                "name": "",
                "title": "",
                "description": "",
                "sequencingProject": {},
                "attributes": [
                ],
                "project_links": [
                    {
                    }
                ]
            }
        ]
    }
    return project_json

def get_project_json_example():
    """"""

    project_json = """
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
    print (project_json)

def get_sample_json(specific_base_template):
    sample_json = get_sample_json_template()
    logger.debug(f"------------------------------------------")
    logger.debug(f"sample_json={sample_json}")
    logger.debug(f"------------------------------------------\n")
    all_tags = specific_base_template[1]
    logger.debug(f"all_tags={all_tags}")
    already_done = {'tax_id', 'sample_alias', 'sample_title'}
    logger.debug(f"already_done={already_done}")
    all_tags.append("ena-checklist")
    checklist_id = specific_base_template[0][1]
    logger.debug(f"checklist_id={checklist_id}")

    for tag_name in all_tags:
        #logger.debug(f"tag_name-->{tag_name}<---")
        if tag_name in already_done:
            logger.debug(f"YIPPEE Found tag_name-->{tag_name}<--")
            continue
        else:
            logger.debug(f"              NOT Found tag_name=-->{tag_name}<---")

        tag_json = {
            "tag" :  f"{tag_name}",
            "value": ""
         }

        if tag_name == "ena-checklist":
            tag_json['value'] = checklist_id
        # logger.debug(f"tag_json={tag_json}")
        # logger.info(f"sample_json={sample_json}")
        # logger.info(f"sample_json={sample_json['samples']}")
        # logger.info(f"sample_json={sample_json['samples'][0]['attributes']}")

        sample_json["samples"][0]["attributes"].append(tag_json)

    logger.info(f"sample_json={json.dumps(sample_json,indent=4)}")
    return sample_json



def  get_sample_json_template():
    sample_json = {
        "samples": [
            {
               "alias": "",
               "title": "",
                  "organism": {
                 "taxonId": ""
                 },
                "attributes": [
                ]
             }
        ]
    }

    logger.debug(sample_json)
    return sample_json

def get_sample_example_json():
    """"""
    json = { "samples": []}
    json = """
    "samples": [
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

    return json

def add_checklist2base(base_template, field_name_set, checklist_id, checklist_name):
    logger.debug(f"add_checklist2base--------------------------------------------")

    base_template[0][1] = checklist_id
    base_template[0][2] = checklist_name
    # logger.debug(f"base_template={base_template}")

    base_field_name_set = set(base_template[1])
    # logger.debug(f"base_field_name_set={base_field_name_set}")
    # intersects of base and field_name_set
    intersect_set = base_field_name_set.intersection(field_name_set)
    # logger.debug(f"intersect_set={intersect_set}")
    difference_set = field_name_set.difference(base_field_name_set)
    checklist_fields_to_add = sorted(difference_set)
    # logger.debug(f"checklist_fields_to_add={checklist_fields_to_add}")
    base_template[1].extend(checklist_fields_to_add)
    logger.debug(f"base_template={base_template}")
    return base_template


def get_base_template():
    base = {}
    base[0] = ['Checklist', 'ERC000011', 'ENA default sample checklist']
    base[1] = ["tax_id","collection date","sample_alias","sample_description","sample_title","scientific_name","geographic location (country and/or sea)"]
    base[2] = ['# units']
    return base


def main():

    checklist_id = "ERC000053"
    field_name_set, checklist_name = get_checklist(checklist_id)
    base_template = get_base_template()
    logger.debug(f"base_template={base_template}")
    new_base_template = add_checklist2base(base_template, field_name_set, checklist_id, checklist_name)
    outfile = f"base_{checklist_id}.tsv"
    logger.debug(f"outfile={outfile}")

    sample_json = get_sample_json(new_base_template)
    project_json = get_project_json_template()
    logger.debug(f"project_json={project_json}")
    submission_json = get_submission_json()

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(message)s')
    main()
