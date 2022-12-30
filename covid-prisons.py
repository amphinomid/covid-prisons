import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

PRISON_POP_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/prison_populations.csv')
def load_prison_pop_data():
    prison_pop_data = pd.read_csv(PRISON_POP_DATA_URL,
                                  names = ['name', 'abbreviation', 'month', 'as_of_date', 'pop'],
                                  usecols = ['name', 'as_of_date', 'pop'],
                                  skiprows = 1,
                                  )
    prison_pop_data = prison_pop_data.drop_duplicates(subset = ['name'], keep = 'last')
    return prison_pop_data
prison_pop_data = load_prison_pop_data()

COVID_PRISON_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/covid_prison_cases.csv')
def load_covid_prison_data():
    covid_prison_data = pd.read_csv(COVID_PRISON_DATA_URL, nrows = 50,
                                    names = ['name', 'abbreviation', 'staff_tests', 'staff_tests_with_multiples', 'total_staff_cases',
                                             'staff_recovered', 'total_staff_deaths', 'staff_partial_dose', 'staff_full_dose',
                                             'prisoner_tests', 'prisoner_test_with_multiples', 'total_prisoner_cases', 'prisoners_recovered',
                                             'total_prisoner_deaths', 'prisoners_partial_dose', 'prisoners_full_dose', 'as_of_date', 'notes'],
                                    usecols = ['name', 'total_prisoner_cases', 'total_prisoner_deaths', 'as_of_date'],
                                    skiprows = 154, # Relatively recent with relatively few non-reporters (Delaware for cases and Maine and Nevada for deaths)
                                    )
    covid_prison_data['Prison_CR'] = covid_prison_data['total_prisoner_cases']# * 100000 / prison_pop_data['pop']
    covid_prison_data['Prison_MR'] = covid_prison_data['total_prisoner_deaths'] * 100000 / prison_pop_data['pop']
    covid_prison_data['Prison_CFR'] = covid_prison_data['total_prisoner_deaths'] * 100000 / covid_prison_data['total_prisoner_cases']
    return covid_prison_data
covid_prison_data = load_covid_prison_data()
data_date = covid_prison_data.at[0, 'as_of_date']
data_date = data_date.replace('/', '-')

COVID_DATA_URL = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/' + data_date + '.csv') # Change according to date
def load_covid_data():
    covid_data = pd.read_csv(COVID_DATA_URL, nrows = 50,
                             names = ['Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered',
                                      'Active','FIPS','Incident_Rate','Total_Test_Results','People_Hospitalized','Case_Fatality_Ratio',
                                      'UID','ISO3','Testing_Rate','Hospitalization_Rate','Date','People_Tested','Mortality_Rate'],
                             usecols = ['Province_State', 'Confirmed', 'Deaths', 'Incident_Rate', 'Case_Fatality_Ratio'],
                             skiprows = [0, 3, 10, 11, 14, 15, 40, 45, 53],
                            )
    covid_data = covid_data.rename(columns = {'Incident_Rate': 'State_CR'})
    covid_data = covid_data.rename(columns = {'Case_Fatality_Ratio': 'State_CFR'})
    covid_data['State_CFR'] = covid_data['State_CFR'] * 1000
    covid_data['population'] = (covid_data['Confirmed'] * 100000 / covid_data['State_CR']).astype(int)
    covid_data['State_MR'] = covid_data['Deaths'] * 100000 / covid_data['population']
    return covid_data
covid_data = load_covid_data()

combined_data = pd.concat([covid_prison_data, covid_data], axis = 1)
combined_data = combined_data.drop(columns = ['total_prisoner_cases', 'total_prisoner_deaths', 'Province_State', 'Confirmed', 'Deaths',
                                              'population'])


