import plotly.express as px
from Preprocess import data_cleaning
from Clustering import dbscan
import pandas as pd
import plotly.graph_objects as go
from AssociationRules import find_association

# load Flickr data from CSV to DataFrame
filename = './flickr_14.10.2020.csv'
cluster_result_path = 'dbscan_0.06_40.xls'
df = pd.read_csv(filename, sep=';', encoding='latin-1')

df, analysis_cluster = data_cleaning(df)
df = dbscan(df)
rule = find_association(df, analysis_cluster)

# Visualisation

mapbox_access_token = \
    'pk.eyJ1Ijoiem9pcGh5IiwiYSI6ImNraGVwdm1qbjA0aTEzMW0yeGhmdTh3aGgifQ.uYmOx-yQ5hJdBQgRm7SO3w'
px.set_mapbox_access_token(mapbox_access_token)

cluster_list = df.cluster.unique()
amount_list = []
lat_mean_list = []
lon_mean_list = []
for cluster_list_iter in cluster_list:
    item = df[df['cluster'] == cluster_list_iter]
    amount_list.append(item.shape[0])
    lat_mean_list.append(item.latitude.mean())
    lon_mean_list.append(item.longitude.mean())

cluster_mean_dict = {'cluster': cluster_list,
                     'amount': amount_list,
                     'lat_mean': lat_mean_list,
                     'lon_mean': lon_mean_list
                     }
cluster_mean = pd.DataFrame(cluster_mean_dict)
cluster_mean['cluster'] = cluster_mean['cluster'].astype(str)

fig = px.scatter_mapbox(cluster_mean, title='',
                        lat="lat_mean", lon="lon_mean",
                        color="cluster",
                        color_discrete_sequence=px.colors.qualitative.Prism,
                        size="amount", size_max=40, hover_name="cluster",
                        hover_data={'cluster':False,
                                    'lat_mean':False,
                                    'lon_mean':False},
                        zoom=8.85, center={'lat': 47.45, 'lon': 9.43})
fig.update_traces(showlegend=False)

fig.add_trace(go.Scattermapbox(lat= df.latitude, lon= df.longitude,
                               mode='markers', hoverinfo='skip',
                               marker=go.scattermapbox.Marker(size=3,
                                                              opacity= 0.5,
                                                              color='gray'),
                               showlegend=False))

for index, rule_iter in rule.iterrows():
    for ante_item in rule_iter.antecedents:
        for conse_item in rule_iter.consequents:
            ante_lat = cluster_mean[cluster_mean[
                                        'cluster']==str(
                ante_item)].lat_mean.values
            ante_lon = cluster_mean[cluster_mean[
                                        'cluster']==str(
                ante_item)].lon_mean.values
            conse_lat = cluster_mean[cluster_mean[
                                        'cluster']==str(
                conse_item)].lat_mean.values
            conse_lon = cluster_mean[cluster_mean[
                                        'cluster']==str(
                conse_item)].lon_mean.values
            fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lat = [ante_lat[0], conse_lat[0]],
                lon = [ante_lon[0], conse_lon[0]],
                hoverinfo = 'skip',
                name = str(ante_item) + ' --> ' + str(conse_item),
                line = dict(width = 3 * (rule_iter.confidence)**4)))
fig.update_layout(legend_title_text = 'Association Rules')
fig.show()
