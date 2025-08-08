#!/usr/bin/env python3
"""
Script to extract a table from a Google Docs document or a Markdown file and output it in YAML format.

This script takes either a Google Docs URL or a local Markdown file path as a command-line argument,
extracts the "Tools or resource table", and outputs the data in YAML format.

Usage:

    python google_docs_table_to_yaml.py --file <markdown_file_path>
    # the google_docs extraction did not work properly for me, so rewritten to use the markdown file,
    that gets export from Google Docs
    python google_docs_table_to_yaml.py <google_docs_url>

Example:
    python google_docs_table_to_yaml.py https://docs.google.com/document/d/1ef8HsrCffDi65cB-dy42fs1GBiIpGgrFHMf4U5ZBJIk/edit
    python google_docs_table_to_yaml.py --file /path/to/document.md

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2025-08-08
__docformat___ = 'reStructuredText'
"""

import argparse
import logging
import sys
import requests
import os
from bs4 import BeautifulSoup
import yaml
import re
import sys
import pandas as pd

logger = logging.getLogger(__name__)

def extract_table_from_markdown_file(file_path):
    """
    Extract a table from a Markdown file.
    
    Args:
        file_path (str): Path to the Markdown file
        
    Returns:
        list: List of dictionaries representing the table data
    """
    logger.info(f"Reading Markdown file: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        sys.exit(1)
    
    # Parse the Markdown content using BeautifulSoup with 'html.parser'
    # This works because we're looking for markdown tables which have a specific format
    # that BeautifulSoup can interpret as HTML-like structure
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the "Tools or resource table" section
    # First, try to find the heading
    heading_text = "Tools or resource"
    heading = None
    
    # Look for headings that might contain the text
    for line in content.split('\n'):
        if line.startswith('#') and heading_text.lower() in line.lower():
            heading = line
            break
    
    # Find table markers (lines starting with |)
    table_lines = []
    in_table = False
    table_start_index = 0
    
    if heading:
        # If heading found, look for the table after the heading
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if heading in line:
                table_start_index = i + 1
                break
    
    lines = content.split('\n')[table_start_index:]
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('|') and stripped_line.endswith('|'):
            if not in_table:
                in_table = True
            table_lines.append(stripped_line)
        elif in_table and not stripped_line:
            # Empty line after table - end of table
            break
        elif in_table:
            # Non-empty line that doesn't start with | - end of table
            break
    
    if not table_lines:
        logger.error("No markdown table found in the file")
        sys.exit(1)
    
    # Parse the table
    table_data = []
    
    # Extract headers from the first row
    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.split('|')[1:-1]]  # Skip first and last empty cells

    # default = ['', 'Description', 'ID', 'Link to the tool (URL)', 'Registries', 'New or not']
    new_headers = ['name', 'description', 'id', 'url', 'registry']


    # Skip the separator line (second line)
    for row_line in table_lines[2:]:
        cells = [cell.strip() for cell in row_line.split('|')[1:-1]]  # Skip first and last empty cells
        if len(cells) == len(headers):
            row_data = {}
            for i, cell in enumerate(cells):

                logger.debug(f"cell {i}: {cell}")
                if headers[i] != 'New or not':
                    row_data[new_headers[i]] = cell
            if row_data['name'] != 'Name':
                table_data.append(row_data)

    if not table_data:
        logger.error("No table data extracted")
        sys.exit(1)

    col_num=0
    logger.info(f"Table columns [{col_num}]: {table_data[col_num].keys()}")
    logger.info(f"col {col_num}: {table_data[col_num]}")
    col_num = 2
    logger.info(f"Table columns [{col_num}]: {table_data[col_num].keys()}")
    logger.info(f"col {col_num}: {table_data[col_num]}")

    return table_data

def extract_table_from_google_docs(url):
    """
    Extract a table from a Google Docs document.
    
    Args:
        url (str): URL of the Google Docs document
        
    Returns:
        list: List of dictionaries representing the table data
    """
    # Modify URL to get the published/exported HTML version
    # This is a workaround since direct API access requires authentication
    export_url = url.replace('/edit', '/pub')
    
    logger.info(f"Fetching document from: {export_url}")
    
    try:
        response = requests.get(export_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching document: {e}")
        sys.exit(1)
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the "Tools or resource table" section
    # First, try to find the heading
    heading_text = "Tools or resource"
    heading = None
    
    # Look for headings that contain the text
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if heading_text.lower() in h.get_text().lower():
            heading = h
            break
    
    if not heading:
        logger.warning(f"Could not find heading containing '{heading_text}'")
        # If heading not found, try to find the table directly
        tables = soup.find_all('table')
        if not tables:
            logger.error("No tables found in the document")
            sys.exit(1)
        table = tables[0]  # Use the first table as fallback
    else:
        # Find the next table after the heading
        table = heading.find_next('table')
        if not table:
            logger.error(f"No table found after the '{heading_text}' heading")
            sys.exit(1)
    
    # Extract table data
    table_data = []
    rows = table.find_all('tr')
    
    # Extract headers from the first row
    headers = [th.get_text().strip() for th in rows[0].find_all(['th', 'td'])]
    
    # Extract data from remaining rows
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) == len(headers):
            row_data = {}
            for i, cell in enumerate(cells):
                row_data[headers[i]] = cell.get_text().strip()
            table_data.append(row_data)


    if not table_data:
        logger.error("No table data extracted")
        sys.exit(1)

    logger.info(f"Table columns: {table_data.columns}")
    
    return table_data

