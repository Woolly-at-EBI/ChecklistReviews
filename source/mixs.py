from icecream import ic
import sys
import os
import json
import pickle

class mixs:
    def ingest_ena_cl(self):
        self.my_dict = process_ena_cl(self.my_dict_raw, self.linkml_mixs_dict)

    def __init__(self, my_dict, type, linkml_mixs_dict):
        ic()
        # type could be  "mixs_v5" or "mixs_v6"
        self.type = type

        if type == "ena_cl":
            #ic(f"type = {type}")
            #ic(f"self.type = {self.type}")
            self.my_dict_raw = my_dict
            self.linkml_mixs_dict = linkml_mixs_dict
            self.ingest_ena_cl()
            # self.cl_details_dict = get_ena_cl_details(self.my_dict_raw)
            # ic(f"self.type = {self.type}")
        else:
            # ic(f"type = {type}")
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
        ic(self)
        if not hasattr(self, 'terms_with_freq'):
            self.get_terms_by_freq()

        return self.terms_with_freq

    def get_terms_by_freq(self):
        """

        :return:  40: {'term_count_with_freq': 2,
                        'terms': dict_keys(['collection date', 'geographic location (country and/or sea)'])}}
        """

        if hasattr(self, 'my_just_freq'):
            return self.my_just_freq

        my_just_freq = {}
        if "by_term_count" not in self.my_dict:
            add_term_package_count(self.my_dict)
        self.terms_with_freq = {}


        freq_keys = sorted(self.my_dict["by_term_count"].keys(), reverse = True)
        # ic("KEYS=+++++++++++++++++++++++++")
        # ic(freq_keys)
        # ic(self.my_dict["by_term_count"][40].keys())
        for freq_key in freq_keys:
            my_just_freq[freq_key] = {}
            my_just_freq[freq_key]["terms"] = list(self.my_dict["by_term_count"][freq_key].keys())
            my_just_freq[freq_key]["term_count_with_freq"] = len(my_just_freq[freq_key]["terms"])
            for term in my_just_freq[freq_key]["terms"]:
                self.terms_with_freq[term] = freq_key
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
            # ic(my_just_freq[freq_key]["terms"])
            top_terms.extend(list(my_just_freq[freq_key]["terms"]))
            if len(top_terms) >= first_number:
                return top_terms[0:first_number]
        return top_terms

    def get_all_term_count(self):
        return (len(self.my_dict['by_term'].keys()))

    def print_term_summary(self, top):
        """

        :param top: = top # number to print, if "", print all, well string to print
        :return:
        """
        if top == "":
            return_str = f"term_count={self.get_all_term_count()}  terms={self.get_all_term_list()}"
        else:
            return_str = f"term_count={self.get_all_term_count()} first {top} terms={self.get_all_term_list()[0:top]}"
        return return_str

    def get_gsc_packages(self):
        if hasattr(self, 'gsc_package_set'):
            return list(self.gsc_package_set)

        if self.type == 'ena_cl':
            self.gsc_package_set = set(filter(lambda x: x.startswith("GSC"), self.get_all_package_list()))
            self.not_gsc_package_set = [x for x in self.get_all_package_list() if x not in self.gsc_package_set]
        else: #will be GSC MIXS
            self.gsc_package_set = set(self.get_all_package_list())
            self.not_gsc_package_set = set()
        return list(self.gsc_package_set)

    def get_gsc_package_name_dict(self):
        if hasattr(self, 'gsc_package_name_dict'):
            return self.gsc_package_name_dict
        self.get_gsc_packages()
        return self.gsc_package_name_dict


    def get_not_gsc_packages(self):
        if not hasattr(self, 'not_gsc_package_set'):
            self.get_gsc_packages()
        return list(self.not_gsc_package_set)

    def get_gsc_packages_mixs_style_nomenclature_list(self):
        """
        remove things like GSC prefix
        :return:
        """
        if hasattr(self, 'gsc_packages_mixs_style_nomenclature_set'):
            return self.gsc_packages_mixs_style_nomenclature_set
        self.gsc_packages_mixs_style_nomenclature_set = set()
        if self.type == 'ena_cl':
            self.gsc_package_name_dict = {}
            for package_name in self.get_gsc_packages():
                mixs_package_style_name = package_name.removeprefix('GSC ').removeprefix('MIxS ').replace(' ', '-', 1) \
                    .replace(' ', '', 1)
                # saving first and rest using split()
                init, *temp = mixs_package_style_name .split(' ')

                # using map() to get all words other than 1st
                # and titlecasing them
                mixs_package_style_name = ''.join([init.capitalize(), *map(str.title, temp)])
                mixs_package_style_name = mixs_package_style_name.replace('Misags', 'MISAG').replace('Mimags', 'MIMAG')\
                    .replace('Miuvigs','MIUVIG').replace('Built-environment','BuiltEnvironment')\
                    .replace('Miscellaneous-naturalorArtificialEnvironment','MiscellaneousNaturalOrArtificialEnvironment') \
                    .replace('Wastewater-sludge','WastewaterSludge').replace('Microbial-matbiolfilm','MicrobialMatBiofilm')
                self.gsc_packages_mixs_style_nomenclature_set.add(mixs_package_style_name)
                self.gsc_package_name_dict[package_name] = {'mix_style_name': mixs_package_style_name}
        else:
            self.gsc_packages_mixs_style_nomenclature_set = set(self.get_gsc_packages())
        #ic(self.gsc_package_name_dict)
        return self.gsc_packages_mixs_style_nomenclature_set

    def get_all_package_list(self):
        if hasattr(self, 'all_package_list'):
            return self.all_package_list
        self.all_package_list = sorted(self.my_dict['by_package'].keys())
        #ic(type(self.all_package_list))
        return self.all_package_list

    def get_all_package_count(self):
        return (len(self.my_dict['by_package'].keys()))

    def print_package_summary(self):
        """
        all kinds of wierdness happening with a simple list to string conversion...
        f strings even misbehaved so had to break it down. no idea why. oh well.
        :return:
        """
        package_list = self.get_all_package_list()
        # ic(package_list)
        package_list_string = ', '.join(package_list)
        # print(package_list_string)
        # print("++++++++++++++++++++++++++++++++++++++++")
        return_str = "package_count=" + str(self.get_all_package_count()) + " packages=" + package_list_string
        # print(return_str)
        return return_str

    def print_summaries(self):
        print(self.print_term_summary(10))
        print(self.print_package_summary())

    # def get_all_checklists(self):
    #     self.cl_details_dict

    def get_term_list_for_package(self, package_cl_name):
        # ic("inside get_term_list_for_package", package_cl_name)
        # ic(self.my_dict['by_package'][package_cl_name])
        return list(self.my_dict['by_package'][package_cl_name]['field'].keys())


