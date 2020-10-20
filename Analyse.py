import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

# Condition 1: datetaken and dateupload are NOT identical
for i in df.index:
    if df.datetaken[i] == df.dateupload[i]:
        df = df.drop(index=i)
df.reset_index(drop=True,inplace=True)

# Condition 2: maximal time interval within a year is NOT more than 30 days
time_interval = pd.DataFrame(columns=['owner','interval'])
format = '%Y-%m-%d %H:%M:%S'
owner = df['owner']
owner.drop_duplicates(keep='first',inplace=True)
for owner_id in owner:
    item = df[df['owner'].str.contains(owner_id)]
    item = item['datetaken'].to_list()
    item = sorted([datetime.datetime.strptime(i,format) for i in item], reverse=False)
    i = 1
    while i < len(item)-1:
        if item[i].year == item[i-1].year:
            if item[i].year != item[i+1].year:
                i += 1
            else:
                item.pop(i)
        else:
            i += 1
    time_interval = time_interval.append({'owner': owner_id,
                                          'interval': item},
                                         ignore_index=True)
# i =0
# for index, row in time_interval.iterrows():
#     if len(row['interval']) > 1:
#         i += 1
time = []
for index, row in time_interval.iterrows():
    if len(row['interval']) > 1:
        i = 1
        while i < len(row['interval']):
            if row['interval'][i].year == row['interval'][i-1].year:
                delta = (row['interval'][i]-row['interval'][i-1]).days \
                        + (row['interval'][i]-row['interval'][i-1]).seconds/3600
                time.append((delta))
                i += 2
            else:
                # time.append(datetime.timedelta(seconds=0).seconds)
                i += 1

num_bins = 300
plt.hist(time, num_bins)
x_ticks = range(0,105,15)
plt.xticks(x_ticks)
plt.show()