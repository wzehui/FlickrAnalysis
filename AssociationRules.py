from mlxtend.frequent_patterns import fpgrowth, association_rules
import pandas as pd
import numpy as np

def find_association(df, analysis_cluster):
    # remove the users, whose photos are only in one cluster and whose
    # interval of photos are more than 30 days
    owner_list = df.owner.unique()
    for owner_list_iter in owner_list:
        item_delete = df[df['owner'] == owner_list_iter]
        if item_delete.cluster.unique().size == 1:
            pass
        else:
            interval_list = analysis_cluster[analysis_cluster['owner'] ==
                           owner_list_iter].interval.values[0]
            for interval_list_iter in interval_list:
                [year, duration] = interval_list_iter.split(':')
                if float(duration) < 30:
                    item_retain = item_delete[item_delete['datetaken'].str.contains(
                        year)]
                    item_delete = item_delete.append(item_retain)
                    item_delete.drop_duplicates(keep=False, inplace=True)

        df = df.append(item_delete)
        df.drop_duplicates(keep=False, inplace=True, ignore_index=True)

    # generate pivot table for association analysis
    df['frequency'] = 1
    pivot_table = pd.pivot_table(df, values='frequency', index=['owner'],
                           columns=['cluster'], aggfunc=np.sum, fill_value=0)
    frequent_itemsets = fpgrowth(pivot_table.astype('bool'), min_support=0.03,
                                 use_colnames=True)
    # print(frequent_itemsets)
    rule = association_rules(frequent_itemsets, metric='confidence',
                            min_threshold=0.7)
    return rule

if __name__ == '__main__':
    from Preprocess import data_cleaning
    from Clustering import dbscan
    from Visualization import map
    import pandas as pd

    # load Flickr data from CSV to DataFrame
    filename = './flickr_14.10.2020.csv'
    cluster_result_path = 'dbscan_0.06_40.xls'
    df = pd.read_csv(filename, sep=';', encoding='latin-1')

    df, analysis_cluster = data_cleaning(df)
    df = dbscan(df)
    find_association(df, analysis_cluster)
