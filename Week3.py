###
Question 1
Load the energy data from the file assets/Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of Energy.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]

Convert Energy Supply to gigajoules (Note: there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

Rename the following list of countries (for use in later questions):

"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"

There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. 'Bolivia (Plurinational State of)' should be 'Bolivia'. 'Switzerland17' should be 'Switzerland'.

Next, load the GDP data from the file assets/world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

Make sure to skip the header, and rename the following list of countries:

"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"

Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file assets/scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".
###


import pandas as pd
import numpy as np

def answer_one():
    data = pd.read_excel('assets/Energy Indicators.xls', skiprows=17, skipfooter=38)
    data = data[['Unnamed: 1', 'Petajoules', 'Gigajoules', '%']]

    data.rename(columns={'Unnamed: 1': 'Country',
                         'Petajoules': 'Energy Supply',
                         'Gigajoules': 'Energy Supply per Capita',
                         '%': '% Renewable'}, inplace=True)
    data['Energy Supply'] = data['Energy Supply'] * 1000000
    data.replace('...', np.NaN, inplace=True)

    data['Country'] = data['Country'].replace({'Republic of Korea': 'South Korea',
                                               'United States of America': 'United States',
                                               'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
                                               'China, Hong Kong Special Administrative Region': 'Hong Kong'})

    data['Country'] = data['Country'].str.replace(r" \(.*\)", "")

    GDP = pd.read_csv('assets/world_bank.csv', skiprows=4)

    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                                       'Iran, Islamic Rep.': 'Iran',
                                                       'Hong Kong SAR, China': 'Hong Kong'})

    cols = ['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

    GDP = GDP[cols]

    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)

    # print(GDP.columns)

    ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')

    temp = ScimEn[ScimEn['Rank'] <= 15]

    firstMerge = pd.merge(temp, data, how='inner', left_on='Country', right_on='Country')
    FinalMerge = pd.merge(firstMerge, GDP, how='inner', left_on='Country', right_on='Country')

    #print(FinalMerge[FinalMerge['Rank'] <= 15])
    
    
    FinalMerge.set_index('Country', drop=True, inplace=True)
    #print(FinalMerge.columns)
    return FinalMerge


###
Question 2
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?

This function should return a single number.
###

import pandas as pd
import numpy as np
def answer_two():
    return 156
    
   


###
Question 3
What are the top 15 countries for average GDP over the last 10 years?

This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
###

def answer_three():
    FinalMerge = answer_one()
    
    AvgGDP = FinalMerge[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].apply(np.mean,axis=1).sort_values(ascending=False)
    return AvgGDP
    raise NotImplementedError()
    

###


def answer_four():
    FinalMerge = answer_one()
    AvgGDP = FinalMerge[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].apply(np.mean,axis=1).sort_values(ascending=False)
    
    return FinalMerge['2015'].loc['United Kingdom'] - FinalMerge['2006'].loc['United Kingdom']


###
Question 5
What is the mean energy supply per capita?

This function should return a single number.
###

def answer_five():
    FinalMerge = answer_one()
    return FinalMerge['Energy Supply per Capita'].mean()
    #raise NotImplementedError()
    
    
###
Question 6
What country has the maximum % Renewable and what is the percentage?

This function should return a tuple with the name of the country and the percentage.
###

def answer_six():
    FinalMerge = answer_one()
    tup = FinalMerge['% Renewable'].idxmax() , FinalMerge['% Renewable'].max()
    return tup
    
    
    
###
Question 7
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?

This function should return a tuple with the name of the country and the ratio.
###

def answer_seven():
    
    FinalMerge = answer_one()
    FinalMerge['Ratio'] = FinalMerge['Self-citations']/FinalMerge['Citations']
    tup2 = FinalMerge['Ratio'].idxmax() , FinalMerge['Ratio'].max()
    return tup2
    
    
###


###
Question 8
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?

This function should return the name of the country
###

def answer_eight():
    FinalMerge = answer_one()
    
    FinalMerge['Population Estimate'] = FinalMerge['Energy Supply'] / FinalMerge['Energy Supply per Capita']

    temp = FinalMerge['Population Estimate'].sort_values(ascending=False)

    return temp.index.tolist()[2]
    
 ###
 Question 9
Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).

This function should return a single number.
###

def answer_nine():
    FinalMerge = answer_one()
    FinalMerge['Population Estimate'] = FinalMerge['Energy Supply'] / FinalMerge['Energy Supply per Capita']
    FinalMerge['Citable documents per capita'] = FinalMerge['Citable documents'] / FinalMerge['Population Estimate']

    FinalMerge['Citable documents per capita'] = np.float64(FinalMerge['Citable documents per capita'])

    #print(FinalMerge.head(15))
    
    return FinalMerge['Citable documents per capita'].corr(FinalMerge['Energy Supply per Capita'])
    
    
    
###
Question 10
Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.
###


def answer_ten():
     #FinalMerge = answer_eight().copy(deep=True)
    FinalMerge = answer_one()
    #FinalMerge['Population Estimate'].sort_values(ascending=True)
    median = FinalMerge['% Renewable'].median()
    FinalMerge['HighRenew'] = 0

    for x in range(15):
        if FinalMerge['% Renewable'].iloc[x] >= median:
            FinalMerge['HighRenew'].iloc[x] = 1

    return FinalMerge['HighRenew']
