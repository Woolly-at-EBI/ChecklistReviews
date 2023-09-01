class mixs:
    def ingest_ena_cl(self):
        self.my_dict = process_ena_cl(self.my_dict_raw, self.linkml_mixs_dict)

    def __init__(self, my_dict, type, linkml_mixs_dict):
        # type could be  "mixs_v5" or "mixs_v6"
        self.type = type

        if type == "ena_cl":
            print(f"type = {type}")
            self.my_dict_raw = my_dict
            self.linkml_mixs_dict = linkml_mixs_dict
            self.ingest_ena_cl()

            # self.cl_details_dict = get_ena_cl_details(self.my_dict_raw)
        else:
            self.my_dict = my_dict

    def get_type(self):
        return self.type

    def get_all_term_list(self):
        my_list = list(self.my_dict['by_term'].keys())
        my_list.sort()
        return my_list

    def get_terms_with_freq(self):
        """
                :return:  {'Food_Product_type': 12,
                                        'Food_source': 12,
                                        'HACCP_term': 36,
        """
        self.get_terms_by_freq()
        return self.term_with_freq

    def get_terms_by_freq(self):
        """

        :return:  40: {'term_count_with_freq': 2,
                        'terms': dict_keys(['collection date', 'geographic location (country and/or sea)'])}}
        """
        ic()
        if hasattr(self, 'my_just_freq'):
            return self.my_just_freq

        my_just_freq = {}
        if "by_term_count" not in self.my_dict:
            add_term_package_count(self.my_dict)

        self.term_with_freq = {}

        freq_keys = sorted(self.my_dict["by_term_count"].keys(), reverse = True)
        # ic("KEYS=+++++++++++++++++++++++++")
        # ic(freq_keys)
        # ic(self.my_dict["by_term_count"][40].keys())
        for freq_key in freq_keys:
            my_just_freq[freq_key] = {}
            my_just_freq[freq_key]["terms"] = list(self.my_dict["by_term_count"][freq_key].keys())
            my_just_freq[freq_key]["term_count_with_freq"] = len(my_just_freq[freq_key]["terms"])
            for term in my_just_freq[freq_key]["terms"]:
                self.term_with_freq[term] = freq_key
        # ic(my_just_freq)
        # sys.exit()

        self.my_just_freq = my_just_freq
        return self.my_just_freq

        #
        #
        # total_count =0
        # # my_dict["by_term_count"]
        # ic(self.my_dict["by_term_count"].keys())
        # ic(self.my_dict["by_term_count"])
        #
        # return (self.my_dict["by_term_count"])

    def get_term_top(self, first_number):
        """
        get_term_top - get the first 10, or whatever in terms of frequency
        :param first_number:
        :return:
        """
        my_just_freq = self.get_terms_by_freq()
        total_found_so_far = 0
        top_terms = []
        for freq_key in my_just_freq:
            ic(my_just_freq[freq_key]["terms"])
            top_terms.extend(list(my_just_freq[freq_key]["terms"]))
            if len(top_terms) >= first_number:
                return top_terms[0:first_number - 1]
        return top_terms

    def get_all_term_count(self):
        return (len(self.my_dict['by_term'].keys()))

    def print_term_summary(self, top):
        """

        :param top: = top # number to print, if "", print all
        :return:
        """
        if top == "":
            print(f"term_count={self.get_all_term_count()}  terms={self.get_all_term_list()}")
        else:
            print(f"term_count={self.get_all_term_count()} first {top} terms={self.get_all_term_list()[0:top]}")

    def get_all_package_list(self):
        my_list = list(self.my_dict['by_package'].keys())
        my_list.sort()
        return my_list

    def get_all_package_count(self):
        return (len(self.my_dict['by_package'].keys()))

    def print_package_summary(self):
        print(f"package_count={self.get_all_package_count()} packages={self.get_all_package_list()}")

    def print_summaries(self):
        self.print_term_summary(10)
        self.print_package_summary()

    # def get_all_checklists(self):
    #     self.cl_details_dict

    def get_term_list_for_package(self, package_cl_name):
        # ic("inside get_term_list_for_package", package_cl_name)
        # ic(self.my_dict['by_package'][package_cl_name])
        return list(self.my_dict['by_package'][package_cl_name]['field'].keys())


# **********************************************************************************



