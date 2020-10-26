import pandas as pd
import math
from datetime import datetime

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

# Condition 1: datetaken and dateupload are NOT identical
for i in df.index:
    if df.datetaken[i] == df.dateupload[i]:
        df = df.drop(index=i)
df.reset_index(drop=True,inplace=True)

# Condition 2: maximal time interval within a year is NOT more than 30 days
format = '%Y-%m-%d %H:%M:%S'
time_interval = pd.DataFrame(columns=['owner','date_min','date_max'])
# for i in df.index:
#     if df.owner[i] not in time_interval['owner'].values:
#         time_interval = time_interval.append({'owner':df.owner[i],
#                                               'date_min':df.datetaken[i],
#                                               'date_max':df.datetaken[i]},
#                                              ignore_index=True)
#     else:
#         item = time_interval[time_interval['owner'].str.contains(df.owner[i])]
#         for idx in item.index:
#             print(df.datetaken[i])
#             if datetime.strptime(df.datetaken[i], format).year != datetime.strptime(item.loc[idx].iat[1], format).year:
#                 time_interval = time_interval.append({'owner': df.owner[i],
#                                                       'date_min': df.datetaken[i],
#                                                       'date_max': df.datetaken[i]},
#                                                      ignore_index=True)
#                 item = time_interval[time_interval['owner'].str.contains(df.owner[i])]
#             else:
#                 if datetime.strptime(df.datetaken[i],format) < datetime.strptime(item.loc[idx].iat[1],format):
#                     time_interval.loc[time_interval['owner'].str.contains(df.owner[i]), 'date_min'] = df.datetaken[i]
#                 elif datetime.strptime(df.datetaken[i],format) > datetime.strptime(item.loc[idx].iat[2],format):
#                     time_interval.loc[time_interval['owner'].str.contains(df.owner[i]), 'date_max'] = df.datetaken[i]

owner = df['owner']
owner_dict = {'owner': owner}
owner = pd.DataFrame(owner_dict)
owner.drop_duplicates('owner', keep="first", inplace=True, ignore_index=True)

for owner_id in owner.itertuples():
    item = df[df['owner'].str.contains(owner_id.owner)]
    var_lati = (item.latitude*1e5).var()
    var_long = (item.longitude*1e5).var()
    if math.isnan(var_lati):
        var_loc = 0
    else:
        var_loc = math.sqrt((var_lati + var_long)/(2*1e5))
    idx = owner[owner['owner'].str.contains(owner_id.owner)].index
    owner.loc[idx,'var_loc'] = var_loc

# 30 days and holiday condition

# location condition
owner_d = owner.copy(deep=True)
for item in owner.itertuples():
    if item.var_loc > 20:
        owner_d.drop(index=item.Index,inplace=True)

