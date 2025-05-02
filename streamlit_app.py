import streamlit as st
import altair as alt
import data_processing

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='World Happiness Dashboard',
    page_icon='resources\static\images\Ipsos logo with transparent background.png', 
)

# -----------------------------------------------------------------------------
# Declare some useful functions.
def compute_region_averages(df):
    '''
    Calculates average scores per region per year.
    '''
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if 'Year' in numeric_cols:
        numeric_cols.remove('Year')

    region_agg_df = df.groupby(['Region', 'Year'])[numeric_cols].mean().reset_index()
    return region_agg_df

# Get the data you're going to visualise
happiness_df = data_processing.get_happiness_data('data')
min_value = happiness_df['Year'].min()
max_value = happiness_df['Year'].max()

# -----------------------------------------------------------------------------

# Title
'''
# :earth_africa: World Happiness Dashboard

Embark on a journey through global happiness trends with data collected by [Ipsos](https://ipsos.com/) from 2015 to 2019, uncovering insights and stories behind the smiles around the world.
'''
''
''

# ------------------------Score over time Start
st.header('Country/Region Happiness Score over Time', divider='gray')
''

# Year slider
from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])
''

# Country or Region filtering
filter_choice = st.radio(
    "Filter by:",
    ('Country', 'Region')
)
''

if filter_choice == 'Country':
    countries = sorted(happiness_df['Country'].unique())
    selected_options = st.multiselect(
        'Select countries',
        countries,
        ['Germany', 'France', 'United Kingdom', 'Canada', 'Chile', 'South Korea']
    )
elif filter_choice == 'Region':
    regions = sorted(happiness_df['Region'].unique())
    selected_options = st.multiselect(
        'Select regions:',
        regions,
        ['Western Europe', 'Eastern Asia', 'North America']
    )
''
''

if filter_choice == 'Country':
    filtered_df = happiness_df[
        (happiness_df['Country'].isin(selected_options))
        & (happiness_df['Year'] <= to_year)
        & (from_year <= happiness_df['Year'])
    ]
elif filter_choice == 'Region':
    region_df = compute_region_averages(happiness_df)
    filtered_df = region_df[
        (region_df['Region'].isin(selected_options))
        & (region_df['Year'] <= to_year)
        & (from_year <= region_df['Year'])
    ]

# Converting Year to string, otherwise it looks super wonky in the chart
filtered_df['Year'] = filtered_df['Year'].astype(str)

# Visualising
st.line_chart(
    filtered_df,
    x='Year',
    y='Happiness Score',
    color=filter_choice
)
''
''
# ------------------------Score over time Start

# ------------------------Correlations Start
st.header('Happiness and the Wider Societal Context', divider='gray')
''

selected_year = st.slider(
    'Select a year:',
    min_value=min_value,
    max_value=max_value,
    value=min_value,
    step=1
)
''

factors = ["GDP per Capita", "Life Expectancy", "Freedom", "Trust in Government", "Generosity"]
target = "Happiness Score"

filtered_df = happiness_df[happiness_df['Year'] == selected_year]

tabs = st.tabs(factors)

for tab, factor in zip(tabs, factors):
    with tab:
        scatter_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x=alt.X(factor, scale=alt.Scale(zero=False)),
            y=alt.Y(target, scale=alt.Scale(zero=False)),
            color=alt.Color('Happiness Rank').scale(scheme="yellowgreenblue"),
            tooltip=["Country", target, factor]
        ).properties(
            width=600,
            height=300,
            title=f"{factor} vs. {target} ({selected_year})"
        ).interactive()

        st.altair_chart(scatter_chart, use_container_width=True)
''

st.markdown("""
**Correlation Insights: Factors Influencing Happiness**

The analysis of global happiness data over several years reveals interesting insights:

- **GDP per Capita** and **Life Expectancy** show the strongest correlations with happiness scores, underscoring the significance of economic prosperity and health as primary determinants of happiness. These factors suggest that material well-being and longevity contribute positively to people's overall happiness.

- **Freedom** presents a moderate correlation with happiness, highlighting the role of personal and political liberties in enhancing individuals' life satisfaction. This indicates that having the freedom to make personal choices contributes appreciably to happiness.

- **Trust in Government** and **Generosity** are less closely correlated with happiness scores, suggesting that these factors may be influenced by regional and cultural variations. While these elements are important, their impact on happiness is not as pronounced as economic and health factors.
""")
''

# ------------------------Correlations End

# ------------------------Ranking Start
st.header(f'Happiness Rankings in {selected_year}', divider='gray')
''

filtered_df = happiness_df[happiness_df['Year'] == selected_year]

tab1, tab2, tab3 = st.tabs(["Top 10", "Bottom 10", "Full Ranking"])

chart1 = alt.Chart(filtered_df.sort_values('Happiness Rank', ascending=True).head(10)).mark_bar().encode(
    x='Happiness Score',
    y=alt.Y('Country', sort='-x'),
    color=alt.Color('Happiness Rank').scale(scheme="yellowgreenblue")
).interactive()

chart2 = alt.Chart(filtered_df.sort_values('Happiness Rank', ascending=False).head(10)).mark_bar().encode(
    x='Happiness Score',
    y=alt.Y('Country', sort='x'),
    color=alt.Color('Happiness Rank').scale(scheme="yellowgreenblue"),
).interactive()


# chart3 = alt.Chart(filtered_df.sort_values('Happiness Rank', ascending=False)).mark_bar().encode(
#     x='Happiness Score',
#     y=alt.Y('Country', sort='-x'),
#     color=alt.Color('Happiness Rank').scale(scheme="yellowgreenblue")
# ).interactive()

tab1.altair_chart(chart1)
''

tab2.altair_chart(chart2)
''

with tab3:
    rankings_df = filtered_df[['Country', 'Happiness Score', 'Happiness Rank']].sort_values('Happiness Rank')
    rankings_df.set_index('Happiness Rank', inplace=True)
    st.dataframe(rankings_df, height=250, use_container_width=True)

# ------------------------Ranking End

# Footer
footer_html = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        color: white;
        text-align: center;
        padding: 10px;
        background-color: #31333F;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        © 2016 - 2025 Ipsos All Rights Reserved
    </div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
