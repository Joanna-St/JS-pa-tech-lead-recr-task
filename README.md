# World Happiness Dashboard

## Overview
The World Happiness Dashboard is an interactive web application built with Streamlit that visualizes global happiness trends using data collected by [Ipsos](https://ipsos.com) from 2015 to 2019. Users can explore different dimensions of happiness and social factors through various features, including line charts, scatter plots, and rankings.

## Features
- **Year Selection**: Choose a specific year or range of years to analyze data.
- **Country/Region Filtering**: Filter views by country or region.
- **Happiness Rankings**: Display top 10, bottom 10, and full rankings for a selected year.
- **Correlation Plots**: Visualize relationships between happiness scores and other socio-economic factors.
- **Interactive Charts**: Use Altair charts for dynamic interaction and detailed data exploration.
- **Customized Visual Appearance**: Includes company branding with custom themes and logos.

## Folder Structure
```
project/
├── .devcontainer/
│   └── devcontainer.json
├── .streamlit/
│   └── config.toml
├── data/
│   ├── 2015.csv
│   ├── 2016.csv
│   ├── 2017.csv
│   ├── 2018.csv
│   └── 2019.csv
├── resources/
│   └── static/
│       └── images/
│           └── Ipsos logo with transparent background.png
├── pycache/
│   └── data_processing.cpython-310.pyc
├── .gitignore
├── data_processing.py
├── LICENSE
├── README.md
├── requirements.txt
└── streamlit_app.py
```

## Installation

### Prerequisites
- Python 3.9 - 3.11
- Pip (Python package manager)

### Setup
1. **Clone the repository**
2. **Install dependencies:** pip install -r requirements.txt
3. **Run the application:** streamlit run streamlit_app.py


## Configuration
- The application uses a config.toml file for theme customization located in the .streamlit directory.
- The logo used in the application is located in resources/static/images.

## Local usage
- Launch the application using the terminal command provided in the setup section.
- Use the sliders and dropdowns to filter data by year, country, or region.
- Navigate through tabs to view various charts including line charts for trends and scatter plots for correlations

## Public link
https://js-world-happiness-mnn8egd2k76g6n9mwxm7in.streamlit.app/

## Acknowledgments
Data courtesy of Ipsos.

## Contact
For questions or feedback, please contact the project maintainer at joanna.stoyanova@ipsos.com.
