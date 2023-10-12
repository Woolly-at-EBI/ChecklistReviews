from icecream import ic
import pandas as pd
from clean_terms import *
from rapidfuzz import process
import sys
import re

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
        # ic(self.get_left_name())
        self.left_term_list = self.unique_sorted_list(left_term_list)
        self.right_term_list = self.unique_sorted_list(right_term_list)
        clean_hash = self.get_clean_hash()

        pairwise_matches = {'left': {"exact": {}, "harmonised": {}, "no_matches": {}}, 'right': {"no_matches": {}}}
        self.pairwise_matches = pairwise_matches
        left_pairwise_matches = pairwise_matches["left"]
        right_pairwise_matches = pairwise_matches["right"]

        self.comparison_df = compareAllTerms(self.left_term_list, self.right_term_list)
        df = self.comparison_df

        # ic(df.head(20))
        # ic(df['match_type'].unique())
        self.left_all_set = set(self.left_term_list)
        self.left_exact_matched_set = set()
        self.left_fuzzy_matched_set = set()
        self.left_harmonised_matched_set = set()
        self.left_not_matched_set = set()

        self.left_high_confident_matched_list = []
        self.left_medium_confident_matched_list = []
        self.left_low_confident_matched_list = []
        self.right_high_confident_matched_list = []
        self.right_medium_confident_matched_list = []
        self.right_low_confident_matched_list = []

        self.right_exact_matched_set = set()
        self.right_fuzzy_matched_set = set()
        self.right_harmonised_matched_set = set()
        self.right_not_matched_set = set()


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

        self.left_confident_matched_set = set(self.left_exact_matched_set)
        self.left_confident_matched_set.union(self.left_harmonised_matched_set )
        self.set_right_sets()

    def get_complete_matches_df(self):
        """

        :return: the dataframe of all the matches (and none matches)
        """
        return (self.comparison_df)


    def get_harmonised_and_exact_match_df(self):
        """
        filters the df to just provide the confident match rows, N.B. may still have some errors
        :return: harmonised_df
        """
        ic()

        if hasattr(self,'harmonised_df'):
            return self.harmonised_df

        df = self.comparison_df
        ic(len(df))
        fuzzy_cut_off = 90
        harmonised_df = df.query('fuzzy_score > @fuzzy_cut_off')
        self.harmonised_df = self.assess_likely_map_accuracy(harmonised_df)

        self.vlow_confidence_mapping_df = df.query('fuzzy_score <= @fuzzy_cut_off & match_type != "none"')
        #print(self.vlow_confidence_mapping_df.head(30).to_markdown())
        ic(len(self.harmonised_df))
        return self.harmonised_df

    def get_vlow_confidence_mapping_match_df(self):
        def do_counts():
            self.left_vlow_confident_matched_list = self.vlow_confidence_mapping_df['left_term'].to_list()
            self.right_vlow_confident_matched_list = self.vlow_confidence_mapping_df['match'].to_list()

        if hasattr(self,'vlow_confidence_mapping_df'):
            do_counts()
            return self.vlow_confidence_mapping_df

        self.get_harmonised_and_exact_match_df()   #runs this, it populates the df needed to.
        #means don;t have the fizzy cut off in 2 places
        do_counts()

        return self.vlow_confidence_mapping_df

    def get_just_harmonised_df(self):
        """
        filters the df to just provide the confident, but not exact match rows, N.B. may still have some errors
        :return: harmonised_df
        """
        ic()
        df = self.comparison_df
        ic(len(df))
        harmonised_df = df.query('fuzzy_score > 90 and match_type != "exact"')
        ic(len(harmonised_df))
        harmonised_df = self.assess_likely_map_accuracy(harmonised_df)
        return harmonised_df

    def process_assessments(self, assessed_df):
        ic(assessed_df.head(2))
        filtered_df = assessed_df.query('likely_map_accuracy > 0.7 & match_type != "exact"')
        self.left_high_confident_matched_list = filtered_df['left_term'].to_list()
        self.right_high_confident_matched_list = filtered_df['match'].to_list()


        filtered_df = assessed_df.query('likely_map_accuracy <= 0.7 & likely_map_accuracy > 0.5')
        ic(filtered_df)
        self.left_medium_confident_matched_list = filtered_df['left_term'].to_list()
        self.right_medium_confident_matched_list = filtered_df['match'].to_list()

        filtered_df = assessed_df.query('likely_map_accuracy <= 0.5 & likely_map_accuracy >= 0')
        self.left_low_confident_matched_list = filtered_df['left_term'].to_list()
        ic(self.left_low_confident_matched_list)
        self.right_low_confident_matched_list = filtered_df['match'].to_list()

        ic(self.left_high_confident_matched_list)
        # ic(self.right_high_confident_matched_list)
        ic(self.left_medium_confident_matched_list)
        # ic(self.right_medium_confident_matched_list)
        ic(self.left_low_confident_matched_list)
        # ic(self.right_low_confident_matched_list)

        ic(assessed_df.query('left_term == "total nitrogen method"'))
        #sys.exit()



    def assess_likely_map_accuracy(self, df):
        """
        adding an assessment of mapping accuracy, with 2 columns
         likely_map_accuracy  = 0-1 where 1 is exact and 0 ignore.
         map_accuracy_des = textual description of why the accuracy was called.
         There is already the fuzzy mapping score, but after the use as a rough cutoff is not that useful
        :param df:
        :return:
        """
        def assess_mapping(row):


            if row['match_type'] == 'none':
                return pd.Series([0, "no match"])
            elif row['match_type'] == 'exact':
                return pd.Series([1, "exact"])
            elif row['fuzzy_score'] == 100:
                return pd.Series([1, "very_close"])
            elif re.search("[0-9]$", row['left_term']) and not re.search("[0-9]$", row['match']):
                return pd.Series([0.5, "left has numerical suffix"])
            elif not row['match_term_duplicated'] and (row['match'] in row['left_term']):
                return pd.Series([0.7, "right is a substring of left"])
            elif row['match_term_duplicated'] and (row['match'] in row['left_term']):
                return pd.Series([0.3, "right is a substring of left, but also matched elsewhere"])

            # now need to do some more in depth checking
            clean_left = clean_term(row['left_term'])
            clean_right = clean_term(row['match'])
            clean_left_set = set(clean_left.split('_'))
            clean_right_set = set(clean_right.split('_'))
            #print(f"cleft={clean_left} cright={clean_right}")
            if clean_left == clean_right:
                return pd.Series([1, "exact after simple harmonisation"])
            elif not row['match_term_duplicated'] and (clean_right in clean_left):
                return pd.Series([0.7, "right is a substring of left"])
            elif not row['match_term_duplicated'] and (clean_left in clean_right):
                return pd.Series([0.7, "left is a substring of right"])
            elif row['match_term_duplicated'] and (clean_right in clean_left):
                return pd.Series([0.3, "right is a substring of left, but also matched elsewhere"])
            elif row['match_term_duplicated'] and (clean_left in clean_right):
                return pd.Series([0.7, "left is a substring of right, but also matched elsewhere"])
            elif not row['match_term_duplicated'] and len(clean_right_set.intersection(clean_left_set)) >= (len(clean_left_set) -1):
                return pd.Series([0.7, "left and right one word apart"])
            elif row['match_term_duplicated'] and len(clean_right_set.intersection(clean_left_set)) >= (len(clean_left_set) -1):
                return pd.Series([0.5, "left and right one word apart, but also matched elsewhere"])
            elif len(clean_right_set.intersection(clean_left_set)) >= (len(clean_left_set) -2):
                return pd.Series([0.3, "left and right two words apart"])
            else:
                return pd.Series([0, "doubtful"])

        assessed_df = df.copy()

        assessed_df[['likely_map_accuracy', 'map_accuracy_des']] = assessed_df.apply(assess_mapping, axis = 1)
        #assessed_df = assessed_df.query('likely_map_accuracy < 1')
        #print(assessed_df.to_markdown(index = False))


        self.process_assessments(assessed_df)

        return assessed_df

    def get_left_exact_matched_list(self):
        return sorted(self.left_exact_matched_set)

    def get_left_harmonised_matched_list(self):
        return sorted(self.left_harmonised_matched_set)

    def get_left_fuzzy_matched_list(self):
        return sorted(self.left_fuzzy_matched_set)

    def get_left_confident_matched_list(self):
        return sorted(self.left_confident_matched_set)

    def get_left_not_matched_list(self):
        return sorted(self.left_not_matched_set)

    def get_right_exact_matched_list(self):
        return sorted(self.right_exact_matched_set)

    def get_right_harmonised_matched_list(self):
        return sorted(self.right_harmonised_matched_set)

    def get_right_fuzzy_matched_list(self):
        return sorted(self.right_fuzzy_matched_set)

    def get_right_confident_matched_list(self):
        return sorted(self.right_confident_matched_set)

    def set_right_sets(self):
        # ic(len(self.right_term_list))
        # ic(len(self.right_exact_matched_set))
        # ic(len(self.right_harmonised_matched_set))
        # ic(len(self.right_fuzzy_matched_set))
        self.any_right_matched_set = set(self.right_exact_matched_set)
        self.any_right_matched_set.update(self.right_harmonised_matched_set)
        #ic(len(self.any_right_matched_set))

        self.right_not_matched_set = set(self.right_term_list)
        #ic(len(self.right_not_matched_set))
        self.right_not_matched_set.difference_update(self.any_right_matched_set)
        #ic(len(self.right_not_matched_set))
        self.right_confident_matched_set = set(self.right_exact_matched_set)
        self.right_confident_matched_set.union(self.right_harmonised_matched_set)


    def get_right_not_matched_list(self):
        return sorted(self.right_not_matched_set)

    def get_any_left_match_list(self):
        return sorted(self.any_right_matched_set)


    def get_clean_hash(self):
        clean_hash = {}
        pairwise_matches = {}
        for left in self.left_term_list:
            clean_hash[left] = clean_term(left)
        for right in self.right_term_list:
            clean_hash[right] = clean_term(right)
        self.clean_hash = clean_hash
        return self.clean_hash

    def put_right_obj(self, right_obj):
        self.right_obj = right_obj

    def put_left_obj(self, left_obj):
        self.left_obj = left_obj


    def get_right_no_match_freq_dict(self):
        """
        yes suboptimal as need to have a right obj!
        :param :
        :return:
        """
        right_obj = self.right_obj
        right_all_match_freq = right_obj.get_terms_with_freq()
        right_no_match_freq = {"by_freq": {}, "by_term": {}}
        for right in self.right_not_matched_set:
            right_no_match_freq["by_term"][right] = right_all_match_freq[right]
            freq = right_all_match_freq[right]
            if freq not in right_no_match_freq["by_freq"]:
                right_no_match_freq["by_freq"][freq] = []
            right_no_match_freq["by_freq"][freq].append(right)
        return(right_no_match_freq)

    def print_stats(self):
        stats = ""
        stats += "left term count         : " + str(len(self.left_term_list)) + "\n"
        stats += "exact matches total     : " + str(len(self.right_exact_matched_set)) + "\n"
        stats += "harmonised matches total: " + str(len(self.right_harmonised_matched_set)) + "\n"
        stats += "confident match total   : " + str(len(self.left_confident_matched_set)) + "\n"
        stats += "fuzzy matches count     : " + str(len(self.left_fuzzy_matched_set)) + "\n"
        stats += "\n"
        stats += "left not matches count  : " + str(len(self.left_not_matched_set)) + "\n"
        stats += "right term count        : " + str(len(self.right_term_list)) + "\n"
        stats += "right confidence count  : " + str(len(self.right_confident_matched_set)) + "\n"
        stats += "right not matches count : " + str(len(self.right_not_matched_set)) + "\n"
        return stats


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
    # ic(df.head(10))
    # print(df.to_markdown(index=False))

    return df


