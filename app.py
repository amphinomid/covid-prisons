import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Note: improve / beautify data descriptions & epidemiological terms, caveats, discussion; animate charts

PRISON_POP_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/prison_populations.csv')
@st.cache
def load_prison_pop_data():
    prison_pop_data = pd.read_csv(PRISON_POP_DATA_URL, nrows = 50,
                                  names = ['name', 'abbreviation', 'april_pop', 'as_of_date'],
                                  usecols = ['name', 'april_pop', 'as_of_date'],
                                  skiprows = 1,
                                  )
    nationwide_prison_pop_data = {'name': 'NATIONWIDE', 'april_pop': prison_pop_data.sum(0).loc['april_pop'], 'as_of_date': 'N/A'}
    prison_pop_data = prison_pop_data.append(nationwide_prison_pop_data, ignore_index = True)
    return prison_pop_data
prison_pop_data = load_prison_pop_data()

COVID_PRISON_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/covid_prison_cases.csv')
@st.cache
def load_covid_prison_data():
    covid_prison_data = pd.read_csv(COVID_PRISON_DATA_URL, nrows = 50,
                                    names = ['name', 'abbreviation', 'staff_tests', 'staff_tests_with_multiples', 'prisoner_tests',
                                             'prisoner_test_with_multiples', 'total_staff_cases', 'total_prisoner_cases', 'staff_recovered',
                                             'prisoners_recovered', 'total_staff_deaths', 'total_prisoner_deaths', 'as_of_date', 'notes'],
                                    usecols = ['name', 'total_prisoner_cases', 'total_prisoner_deaths'],
                                    skiprows = 1, # Can change according to date
                                    )
    covid_prison_data['Prison_CR'] = covid_prison_data['total_prisoner_cases'] * 100000 / prison_pop_data['april_pop']
    covid_prison_data['Prison_MR'] = covid_prison_data['total_prisoner_deaths'] * 100000 / prison_pop_data['april_pop']
    covid_prison_data['Prison_CFR'] = covid_prison_data['total_prisoner_deaths'] * 100000 / covid_prison_data['total_prisoner_cases']
    nationwide_covid_prison_data = {'name': 'NATIONWIDE', 'total_prisoner_cases': covid_prison_data.sum(0).loc['total_prisoner_cases'],
                                    'total_prisoner_deaths': covid_prison_data.sum(0).loc['total_prisoner_deaths'],
                                    'Prison_CR': '', 'Prison_MR': '', 'Prison_CFR': ''}
    nationwide_covid_prison_data['Prison_CR'] = nationwide_covid_prison_data['total_prisoner_cases'] * 100000 / prison_pop_data.sum(0).loc['april_pop']
    nationwide_covid_prison_data['Prison_MR'] = nationwide_covid_prison_data['total_prisoner_deaths'] * 100000 / prison_pop_data.sum(0).loc['april_pop']
    nationwide_covid_prison_data['Prison_CFR'] = nationwide_covid_prison_data['total_prisoner_deaths'] * 100000 / nationwide_covid_prison_data['total_prisoner_cases']
    covid_prison_data = covid_prison_data.append(nationwide_covid_prison_data, ignore_index = True)
    return covid_prison_data
covid_prison_data = load_covid_prison_data()

COVID_DATA_URL = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/07-14-2020.csv') # Can change according to date
@st.cache
def load_covid_data():
    covid_data = pd.read_csv(COVID_DATA_URL, nrows = 50,
                             names = ['Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered',
                                      'Active', 'FIPS', 'Incident_Rate', 'People_Tested', 'People_Hospitalized', 'Mortality_Rate', 'UID',
                                      'ISO3', 'Testing_Rate', 'Hospitalization_Rate'],
                             usecols = ['Province_State', 'Confirmed', 'Deaths', 'Incident_Rate', 'Mortality_Rate'],
                             skiprows = [0, 3, 10, 11, 14, 15, 40, 45, 53],
                             )
    covid_data = covid_data.rename(columns = {'Incident_Rate': 'State_CR'})
    covid_data = covid_data.rename(columns = {'Mortality_Rate': 'State_CFR'})
    covid_data['State_CFR'] = covid_data['State_CFR'] * 1000
    covid_data['population'] = (covid_data['Confirmed'] * 100000 / covid_data['State_CR']).astype(int)
    covid_data['State_MR'] = covid_data['Deaths'] * 100000 / covid_data['population']
    nationwide_covid_data = {'Province_State': 'NATIONWIDE', 'Confirmed': covid_data.sum(0).loc['Confirmed'], 'Deaths': covid_data.sum(0).loc['Deaths'],
                             'State_CR': '', 'State_CFR': '', 'population': covid_data.sum(0).loc['population'], 'State_MR': ''}
    nationwide_covid_data['State_CR'] = nationwide_covid_data['Confirmed'] * 100000 / nationwide_covid_data['population']
    nationwide_covid_data['State_CFR'] = nationwide_covid_data['Deaths'] * 100000 / nationwide_covid_data['Confirmed']
    nationwide_covid_data['State_MR'] = nationwide_covid_data['Deaths'] * 100000 / nationwide_covid_data['population']
    covid_data = covid_data.append(nationwide_covid_data, ignore_index = True)
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
                          ''  , 'AK', ''  , 'HI', ''  , ''  , ''  , ''  , ''  , ''  , 'NAT', '' ,),
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
    
    grid.add_trace(go.Bar(x = ['In prisons'], y = combined_data.loc[combined_data['name'] == 'NATIONWIDE']['Prison_' + metric], width = 0.3, marker_color = color, legendgroup = '1', showlegend = False), row = 8, col = 11)
    grid.add_trace(go.Bar(x = ['Statewide'], y = combined_data.loc[combined_data['name'] == 'NATIONWIDE']['State_' + metric], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 8, col = 11)

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
        font = dict(family = 'IBM Plex Sans', size = 12, color = '#000000'),
    )

    grid.update_xaxes(showticklabels = False, linecolor = '#000000')
    grid.update_yaxes(range = [0.01 * max(combined_data['Prison_' + metric].max(),combined_data['State_' + metric].max()),
                               max(combined_data['Prison_' + metric].max(), combined_data['State_' + metric].max()) + 0.05 * max(combined_data['Prison_' + metric].max(), combined_data['State_' + metric].max())], visible = False)
    
    return grid