def reformat_table_to_rdmkit_need(table_data):
    """
    Reformat the extracted table rows into the required YAML-friendly structure.
    Ensures key order and parses the registry field into a nested mapping.
    :param table_data: list of dicts with keys ['name','description','id','url','registry']
    :return: list of dicts with keys in order ['description','id','name','registry','url']
    """
    # Patterns to recognize known registries
    biotools_pattern = re.compile(r'bio\.?tools', re.IGNORECASE)
    fairsharing_pattern = re.compile(r'FAIRsharing', re.IGNORECASE)
    tess_pattern = re.compile(r'tess', re.IGNORECASE)

    def get_clean_registry_name(registry_name):
        """
        Normalize variants of registry names to canonical keys.
        """
        registry_name = registry_name.strip()
        if biotools_pattern.match(registry_name):
            return "biotools"
        if fairsharing_pattern.match(registry_name):
            return "fairsharing"
        if tess_pattern.match(registry_name):
            return "tess"
        registry_name_lower = registry_name.lower()
        logger.info(f"registry_name is unknown={registry_name}, but changing to {registry_name_lower}")
        return registry_name_lower

    def get_clean_registry_value(reg_value):
        """
        sometimes links and sometimes registry names are in the same cell,
        :param reg_value:
        :return: reg_value:
        """
        logger.debug(f"reg_value={reg_value}")
        if reg_value.startswith('http'):
            return reg_value
        elif reg_value.startswith('['):
            logger.debug(f"reg_value={reg_value}")
            reg_value = reg_value.strip(')').split('(')[1].strip()
            logger.debug(f"reg_value={reg_value}")


        if not reg_value.startswith('http'):
            logger.warning(f"WARNING registry_value looks dubious={reg_value}")
        return reg_value

    new_table_data = []
    headers_currently = ['name', 'description', 'id', 'url', 'registry']
    # Desired output order (registry before url as per requirement)
    headers_want = ['description', 'id', 'name', 'registry', 'url']

    logger.info(f"len={len(table_data)}")
    for row_num in range(len(table_data)):
        row_data = table_data[row_num]
        new_row_data = {}
        for header_want in headers_want:
            if header_want in headers_currently:
                if header_want != 'registry':
                    val = row_data.get(header_want, '')
                    if isinstance(val, str):
                        val = val.strip()
                    new_row_data[header_want] = val
                else:
                    # Build nested registry mapping
                    registry_field = row_data.get('registry', '') or ''
                    reg_map = {}
                    for registry_element in [r for r in (x.strip() for x in registry_field.split(',')) if r]:
                        parts = [p.strip() for p in registry_element.split(':', 1)]
                        if len(parts) >= 2 and parts[1]:
                            reg_name = get_clean_registry_name(parts[0])
                            reg_value = get_clean_registry_value(parts[1])
                            reg_map[reg_name] = reg_value
                    new_row_data['registry'] = reg_map
            else:
                new_row_data[header_want] = ""
        new_table_data.append(new_row_data)

    logger.info("Finished: reformat_table_to_rdmkit_need")
    return new_table_data


def convert_to_yaml(table_data):
    """
    Convert table data to YAML format.
    
    Args:
        table_data (list): List of dictionaries representing the table data
        
    Returns:
        str: YAML formatted string
    """

    table_data = reformat_table_to_rdmkit_need(table_data)
    return yaml.dump(table_data, sort_keys=False, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Extract a table from Google Docs or Markdown file and output as YAML')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', help='URL of the Google Docs document')
    group.add_argument('--file', help='Path to a local Markdown file')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s - %(message)s')
    
    # Extract table data
    if args.url:
        table_data = extract_table_from_google_docs(args.url)
    else:
        table_data = extract_table_from_markdown_file(args.file)
    
    if not table_data:
        logger.error("No table data extracted")
        sys.exit(1)
    
    # Convert to YAML
    yaml_output = convert_to_yaml(table_data)
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(yaml_output)
        logger.info(f"YAML output written to {args.output}")
    else:
        print(yaml_output)

if __name__ == '__main__':
    main()