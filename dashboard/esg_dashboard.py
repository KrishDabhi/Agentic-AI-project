import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Sample data for demonstration
data = {
    'Company': ['Company A', 'Company B', 'Company C', 'Company D'],
    'ESG_Score': [85, 72, 90, 68],
    'Environmental': [80, 75, 95, 70],
    'Social': [88, 70, 85, 65],
    'Governance': [87, 71, 90, 69]
}
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='ESG Monitor Dashboard'),

    html.Div(children='''
        Real-time ESG risk monitoring.
    '''),

    dcc.Graph(
        id='esg-scores',
        figure=px.bar(df, x='Company', y='ESG_Score', title='ESG Scores by Company')
    ),

    dcc.Graph(
        id='esg-breakdown',
        figure=px.line(df, x='Company', y=['Environmental', 'Social', 'Governance'], title='ESG Breakdown')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)