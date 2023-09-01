
def clean_term(term):
    """
    replicates what is in clean_list but for a single term...
    :param term:
    :return:
    """
    # ic(term)
    clean = term.lower().replace(' ', '_').replace('-', '_').replace('/', '_').removesuffix("_")
    return clean

def clean_list(my_list):
    """
        function to do some simple cleaning on textual lists.
        e.g. make lower case and use underscore as the main delimiter.
        :param my_list:
        :return: clean_list
    """
    term_list_clean = list(map(str.lower, my_list))
    term_list_clean = [s.replace(' ', '_') for s in term_list_clean]
    term_list_clean = [s.replace('-', '_') for s in term_list_clean]
    term_list_clean = [s.replace('/', '_') for s in term_list_clean]
    term_list_clean = [s.removesuffix("_") for s in term_list_clean]
    return term_list_clean


def generate_clean_dict(my_list):
    """
    re-uses the clean_list to keep it consistent
    :param my_list:
    :return: clean_dict, raw_dict
    a hash of clean term as the index, and original term as the value and vice versa
    """
    my_clean_list = clean_list(my_list)
    clean_dict = {}
    raw_dict = {}
    pos = 0
    for clean_term in my_clean_list:
        clean_dict[clean_term] = my_list[pos]
        raw_dict[my_list[pos]] = clean_term
        pos += 1
    # print(clean_dict)
    # print(raw_dict)
    return clean_dict, raw_dict

def cleanList2set(term_list):
    clean_term_list = clean_list(term_list)
    return (set(clean_term_list))

