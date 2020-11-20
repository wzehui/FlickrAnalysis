import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )
def dash(fig_1, fig_2, fig_3, fig_4):
    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    app = dash.Dash()
    app.layout = html.Div(#className='row',
                          children=[
                              dcc.Graph(figure=fig_1, style={
                                  'height':'100vh'}),
                              dcc.Graph(figure=fig_3),
                              dcc.Graph(figure=fig_4),
                             # dcc.Graph(figure=fig_2)
                          ])
                          #[dcc.Graph(figure=fig)])

    app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter