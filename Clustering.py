from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import pandas as pd

def cluster(df):
    # Clustering
    df_sub = df[['latitude', 'longitude']]
    # Standarize features
    scaler = StandardScaler()
    df_std = scaler.fit_transform(df[['latitude', 'longitude']])

    # Conduct DBSCAN Clustering
    clt = DBSCAN(eps=0.06, min_samples=40)

    # Train model
    model = clt.fit(df_std)

    # Predict clusters
    clusters = pd.DataFrame(model.fit_predict(df_std))
    df['cluster'] = clusters
    df.drop(df[df['cluster'] == -1].index, inplace=True)

    # Condition 4: popular clusters, whose owner is larger than 2%
    cluster_list = df.cluster.unique()
    owner_sum = df.owner.unique().size
    for cluster_list_iter in cluster_list:
        owner_cluster = df[df['cluster']==cluster_list_iter].owner.unique()
        # owner_cluster = owner_cluster.drop_duplicates(keep="first", inplace=True)
        if (owner_cluster.size / owner_sum) < 0.02:
            df = df.append(df[df['cluster']==cluster_list_iter])
            df.drop_duplicates(keep=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df