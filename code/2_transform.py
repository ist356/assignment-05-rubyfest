import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

'''The bulk of the work is done in the transform process. Here we read our data from the cache back into pandas. From there we will clean the data, engineer new columns, join datasets together, etc all on route to producing a dataset from which we can create the reports. In the final transformation step, we write the reports back to the cache. 



**1. First load the data from the cache:**

- Load the states and survey data from the cache into dataframes. `states_data` and `survey_data`
- create a unique list of years from the survey data
- For each year in the survey data, load the cost of living data from the cache into a dataframe, then combine all the dataframes into a single cost of living (COL) dataframe `col_data`
'''
states_data=pd.read_csv('cache/states.csv')
survey_data=pd.read_csv('cache/survey.csv')
years=survey_data['year'].unique()
col_data=pd.concat([pd.read_csv(f'cache/col_{year}.csv') for year in years])
#print(col_data.head())

'''
**2. Merge the survey data with the cost of living data:**

Next, we want to join the `survey_data` with the `col_data` matching on year and city. The problem is the city formats of both datasets are different. Thereore to match "Seattle, WA, United States" from the `col_data` to the `survey_data`, we will need to clean-up and engineer several columns. 

- First, clean the entry under "Which country do you work in?" so that all US countries say "United States" use the `clean_country_usa` function in `pandaslib.py` function here and generate a new column `_country`
- Next under the "If you're in the U.S., what state do you work in?" column we need to convert the states into state codes Example: "New York => NY" to do this, join the states dataframe to the survey dataframe. User and inner join to drop non-matches. Call the new dataframe `survey_states_combined`
- Engineer a new column consisting of the city, a comma, the 2-character state abbreviation, another comma and `_country` For example: "Syracuse, NY, United States". name this column `_full_city`
- create the dataframe `combined` by matching the `survey_states_combined` to cost of living data matching on the `year` and `_full_city` columns
'''
survey_data['_country']=survey_data['What country do you work in?'].apply(pl.clean_country_usa)
survey_states_combined=pd.merge(survey_data,states_data,left_on="If you're in the U.S., what state do you work in?",right_on='State',how='inner')
#removes any part of a string once there is a comma or parenthesis
survey_states_combined['City']=survey_states_combined['What city do you work in?'].str.replace(r',.*|\(.*\)', '', regex=True)
survey_states_combined['_full_city']=survey_states_combined['City']+', '+survey_states_combined['Abbreviation']+', '+survey_states_combined['_country']
combined=pd.merge(survey_states_combined,col_data,left_on=['year','_full_city'],right_on=['year','City'],how='inner')


'''
**3. Normalize the annual salary based on cost of living:**

Finally we want to normalize each annual salary based on cost of living. How do you do this? A COL 90 means the cost of living is 90% of the average, so $100,000 in a COL city of 90 is the equivalent buying power of(100/90) * $100,000 ==  $111,111.11 

- Clean the salary column so that its a float. Use `clean_currency` function in `pandaslib.py`. generate a new column `__annual_salary_cleaned`
- generate a column `_annual_salary_adjusted` based on this formula. 
'''

combined['_annual_salary_cleaned']=combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
combined['_annual_salary_adjusted']=combined.apply(lambda row: row['_annual_salary_cleaned']*(100/row['Cost of Living Index']),axis=1)


'''
**4. Dataset is engineered, time to produce the reports:**

At this point you have engineerd the dataset required to produce the necessary reports.

- Save the engineered dataset to the cache `survey_dataset.csv`
- create the first report to show a pivot table of the the average `_annual_salary_adjusted` with `_full_city` in the row and Age band (How old are you?) in the column. Save this back to the cache as `annual_salary_adjusted_by_location_and_age.csv`
- create a similar report but show highest level of education in the column. Save this back to the cache as `annual_salary_adjusted_by_location_and_education.csv`
'''
combined.to_csv('cache/survey_dataset.csv',index=False)
sal_city_age=combined.pivot_table(index='_full_city',columns='How old are you?',values='_annual_salary_adjusted',aggfunc='mean')
sal_city_edu=combined.pivot_table(index='_full_city',columns='What is your highest level of education completed?',values='_annual_salary_adjusted',aggfunc='mean')

sal_city_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')
sal_city_edu.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')
#st.dataframe(sal_city_age)
#st.dataframe(sal_city_edu)

'''
st.dataframe(states_data)
st.dataframe(survey_data)
st.dataframe(col_data)
st.dataframe(survey_states_combined)
st.dataframe(combined)
'''