"""
+---------------------------------------------------------------+
| Main function/script                                          |
+---------------------------------------------------------------+
------------------------------------------------------------------
Copyright: 2020 Wang,Zehui (wzehui@hotmail.com)
@author: Wang,Zehui
"""
import pandas as pd
from datetime import datetime, timedelta
from Preprocess import data_cleaning
from Clustering import cluster

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

df = data_cleaning(df)
df = cluster(df)
