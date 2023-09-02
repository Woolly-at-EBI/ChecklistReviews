from icecream import ic
import pandas as pd
from clean_terms import *
from rapidfuzz import process

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

    def __init__(self, pair_string, left_term_list, right_term_list):
        """

        :param pair_string:
        :param left_term_list:
        :param right_term_list:
        """
        self.process_names(pair_string)

        self.left_term_list = left_term_list
        self.right_term_list = right_term_list
        clean_hash = self.get_clean_hash()

        pairwise_matches = {'left': {"exact": {}, "harmonised": {}, "no_matches": {}}, 'right': {"no_matches": {}}}
        self.pairwise_matches = pairwise_matches
        left_pairwise_matches = pairwise_matches["left"]
        right_pairwise_matches = pairwise_matches["right"]
        self.right_exact_matched_set = set()
        self.left_exact_matched_set = set()
        self.right_harmonised_matched_set = set()
        self.left_harmonised_matched_set = set()
        self.right_not_matched_set = set()
        self.left_not_matched_set = set()

        for left in left_term_list:
            exact_matches_found = False
            harmonised_matches_found = False
            left_pairwise_matches["exact"][left] = {}
            left_pairwise_matches["harmonised"][left] = {}
            first_right_harmonised = ""
            local_right_harmonised_list = []
            right_count = 0
            for right in right_term_list:
                right_match_found = False
                right_count += 1
                if left == right:
                    left_pairwise_matches["exact"][left][right] = ""
                    exact_matches_found = True
                    self.right_exact_matched_set.add(right)
                    self.left_exact_matched_set.add(left)
                    break
                elif clean_hash[left] == clean_hash[right]:
                    # only add them if no exact matches, so have to do it later
                    left_pairwise_matches["harmonised"][left][right] = ""
                    harmonised_matches_found = True
                    local_right_harmonised_list.append(right)
            if exact_matches_found:
                del left_pairwise_matches["harmonised"][left]
            elif harmonised_matches_found:
                del left_pairwise_matches["exact"][left]
                self.left_harmonised_matched_set.add(left)
                self.right_harmonised_matched_set.add(local_right_harmonised_list[0])
            else:
                # if not exact_matches_found and not harmonised_matches_found:
                left_pairwise_matches["no_matches"][left] = ""
                self.left_not_matched_set.add(left)
                del left_pairwise_matches["harmonised"][left]
                del left_pairwise_matches["exact"][left]

        # some terms may still possibly be classified as harmonised as well as exact, so resolving that.
        self.left_harmonised_matched_set.difference_update(self.left_exact_matched_set)
        self.right_harmonised_matched_set.difference_update(self.right_exact_matched_set)

        self.right_not_matched_set = set(right_term_list)
        self.right_not_matched_set.difference_update(self.right_exact_matched_set)
        self.right_not_matched_set.difference_update(self.right_harmonised_matched_set)

        # left_pairwise_matches["exact"][left] = {}
        # left_pairwise_matches["harmonised"][left] = {}
        self.set_harmonised_matches()

    def set_harmonised_matches(self):
        ic()
        left_ordered_list = []
        right_ordered_list = []
        for left in self.left_harmonised_matched_set:
            left_ordered_list.append(left)
            right = ', '.join(list(self.pairwise_matches["left"]["harmonised"][left].keys()))
            right_ordered_list.append(right)
            self.left_harmonised_matching_list = left_ordered_list
            self.right_harmonised_matching_list = right_ordered_list
        # ic(self.left_harmonised_matching_list)
        # ic(self.right_harmonised_matching_list)

        self.right_all_matches_set = self.right_exact_matched_set
        self.right_all_matches_set.union(self.left_harmonised_matched_set)
        return

    def get_clean_hash(self):
        clean_hash = {}
        pairwise_matches = {}
        for left in self.left_term_list:
            clean_hash[left] = clean_term(left)
        for right in self.right_term_list:
            clean_hash[right] = clean_term(right)
        self.clean_hash = clean_hash
        return self.clean_hash

    def get_harmonised_match_df(self):
        df = pd.DataFrame(list(zip(self.left_harmonised_matching_list, self.right_harmonised_matching_list)),
                          columns = [self.left_name, self.right_name]).sort_values(self.left_name)

        return df


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