# **********************************************************************************

def process_mixs_dict(my_dict, linkml_dict):
    """
    /used for mixs5 at least

    :param my_dict:
    :param linkml_dict:
    :return:
    """
    # for top in my_dict:
    #     print(top)

    #
    # for top_defs in my_dict["$defs"]:
    #     # ic(top_defs)
    #     pass
    #
    # for agr_defs in my_dict["$defs"]["Agriculture"]:
    #     ic(agr_defs)
    #
    # for agr_prop_defs in my_dict["$defs"]["Agriculture"]["properties"]:
    #     ic(agr_prop_defs)

    MIXS_review_dict = {"by_package": {}, "by_term": {}}

    def get_long_name(short_term_name, linkml_dict):
        if short_term_name in linkml_dict["slots"]:
            return linkml_dict["slots"][short_term_name]['title']
        return short_term_name

    for top_def in my_dict["$defs"]:
        # print(top_def)
        package_name = top_def
        printed_top = False
        for second_def in my_dict["$defs"][top_def]:
            if not printed_top and second_def == 'properties':
                MIXS_review_dict["by_package"][top_def] = {}
                MIXS_review_dict["by_package"][top_def]["count"] = 0
                MIXS_review_dict["by_package"][top_def]["field"] = {}
                # print("") #
                # print(top_def, end = ": ")
                printed_top = True
            # print(f"\t{second_def}")
            # print(f"\t\tsub_dict={my_dict['$defs'][top_def][second_def]}")
            # sub_dict = my_dict["$defs"][top_def][second_def]
            # print(f"\t\tsub={sub_dict}")
            if second_def == 'properties':
                # print(f"\t\t{second_def} property_count={len(my_dict['$defs'][top_def][second_def])}", end = " properties: ")
                for third_def in my_dict["$defs"][top_def][second_def]:
                    # print(f"{third_def}", end = ", ")

                    term_name = get_long_name(third_def, linkml_dict)
                    MIXS_review_dict["by_package"][top_def]["field"][term_name] = {}

                MIXS_review_dict["by_package"][package_name]["count"] = len(
                    MIXS_review_dict["by_package"][package_name]["field"])
            else:
                pass
    # ic(MIXS_review_dict)
    MIXS_review_dict = add_term_package_count(MIXS_review_dict)
    # print_mixs_review_dict_stats(MIXS_review_dict)
    return MIXS_review_dict

def parse_new_linkml():
    """

    :return:
    mixs6_2_dict
        ["slots"][short_term_name]['description'] = "description"
        ["slots"][short_term_name]['title'] = "long_name_ena_uses"
    """
    json_file = "/Users/woollard/projects/GSC/code/mixs-6-2-release-candidate/schema-derivatives/mixs_6_2_rc.json"

    if os.path.isfile(json_file):
        ic(f"about to open {json_file}")
        with open(json_file) as f:
            r_json = json.load(f)

    # for slot in r_json["slots"]:
    #     print(slot)
    #     #title  id
    #     for tag in ('slot_uri', 'description', 'title'):
    #         if tag in r_json['slots'][slot]:
    #             print(f"\t{tag}=\t{r_json['slots'][slot][tag]}")
    #
    #     if slot == "alt":
    #         print(r_json['slots'][slot])

    return r_json

def get_mixs_dict(dict_name):
    """

    :return:
    """
    if dict_name == "my_dict_v6":
        pickle_file = '../data/v6_mixs.schema.json.pickle'
    elif dict_name == "my_dict_v5":
        pickle_file = '../data/v5_mixs.schema.json.pickle'
    else:
        print(f"ERROR: {dict_name} is not recognised")
        sys.exit()

    if not os.path.isfile(pickle_file):
        my_dict = json.loads(get_data())
        with open(pickle_file, 'wb') as handle:
            pickle.dump(my_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)

    if os.path.isfile(pickle_file):
        with open(pickle_file, 'rb') as handle:
            my_dict = pickle.load(handle)
    else:
        print(f"ERROR no {pickle_file}")
        sys.exit()

    return my_dict
def generate_mixs6_object():
    """
    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    :return:
    """
    linkml_mixs_dict = parse_new_linkml()
    my_dict_v6 = get_mixs_dict("my_dict_v6")
    mixs_v6_dict = process_mixs_dict(my_dict_v6, linkml_mixs_dict)
    mixs_v6_obj = mixs(mixs_v6_dict, "mixs_v6", linkml_mixs_dict)
    return mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict


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

