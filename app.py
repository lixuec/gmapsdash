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
# ------------------------------------------------------------------------------
# Create the plot
# ------------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return_high'],name='high',line_shape='spline'))
fig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return'],name='mean',line_shape='spline'))
fig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return_low'],name='low',line_shape='spline'))
fig.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')
# ------------------------------------------------------------------------------
# Building the pages
# ------------------------------------------------------------------------------
es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)




app.layout = html.Div(children=[
    html.H1(children='Return'),
    dcc.Graph(figure=fig)])
# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)