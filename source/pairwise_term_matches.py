from icecream import ic
import pandas as pd
from clean_terms import *
from rapidfuzz import process
import sys

class pairwise_term_matches:
    """pairwise_term_matches object as simple object orientated to reduce complexity and saves passing a big hash.

    pairwise_term_matches(pair_string, left_term_list, right_term_list)
    """

    def process_names(self, pair_string):
        """

        :param pair_string:
        :return:
        """
        self.pair_string = pair_string
        ic(pair_string)
        pair_source = pair_string.split('::')
        self.left_name = pair_source[0]
        self.right_name = pair_source[1]

    def get_left_name(self):
        return(self.left_name)

    def get_right_name(self):
        return(self.right_name)

    def unique_sorted_list(self, my_list):
        return sorted(list(set(my_list)))

    def __init__(self, pair_string, left_term_list, right_term_list):
        """

        :param pair_string:
        :param left_term_list:
        :param right_term_list:
        """
        ic()
        self.process_names(pair_string)
        ic(self.get_left_name())
        self.left_term_list = self.unique_sorted_list(left_term_list)
        self.right_term_list = self.unique_sorted_list(right_term_list)
        clean_hash = self.get_clean_hash()

        pairwise_matches = {'left': {"exact": {}, "harmonised": {}, "no_matches": {}}, 'right': {"no_matches": {}}}
        self.pairwise_matches = pairwise_matches
        left_pairwise_matches = pairwise_matches["left"]
        right_pairwise_matches = pairwise_matches["right"]

        self.comparison_df = compareAllTerms(self.left_term_list, self.right_term_list)
        df = self.comparison_df
        # test_comparison_df_file = "../data/" + pair_string + "_comparison_df.tsv"
        # df.to_csv(test_comparison_df_file, sep="\t")
        # ic(f"created {test_comparison_df_file}")

        ic(df.head(20))
        ic(df['match_type'].unique())

        for match_type in df['match_type'].unique():
            tmp_df = df.query('match_type == @match_type')
            #ic(match_type)
            #ic(tmp_df.head(5))
            if match_type == "exact":
                self.left_exact_matched_set = set(tmp_df.left_term)
                self.right_exact_matched_set = set(tmp_df.match)
            elif match_type == "harmonised":
                self.left_harmonised_matched_set = set(tmp_df.left_term)
                self.right_harmonised_matched_set = set(tmp_df.match)
            elif match_type == "fuzzy":
                self.left_fuzzy_matched_set = set(tmp_df.left_term)
                self.right_fuzzy_matched_set = set(tmp_df.match)
            elif match_type == "none":
                self.left_not_matched_set = set(tmp_df.left_term)
            else:
                print(f"ERROR: match_type={match_type} is not yet being processed correctly")
                sys.exit()
        #sys.exit()
    def get_left_exact_matched_list(self):
        return sorted(self.left_exact_matched_set)

    def get_left_harmonised_matched_list(self):
        return sorted(self.left_harmonised_matched_set)

    def get_left_fuzzy_matched_list(self):
        return sorted(self.left_fuzzy_matched_set)

    def get_left_not_matched_list(self):
        return sorted(self.left_not_matched_set)

    def get_right_exact_matched_list(self):
        return sorted(self.right_exact_matched_set)

    def get_right_harmonised_matched_list(self):
        return sorted(self.right_harmonised_matched_set)

    def get_right_fuzzy_matched_list(self):
        return sorted(self.right_fuzzy_matched_set)

    def set_right_sets(self):
        self.any_right_matched_set = self.right_exact_matched_set
        self.any_right_matched_set.update(self.right_harmonised_matched_set)
        self.confident_any_right_matched_set = self.any_right_matched_set
        self.any_right_matched_set.update(self.right_fuzzy_matched_set)
    def get_right_not_matched_list(self):
        return(sorted(self.right_not_matched_set))


    def get_any_left_match_list(self):
        return list(self.any_right_matched_set)



    def get_clean_hash(self):
        clean_hash = {}
        pairwise_matches = {}
        for left in self.left_term_list:
            clean_hash[left] = clean_term(left)
        for right in self.right_term_list:
            clean_hash[right] = clean_term(right)
        self.clean_hash = clean_hash
        return self.clean_hash



def term_alignment_dict2df(my_dict):
    """

    :param my_dict:
    :return: df
    df = df[["left_term", "match_type", "match", "fuzzy_score"]]
    """
    df = pd.DataFrame.from_dict(my_dict, orient = 'index')
    df["left_term"] = df.index
    df = df[["left_term", "match_type", "match", "fuzzy_score"]]
    df["fuzzy_score"] = df["fuzzy_score"].astype(int)
    return df

def compareAllTerms(left_list, right_list):
    """
    The most important method of the lot as this compares all terms in one list with another.
    Currently, it supports match_type:exact|harmonised|fuzzy|none
      harmonised is where terms are simply cleaned: lower cased and punctuation changed to "_"
      it could have all been doing with rapidfuzz, but thought a little flexibility/control wise
      and allows some future flexibility of additional comparators.
      Also, the run time will be slightly quicker not putting everything through rapidfuzz
    :param left_list:
    :param right_list:
    :return: df: #['left_term', 'match_type:exact|harmonised|fuzzy|none', 'match', 'fuzzy_score', 'match_term_duplicated:boolean']
    """
    #make sure that the lists are unique and sorted, note the slight name change, in case we need the original list again
    left_term_set = set(left_list)
    right_term_set = set(right_list)
    left_term_list = sorted(left_term_set)
    right_term_list = sorted(right_term_set)
    # ic(f"left len={len(left_term_list)} right len={len(right_term_list)}")

    left_clean_dict, left_raw_dict = generate_clean_dict(left_term_list)
    right_clean_dict, right_raw_dict = generate_clean_dict(right_term_list)

    left_clean_set = set(left_clean_dict.keys())
    right_clean_set = set(right_clean_dict.keys())
    exact_intersection_set = left_term_set.intersection(right_term_set)
    clean_intersection_set = left_clean_set.intersection(right_clean_set)

    my_dict = {}
    fuzzy_threshold = 85
    for left_term in left_term_list:
        my_dict[left_term] = {"match_type": "none", "fuzzy_score": 100}
        left_clean = left_raw_dict[left_term]
        # print(f"{left_term} - {left_clean}")
        if left_term in exact_intersection_set:
            my_dict[left_term]["match"] = left_term
            my_dict[left_term]["match_type"] = "exact"
        elif left_clean in clean_intersection_set:
            my_dict[left_term]["match"] = right_clean_dict[left_clean]
            my_dict[left_term]["match_type"] = "harmonised"
        else:
            resp_match = process.extractOne(left_term, right_term_list)
            if resp_match[1] > fuzzy_threshold:
                my_dict[left_term]["match_type"] = "fuzzy"
                my_dict[left_term]["fuzzy_score"] = resp_match[1]
                my_dict[left_term]["match"] = resp_match[0]
            else:
                my_dict[left_term]["fuzzy_score"] = 0
                my_dict[left_term]["match_type"] = "none"
                my_dict[left_term]["match"] = ""

    df = term_alignment_dict2df(my_dict)
    # Indicate where  match_term is duplicated
    # ic(df.match_type.value_counts())
    tmp_df = df.match.value_counts().rename_axis('unique_values').to_frame('counts').reset_index().query('counts > 1')
    dup_set = set(tmp_df.unique_values.tolist())
    # ic(dup_set)
    df['match_term_duplicated'] = df['match'].apply(lambda x: True if x in dup_set and x != "" else False)
    # ic(df.head(20))
    # print(df.to_markdown(index=False))

    return df