# Create grid map with Plotly subplots
# Based off grid from http://awesome-streamlit.org --> Gallery --> 'Layout and Style Experiments'
def make_grid(metric, color):
    grid = make_subplots(
        rows = 9,
        cols = 12,
        
        subplot_titles = (''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  ,
                          ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , 'ME',
                          'WA', 'MT', 'ND', 'MN', 'WI', 'MI', ''  , ''  , 'NY', 'VT', 'NH', 'MA',
                          'OR', 'ID', 'WY', 'SD', 'IA', 'IL', 'IN', 'OH', 'PA', 'NJ', 'CT', 'RI',
                          'NV', 'UT', 'CO', 'NB', 'KS', 'MO', 'TN', 'KY', 'WV', 'VA', 'MD', 'DE',
                          ''  , 'CA', 'AZ', 'NM', 'OK', 'AR', 'MS', 'AL', 'GA', 'SC', 'NC', ''  ,
                          ''  , ''  , ''  , ''  , 'TX', 'LA', ''  , ''  , 'FL', ''  , ''  , ''  ,
                          ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  ,
                          ''  , 'AK', ''  , 'HI', ''  , ''  , ''  , ''  , ''  , ''  , '', '' ,),
        specs = [
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
            [ {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'} ],
        ],
    )

    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Maine']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', name = 'In prisons'), row = 1, col = 12)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Maine']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', name = 'Statewide'), row = 1, col = 12)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Washington']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 1)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Washington']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 1)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Montana']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 2)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Montana']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 2)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'North Dakota']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 3)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'North Dakota']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 3)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Minnesota']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 4)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Minnesota']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 4)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Wisconsin']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 5)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Wisconsin']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 5)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Michigan']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 6)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Michigan']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 6)
   
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'New York']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 9)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'New York']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 9)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Vermont']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 10)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Vermont']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 10)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'New Hampshire']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 11)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'New Hampshire']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 11)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Massachusetts']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 2, col = 12)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Massachusetts']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 12)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Oregon']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 1)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Oregon']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 1)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Idaho']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 2)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Idaho']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 2)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Wyoming']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 3)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Wyoming']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 3)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'South Dakota']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 4)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'South Dakota']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 4)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Iowa']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 5)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Iowa']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 5)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Illinois']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 6)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Illinois']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 6)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Indiana']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 7)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Indiana']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 7)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Ohio']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 8)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Ohio']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 8)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Pennsylvania']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 9)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Pennsylvania']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 9)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'New Jersey']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 10)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'New Jersey']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 10)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Connecticut']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 11)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Connecticut']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 11)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Rhode Island']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 3, col = 12)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Rhode Island']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 12)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Nevada']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 1)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Nevada']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 1)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Utah']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 2)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Utah']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 2)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Colorado']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 3)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Colorado']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 3)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Nebraska']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 4)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Nebraska']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 4)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Kansas']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 5)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Kansas']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 5)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Missouri']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 6)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Missouri']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 6)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Tennessee']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 7)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Tennessee']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 7)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Kentucky']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 8)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Kentucky']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 8)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'West Virginia']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 9)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'West Virginia']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 9)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Virginia']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 10)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Virginia']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 10)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Maryland']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 11)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Maryland']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 11)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Delaware']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 4, col = 12)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Delaware']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 12)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'California']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 2)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'California']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 2)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Arizona']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 3)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Arizona']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 3)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'New Mexico']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 4)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'New Mexico']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 4)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Oklahoma']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 5)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Oklahoma']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 5)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Arkansas']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 6)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Arkansas']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 6)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Mississippi']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 7)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Mississippi']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 7)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Alabama']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 8)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Alabama']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 8)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Georgia']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 9)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Georgia']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 9)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'South Carolina']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 10)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'South Carolina']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 10)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'North Carolina']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 5, col = 11)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'North Carolina']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 11)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Texas']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 6, col = 5)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Texas']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 6, col = 5)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Louisiana']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 6, col = 6)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Louisiana']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 6, col = 6)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Florida']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 6, col = 9)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Florida']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 6, col = 9)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Alaska']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 8, col = 2)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Alaska']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 8, col = 2)
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'Hawaii']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 8, col = 4)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'Hawaii']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 8, col = 4)
    
    grid.update_layout(
        #width = 1100,
        #height = 1038,
        width = 1000,
        height = 944,
        #showlegend = False,
        #legend_itemclick = False,
        #legend_itemdoubleclick = False,
        legend = dict (
            font = dict (
                size = 14,
            ),
        ),
        plot_bgcolor = '#ffffff',
        #font = dict(family = 'sans serif', size = 12, color = '#000000'),
        font = dict(size = 12, color = '#000000'),
    )

    grid.update_xaxes(showticklabels = False)#, linecolor = '#000000')
    grid.update_yaxes(range = [0, max(combined_data['Prison_' + metric].max(), combined_data['State_' + metric].max()) + 0.05 * max(combined_data['Prison_' + metric].max(), combined_data['State_' + metric].max())], visible = False)
    
    return grid


