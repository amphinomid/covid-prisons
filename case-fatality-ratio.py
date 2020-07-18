import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Add sidebar for navigation, slider (see how these variables changed with respect to each other over the course of the
# outbreak), keep scale same across time (for slider), prob need st.cache,
# Add statistics for nationwide, graphs for mortality rate, incidence rate

# Since some bars not touching zeroline for some reason, offsetted zeroline by a tiny amount (max value * 0.01) -- not sure
# if this is bad practice? Since map is intended to show relationship rather than value,
# and because of subplots' scale, doesn't make a discernable difference


COVID_PRISON_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/covid_prison_cases.csv')
covid_prison_data = pd.read_csv(COVID_PRISON_DATA_URL, nrows = 50,
                    names = ["name", "abbreviation", "staff_tests", "staff_tests_with_multiples", "prisoner_tests", "prisoner_tests_with_multiples",
                            "total_staff_cases", "total_prisoner_cases", "staff_recovered", "prisoners_recovered", "total_staff_deaths","total_prisoner_deaths",
                            "as_of_date", "notes"],
                    usecols = ["name", "total_prisoner_cases", "total_prisoner_deaths"],
                    skiprows = 1, # Change according to date
                    )
covid_prison_data["Prison_CFR"] = covid_prison_data["total_prisoner_deaths"] * 100 / covid_prison_data["total_prisoner_cases"]


COVID_DATA_URL = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/07-14-2020.csv') # Change according to date
covid_data = pd.read_csv(COVID_DATA_URL, nrows = 50,
                    names = ["Province_State", "Country_Region", "Last_Update", "Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Active", "FIPS",
                            "Incident_Rate", "People_Tested", "People_Hospitalized", "Mortality_Rate", "UID", "ISO3", "Testing_Rate", "Hospitalization_Rate"],
                    usecols = ["Province_State", "Mortality_Rate"],
                    skiprows = [0, 3, 10, 11, 14, 15, 40, 45, 53],
                    )
covid_data = covid_data.rename(columns = {'Mortality_Rate': 'State_CFR'})


combined_data = pd.concat([covid_prison_data, covid_data], axis = 1)
combined_data = combined_data.drop(columns = "total_prisoner_cases")
combined_data = combined_data.drop(columns = "total_prisoner_deaths")
combined_data = combined_data.drop(columns = "Province_State")


# Based off grid from http://awesome-streamlit.org --> Gallery --> "Layout and Style Experiments"
def make_grid():
    grid = make_subplots(
        rows = 9,
        cols = 12,
        
        subplot_titles = (""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ,
                          ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , "ME",
                          "WA", "MT", "ND", "MN", "WI", "MI", ""  , ""  , "NY", "VT", "NH", "MA",
                          "OR", "ID", "WY", "SD", "IA", "IL", "IN", "OH", "PA", "NJ", "CT", "RI",
                          "NV", "UT", "CO", "NB", "KS", "MO", "TN", "KY", "WV", "VA", "MD", "DE",
                          ""  , "CA", "AZ", "NM", "OK", "AR", "MS", "AL", "GA", "SC", "NC", ""  ,
                          ""  , ""  , ""  , ""  , "TX", "LA", ""  , ""  , "FL", ""  , ""  , ""  ,
                          ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ,
                          ""  , "AK", ""  , "HI", ""  , ""  , ""  , ""  , ""  , ""  , "NAT", "" ,),
        specs = [
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
        ],
    )

    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Maine']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', name = 'In prisons'), row = 1, col = 12)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Maine']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', name = 'Statewide'), row = 1, col = 12)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Washington']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 1)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Washington']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 1)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Montana']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 2)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Montana']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 2)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'North Dakota']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 3)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'North Dakota']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 3)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Minnesota']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 4)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Minnesota']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 4)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Wisconsin']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 5)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Wisconsin']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 5)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Michigan']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 6)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Michigan']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 6)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'New York']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 9)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'New York']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 9)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Vermont']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 10)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Vermont']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 10)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'New Hampshire']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 11)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'New Hampshire']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 11)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Massachusetts']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 2, col = 12)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Massachusetts']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 2, col = 12)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Oregon']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 1)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Oregon']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 1)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Idaho']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 2)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Idaho']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 2)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Wyoming']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 3)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Wyoming']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 3)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'South Dakota']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 4)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'South Dakota']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 4)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Iowa']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 5)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Iowa']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 5)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Illinois']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 6)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Illinois']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 6)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Indiana']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 7)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Indiana']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 7)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Ohio']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 8)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Ohio']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 8)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Pennsylvania']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 9)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Pennsylvania']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 9)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'New Jersey']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 10)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'New Jersey']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 10)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Connecticut']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 11)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Connecticut']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 11)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Rhode Island']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 3, col = 12)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Rhode Island']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 3, col = 12)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Nevada']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 1)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Nevada']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 1)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Utah']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 2)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Utah']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 2)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Colorado']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 3)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Colorado']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 3)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Nebraska']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 4)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Nebraska']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 4)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Kansas']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 5)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Kansas']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 5)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Missouri']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 6)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Missouri']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 6)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Tennessee']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 7)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Tennessee']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 7)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Kentucky']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 8)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Kentucky']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 8)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'West Virginia']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 9)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'West Virginia']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 9)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Virginia']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 10)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Virginia']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 10)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Maryland']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 11)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Maryland']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 11)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Delaware']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 4, col = 12)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Delaware']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 4, col = 12)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'California']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 2)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'California']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 2)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Arizona']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 3)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Arizona']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 3)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'New Mexico']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 4)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'New Mexico']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 4)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Oklahoma']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 5)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Oklahoma']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 5)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Arkansas']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 6)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Arkansas']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 6)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Mississippi']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 7)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Mississippi']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 7)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Alabama']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 8)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Alabama']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 8)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Georgia']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 9)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Georgia']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 9)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'South Carolina']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 10)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'South Carolina']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 10)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'North Carolina']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 5, col = 11)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'North Carolina']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 5, col = 11)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Texas']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 6, col = 5)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Texas']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 6, col = 5)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Louisiana']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 6, col = 6)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Louisiana']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 6, col = 6)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Florida']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 6, col = 9)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Florida']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 6, col = 9)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Alaska']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 8, col = 2)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Alaska']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 8, col = 2)
    
    grid.add_trace(go.Bar(x = ["In prisons"], y = combined_data.loc[combined_data['name'] == 'Hawaii']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b', legendgroup = '1', showlegend = False), row = 8, col = 4)
    grid.add_trace(go.Bar(x = ["Statewide"], y = combined_data.loc[combined_data['name'] == 'Hawaii']['State_CFR'], width = 0.3, marker_color = '#000000', legendgroup = '2', showlegend = False), row = 8, col = 4)

    grid.update_layout(
        width = 1000,
        height = 944,
        #width = 950,
        #height = 897,
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
    #grid.update_yaxes(range = [0, max(combined_data["Prison_CFR"].max(), combined_data["Mortality_Rate"].max()) + 0.05 * max(combined_data["Prison_CFR"].max(), combined_data["State_CFR"].max())], visible = False)
    grid.update_yaxes(range = [0.01 * max(combined_data["Prison_CFR"].max(), combined_data["State_CFR"].max()), max(combined_data["Prison_CFR"].max(), combined_data["State_CFR"].max()) + 0.05 * max(combined_data["Prison_CFR"].max(), combined_data["State_CFR"].max())], visible = False)
    
    return grid


st.title('COVID-19 in US Prisons')
# CSS trick: https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/24, https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
#with open("style.css") as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


# Show grid map with Plotly
st.markdown('<h3>Map of Mortality</h3>', unsafe_allow_html = True)
st.plotly_chart(make_grid())


# Show bar chart with Plotly
st.markdown('<h3>Another Visualization</h3>', unsafe_allow_html = True)
bar_chart = go.Figure()
bar_chart.add_trace(go.Bar(
    x = combined_data['Prison_CFR'],
    y = combined_data['name'],
    orientation = 'h',
    name = 'In prisons',
    marker_color = '#f13b3b',
))
bar_chart.add_trace(go.Bar(
    x = combined_data['State_CFR'],
    y = combined_data['name'],
    orientation = 'h',
    name = 'Statewide',
    marker_color = '#000000',
))
bar_chart.update_layout(
    xaxis_title = 'COVID-19 Case-Fatality Ratio (deaths per 100 confirmed cases)',
    yaxis_title = 'State',
    width = 1000,
    height = 1100,
    barmode = 'group',
    bargap = 0.4,
    plot_bgcolor = '#ffffff',
    font = dict(family = 'IBM Plex Sans', size = 14, color = '#000000'),
)
bar_chart.update_yaxes(autorange = 'reversed')
st.write(bar_chart)


# Show data with Streamlit
st.markdown('<h3>Data</h3>', unsafe_allow_html = True)
as_of_date = datetime.strptime(COVID_DATA_URL[115: -4], '%m-%d-%Y').strftime('%B %d, %Y')
st.write('As of ' + as_of_date + '.')

st.markdown('<h4>COVID-19 in US State Prisons</h4>', unsafe_allow_html = True)
st.write(covid_prison_data)
st.markdown('[Data](https://github.com/themarshallproject/COVID_prison_data) from The Marshall Project, a nonprofit investigative newsroom dedicated to the U.S. criminal justice system. Here, "Prison_CFR" refers to case-fatality ratios in US state prisons, calculated using total prisoner cases and total prisoner deaths.')

st.markdown('<h4>COVID-19 in US States</h4>', unsafe_allow_html = True)
st.write(covid_data)
st.markdown('[Data](https://github.com/CSSEGISandData/COVID-19) from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University. Here, "State_CFR" refers to case-fatality ratio in US states, provided directly by the dataset.')

st.markdown('<h4>Side-by-Side Comparison</h4>', unsafe_allow_html = True)
st.write(combined_data)


# Explanation of epidemiological terms, potential problems, and other discussion
st.markdown('<h3>Epidemiological terms, caveats, discussion</h3>', unsafe_allow_html = True)
st.markdown('Case-fatality ratio is an epidemiological measure of mortality. A formula for case-fatality ratio is as follows: <i>number of recorded deaths * 100 / number of confirmed cases</i>.', unsafe_allow_html = True)
st.write('Some caveats include: (1) underreporting, (2) at any given moment, the instantaneous numbers may not reflect the ultimate numbers (e.g. uncertainty regarding ultimate number of deaths).')
st.write('Also note: federal prisons were excluded from these analyses, since the Marshall data placed them in a separate category (rather than grouping them with their state\'s data). The Marshall data did not include D.C. data, so D.C. was also omitted from these analyses. Finally&#8212I\'m assuming due to some sizing or rendering error&#8212some bars of the bar charts inside the map floated just above their zerolines; to fix this, I offset the y-ranges by a tiny amount. The map is only intended to show relative heights, and the scale of each bar chart is small enough that the offset doesn\'t make a discernable difference, but nonetheless, I\'m not sure if this is bad practice? (Feel free to roast me if it is.)')
st.write('In addition, prison mortality rates were estimated using population figures retrieved as early as January 2020.')
st.markdown('<b>The US has a mass incarceration problem.</b> Of all the prisoners in the world, 20% are held in the US ([Source](https://www.prisonpolicy.org/blog/2020/01/16/percent-incarcerated/)). And over the course of the COVID-19 pandemic, many prisons have failed to take adequate measures to protect prisoners from the disease.', unsafe_allow_html = True)
