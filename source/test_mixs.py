import sys
import unittest
from analyse_mixs import *
from icecream import ic


class Testmixs(unittest.TestCase):
    linkml_mixs_dict = parse_new_linkml()
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)

    def test_ingest_ena_cl(self):
        ic(type(self.ena_cl_obj))
        self.assertIsInstance(self.ena_cl_obj, mixs)

    def test_get_type(self):
        self.assertEqual(self.ena_cl_obj.get_type(), 'ena_cl')

    def test_get_all_term_list(self):
        # ic(self.ena_cl_obj.get_all_term_list())
        term_list = self.ena_cl_obj.get_all_term_list()
        self.assertEqual(term_list[0], '16S recovered')

    def test_get_terms_with_freq(self):
        # ic(self.ena_cl_obj.get_terms_with_freq())
        my_dict = self.ena_cl_obj.get_terms_with_freq()
        self.assertEqual(my_dict['isolation and growth condition'], 18)

    def test_get_terms_by_freq(self):
        my_dict = self.ena_cl_obj.get_terms_by_freq()
        test_18 = {'term_count_with_freq': 7,
                   'terms': ['ploidy',
                             'estimated size',
                             'sample volume or weight for DNA extraction',
                             'pcr primers',
                             'isolation and growth condition',
                             'sample storage duration',
                             'sample storage location']}
        self.assertDictEqual(my_dict[18], test_18)

    def test_get_term_top(self):
        # ic(self.ena_cl_obj.get_term_top(2))
        test_list = ['collection date', 'geographic location (country and/or sea)']
        self.assertListEqual(self.ena_cl_obj.get_term_top(2), test_list)


    def test_get_all_term_count(self):
        #ic(self.ena_cl_obj.get_all_term_count())
        self.assertEqual(self.ena_cl_obj.get_all_term_count(), 625)

    def test_print_term_summary(self):
        ic(self.ena_cl_obj.print_term_summary(2))
        test_out = "term_count=625 first 2 terms=['16S recovered', '16S recovery software']"
        self.assertEqual(self.ena_cl_obj.print_term_summary(2), test_out)

    def test_get_all_package_list(self):
        ic("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.assertEqual(len(self.ena_cl_obj.get_all_package_list()),40)

    # def test_get_all_package_count(self):
    #     self.fail()
    #
    # def test_print_package_summary(self):
    #     self.fail()
    #
    # def test_print_summaries(self):
    #     self.fail()
    #
    # def test_get_term_list_for_package(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