st.title('COVID-19 in US Prisons, as Told by Data')

# Show/hide Plotly grid maps & bar charts with Streamlit radio buttons
# CSS for horizontal radio button layout from https://discuss.streamlit.io/t/horizontal-radio-buttons/2114
display_data = st.radio('', ('Case Rate', 'Mortality Rate', 'Case-Fatality Ratio'))
st.write('<style> div.Widget.row-widget.stRadio > div { flex-direction: row; justify-content: space-between; width: 580px; } </style>', unsafe_allow_html=True)
if display_data == 'Mortality Rate':
    st.plotly_chart(make_grid('MR', '#1E88E5'))
    mr_chart = go.Figure()
    mr_chart.add_trace(go.Bar(
        x = combined_data['Prison_MR'],
        y = combined_data['name'],
        orientation = 'h',
        name = 'In prisons',
        marker_color = '#1E88E5',
        ))
    mr_chart.add_trace(go.Bar(
        x = combined_data['State_MR'],
        y = combined_data['name'],
        orientation = 'h',
        name = 'Statewide',
        marker_color = '#000000',
        ))
    mr_chart.update_layout(
        xaxis_title = 'COVID-19 Mortality Rate (confirmed deaths per 100,000 persons)',
        yaxis_title = 'State',
        width = 1000,
        height = 1100,
        barmode = 'group',
        bargap = 0.4,
        plot_bgcolor = '#ffffff',
        #font = dict(family = 'sans serif', size = 14, color = '#000000'),
        font = dict(size = 14, color = '#000000'),
        )
    mr_chart.update_yaxes(autorange = 'reversed')
    st.write(mr_chart)
elif display_data == 'Case-Fatality Ratio':
    st.plotly_chart(make_grid('CFR', '#FFC107'))
    cfr_chart = go.Figure()
    cfr_chart.add_trace(go.Bar(
        x = combined_data['Prison_CFR'],
        y = combined_data['name'],
        orientation = 'h',
        name = 'In prisons',
        marker_color = '#FFC107',
        ))
    cfr_chart.add_trace(go.Bar(
        x = combined_data['State_CFR'],
        y = combined_data['name'],
        orientation = 'h',
        name = 'Statewide',
        marker_color = '#000000',
        ))
    cfr_chart.update_layout(
        xaxis_title = 'COVID-19 Case-Fatality Ratio (confirmed deaths per 100,000 confirmed cases)',
        yaxis_title = 'State',
        width = 1000,
        height = 1100,
        barmode = 'group',
        bargap = 0.4,
        plot_bgcolor = '#ffffff',
        #font = dict(family = 'sans serif', size = 14, color = '#000000'),
        font = dict(size = 14, color = '#000000'),
        )
    cfr_chart.update_yaxes(autorange = 'reversed')
    st.write(cfr_chart)
