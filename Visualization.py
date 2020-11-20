import plotly.graph_objects as go
import plotly.express as px

def map(df, rule):
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
                            hover_data={'cluster': False,
                                        'lat_mean': False,
                                        'lon_mean': False},
                            zoom=8.85, center={'lat': 47.45, 'lon': 9.43})
    fig.update_traces(showlegend=False)

    fig.add_trace(go.Scattermapbox(lat=df.latitude, lon=df.longitude,
                                   mode='markers', hoverinfo='skip',
                                   marker=go.scattermapbox.Marker(size=3,
                                                                  opacity=0.5,
                                                                  color='gray'),
                                   showlegend=False))

    for index, rule_iter in rule.iterrows():
        for ante_item in rule_iter.antecedents:
            for conse_item in rule_iter.consequents:
                ante_lat = cluster_mean[cluster_mean[
                                            'cluster'] == str(
                    ante_item)].lat_mean.values
                ante_lon = cluster_mean[cluster_mean[
                                            'cluster'] == str(
                    ante_item)].lon_mean.values
                conse_lat = cluster_mean[cluster_mean[
                                             'cluster'] == str(
                    conse_item)].lat_mean.values
                conse_lon = cluster_mean[cluster_mean[
                                             'cluster'] == str(
                    conse_item)].lon_mean.values
                fig.add_trace(go.Scattermapbox(
                    mode="lines",
                    lat=[ante_lat[0], conse_lat[0]],
                    lon=[ante_lon[0], conse_lon[0]],
                    hoverinfo='skip',
                    name=str(ante_item) + ' --> ' + str(conse_item),
                    line=dict(width=3 * (rule_iter.confidence) ** 4)))
    fig.update_layout(legend_title_text='Association Rules',
                      title='Clustering and Association Analysis',)
    fig.show()

    return fig
#    sheet = pd.read_excel(io=path)
#    colors = [
#        'red',
#        'blue',
#        'gray',
#        'darkred',
#        'lightred',
#        'orange',
#        'beige',
#        'green',
#        'darkgreen',
#        'lightgreen',
#        'darkblue',
#        'lightblue',
#        'purple',
#        'darkpurple',
#        'pink',
#        'cadetblue',
#        'lightgray',
#        'black',
#    ]
#    m = folium.Map(
#        location=[47.6, 9.4],
#        zoom_start=10,
#    )
#    m.add_child(folium.LatLngPopup())
#    for i in sheet.owner.index:
#        long = sheet.longitude[i]
#        lati = sheet.latitude[i]
#        folium.Marker(
#            location=[lati, long],
#            popup=str(sheet.dbscan[i]),
#            icon=folium.Icon(color=colors[sheet.dbscan[i] % 18])
#        ).add_to(m)
#    m.save('Bodensee_0.06_40.html')

def heatmap(df):
    df['magnitude'] = 1
    fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='magnitude',
                            radius=10,
                            center=dict(lat=47.45, lon=9.43), zoom=8.85,
                            opacity = 0.8,
                            hover_data={'magnitude':False,
                                        'latitude':False,
                                        'longitude':False},
                            mapbox_style="stamen-terrain")
    fig.show()

    return fig

def calendar_heatmap(df):
    import datetime
    import numpy as np

    format = '%Y-%m-%d %H:%M:%S'
    for index, df_iter in df.iterrows():
        df.loc[index,'month'] = datetime.datetime.strptime(
            df_iter.datetaken, format).month
        df.loc[index,'day'] = datetime.datetime.strptime(
            df_iter.datetaken, format).day
        df.loc[index,'weekday'] = datetime.datetime.strptime(
            df_iter.datetaken, format).weekday()

    df['magnitude'] = 1
    pivot_table = pd.pivot_table(df, values='magnitude', index=['weekday'],
                                 columns=['month'], aggfunc=np.sum,
                                 fill_value=0)

    x_label = ['Jan', 'Feb', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.',
               'Sept.', 'Oct.', 'Nov.', 'Dec.']
    y_label = ['Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.']

    fig = go.Figure(data=go.Heatmap(
        z=pivot_table,
        x=x_label,
        y=y_label,
        hoverinfo='skip',
        colorscale='Viridis'))

    fig.update_layout(
        title='Time distribution of visit frequency',
        xaxis_nticks=12)

    fig.show()

    return fig

def line(df):
    import datetime
    import numpy as np
    format = '%Y-%m-%d %H:%M:%S'
    for index, df_iter in df.iterrows():
        df.loc[index, 'year'] = datetime.datetime.strptime(
            df_iter.datetaken, format).year
    df['magnitude'] = 1
    pivot_table = pd.pivot_table(df, values='magnitude', index=['year'],
                                 aggfunc=np.sum, fill_value=0)
    fig = px.line(pivot_table, x=pivot_table.index, y='magnitude',
    title='Year distribution of visit frequency')
    fig.show()
    return fig



if __name__ == '__main__':
    from Preprocess import data_cleaning
    from Clustering import dbscan
    import pandas as pd
    from AssociationRules import find_association

    # load Flickr data from CSV to DataFrame
    filename = './flickr_14.10.2020.csv'
    cluster_result_path = 'dbscan_0.06_40.xls'
    df = pd.read_csv(filename, sep=';', encoding='latin-1')

    df, analysis_cluster = data_cleaning(df)
    fig_line = line(df)
    fig_calender_heatmap = calendar_heatmap(df)
    df = dbscan(df)
    fig_heatmap = heatmap(df)
    rule = find_association(df, analysis_cluster)
    fig_map = map(df, rule)
    from test_dash import dash
    dash(fig_map, fig_heatmap, fig_calender_heatmap, fig_line)
