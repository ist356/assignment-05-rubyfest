import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here
'''
In the extract phase you pull your data from the internet and store it locally for further processing. This way you are not constantly accessing the internet and scraping data more than you need to. This also decouples the transformation logic from the logic that fetches the data. This way if the source data changes we don't need to re-implement the transformations. 

- For each file you extract save it in `.csv` format with a header to the `cache` folder. The basic process is to read the file, add lineage, then write as a `.csv` to the `cache` folder. 
- Extract the states with codes google sheet. Save as `cache/states.csv`
- Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
- For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`

After you've completed this part commit your changes to git, but DO NOT PUSH.'''

# Extract the states with codes google sheet. Save as `cache/states.csv`
state_file='https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv'
states=pd.read_csv(state_file)
states.to_csv('cache/states.csv',index=False)

# Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
file='https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv'
survey=pd.read_csv(file)
survey['year']=survey['Timestamp'].apply(pl.extract_year_mdy)
survey.to_csv('cache/survey.csv',index=False)

# For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`
years=survey['year'].unique()
for year in years:
    col_file=f'https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0'
    col=pd.read_html(col_file)
    col=col[1]
    col['year']=year
    col.to_csv(f'cache/col_{year}.csv',index=False)