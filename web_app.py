import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# How to handle data from federal prisons and D.C.? Federal prisons: not exactly state-based, but it would be misleading
# to use "nationwide" COVID data? D.C.: Marshall data doesn't include, but JHU data does.

# Other stuff: shift grid map to the left, bold state abbreviations, add column of zeroes to combined data to create gap between two bars
# add titles to grid map and bar chart, add sidebar for navigation, bar chart --> sortable?, implement slider (see how these variables
# changed with respect to each other over the course of the outbreak), keep scale same across time (for slider), prob need st.cache,
# add statistics for overall / nationwide, graphs for mortality rate, incidence rate, do bar graphs inside grid map all need to have same
# scale? Or does the bar chart serve as "normalized" visualization? But if normalize grid map, can remove all axis marker things?


COVID_PRISON_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/covid_prison_cases.csv')
covid_prison_data = pd.read_csv(COVID_PRISON_DATA_URL, nrows = 50,
                    names = ["name", "abbreviation", "staff_tests", "staff_tests_with_multiples", "prisoner_tests", "prisoner_tests_with_multiples",
                            "total_staff_cases", "total_prisoner_cases", "staff_recovered", "prisoners_recovered", "total_staff_deaths","total_prisoner_deaths",
                            "as_of_date", "notes"],
                    usecols = ["name", "total_prisoner_cases", "total_prisoner_deaths"],
                    skiprows = 1, # Change according to date
                    )


COVID_DATA_URL = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/07-07-2020.csv') # Change according to date
covid_data = pd.read_csv(COVID_DATA_URL, nrows = 50,
                    names = ["Province_State", "Country_Region", "Last_Update", "Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Active", "FIPS",
                            "Incident_Rate", "People_Tested", "People_Hospitalized", "Mortality_Rate", "UID", "ISO3", "Testing_Rate", "Hospitalization_Rate"],
                    usecols = ["Province_State", "Mortality_Rate"],
                    skiprows = [0, 3, 10, 11, 14, 15, 40, 45, 53],
                    )


combined_data = pd.concat([covid_prison_data, covid_data], axis = 1)
combined_data["Prison_CFR"] = combined_data["total_prisoner_deaths"] * 100 / combined_data["total_prisoner_cases"]
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

    grid.update_layout(
        width = 1000,
        height = 944,
        plot_bgcolor = '#ffffff',
        font = dict(family = 'IBM Plex Sans', size = 12, color = '#000000'),
    )

    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Maine']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 1, col = 12)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Maine']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 1, col = 12)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Washington']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 1)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Washington']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 1)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Montana']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 2)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Montana']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 2)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'North Dakota']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 3)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'North Dakota']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 3)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Minnesota']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 4)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Minnesota']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 4)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Wisconsin']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 5)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Wisconsin']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 5)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Michigan']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 6)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Michigan']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 6)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'New York']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 9)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'New York']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 9)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Vermont']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 10)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Vermont']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 10)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'New Hampshire']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 11)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'New Hampshire']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 11)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Massachusetts']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 2, col = 12)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Massachusetts']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 2, col = 12)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Oregon']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 1)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Oregon']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 1)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Idaho']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 2)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Idaho']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 2)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Wyoming']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 3)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Wyoming']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 3)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'South Dakota']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 4)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'South Dakota']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 4)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Iowa']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 5)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Iowa']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 5)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Illinois']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 6)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Illinois']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 6)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Indiana']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 7)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Indiana']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 7)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Ohio']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 8)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Ohio']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 8)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Pennsylvania']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 9)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Pennsylvania']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 9)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'New Jersey']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 10)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'New Jersey']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 10)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Connecticut']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 11)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Connecticut']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 11)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Rhode Island']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 3, col = 12)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Rhode Island']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 3, col = 12)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Nevada']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 1)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Nevada']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 1)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Utah']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 2)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Utah']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 2)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Colorado']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 3)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Colorado']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 3)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Nebraska']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 4)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Nebraska']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 4)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Kansas']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 5)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Kansas']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 5)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Missouri']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 6)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Missouri']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 6)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Tennessee']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 7)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Tennessee']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 7)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Kentucky']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 8)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Kentucky']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 8)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'West Virginia']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 9)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'West Virginia']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 9)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Virginia']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 10)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Virginia']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 10)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Maryland']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 11)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Maryland']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 11)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Delaware']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 4, col = 12)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Delaware']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 4, col = 12)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'California']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 2)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'California']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 2)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Arizona']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 3)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Arizona']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 3)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'New Mexico']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 4)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'New Mexico']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 4)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Oklahoma']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 5)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Oklahoma']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 5)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Arkansas']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 6)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Arkansas']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 6)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Mississippi']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 7)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Mississippi']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 7)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Alabama']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 8)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Alabama']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 8)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Georgia']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 9)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Georgia']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 9)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'South Carolina']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 10)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'South Carolina']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 10)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'North Carolina']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 5, col = 11)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'North Carolina']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 5, col = 11)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Texas']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 6, col = 5)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Texas']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 6, col = 5)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Louisiana']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 6, col = 6)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Louisiana']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 6, col = 6)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Florida']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 6, col = 9)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Florida']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 6, col = 9)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Alaska']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 8, col = 2)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Alaska']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 8, col = 2)
    
    grid.add_trace(go.Bar(x = [" "], y = combined_data.loc[combined_data['name'] == 'Hawaii']['Prison_CFR'], width = 0.3, marker_color = '#f13b3b'), row = 8, col = 4)
    grid.add_trace(go.Bar(x = ["  "], y = combined_data.loc[combined_data['name'] == 'Hawaii']['Mortality_Rate'], width= 0.3, marker_color = '#000000'), row = 8, col = 4)
    
    return grid