else:
    st.plotly_chart(make_grid('CR', '#F13B3B'))
    cr_chart = go.Figure()
    cr_chart.add_trace(go.Bar(
        x = combined_data['Prison_CR'],
        y = combined_data['name'],
        orientation = 'h',
        name = 'In prisons',
        marker_color = '#F13B3B',
        ))
    cr_chart.add_trace(go.Bar(
        x = combined_data['State_CR'],
        y = combined_data['name'],
        orientation = 'h',
        name = 'Statewide',
        marker_color = '#000000',
        ))
    cr_chart.update_layout(
        xaxis_title = 'COVID-19 Case Rate (confirmed cases per 100,000 persons)',
        yaxis_title = 'State',
        width = 1000,
        height = 1100,
        barmode = 'group',
        bargap = 0.4,
        plot_bgcolor = '#ffffff',
        #font = dict(family = 'sans serif', size = 14, color = '#000000'),
        font = dict(size = 14, color = '#000000'),
        )
    cr_chart.update_yaxes(autorange = 'reversed')
    st.write(cr_chart)


# Show/hide data with Streamlit checkbox
if st.checkbox('Show Data'):
    as_of_date = datetime.strptime(COVID_DATA_URL[115: -4], '%m-%d-%Y').strftime('%B %d, %Y')
    st.write('Data as of ' + as_of_date + ' (except prison population data, for which date is indicated in the datatable).')

    st.markdown('<h4>US State Prison Populations</h4>', unsafe_allow_html = True)
    st.write(prison_pop_data)
    st.markdown('[Data](https://github.com/themarshallproject/COVID_prison_data) from The Marshall Project, a nonprofit investigative newsroom dedicated to the U.S. criminal justice system.')
    st.markdown('*pop:* "The total population of people in prison."')
    st.markdown('*as_of_date:* "The date the count reflects."')

    st.markdown('<h4>COVID-19 in US State Prisons</h4>', unsafe_allow_html = True)
    covid_prison_data = covid_prison_data[['name', 'total_prisoner_cases', 'total_prisoner_deaths', 'Prison_CR', 'Prison_MR', 'Prison_CFR']]
    st.write(covid_prison_data)
    st.markdown('[Data](https://github.com/themarshallproject/COVID_prison_data) from The Marshall Project, a nonprofit investigative newsroom dedicated to the U.S. criminal justice system.')
    st.markdown('*total_prisoner_cases:* "The cumulative number of positive coronavirus cases among the incarcerated population."')
    st.markdown('*total_prisoner_deaths:* "The number of deaths of incarcerated individuals to date."')
    st.markdown('*Prison_CR:* prison case rate; calculated as *total_prisoner_cases \* 100000 / population* (from prison population data).')
    st.markdown('*Prison_MR:* prison mortality rate; calculated as *total_prisoner_deaths \* 100000 / population* (from prison population data).')
    st.markdown('*Prison_CFR:* prison case-fatality ratio; calculated as *total_prisoner_deaths \* 100000 / total_prisoner_cases*.')

    st.markdown('<h4>COVID-19 in US States</h4>', unsafe_allow_html = True)
    covid_data = covid_data[['Province_State', 'Confirmed', 'Deaths', 'population', 'State_CR', 'State_MR', 'State_CFR']]
    st.write(covid_data)
    st.markdown('[Data](https://github.com/CSSEGISandData/COVID-19) from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.')
    st.markdown('*Confirmed:* "Aggregated confirmed case count for the state."')
    st.markdown('*Deaths:* "Aggregated Death case count for the state."')
    st.markdown('*population:* calculated using State_CR, provided as "Incident_Rate" by the dataset; *Confirmed \* 100000 / Incident_Rate*.')
    st.markdown('*State_CR:* state case rate; provided as "Incident_Rate" by the dataset; "confirmed cases per 100,000 persons."')
    st.markdown('*State_MR:* state mortality rate; calculated as *Deaths \* 100000 / population*.')
    st.markdown('*State_CFR:* state case-fatality ratio; provided as "Case_Fatality_Ratio" by the dataset, except was per 100 confirmed cases ("Number recorded deaths * 100/ Number confirmed cases"); multipled by 1,000 to convert to number of recorded deaths per 100,000 confirmed cases.')

    st.markdown('<h4>Side-by-Side Comparison</h4>', unsafe_allow_html = True)
    combined_data = combined_data[['name', 'Prison_CR', 'State_CR', 'Prison_MR', 'State_MR', 'Prison_CFR', 'State_CFR']]
    st.write(combined_data)


