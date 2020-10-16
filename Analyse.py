import pandas as pd
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
#