st.title('COVID-19 in US Prisons')
# CSS trick: https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/24, https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
#with open("style.css") as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


# Show grid map with Plotly
st.markdown('<h3>Grid Map</h3>', unsafe_allow_html = True)
st.plotly_chart(make_grid())


# Show bar chart with Plotly
st.markdown('<h3>Bar Chart</h3>', unsafe_allow_html = True)
bar_chart = go.Figure()
bar_chart.add_trace(go.Bar(
    x = combined_data['Prison_CFR'],
    y = combined_data['name'],
    orientation = 'h',
    name = 'In prisons',
    marker_color = '#f13b3b',
))
bar_chart.add_trace(go.Bar(
    x = combined_data['Mortality_Rate'],
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


# Show side-by-side comparison of case-fatality ratios with Streamlit
st.markdown('<h3>Side-by-Side Comparison</h3>', unsafe_allow_html = True)
st.write(combined_data)
st.markdown('Here, "Prison_CFR" refers to case-fatality ratios in US state prisons, calculated using total prisoner cases and total prisoner deaths from The Marshall Project\'s dataset (see below). "Mortality_Rate" refers to case-fatality ratios in US states, provided by JHU CSSE\'s dataset.')


# Show raw data with Streamlit
st.markdown('<h3>Raw Data</h3>', unsafe_allow_html = True)
as_of_date = datetime.strptime(COVID_DATA_URL[115:-4], '%m-%d-%Y').strftime('%B %d, %Y')
st.write('As of ' + as_of_date + '.')
st.markdown('<h4>COVID-19 in US State Prisons</h4>', unsafe_allow_html = True)
st.write(covid_prison_data)
st.markdown('[Data](https://github.com/themarshallproject/COVID_prison_data) from The Marshall Project, a nonprofit investigative newsroom dedicated to the U.S. criminal justice system.')
st.markdown('<h4>COVID-19 in US States</h4>', unsafe_allow_html = True)
st.write(covid_data)
st.markdown('[Data](https://github.com/CSSEGISandData/COVID-19) from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University. Here, "Mortality_Rate" refers to case-fatality ratio.')


# Explain epidemiological terms, potential problems
st.markdown('<h3>Epidemiological terms, caveats</h3>', unsafe_allow_html = True)
st.markdown('Case-fatality ratio is an epidemiological measure of mortality. A formula for case-fatality ratio is as follows: <i>number of recorded deaths * 100 / number of confirmed cases</i>.', unsafe_allow_html = True)
st.write('Some potential problems with these analyses include: (1) underreporting, whether deaths or cases, (2) at any given moment, the instantaneous numbers may not reflect the ultimate numbers (e.g. uncertainty regarding ultimate number of deaths).')


