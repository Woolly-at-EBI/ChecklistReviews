from icecream import ic
import pandas as pd
import plotly.express as px
import sys
# from analyse_mixs import names2pair_string

class COMPARISONS:
    """
      Allows comparison of source checklist/packages.
      not yet a proper or even rich object...
        if more development, need to improve this.
        (still it served a purpose and broke up an excessively long routine)
    """

    def __init__(self, comparisonStats, comparison_source):
        ic()
        ic(comparison_source)
        self.source_list = []
        self.source_list = comparison_source.split('::')
        self.comparisonStats = comparisonStats
        ic("---------------------------")
        self.ingest()

    def left_source(self):
        return self.source_list[0]

    def right_source(self):
        return self.source_list[1]

    def put_reorg_df(self, df):
        self.reorg_df = df

        if self.left_source() == 'ena_cl':
            self.reorg_df['short_ena'] = df['ena_cl'].str.extract(r"([A-Za-z]+ [A-Za-z]+ [A-Za-z]+)")
        if self.right_source() == 'mixs_v6':
            self.reorg_df['short_mixs_v6'] = df['mixs_v6'].str.extract(r"([A-Z][a-z]+)")

    def process_max_intersection_len(self):
        """

        :return:
        """
        # for each ENA checklist, get the maximum length of intersections
        # sources = source_list  # ['ena', 'mixs_v6']
        for source in self.source_list:
            ic(source)
            if source == 'ena':
                target_cols = [source, 'length_clean_intersection']
            else:
                target_cols = [source, 'length_clean_intersection', 'short_mixs_v6']
            new_df = self.reorg_df[target_cols].drop_duplicates()
            ic(new_df.head().to_string(index = False))

            # for each ENA or Mixs checklist, get the checklists with >= 20% overlap with at least one GSC MIx
            new_df = self.reorg_df
            target_cols = [source]
            if source == 'short_mixs_v6':
                target_cols.append('short_mixs_v6')
            alltarget_cols = target_cols
            alltarget_cols.append('pc_left_of_right')

            max_df = new_df[alltarget_cols].groupby(target_cols).max().reset_index()
            self.max_df = max_df
            # print(max_df.to_string(index = False))

            if source == 'mixs_v6':
                mixs6_matches_plots(self.reorg_df, new_df)
            print(f"each {source} checklist with >= 20% overlap with at least one GSC MIx")
            tmp_df = max_df.query('pc_left_of_right >= 0.2')
            # print(tmp_df.to_string(index = False))
            # print(f"{tmp_df[source].unique()} \ntotal={len(tmp_df[source].unique())}")
            print("each {source} checklist with a maximum < 20% overlap with any GSC MIx")
            tmp_df = max_df.query('pc_left_of_right < 0.2')
            # print(tmp_df.to_string(index = False))
            # print(f"{tmp_df[source].unique()} \ntotal={len(tmp_df[source].unique())}")
            #self.max_intersection_len
            # end of process_max_intersection_len

    def ingest(self):
        ic("start of ingest================================================"+ "\n")
        # ic()
        reorg_dict = {self.left_source(): [], self.right_source(): [], "left_source": [], "right_source": [],
                      "pair": []}
        sub_dict_elements = ['length_clean_intersection', 'pc_left_of_right']
        for element in sub_dict_elements:
            reorg_dict[element] = []
        comparison_source = names2pair_string(self.left_source(), self.right_source())
        ic(comparison_source)
        comparisonStats = self.comparisonStats
        # ic(comparisonStats)
        count = 0

        if comparison_source not in comparisonStats:
            ic(f"ERROR {comparison_source} not in comparisonStats")
            # ic(comparisonStats)
            sys.exit()
        for pair in comparisonStats[comparison_source]['by_package']:
            # ic(pair)
            pair_list = pair.split('::')
            # ic(pair_list)
            # ic(comparisonStats[comparison_source]['by_package'][pair])
            sub_dict = comparisonStats[comparison_source]['by_package'][pair]
            # ic(sub_dict)
            reorg_dict[self.left_source()].append(pair_list[0])
            reorg_dict[self.right_source()].append(pair_list[1])
            reorg_dict['left_source'].append(self.left_source())
            reorg_dict['right_source'].append(self.right_source())
            reorg_dict['pair'].append(pair)
            for element in sub_dict_elements:
                # ic(sub_dict[element])
                reorg_dict[element].append(sub_dict[element])
            if count > 3:
                break
            else:
                count += 1
        # ic(reorg_dict)
        self.put_reorg_df(pd.DataFrame.from_dict(reorg_dict))
        df = self.reorg_df
        ic()
        ic(df.head(5))
        # ic(df['short_ena'].unique())
        # ic(df['short_mixs_v6'].unique())
        self.process_max_intersection_len()
        # ic("-------end of ingest------")