def process_ena_cl(my_dict, linkml_mixs_dict):
    """
    function to parse the ena_cl in a similar way to how the mixs versions have been parsed

    :param my_dict:
    :return:
    """
    # print(my_dict)
    # print(my_dict.keys())
    # print(my_dict["CHECKLIST_SET"].keys())
    MIXS_review_dict = {"by_package": {}, "by_term": {}}

    # print("----------------------------------")
    for checklist in my_dict["CHECKLIST_SET"]["CHECKLIST"]:
        # print(checklist)
        # print(checklist["@accession"])
        # print(checklist["@checklistType"])
        # print(f"name={checklist['DESCRIPTOR']['NAME']} DESCRIPTION={checklist['DESCRIPTOR']['DESCRIPTION']}")
        checklist_name = checklist['DESCRIPTOR']['NAME']
        # ic(checklist_name)
        if not hasattr(MIXS_review_dict["by_package"], checklist_name):
            MIXS_review_dict["by_package"][checklist_name] = {'field': {}}

        for field_group in checklist['DESCRIPTOR']["FIELD_GROUP"]:
            # print(field_group)
            # print(f"\tname={field_group['NAME']} DESCRIPTION={field_group['DESCRIPTION']}")
            for field in field_group["FIELD"]:
                # print(f"\t\tfield={field}")
                # ic(field)
                if field in ["LABEL", "NAME", "DESCRIPTION", "FIELD_TYPE", "MANDATORY", "MULTIPLICITY", "SYNONYM",
                             "UNITS"]:
                    continue
                field_name = field['NAME']

                if field_name in linkml_mixs_dict['slots']:
                    # ic(linkml_mixs_dict['slots'][field_name])
                    long_field_name = linkml_mixs_dict['slots'][field_name]['title']  # ENA uses the long_field_name
                    # ic(field_name)
                    # ic(long_field_name)
                    # sys.exit()
                else:
                    long_field_name = field_name

                if field_name not in MIXS_review_dict["by_term"]:
                    MIXS_review_dict["by_term"][long_field_name] = {}
                if field_name not in MIXS_review_dict["by_package"][checklist_name]['field']:
                    MIXS_review_dict["by_package"][checklist_name]['field'][long_field_name] = {}
                # MIXS_review_dict["by_package"][checklist_name][field_name]['name'] = field_name

                description = "no_description"
                if "DESCRIPTION" in field:
                    description = field["DESCRIPTION"]
                else:
                    # print(f"no DESCRIPTION, so using LABEL for {field_name}")
                    if 'LABEL' in field:
                        description = field["LABEL"]
                        # print(f"no description so using label={description}")

                MIXS_review_dict["by_term"][long_field_name]['DESCRIPTION'] = description
                MIXS_review_dict["by_package"][checklist_name]['field'][long_field_name]["DESCRIPTION"] = description
                # ic(MIXS_review_dict["by_package"][checklist_name]['field'][field_name])

            # end of for field_group
            # ic(MIXS_review_dict["by_package"])
            # ic(MIXS_review_dict["by_term"])
            # sys.exit()
            for checklist_name in MIXS_review_dict["by_package"]:
                # ic(checklist_name)
                # ic(MIXS_review_dict["by_package"][checklist_name])
                if 'field' in MIXS_review_dict["by_package"][checklist_name]:
                    MIXS_review_dict["by_package"][checklist_name]['count'] = len(
                        MIXS_review_dict["by_package"][checklist_name]['field'].keys())
                # else:
                # ic("WARNING: package seems to be missing any fields!", checklist_name)

        # print()
        # end of for each checklist
        # sys.exit()

    MIXS_review_dict = add_term_package_count(MIXS_review_dict)

    return MIXS_review_dict


def add_term_package_count(my_dict):
    """
    for all the term_name's add the package_name and count.
    slightly verbose, being careful in case the dictionary has already been partially populated.

    :param my_dict:
    :return: my_dict
    """

    for package_name in my_dict["by_package"]:
        for term_name in my_dict["by_package"][package_name]["field"]:
            if term_name in my_dict["by_term"] and 'packages' in my_dict["by_term"][term_name]:
                my_dict["by_term"][term_name]['packages'].append(package_name)
                my_dict["by_term"][term_name]['count'] += 1
            else:
                if term_name not in my_dict["by_term"]:
                    my_dict["by_term"][term_name] = {}
                my_dict["by_term"][term_name]['packages'] = [package_name]
                my_dict["by_term"][term_name]['count'] = 1
    my_dict["by_term_count"] = {}

    # now to add by_term_count
    for term_name in my_dict["by_term"]:
        my_total = my_dict["by_term"][term_name]['count']
        if my_total not in my_dict["by_term_count"]:
            my_dict["by_term_count"][my_total] = {}
        my_dict["by_term_count"][my_total][term_name] = {}
        my_dict["by_term_count"][my_total][term_name]['packages'] = my_dict["by_term"][term_name]['packages']

    # ic(my_dict["by_term_count"])
    # sys.exit()
    return my_dict

