"""
script to parse Felix's single cell stuff and map
"""

from bs4 import BeautifulSoup
import json
import sys

import logging
logger = logging.getLogger(__name__)
import os
import pandas as pd
from pairwise_term_matches import compareAllTerms


def create_sc_table():
    #  cat process_sc_html.json | jq '.[] | [.Header, .Required, .Name, .Description, .Example, .Reference, .Regex] ' | jq -r @tsv > tmp.txt

    html_content = """<div class="row">
        <div class="col-3"></div>
        <div class="col-6">
    
        <div class="accordion" id="accordionExample">
    
            <div class="accordion-item">
                <div class="accordion-header">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapsestudy" aria-expanded="true"
                            aria-controls="collapsestudy">
                        study
                    </button>
                </div>
                <div id="collapsestudy" class="accordion-collapse collapse"
                     data-bs-parent="#accordionExample">
                    <div class="accordion-body">
    
                        <div class="card">
    
                            <h5 class="card-header d-flex align-items-start">
                                Study ID <span class="badge bg-dark ms-auto">Required</span>
                            </h5>
    
                            <div class="card-body">
                                <table class="table">
    
                                    <tr>
                                        <td>Name</td>
                                        <td>study_id</td>
                                    </tr>
                                    <tr>
                                        <td>Description</td>
                                        <td>A unique alphanumeric identifier for this study</td>
                                    </tr>
                                    <tr>
                                        <td>Example</td>
                                        <td>A7F9B3X2</td>
                                    </tr>
                                    <tr>
                                        <td>Reference</td>
                                        <td>https://schema.org/id</td>
                                    </tr>
                                    <tr>
                                        <td>Regex</td>
                                        <td>^[a-zA-Z0-9]+$</td>
                                    </tr>
    
                                </table>
                            </div>
                        </div>
    
                        <div class="card">
    
                            <h5 class="card-header d-flex align-items-start">
                                First Name <span class="badge bg-dark ms-auto">Required</span>
                            </h5>
    
                            <div class="card-body">
                                <table class="table">
    
                                    <tr>
                                        <td>Name</td>
                                        <td>contact_first_name</td>
                                    </tr>
                                    <tr>
                                        <td>Description</td>
                                        <td>Given first name</td>
                                    </tr>
                                    <tr>
                                        <td>Example</td>
                                        <td>Jane</td>
                                    </tr>
                                    <tr>
                                        <td>Reference</td>
                                        <td>https://schema.org/givenName</td>
                                    </tr>
                                    <tr>
                                        <td>Regex</td>
                                        <td>^[a-zA-Z]+$</td>
                                    </tr>
    
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    # curl 'https://singlecellschemas.org/checklists/extended/html/dwc/sc_rnaseq_dwc_extended.html' > sc_rnaseq_dwc_extended.html
    with open('sc_rnaseq_dwc_extended.html', 'r') as f:
        html_content = f.read()
    #print(html_content)
    html_content ;
    # Parse HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract all cards
    cards = soup.find_all("div", class_ = "card")

    # Parse each card
    result = []
    for card in cards:
        card_data = {}

        # Extract header and badge
        header = card.find("h5", class_ = "card-header").text.strip()
        card_data["Header"] = header.split("Required")[0].strip()
        card_data["Required"] = "Required" in header

        # Extract table data
        table_rows = card.find("table").find_all("tr")
        for row in table_rows:
            key = row.find_all("td")[0].text.strip()
            value = row.find_all("td")[1].text.strip()
            card_data[key] = value

        result.append(card_data)

    # Convert to JSON
    json_output = json.dumps(result, indent = 4)

    # Print JSON
    # print(json_output)


class do_mapping_class:
    """
    logger.info(self.get_source_terms())
    logger.info(self.get_target_terms())
    """

    def __init__(self, file_name, sheet_dict):
        logger.debug("inside do_mapping_class")
        self.file_name = file_name
        self.sheet_dict = sheet_dict
        self.parse_mapping_file()
        self.mapped_df = ''


    def parse_mapping_file(self):
        # file_name = "../data/BGE_sample_metadata_mapping.xlsx" - old one

        logger.info(f"file={self.file_name}")
        xls_obj = pd.ExcelFile(self.file_name)
        logger.info(f"sheets{xls_obj.sheet_names}<-----")

        df_dict  = {}

        for sheet_name in xls_obj.sheet_names:
            logger.debug(f"in XLSX sheet={sheet_name}<----")
            my_df = pd.read_excel(self.file_name, sheet_name=sheet_name)

            my_df_name = sheet_name.replace("'", " ")
            logger.debug(f"sheet=>{sheet_name}<= key_now =>{my_df_name}<=")
            df_dict[my_df_name] = my_df
            logger.debug(f"{my_df.head(5)}")

        self.df_dict = df_dict


    def get_source_sheet_name(self):
        logger.info(f"in get_source_sheet_names(): source sheet name={self.sheet_dict['source']['sheet_name']}<--------")
        return self.sheet_dict['source']['sheet_name']

    def get_target_sheet_name(self):
        logger.info(f"in get_target_sheet_names) target sheet name={self.sheet_dict['target']['sheet_name']}<--------")
        return self.sheet_dict['target']['sheet_name']

    def get_source_df(self):
        logger.info(f"source sheet name RTNED: -->{self.get_source_sheet_name()}<--")
        return self.df_dict[self.get_source_sheet_name()]

    def get_target_df(self):
        return self.df_dict[self.get_target_sheet_name()]
    def get_source_terms(self):
        my_df = self.get_source_df()
        term_set = set(my_df[self.sheet_dict['source']['source_name_header']].tolist())
        return sorted(term_set)

    def get_target_terms(self):
        my_df = self.get_target_df()
        term_set = set(my_df[self.sheet_dict['target']['target_name_header']].tolist())
        return sorted(term_set)

    def map_source_terms_to_target_terms(self):
        self.mapped_df = compareAllTerms(self.get_source_terms(), self.get_target_terms(), 70)
        logger.info(f"mapped_df=\n{self.mapped_df}")

    def analyse_mapping(self):
        logger.info("inside analyse_mapping()")
        mapped_df = self.mapped_df
        logger.info(f"mapped_df=\n{mapped_df.head(3)}")
        exact_df = mapped_df.query('fuzzy_score == 100')
        logger.info(f"exact_df=\n{exact_df}")

def do_matches():
    logger.info("do_matches")

    file_name = "../data/Felix's single cell.xlsx"
    sheet_dict = { 'source': { 'sheet_name': 'Felixs SC terms', 'source_name_header': 'Header' },
                'target': { 'sheet_name': "other_cvs", 'target_name_header': 'ENA terms' }}
    mapping_obj = do_mapping_class(file_name, sheet_dict)
    # logger.info(f"mapping_obj={mapping_obj}")
    # mapping_obj.get_source_field_list()

    mapping_obj.map_source_terms_to_target_terms()
    mapping_obj.analyse_mapping()
    my_outfile = "tmp_out.tsv"
    logger.info(f"my_outfile={my_outfile}")
    with open(my_outfile, "w") as f:
        f.write(mapping_obj.mapped_df.to_csv(sep="\t", index=True))



def main():
    # create_sc_table()
    do_matches()

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format = '%(levelname)s - %(message)s')
    main()