def mixs6_matches_plots(df, new_df):
    """
    :param df:
    :param new_df:
    :return:
    """

    # print(max_df.head(20).to_string(index = False))
    # print("max")
    max_df = new_df[['short_mixs_v6', 'pc_left_of_right']].groupby('short_mixs_v6').max().reset_index().sort_values(
        by = 'pc_left_of_right')
    max_df.rename(columns = {"pc_left_of_right": "maxPC_intersection"}, inplace = True)
    # print(max_df.head(20).to_string(index = False))
    # print("average(mean)")
    mean_pc_df = new_df[['short_mixs_v6', 'pc_left_of_right']].groupby(
        'short_mixs_v6').mean().reset_index().sort_values(by = 'pc_left_of_right')  # average().reset_index()
    mean_pc_df.rename(columns = {"pc_left_of_right": "MeanPC_intersection"}, inplace = True)
    # print(mean_pc_df.head(20).to_string(index = False))
    mean_ints_df = df[['short_mixs_v6', 'length_clean_intersection']].groupby(
        'short_mixs_v6').mean().reset_index().sort_values(by = 'length_clean_intersection')  # average().reset_index()
    mean_ints_df.rename(columns = {"length_clean_intersection": "MeanLen_intersection"}, inplace = True)
    # print(mean_ints_df.head(20).to_string(index = False))
    # print("Count of rows")
    tmp_df = df[['mixs_v6', 'short_mixs_v6']].drop_duplicates()
    package_count_df = tmp_df.groupby('short_mixs_v6').count().reset_index()
    package_count_df.rename(columns = {"mixs_v6": "package_count"}, inplace = True)
    # print(package_count_df.head(20).to_string(index = False))
    stats_df = max_df.merge(mean_pc_df, on = 'short_mixs_v6').merge(package_count_df, on = 'short_mixs_v6')

    title = "Statistics of the MIXS v6 packages with matches from the ENA checklists"
    print(title)
    title += "<BR><sub>size=packages count for each collection</sub>"

    stats_df["maxPC_intersection"] = stats_df["maxPC_intersection"] * 100
    stats_df = stats_df.astype({'maxPC_intersection': 'int'})

    stats_df["MeanPC_intersection"] = stats_df["MeanPC_intersection"] * 100
    print(stats_df.head(20).to_string(index = False))
    fig = px.scatter(stats_df, title = title, x = 'maxPC_intersection', y = 'MeanPC_intersection',
                     size = 'package_count',
                     color = 'package_count', text = 'short_mixs_v6',
                     color_continuous_scale = px.colors.sequential.Viridis)
    fig.update_traces(textposition = 'top center')
    # fig.show()
    fig.write_image("/Users/woollard/projects/ChecklistReviews/docs/ENAvsMIXSv6_ScatterPlot.jpg")

def names2pair_string(left_name, right_name):
    return '::'.join([left_name, right_name])

def pair_string2names(pair_string):
    """
    :param pair_string:
    :return: left_string, right_string
    """
    return pair_string.split(":")

