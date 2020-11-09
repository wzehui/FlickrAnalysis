import math
import pandas as pd
from datetime import datetime, timedelta

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
format = '%Y-%m-%d %H:%M:%S'
df = pd.read_csv(filename, sep=';', encoding='latin-1')


df.drop(columns=['server', 'title', 'datetakenunknown', 'views',
                 'url_l'], inplace=True)

# Condition 1 & 2: datetaken and dateupload are NOT identical & datetaken
# time is valid
for i in df.index:
    if df.datetaken[i] == df.dateupload[i] or datetime.strptime(
            df.datetaken[i], format) > datetime.now():
        df = df.drop(index=i)
df.drop(columns=['dateupload'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Creat table for clustering
analysis_cluster = pd.DataFrame(
    columns=['owner', 'interval', 'weekend', 'total', 'var_loc'])
# Creat user list
owner_list = df['owner']
owner_list.drop_duplicates(keep='first', inplace=True)
owner_list.reset_index(drop=True, inplace=True)

# Generate analysis table
for owner_list_iter in owner_list:
    item_iter = df[df['owner'].str.contains(owner_list_iter)]

    # Calculate the variance of the longitude and latitude for each user
    var_lati = (item_iter['latitude']).var()
    var_longi = (item_iter['longitude']).var()
    if math.isnan(var_lati):
        var_loc = 0
    else:
        var_loc = math.sqrt((var_lati + var_longi) / 2)
    # idx = owner_list[owner_list.str.contains(owner_list_iter)].index

    # Count the number of phototaken on weekend
    datetaken_list = item_iter['datetaken'].to_list()
    datetaken_list = sorted(
        [datetime.strptime(i, format) for i in datetaken_list],
        reverse=False)
    # Check the occurrences of weekend
    total = len(datetaken_list)
    weekend = 0
    for datetaken_list_iter in datetaken_list:
        if datetime.isoweekday(datetaken_list_iter) in [5, 6, 7]:
            weekend += 1

    # Find maximal time interval in each year
    i = 1
    while i < len(datetaken_list) - 1:
        if datetaken_list[i].year == datetaken_list[i - 1].year:
            if datetaken_list[i].year != datetaken_list[i + 1].year:
                i += 1
            else:
                datetaken_list.pop(i)
        else:
            i += 1
    # analysis_cluster.loc[idx, 'var_loc'] = var_loc

    # Calculate time maximal interval between two phototaken in one year
    interval = []
    if len(datetaken_list) > 1:
        i = 1
        while i < len(datetaken_list):
            if datetaken_list[i].year == datetaken_list[i - 1].year:
                delta = (datetaken_list[i] - datetaken_list[i - 1]).days \
                        + (datetaken_list[i] - datetaken_list[
                    i - 1]).seconds / 3600
                interval.append(
                    str(datetaken_list[i].year) + ":" + str(delta))
                i += 2
            else:
                interval.append(str(datetaken_list[i].year) + ":" + str(
                    timedelta(seconds=0).seconds))
                i += 1
    else:
        interval.append(str(datetaken_list[0].year) + ":" + str(
            timedelta(seconds=0).seconds))
    # analysis_cluster.loc[index, 'interval'] = interval
    analysis_cluster = analysis_cluster.append({'owner': owner_list_iter,
                                                'interval': interval,
                                                'weekend': weekend,
                                                'total': total,
                                                'var_loc': var_loc},
                                               ignore_index=True)

#for index, item_iter in analysis_cluster.iterrows():
#    year_delete = []
#    weekend_percent = item_iter.weekend / item_iter.total
#    if weekend_percent < 0.9 and item_iter.var_loc < 0.1:
#        for item_str in item_iter.interval:
#            [year, duration] = item_str.split(':')
#            if float(duration) > 30:
#                year_delete.append(year)
#
#    if len(year_delete) != 0:
#        item = df[df['owner'].str.contains(item_iter.owner)]
#        for year_delete_iter in year_delete:
#            item_delete = item[item['datetaken'].str.contains(
#                year_delete_iter)]
#            df = df.append(item_delete)
#            df.drop_duplicates(subset=df.columns.values, keep=False,
#                               inplace=True)
for i in range(1,max(df.index)):
    find = df.iloc[0:i,:]
    item = df.iloc[0:1,:]
    df_a = find.append(item)
    df_a.drop_duplicates(keep=False,inplace=True)
    if df_a.shape[0] != find.shape[0]-1:
        print(find)
        print(i)


#find = df.iloc[0:43, :]
#item = df.iloc[0:1,:]
#df_a = find.append(item)
#df_a.drop_duplicates(keep=False,inplace=True)
#print(1)