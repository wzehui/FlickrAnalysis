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

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
format = '%Y-%m-%d %H:%M:%S'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

df = data_cleaning(df)

