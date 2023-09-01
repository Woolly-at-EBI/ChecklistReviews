class COMPARISONS:
    """ not yet a proper or even rich object...
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
        self.reorg_df['short_ena'] = df['ena'].str.extract(r"([A-Za-z]+ [A-Za-z]+ [A-Za-z]+)")
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
            # end of process_max_intersection_len

    def ingest(self):
        # ic("start of ingest================================================"+ "\n")
        # ic()
        reorg_dict = {self.left_source(): [], self.right_source(): [], "left_source": [], "right_source": [],
                      "pair": []}
        sub_dict_elements = ['length_clean_intersection', 'pc_left_of_right']
        for element in sub_dict_elements:
            reorg_dict[element] = []
        comparison_source = 'ena::mixs_v6'
        comparisonStats = self.comparisonStats
        # ic(comparisonStats)
        count = 0

        if comparison_source not in comparisonStats:
            ic(f"ERROR {comparison_source} not in comparisonStats")
            ic(comparisonStats)
            sys.exit()
        # else:
        #    ic(f"{comparison_source} is in comparisonStats")

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
        ic(df.head(5))
        # ic(df['short_ena'].unique())
        # ic(df['short_mixs_v6'].unique())
        self.process_max_intersection_len()
        # ic("-------end of ingest------")
        # sys.exit()


