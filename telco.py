from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

strDataset = "https://raw.githubusercontent.com/nelczezulueta/DATANVI-MCO2/main/telecom_customer_churn.csv"

dfDataset = pd.read_csv(strDataset, encoding = "ISO-8859-1")
dfDataset.head() 

dfDataset1 = churned_data = dfDataset[dfDataset['Customer Status'] == 'Churned']
dfDataset1

dfDataset2 = dfDataset1[['Gender', 'Married', 'Offer', 'Phone Service', 'Multiple Lines', 'Internet Service', 'Internet Type', 'Contract', 'Paperless Billing', 'Payment Method']]
dfDataset2

dfDataset3 = dfDataset[['Gender', 'Married', 'Offer', 'Phone Service', 'Multiple Lines', 'Internet Service', 'Internet Type', 'Contract', 'Paperless Billing', 'Payment Method']]

dfDataset4 = dfDataset[dfDataset['Internet Service'] == 'Yes']
dfDataset4

cmpntTitle = html.H1(children = "Data Visualization for Telecom Customer Churn", id = "Title")

cmpntGraphTitle1 = html.H3(children = "Churned Customer Metrics", className = "graph-title")
cmpntGraphTitle2 = html.H3(children = "Scatter Plot of Monthly Charge vs Total Charges of Churned Customers by Category", className = "graph-title")
cmpntGraphTitle3 = html.H3(children = "Number of Churned vs Retained Customers", className = "graph-title")
cmpntGraphTitle4 = html.H3(children = "Box Plot of the tenure of Churned and Retained Customers", className = "graph-title")
cmpntGraphTitle5 = html.H3(children = "Treemap of Churn Categories and Churn Reasons", className = "graph-title")

graphData2 = px.scatter(dfDataset1, x='Monthly Charge', y='Total Charges',
                         hover_data=['Customer ID', 'Payment Method'],
                         color='Total Charges',
                         color_continuous_scale=px.colors.sequential.Blues)

graphData2.update_layout(
    paper_bgcolor='rgba(17,17,17,1)',
    plot_bgcolor='rgba(17,17,17,1)',
    font=dict(color='white'),
    xaxis=dict(gridcolor='grey'),
    yaxis=dict(gridcolor='grey'),
    title=dict(x=0.5, xanchor='center', font=dict(size=20))
)
cmpntGraph2 = dcc.Graph(figure=graphData2, id='scatter-plot')


@application.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-dropdown', 'value')]
)

def update_pie_chart(selected_attribute):

    fig = px.pie(dfDataset2, names=selected_attribute)

    fig.update_layout(
        paper_bgcolor='rgba(17,17,17,1)',
        plot_bgcolor='rgba(17,17,17,1)',
        font=dict(color='white'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


@application.callback(
    Output('bar-chart', 'figure'),
    [Input('bar-dropdown', 'value')]
)


def update_bar_chart(selected_category):
    churned_counts = dfDataset[dfDataset['Customer Status'] == 'Churned'][selected_category].value_counts().rename('Churned')
    retained_counts = dfDataset[dfDataset['Customer Status'] == 'Stayed'][selected_category].value_counts().rename('Stayed')

    combined_counts = pd.concat([churned_counts, retained_counts], axis=1, sort=False).fillna(0)
    fig = px.bar(
        combined_counts,
        barmode='group',
        title=f'Number of Churned vs Retained Customers by {selected_category}'
    )

    fig.update_traces(
    marker_line_color='rgb(8,48,107)',
    marker_line_width=1.5,
    opacity=0.6
)
    fig.update_layout(
        paper_bgcolor='rgba(17,17,17,1)',
        plot_bgcolor='rgba(17,17,17,1)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='grey', tickangle=-45),
        xaxis_title = selected_category,
        yaxis=dict(gridcolor='grey'),
        yaxis_title = 'Count',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        title_font_size = 13,
        title_x = 0.5
    )
    return fig

@application.callback(
    Output('tenure-distribution-plot', 'figure'),
    [Input('churn-status-dropdown', 'value')]
)

def update_boxplot(churn_status):

  filtered_df = dfDataset[dfDataset['Customer Status'] == churn_status]

  fig = px.box(
        filtered_df,
        x='Tenure in Months',
        color='Customer Status',
        notched=True,
        title=f'Distribution of Tenure in Months ({churn_status})'
    )

  fig.update_layout(
        paper_bgcolor='rgba(17,17,17,1)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        transition_duration=500
    )

  return fig

graphData5 = px.treemap(
    dfDataset1,
    path=['Churn Category', 'Churn Reason'],
)

graphData5.update_layout(
    paper_bgcolor='rgba(17,17,17,1)',
    plot_bgcolor='rgba(17,17,17,1)',
    font=dict(color='white'),
)

cmpntGraph5 = dcc.Graph(figure=graphData5, id='churn-treemap')

application = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = application.server

application.layout = dbc.Container(fluid=True, children=[
    
    html.Div(cmpntTitle),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.Div(cmpntGraphTitle1),
            dcc.Dropdown(
                id='pie-dropdown',
                options=[{'label': col, 'value': col} for col in dfDataset2.columns if dfDataset2[col].dtype == 'object'],
                value='Payment Method'
            ),
            dcc.Graph(id='pie-chart')
        ], width=6),


        dbc.Col([
            html.Div(cmpntGraphTitle3),
            dcc.Dropdown(
                id='bar-dropdown',
                options=[{'label': col, 'value': col} for col in dfDataset3.select_dtypes(include=['object']).columns],
                value='Payment Method'
            ),
            dcc.Graph(id='bar-chart')
        ], width=6),
    ]),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.Div(cmpntGraphTitle2),
            cmpntGraph2
        ], width=12)
    ]),
    
    html.Hr(),

    dbc.Row([
        dbc.Col([
          html.Div(cmpntGraphTitle4),
          dcc.Dropdown(
            id='churn-status-dropdown',
            options=[
            {'label': 'Churned', 'value': 'Churned'},
            {'label': 'Stayed', 'value': 'Stayed'},
        ],
        value='Churned',
        clearable=False
    ),
      dcc.Graph(id='tenure-distribution-plot')
        ], width = 12)
    ]),
    
    html.Hr(),
    
      dbc.Row([
        dbc.Col([
          html.Div(cmpntGraphTitle5),
          cmpntGraph5
        ], width = 12)

    ]),

])

if __name__ == '__main__':
    application.run_server(port = 8051)