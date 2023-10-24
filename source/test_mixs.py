import sys
import unittest
from analyse_mixs import *
from mixs import generate_mixs6_object, generate_ena_object, get_ena_dict
from icecream import ic


class Testmixs(unittest.TestCase):

    mixs_v6_obj, mixs_v6_dict, linkml_mixs_dict = generate_mixs6_object()
    ena_cl_dict = get_ena_dict()
    ena_cl_obj = mixs(ena_cl_dict, "ena_cl", linkml_mixs_dict)

    mixs_v5_dict = get_mixs_v5_dict()
    mixs_v5_obj = mixs(mixs_v5_dict, "mixs_v5", linkml_mixs_dict)


    def test_ingest_ena_cl(self):
        # ic(type(self.ena_cl_obj))
        self.assertIsInstance(self.ena_cl_obj, mixs)

    def test_get_type(self):
        self.assertEqual(self.ena_cl_obj.get_type(), 'ena_cl')
        self.assertEqual(self.mixs_v5_obj.get_type(), 'mixs_v5')
        self.assertEqual(self.mixs_v6_obj.get_type(), 'mixs_v6')

    def test_generate_ena_object(self):
        ena_cl_obj, ena_cl_dict = generate_ena_object()
        self.assertEqual(ena_cl_obj.type,'ena_cl')

    def test_get_all_term_list(self):
        # ic(self.ena_cl_obj.get_all_term_list())
        term_list = self.ena_cl_obj.get_all_term_list()
        self.assertEqual(term_list[0], '16S recovered')

    def test_get_term_dict(self):
        my_term_dict = self.ena_cl_obj.get_term_dict()
        #ic(my_term_dict)
        term_count_w_des = 0
        term_count_wo_des = 0
        for term in my_term_dict:
            if 'description' in my_term_dict[term]:
                term_count_w_des += 1
            else:
                term_count_wo_des += 1
        #ic(term_count_w_des)
        #ic(term_count_wo_des)
        self.assertEqual(term_count_wo_des, 0)


    def test_get_terms_with_freq(self):
        # ic(self.ena_cl_obj.get_terms_with_freq())
        my_dict = self.ena_cl_obj.get_terms_with_freq()
        self.assertEqual(my_dict['isolation and growth condition'], 18)

    def test_get_terms_by_freq(self):
        my_dict = self.ena_cl_obj.get_terms_by_freq()
        test_18 = {'term_count_with_freq': 9,
                   'terms': ['ploidy',
                             'estimated size',
                             'sample volume or weight for DNA extraction',
                             'pcr primers',
                             'isolation and growth condition',
                             'sample storage duration',
                             'sample storage location',
                             'host disease status',
                             'known pathogenicity']}
        self.assertDictEqual(my_dict[18], test_18)

    def test_get_term_top(self):
        # ic(self.ena_cl_obj.get_term_top(2))
        test_list = ['collection date', 'geographic location (country and/or sea)']
        self.assertListEqual(self.ena_cl_obj.get_term_top(2), test_list)


    def test_get_all_term_count(self):
        #ic(self.ena_cl_obj.get_all_term_count())
        self.assertEqual(self.ena_cl_obj.get_all_term_count(), 631)

    def test_print_term_summary(self):
        # ic(self.ena_cl_obj.print_term_summary(2))
        test_out = "term_count=631 first 2 terms=['16S recovered', '16S recovery software']"
        self.assertEqual(self.ena_cl_obj.print_term_summary(2), test_out)

    def test_get_all_package_list(self):
        # ic("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.assertEqual(len(self.ena_cl_obj.get_all_package_list()),40)

    def test_get_all_package_count(self):
         self.assertEqual(self.ena_cl_obj.get_all_package_count(),40)

    def test_print_package_summary(self):
        # print(self.ena_cl_obj.print_package_summary())
        test_out = "package_count=40 packages=COMPARE-ECDC-EFSA pilot food-associated reporting standard, COMPARE-ECDC-EFSA pilot human-associated reporting standard, ENA Crop Plant sample enhanced annotation checklist, ENA Global Microbial Identifier Proficiency Test (GMI PT) checklist, ENA Global Microbial Identifier reporting standard checklist GMI_MDM:1.1, ENA Influenza virus reporting standard checklist, ENA Marine Microalgae Checklist, ENA Micro B3, ENA Plant Sample Checklist, ENA Shellfish Checklist, ENA Tara Oceans, ENA UniEuk_EukBank Checklist, ENA binned metagenome, ENA default sample checklist, ENA mutagenesis by carcinogen treatment checklist, ENA parasite sample checklist, ENA prokaryotic pathogen minimal sample checklist, ENA sewage checklist, ENA virus pathogen reporting standard checklist, GSC MIMAGS, GSC MISAGS, GSC MIUVIGS, GSC MIxS air, GSC MIxS built environment, GSC MIxS host associated, GSC MIxS human associated, GSC MIxS human gut, GSC MIxS human oral, GSC MIxS human skin, GSC MIxS human vaginal, GSC MIxS microbial mat biolfilm, GSC MIxS miscellaneous natural or artificial environment, GSC MIxS plant associated, GSC MIxS sediment, GSC MIxS soil, GSC MIxS wastewater sludge, GSC MIxS water, HoloFood Checklist, PDX Checklist, Tree of Life Checklist"
        self.assertEqual(self.ena_cl_obj.print_package_summary(), test_out)

    #
    # def test_print_summaries(self):
    #     self.fail()

    def test_get_term_list_for_package(self):
        #ic(self.ena_cl_obj.get_term_list_for_package('GSC MIxS human gut'))
        self.assertIn('observed biotic relationship', self.ena_cl_obj.get_term_list_for_package('GSC MIxS human gut'))


if __name__ == '__main__':
    unittest.main()
