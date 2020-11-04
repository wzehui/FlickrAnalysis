import math
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import numpy as np

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
format = '%Y-%m-%d %H:%M:%S'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

# Condition 1 & 2: datetaken and dateupload are NOT identical & datetaken time is NOT in the future
for i in df.index:
    if df.datetaken[i] == df.dateupload[i] or datetime.strptime(df.datetaken[i],format) > datetime.now():
        df = df.drop(index=i)
df.reset_index(drop=True,inplace=True)

# Creat table for analysis
analysis = pd.DataFrame(columns=['owner','interval','weekend','total','var_loc'])
# Creat user list
owner = df['owner']
owner.drop_duplicates(keep='first', inplace=True)
owner.reset_index(drop=True, inplace=True)
# Count the number of phototaken on weekend
for owner_id in owner:
    item = df[df['owner'].str.contains(owner_id)]
    item = item['datetaken'].to_list()
    item = sorted([datetime.strptime(i,format) for i in item], reverse=False)
    # check the occurrences of weekend
    total = len(item)
    weekend = 0
    for item_s in item:
        if datetime.isoweekday(item_s) in [5, 6, 7]:
            weekend += 1
    # Find maximal time interval in each year
    i = 1
    while i < len(item)-1:
        if item[i].year == item[i-1].year:
            if item[i].year != item[i+1].year:
                i += 1
            else:
                item.pop(i)
        else:
            i += 1
    analysis = analysis.append({'owner': owner_id,
                                'interval': item,
                                'weekend': weekend,
                                'total': total,},
                               ignore_index=True)
for index, row in analysis.iterrows():
    interval = []
    if len(row['interval']) > 1:
        i = 1
        while i < len(row['interval']):
            if row['interval'][i].year == row['interval'][i-1].year:
                delta = (row['interval'][i]-row['interval'][i-1]).days \
                        + (row['interval'][i]-row['interval'][i-1]).seconds/3600
                interval.append(str(row['interval'][i].year)+ ":" + str(delta))
                i += 2
            else:
                interval.append(str(row['interval'][i].year)+ ":" + str(timedelta(seconds=0).seconds))
                i += 1
    else:
        interval.append(str(row['interval'][0].year)+ ":" + str(timedelta(seconds=0).seconds))
    analysis.loc[index,'interval'] = interval
# Calculate the variance of the longitude and latitude for each user
for owner_id in owner:
    item = df[df['owner'].str.contains(owner_id)]
    var_lati = (item['latitude']).var()
    var_longi = (item['longitude']).var()
    if math.isnan(var_lati):
        var_loc = 0
    else:
        var_loc = math.sqrt((var_lati + var_longi)/2)
    idx = owner[owner.str.contains(owner_id)].index
    analysis.loc[idx, 'var_loc'] = var_loc

# Condition 3: maximal time interval within a year is NOT more than 30 days
analysis_d = analysis.copy(deep=True)
for index, item in analysis_d.iterrows():
    item_d = []
    weekend_percent = item.weekend / item.total
    if weekend_percent < 0.9 and item.var_loc < 0.1:
        for item_s in item.interval:
            [year, duration] = item_s.split(':')
            if float(duration) > 30:
                item_d.append(year)
    analysis_d.loc[index, 'interval'] = item_d
analysis_d.drop(labels=['weekend','total','var_loc'], axis=1, inplace=True)

for item in analysis_d.itertuples():
    if len(item.interval) != 0:
        owner_d = df[df['owner'].str.contains(item.owner)]
        for item_s in item.interval:
            owner_dd = owner_d[owner_d['datetaken'].str.contains(item_s)]
            df = df.append(owner_dd)
            df = df.drop_duplicates(subset=df.columns.values, keep=False)
df.reset_index(drop=True, inplace=True)

# Clustering
df_sub = df[['latitude', 'longitude']]
# Standarize features
scaler = StandardScaler()
df_std = scaler.fit_transform(df_sub)

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
for item in cluster_list:
    owner_cluster = df[df['cluster']==item].owner
    owner_cluster = owner_cluster.drop_duplicates(keep="first", inplace=False)
    if (owner_cluster.size / owner.size) < 0.02:
        df = df.append(df[df['cluster']==item])
        df = df.drop_duplicates(subset=df.columns.values, keep=False)
df.reset_index(drop=True, inplace=True)

# Visualise cluster membership
fig = plt.figure(figsize=(10, 10));
ax = fig.add_subplot(111)
scatter = ax.scatter(df.latitude, df.longitude, c=df.cluster, s=50)
ax.set_title('DBSCAN Clustering')
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
plt.colorbar(scatter)
plt.show()

df.to_excel('dbscan_0.02.xls')


# # Grid Search
# import numpy as np
# from sklearn.model_selection import GridSearchCV
# eps = np.arange(0.01, 0.51, 0.01)
# min_Pts = np.arange(5, 301, 5)
#
# score_max = 0
# x = []
# y = []
# params = []
#
# for eps_item in eps:
#     for min_Pts_item in min_Pts:
#         clt = DBSCAN(eps=eps_item, min_samples=min_Pts_item)
#         model = clt.fit(df_std)
#         clusters = pd.DataFrame(model.fit_predict(df_std))
#         df['cluster'] = clusters
#         df_d = df.copy(deep=True)
#         df_d.drop(df_d[df_d['cluster'] == -1].index, inplace=True)
#         cluster_list = df_d.cluster.unique()
#         for item in cluster_list:
#             owner_cluster = df[df['cluster']==item].owner
#             owner_cluster = owner_cluster.drop_duplicates(keep="first", inplace=False)
#             if (owner_cluster.size / owner.size) < 0.01:
#                 df_d = df_d.append(df_d[df_d['cluster']==item])
#                 df_d = df_d.drop_duplicates(subset=df_d.columns.values, keep=False)
#         df_d.reset_index(drop=True, inplace=True)
#         score = df_d.cluster.unique().size / cluster_list.size
#         x.append(cluster_list.size)
#         y.append(df_d.cluster.unique().size)
#         params.append((eps_item,min_Pts_item))
#
#         if score > score_max:
#             score_max = score
#             param = {'eps': eps_item, 'min_Pts': min_Pts_item}
#             print(df_d.cluster.unique().size)
#             print(cluster_list.size)
#             print(param)
#for i in range(len(x)):
#    a = y[i]/x[i]
#    if a != 1 and a > 0.54 and x[i] >50 and x[i]<100:
#        print(a)
#        print(x[i])
#        print(params[i])
#        print('\n')
##
from mlxtend.frequent_patterns import fpgrowth, association_rules
df_association = df[['owner', 'cluster']].copy(deep=True)
df_association['frequency'] = 1
table = pd.pivot_table(df_association, values='frequency',index=['owner'],columns=['cluster'],aggfunc=np.sum,fill_value=0)
frequent_itemsets = fpgrowth(table.astype('bool'), min_support=0.01, use_colnames=True)
print(frequent_itemsets)
res = association_rules(frequent_itemsets,metric='confidence',min_threshold=0.8)
print(res)
