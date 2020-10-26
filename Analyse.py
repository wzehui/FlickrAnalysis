import math
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt

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
    var_lati = (item['latitude']*1e5).var()
    var_longi = (item['longitude']*1e5).var()
    if math.isnan(var_lati):
        var_loc = 0
    else:
        var_loc = math.sqrt((var_lati + var_longi)/(2*1e5))
    idx = owner[owner.str.contains(owner_id)].index
    analysis.loc[idx, 'var_loc'] = var_loc

# Condition 3: maximal time interval within a year is NOT more than 30 days
analysis_d = analysis.copy(deep=True)
for index, item in analysis_d.iterrows():
    item_d = []
    weekend_percent = item.weekend / item.total
    if weekend_percent < 0.8 and item.var_loc < 20:
        for item_s in item.interval:
            [year, duration] = item_s.split(':')
            if float(duration) > 30:
                item_d.append(year)
    analysis_d.loc[index, 'interval'] = item_d
analysis_d.drop(labels=['weekend','total','var_loc'], axis=1, inplace=True)

for item in analysis_d.itertuples():
    if len(item.interval) != 0:
        owner_d = df[df.str.contains(item.owner)]
        for item_s in item.interval:
            owner_dd = owner_d[owner_d.str.contains(item_s)]
            

#


