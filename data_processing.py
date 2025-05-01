import streamlit as st
import pandas as pd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def get_happiness_data(data_folder):
    csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

    dfs = []

    # Standardize the column names
    column_mapping = {
        'Country or region': 'Country',
        'Happiness.Score': 'Happiness Score',
        'Score': 'Happiness Score',
        'Happiness.Rank': 'Happiness Rank',
        'Overall rank': 'Happiness Rank',
        'Economy (GDP per Capita)': 'GDP per Capita',
        'Economy..GDP.per.Capita.': 'GDP per Capita',
        'GDP per capita': 'GDP per Capita',
        'Health (Life Expectancy)': 'Life Expectancy',
        'Health..Life.Expectancy.': 'Life Expectancy',
        'Healthy life expectancy': 'Life Expectancy',
        'Freedom to make life choices' : 'Freedom',
        'Trust (Government Corruption)': 'Trust in Government',
        'Trust..Government.Corruption.': 'Trust in Government',
        'Perceptions of corruption': 'Trust in Government',
        'Dystopia.Residual': 'Dystopia Residual'
    }

    # Standardize the country names
    country_mapping = {
        'Hong Kong S.A.R., China': 'Hong Kong',
        'Macedonia': 'North Macedonia',
        'North Cyprus': 'Northern Cyprus',
        'Somaliland region': 'Somaliland Region',
        'Taiwan Province of China': 'Taiwan',
        'Trinidad & Tobago': 'Trinidad and Tobago'
    }

    for csv_file in csv_files:
        file_path = os.path.join(data_folder, csv_file)
        df = pd.read_csv(file_path)
        
        # Rename columns based on the mapping
        df.rename(columns=column_mapping, inplace=True)

        # Apply country name mapping
        df['Country'] = df['Country'].replace(country_mapping)
        
        # Get the year based on file name
        year = int(csv_file.split('.')[0])
        df['Year'] = year

        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)

    # Region mapping (we don't have that info in all years)
    region_mapping = dict(
        merged_df[merged_df['Year'].isin([2015, 2016])]
        [['Country', 'Region']].drop_duplicates().values
    )

    merged_df['Region'] = merged_df['Country'].map(region_mapping)

    # Gambia had no info, so assigning manually
    merged_df.loc[merged_df['Country'] == 'Gambia', 'Region'] = 'Sub-Saharan Africa'

    return merged_df