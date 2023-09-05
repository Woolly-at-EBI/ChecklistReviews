import unittest
from clean_terms import clean_term, clean_list, generate_clean_dict, cleanList2set
from icecream import ic

class Test(unittest.TestCase):


    def test_clean_term(self):
        test_in = 'Some-Term'
        test_out = 'some_term'
        self.assertEqual(clean_term(test_in), test_out)
    def test_clean_list(self):
        test_in = ['Some-Term', 'another_TERM']
        test_out = ['some_term', 'another_term']
        self.assertListEqual(clean_list(test_in), test_out)

    def test_generate_clean_dict(self):
        test_list = ['Some-Term']
        test_clean_out = {'some_term': 'Some-Term'}
        test_raw_out = {'Some-Term': 'some_term'}
        clean_dict, raw_dict = generate_clean_dict(test_list)
        self.assertDictEqual(clean_dict, test_clean_out)
        self.assertDictEqual(raw_dict, test_raw_out)

    def test_cleanList2set(self):
        test_in = ['Some-Term', 'another_TERM', 'another_TERM']
        test_out = set(['some_term','another_term'])
        self.assertSetEqual(cleanList2set(test_in), test_out)


if __name__ == '__main__':
    unittest.main()