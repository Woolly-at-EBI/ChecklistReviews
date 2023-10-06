#!/usr/bin/env python3
"""Script of source_package_name_comparisons.py is to source_package_name_comparisons.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-10-06
__docformat___ = 'reStructuredText'
chmod a+x source_package_name_comparisons.py
"""



from icecream import ic
import os
import argparse

class source_package_name_comparisons:
    def __init__(self, source1_list, source2_list):
        self.source1_set = set(source1_list)
        self.source2_set = set(source2_list)
        self.matching_package_name_dict = {}
        self.source2_matched_set = set()
        self.matching_package_name_dict['src1_to_src2'] = {}


    def is_ena_mix_match(self, source1_package_name):

        matching = [s for s in self.source2_set if source1_package_name in s]
        if len(matching) > 0:
            ic(f"match for {source1_package_name} is {matching}")
            self.matching_package_name_dict['ena2mixs'][source1_package_name] = matching
            self.source2_matched_set.update(matching)
            return True
        return False

    def get_matching_s1_set(self):
        if hasattr(self, 'source1_matching_set'):
            return self.source1_matching_set
        self.compareChecklistsByName()
        return self.source1_matching_set

    def get_non_matching_s1_set(self):
        if hasattr(self, 'source1_matching_set'):
            return self.source1_not_matching_set
        self.compareChecklistsByName()
        return self.source1_not_matching_set

    def get_matching_package_name_dict(self):
        if hasattr(self, 'source1_matching_set'):
            return self.matching_package_name_dict
        self.compareChecklistsByName()
        return self.matching_package_name_dict
    #
    def compareChecklistsByName(self):
        self.source1_matching_set = set()
        self.source1_not_matching_set = set()
        def source1_mix_match(source1_package_name, source2_package_list):
            matching = [s for s in source2_package_list if source1_package_name in s]
            if len(matching) > 0:
                ic(f"match for {source1_package_name} is {matching}")
                self.matching_package_name_dict['src1_to_src2'][source1_package_name] = matching
                #mixs_matched_set.update(matching)
                return True
            return False

        for source1_package_name in self.source1_set:
            ic(source1_package_name)
            if source1_mix_match(source1_package_name, list(self.source2_set), ):
                self.source1_matching_set.add(source1_package_name)
            else:
                self.source1_not_matching_set.add(source1_package_name)

        ic(f"matching source1 packages seen in source2: {self.source1_matching_set}")
        ic(f"Not matching source1 packages seen in source2: {self.source1_not_matching_set}")


        #ic(matching_package_name_dict)


def main():
    pass

if __name__ == '__main__':
    ic()
    main()
