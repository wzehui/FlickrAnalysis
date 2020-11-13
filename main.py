"""
+---------------------------------------------------------------+
| Main function/script                                          |
+---------------------------------------------------------------+
------------------------------------------------------------------
Copyright: 2020 Wang,Zehui (wzehui@hotmail.com)
@author: Wang,Zehui
"""
from AssociationRules import find_association
from Preprocess import data_cleaning
from Clustering import dbscan
from Visualization import map
import pandas as pd

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
cluster_result_path = 'dbscan_0.06_40.xls'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

df, analysis_cluster = data_cleaning(df)
df = dbscan(df)

df.to_excel(cluster_result_path)
map(cluster_result_path)

rule = find_association(df, analysis_cluster)
print(rule)