# Explanation of terms, potential problems, and other discussion
st.markdown('<h3>Explanation of terms, caveats, discussion</h3>', unsafe_allow_html = True)
st.markdown('**Case rate** estimates how widespread an illness is. A formula for case rate is as follows: *number of confirmed cases \* 100000 / population*.')
st.markdown('**Mortality rate** estimates how widespread death caused by an illness is. A formula for mortality rate is as follows: *number of recorded deaths \* 100000 / population*.')
st.markdown('**Case-fatality ratio** estimates how deadly an illness is. A formula for case-fatality ratio is as follows: *number of recorded deaths \* 100000 / number of confirmed cases*.')
st.write('**Data doesn\'t always tell the whole story.** The data likely reflects underreporting (some COVID-19 cases and deaths are never ultimately confirmed). Case rate, mortality rate, case-fatality ratio and other metrics depend on both (a) an outbreak itself and (b) our response to it (for example, testing). This project is a snapshot of the situation in around June 2021 for the prison COVID-19 data; The Marshall Project\'s [repo](https://github.com/themarshallproject/COVID_prison_data), which this project relies on, is no longer being updated. I chose a relatively recent snapshot with relatively few data gaps: the non-reporting states are Delaware for prison COVID-19 cases and Maine and Nevada for prison COVID-19 deaths. **An empty spot on the bar graph is *not* a 0! Check the raw data to be sure (\'NaN\' signifies a gap).** Dates don\'t always align due to the various reporting dates of the different sources of data required for this analysis. Finally, federal prisons and D.C. were excluded from this analysis; the Marshall data did not include D.C. data, and placed federal prisons in a separate category (rather than grouping them with their state\'s data).')
st.markdown('**The US has a mass incarceration problem.** According to the [American Civil Liberties Union (ACLU)](https://www.aclu.org/issues/smart-justice/mass-incarceration), "despite making up close to 5% of the global population, the U.S. has nearly 25% of the world\'s prison population". And over the course of the COVID-19 pandemic, many state and local governments have failed to take adequate measures to protect incarcerated individuals from the disease. Incarcerated individuals have continued to live in cramped, crowded and often unsanitary facilities, and interact with staff who travel in-and-out of the surrounding community.')
st.markdown('More on interpreting COVID-19 data: ["How to Understand COVID-19 Numbers"](https://www.propublica.org/article/how-to-understand-covid-19-numbers?utm_source=sailthru&utm_medium=email&utm_campaign=majorinvestigations&utm_content=feature).')
st.markdown('More on mass incarceration: ["Mass Incarceration"](https://www.aclu.org/issues/smart-justice/mass-incarceration).')
st.markdown('More on COVID-19 in prisons, including its implications for people of color—especially Black people, who face both higher incarceration rates and higher COVID-19 mortality rates compared to other racial groups—as well as testing strategies and prison population changes: ["How U.S. Prisons Became Ground Zero for Covid-19"](https://www.politico.com/news/magazine/2020/06/25/criminal-justice-prison-conditions-coronavirus-in-prisons-338022).')
st.markdown('For a more thorough investigation of the issues at hand, check out this article from The Marshall Project, the organization that compiles the prison data I used: ["A State-by-State Look at Coronavirus in Prisons"](https://www.themarshallproject.org/2020/05/01/a-state-by-state-look-at-coronavirus-in-prisons).')
st.write('Grid map layout inspired by this data visualization project: ["States Are Reopening: See How Coronavirus Cases Rise or Fall"](https://projects.propublica.org/reopening-america/).')
st.markdown('View the source code for this project [here](https://github.com/amphinomid/covid-prisons).')
