import math
import pandas as pd
from datetime import datetime, timedelta

def data_cleaning(df):
    df.drop(columns=['userid','server','title','datetakenunknown','views','url_l'], inplace=True)

    # Condition 1 & 2: datetaken and dateupload are NOT identical & datetaken time is NOT in the future
    for i in df.index:
        if df.datetaken[i] == df.dateupload[i] or datetime.strptime(df.datetaken[i], format) > datetime.now():
            df = df.drop(index=i)
    df.drop(columns=['dateupload'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Creat table for clustering
    analysis_cluster = pd.DataFrame(columns=['owner', 'interval', 'weekend', 'total', 'var_loc'])
    # Creat user list
    owner_list = df['owner']
    owner_list.drop_duplicates(keep='first', inplace=True)
    owner_list.reset_index(drop=True, inplace=True)

    # Generate analysis table
    for owner_list_iter in owner_list:
        item = df[df['owner'].str.contains(owner_list_iter)]

        # Calculate the variance of the longitude and latitude for each user
        var_lati = (item['latitude']).var()
        var_longi = (item['longitude']).var()
        if math.isnan(var_lati):
            var_loc = 0
        else:
            var_loc = math.sqrt((var_lati + var_longi)/2)
        # idx = owner_list[owner_list.str.contains(owner_list_iter)].index

        # Count the number of phototaken on weekend
        datetaken_list = item['datetaken'].to_list()
        datetaken_list = sorted([datetime.strptime(i,format) for i in datetaken_list], reverse=False)
        # Check the occurrences of weekend
        total = len(datetaken_list)
        weekend = 0
        for datetaken_list_iter in datetaken_list:
            if datetime.isoweekday(datetaken_list_iter) in [5, 6, 7]:
                weekend += 1

        # Find maximal time interval in each year
        i = 1
        while i < len(datetaken_list)-1:
            if datetaken_list[i].year == datetaken_list[i-1].year:
                if datetaken_list[i].year != datetaken_list[i+1].year:
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
                                + (datetaken_list[i] - datetaken_list[i - 1]).seconds / 3600
                        interval.append(str(datetaken_list[i].year) + ":" + str(delta))
                        i += 2
                    else:
                        interval.append(str(datetaken_list[i].year) + ":" + str(timedelta(seconds=0).seconds))
                        i += 1
        else:
            interval.append(str(datetaken_list[0].year) + ":" + str(timedelta(seconds=0).seconds))
        # analysis_cluster.loc[index, 'interval'] = interval
        analysis_cluster = analysis_cluster.append({'owner': owner_list_iter,
                                                    'interval': interval,
                                                    'weekend': weekend,
                                                    'total': total,
                                                    'var_loc': var_loc},
                                                   ignore_index=True)

#    # Calculate time maximal interval between two phototaken in one year
#    for index, row in analysis_cluster.iterrows():
#        interval = []
#        if len(row['interval']) > 1:
#            i = 1
#            while i < len(row['interval']):
#                if row['interval'][i].year == row['interval'][i-1].year:
#                    delta = (row['interval'][i]-row['interval'][i-1]).days \
#                            + (row['interval'][i]-row['interval'][i-1]).seconds/3600
#                    interval.append(str(row['interval'][i].year)+ ":" + str(delta))
#                    i += 2
#                else:
#                    interval.append(str(row['interval'][i].year)+ ":" + str(timedelta(seconds=0).seconds))
#                    i += 1
#        else:
#            interval.append(str(row['interval'][0].year)+ ":" + str(timedelta(seconds=0).seconds))
#        analysis_cluster.loc[index, 'interval'] = interval
#    # Calculate the variance of the longitude and latitude for each user
#    for owner_iter in owner_list:
#        item = df[df['owner'].str.contains(owner_iter)]
#        var_lati = (item['latitude']).var()
#        var_longi = (item['longitude']).var()
#        if math.isnan(var_lati):
#            var_loc = 0
#        else:
#            var_loc = math.sqrt((var_lati + var_longi)/2)
#        idx = owner_list[owner_list.str.contains(owner_iter)].index
#        analysis_cluster.loc[idx, 'var_loc'] = var_loc

    # Condition 3: maximal time interval within a year is NOT more than 30 days
    analysis_d = analysis_cluster.copy(deep=True)
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

    return df

if __name__ == "__main__":
    # load Flickr data from CSV to DataFrame
    filename = './flickr_14.10.2020.csv'
    format = '%Y-%m-%d %H:%M:%S'
    df = pd.read_csv(filename, sep=';', encoding='latin-1')

    df = data_cleaning(df)
