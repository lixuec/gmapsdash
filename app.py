import dash
import pandas as pd
import datetime
from dash import dcc
from dash import html
from plotly import graph_objs as go
import plotly.express as px

# ------------------------------------------------------------------------------
# Init
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Grabbing the data
# ------------------------------------------------------------------------------
dat = '../gmaps/gmaps/data.csv'
df = pd.read_csv(dat)
# ==============================================================================
# Manipulate the data
# ==============================================================================
# ------------------------------------------------------------------------------
# Change the time to minutes
# ------------------------------------------------------------------------------

df['return'] = df['return']/60.0
df['go'] = df['go']/60.0
# ------------------------------------------------------------------------------
# Change the time to PST
# ------------------------------------------------------------------------------
time = df['timestamp'].to_list()
finaltime = []
for i in time:
    thistime = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f')
    thistime = thistime - datetime.timedelta(hours=8)
    finaltime.append(thistime.strftime('%H:%M'))
df['time'] = finaltime
# ------------------------------------------------------------------------------
# Sort and group the times
# ------------------------------------------------------------------------------
df.sort_values('time',inplace=True)
meandf = df.groupby('time').mean()
stdvdf = df.groupby('time').std()
highdf = meandf + 2*stdvdf
lowdf = meandf - 2*stdvdf
# ------------------------------------------------------------------------------
# Set up the final dataframe
# ------------------------------------------------------------------------------
finaldf = pd.concat([meandf,highdf,lowdf],axis=1)
finaldf.columns = ['go','return','go_high','return_high','go_low','return_low']
returndf = finaldf[['return','return_high','return_low']].copy()
returndf['time'] = returndf.index.to_list()
goingdf = finaldf[['go','go_high','go_low']].copy()
goingdf['time'] = goingdf.index.to_list()
# ==============================================================================
# Create the plot
# ==============================================================================
# ------------------------------------------------------------------------------
# Return graphs
# ------------------------------------------------------------------------------
returnfig = go.Figure()
returnfig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return_high'],name='high',line_shape='spline'))
returnfig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return'],name='mean',line_shape='spline'))
returnfig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return_low'],name='low',line_shape='spline'))
returnfig.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')
# ------------------------------------------------------------------------------
# Going graphs
# ------------------------------------------------------------------------------
goingfig = go.Figure()
goingfig.add_trace(go.Scatter(x=goingdf['time'],y=goingdf['go_high'],name='high',line_shape='spline'))
goingfig.add_trace(go.Scatter(x=goingdf['time'],y=goingdf['go'],name='mean',line_shape='spline'))
goingfig.add_trace(go.Scatter(x=goingdf['time'],y=goingdf['go_low'],name='low',line_shape='spline'))
goingfig.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')

# ==============================================================================
# Building the page
# ==============================================================================
# ------------------------------------------------------------------------------
# Return graphs
# ------------------------------------------------------------------------------
layout = []
layout.append(html.H1(children='Return'))
layout.append(dcc.Graph(figure=returnfig))
layout.append(html.H1(children='Going'))
layout.append(dcc.Graph(figure=goingfig))
# ------------------------------------------------------------------------------
# Going graphs
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Initialize the page in the app
# ------------------------------------------------------------------------------
es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)


app.layout = html.Div(children=layout)
server = app.server
# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)