st.title('COVID-19 in US Prisons, as Told by Data')


# Show/hide grid maps & bar charts with Streamlit radio buttons
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
        font = dict(family = 'IBM Plex Sans', size = 14, color = '#000000'),
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
        font = dict(family = 'IBM Plex Sans', size = 14, color = '#000000'),
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
        font = dict(family = 'IBM Plex Sans', size = 14, color = '#000000'),
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
    st.write('april_pop: "The total population of people held in the agency\'s prisons and secure facilities."')
    st.write('as_of_date: "The date the data reflect. In some instances, an April figure was not available, and we used the most recent number the agency could provide."')

    st.markdown('<h4>COVID-19 in US State Prisons</h4>', unsafe_allow_html = True)
    covid_prison_data = covid_prison_data[['name', 'total_prisoner_cases', 'total_prisoner_deaths', 'Prison_CR', 'Prison_MR', 'Prison_CFR']]
    st.write(covid_prison_data)
    st.markdown('[Data](https://github.com/themarshallproject/COVID_prison_data) from The Marshall Project, a nonprofit investigative newsroom dedicated to the U.S. criminal justice system.')
    st.write('total_prisoner_cases: "The cumulative number of positive coronavirus cases among the incarcerated population."')
    st.write('total_prisoner_deaths: "The number of deaths of prisoners to date."')
    st.write('Prison_CR: prison case rate; calculated as total_prisoner_cases * 100000 / population (from prison population data).')
    st.write('Prison_MR: prison mortality rate; calculated as total_prisoner_deaths * 100000 / population (from prison population data).')
    st.write('Prison_CFR: prison case-fatality ratio; calculated as total_prisoner_deaths * 100000 / total_prisoner_cases.')

    st.markdown('<h4>COVID-19 in US States</h4>', unsafe_allow_html = True)
    covid_data = covid_data[['Province_State', 'Confirmed', 'Deaths', 'population', 'State_CR', 'State_MR', 'State_CFR']]
    st.write(covid_data)
    st.markdown('[Data](https://github.com/CSSEGISandData/COVID-19) from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.')
    st.write('Confirmed: "Aggregated confirmed case count for the state."')
    st.write('Deaths: "Aggregated Death case count for the state."')
    st.write('population: calculated using State_CR, provided as "Incident_Rate" by the dataset; population = Confirmed * 100000 / Incident_Rate.')
    st.write('State_CR: state case rate; provided as "Incident_Rate" by the dataset; "confirmed cases per 100,000 persons."')
    st.write('State_MR: state mortality rate; calculated as Deaths * 100000 / population.')
    st.write('State_CFR: state case-fatality ratio; provided as "Mortality_Rate" by the dataset, except was per 100 confirmed cases ("Number recorded deaths * 100/ Number confirmed cases"); multipled by 1,000 to convert to number of recorded deaths per 100,000 confirmed cases.')

    st.markdown('<h4>Side-by-Side Comparison</h4>', unsafe_allow_html = True)
    combined_data = combined_data[['name', 'Prison_CR', 'Prison_MR', 'Prison_CFR', 'State_CR', 'State_MR', 'State_CFR']]
    st.write(combined_data)


# Explanation of epidemiological terms, potential problems, and other discussion
st.markdown('<h3>Epidemiological terms, caveats, discussion</h3>', unsafe_allow_html = True)
st.markdown('Case rate is a measure of how widespread an illness is in a population. A formula for case rate is as follows: <i>number of confirmed cases * 100000 / population</i>.', unsafe_allow_html = True)
st.markdown('Mortality rate is a measure of the frequency of death in a population due to a disease. A formula for mortality rate is as follows: <i>number of recorded deaths * 100000 / population</i>.', unsafe_allow_html = True)
st.markdown('Case-fatality ratio is a measure of mortality. A formula for case-fatality ratio is as follows: <i>number of recorded deaths * 100 / number of confirmed cases</i>.', unsafe_allow_html = True)
st.write('Some caveats include: (1) underreporting, (2) at any given moment, the instantaneous numbers may not reflect the ultimate numbers (e.g. uncertainty regarding ultimate number of deaths).')
st.write('Also note: federal prisons were excluded from these analyses, since the Marshall data placed them in a separate category (rather than grouping them with their state\'s data). The Marshall data did not include D.C. data, so D.C. was also omitted from these analyses. Finally&#8212I\'m assuming due to some sizing or rendering error&#8212some bars of the bar charts inside the map floated just above their zerolines; to fix this, I offset the y-ranges by a tiny amount. The map is only intended to show relative heights, and the scale of each bar chart is small enough that the offset doesn\'t make a discernable difference, but nonetheless, I\'m not sure if this is bad practice? (Feel free to roast me if it is.)')
st.write('In addition, prison case rates were estimated using population figures retrieved as early as January 2020.')
st.markdown('<b>The US has a mass incarceration problem.</b> Of all the prisoners in the world, 20% are held in the US ([Source](https://www.prisonpolicy.org/blog/2020/01/16/percent-incarcerated/)). And over the course of the COVID-19 pandemic, many prisons have failed to take adequate measures to protect prisoners from the disease.', unsafe_allow_html = True)
