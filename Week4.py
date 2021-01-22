#Assignment 4
#Description
#In this assignment you must read in a file of metropolitan regions and associated sports teams from assets/wikipedia_data.html and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in assets/nfl.csv), MLB (baseball, in assets/mlb.csv), NBA (basketball, in assets/nba.csv or NHL (hockey, in assets/nhl.csv). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!

#For each sport I would like you to answer the question: what is the win/loss ratio's correlation with the population of the city it is in? Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with pearsonr, so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%*4=80%) of the grade for this assignment. You should only use data from year 2018 for your analysis -- this is important!

#Notes
#Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
#I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
#It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
#There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

import pandas as pd
import numpy as np
import scipy.stats as stats
import re


cities = pd.read_html("assets/wikipedia_data.html")[1]
df = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]



def nhl_correlation():
    df.rename(columns={"Population (2016 est.)[8]" : "Population"}, inplace=True)

    df['NFL'] = df['NFL'].str.replace(r"\[.*\]" , "")
    df['MLB'] = df['MLB'].str.replace(r"\[.*\]" , "")
    df['NBA'] = df['NBA'].str.replace(r"\[.*\]" , "")
    df['NHL'] = df['NHL'].str.replace(r"\[.*\]" , "")


    Pop = df[['Metropolitan area','Population','NHL']].copy()
    Pop['NHL'].replace('—',np.nan,inplace=True)
    Pop['NHL'].replace('',np.nan,inplace=True)
    Pop.dropna(subset=['NHL'],inplace=True)
    Pop['NHL'] = Pop['NHL'].str.replace('[\w.]*\ ',"")
    Pop['NHL'] = Pop['NHL'].replace(['RangersIslandersDevils'],'Devils')
    Pop.rename(columns={"NHL" : "team"}, inplace=True)

    NHL = pd.read_csv('assets/nhl.csv')
    NHL['team'] = NHL['team'].str.replace('[*]' , "")
    cols = ['team','W','L','year']
    NHL = NHL[cols]
    NHL = NHL[NHL['year'] == 2018]
    NHL.drop([0,9,18,26], inplace=True)
    NHL['W/L%'] = (NHL['W'].astype(float) / ((NHL['W'].astype(float) + NHL['L'].astype(float))))
    NHL['team'] = NHL['team'].str.replace('[\w.]*\ ' , "")
    #Adding all new york teams together and finding the average win/loss for all of them combined
    Wins = int(NHL[NHL['team'] == 'Rangers']['W'].values[0]) + int(NHL[NHL['team'] == 'Islanders']['W'].values[0]) + int(NHL[NHL['team'] == 'Devils']['W'].values[0])
    Loss = int(NHL[NHL['team'] == 'Rangers']['L'].values[0]) + int(NHL[NHL['team'] == 'Islanders']['L'].values[0]) + int(NHL[NHL['team'] == 'Devils']['L'].values[0])
    RangersIslandersDevils = {'team' : 'RangersIslandersDevils' ,
                       'W' : Wins,
                          'L' :Loss ,
                          'year' : '2018',
                          'W/L%' : float(Wins) / (float(Wins) + float(Loss))}

    NHL = NHL.append(RangersIslandersDevils,ignore_index=True)
    NHL.drop([14,15,12], inplace=True)

    Wins = int(NHL[NHL['team'] == 'Kings']['W'].values[0]) + int(NHL[NHL['team'] == 'Ducks']['W'].values[0])
    Loss = int(NHL[NHL['team'] == 'Kings']['L'].values[0]) + int(NHL[NHL['team'] == 'Ducks']['L'].values[0])

    KingsDucks = {'team' : 'KingsDucks' ,
                       'W' : Wins,
                          'L' :Loss ,
                          'year' : '2018',
                          'W/L%' : float(Wins) / (float(Wins) + float(Loss))}

    NHL = NHL.append(KingsDucks,ignore_index=True)
    NHL.drop([21,23], inplace=True)
    NHL.reset_index(inplace=True)
    del NHL['index']

    merge = pd.merge(NHL,Pop, how='outer' , on='team')
    #X = NHL[NHL['team'] == 'Rangers']['W'].values[0]
    X = merge[merge['team'] == 'Devils']['Metropolitan area'].values[0]
    Y = merge[merge['team'] == 'Devils']['Population'].values[0]
    #cities['NHL'] = cities['NHL'].replace(['RangersIslandersDevils'],'Devils')
    merge['Metropolitan area'] = merge['Metropolitan area'].replace(np.nan,X)
    merge['Population'] = merge['Population'].replace(np.nan,Y)
    merge.drop([28], inplace=True)

    merge = merge.astype({'W' : int,
                      'L' : int,
                      'Population':float,
                      'W/L%' : float})

    merge=merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})


    population_by_region = merge['Population']
    win_loss_by_region = merge['W/L%']
    

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
    #For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NBA using 2018 data.
    
    import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities = pd.read_html("assets/wikipedia_data.html")[1]
df = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]


def nba_correlation():
    
    Pop = df[['Metropolitan area','Population (2016 est.)[8]','NBA']].copy()
    Pop['NBA'] = Pop['NBA'].str.replace(r"\[.*\]" , "")
    Pop.rename(columns={'Population (2016 est.)[8]' : 'Population'}, inplace=True)
    Pop['NBA'].replace('—', np.nan, inplace=True)
    Pop['NBA'].replace('',np.nan,inplace=True)
    Pop.dropna(subset=['NBA'],inplace=True)
    Pop.rename(columns={'NBA' : 'team'}, inplace=True)
    Pop['team'].replace('Trail Blazers', 'Blazers', inplace=True)
    Pop.reset_index(inplace=True)
    del Pop['index']


    NBA = pd.read_csv('assets/nba.csv')
    NBA = NBA[['team','W','L','W/L%','year']]
    NBA = NBA[NBA['year']==2018]
    NBA['team'] = NBA['team'].str.replace(r'[\*]', '')
    NBA['team'] = NBA['team'].str.replace(r'\(\d*\)', '')
    NBA['team'] = NBA['team'].str.replace(r'[\xa0]', '')
    NBA['team'] = NBA['team'].str.replace('[\w.]* ', '')

    Wins = int(NBA[NBA['team'] == 'Knicks']['W'].values[0]) + int(NBA[NBA['team'] == 'Nets']['W'].values[0])
    Loss = int(NBA[NBA['team'] == 'Knicks']['L'].values[0]) + int(NBA[NBA['team'] == 'Nets']['L'].values[0])
    WLratio = float(Wins) / (float(Wins) + float(Loss))

    KnicksNets = {'team' : 'KnicksNets',
              'W' : Wins ,
              'L' : Loss,
              'W/L%' : WLratio,
              'year' : '2018'}

    Wins = int(NBA[NBA['team'] == 'Lakers']['W'].values[0]) + int(NBA[NBA['team'] == 'Clippers']['W'].values[0])
    Loss = int(NBA[NBA['team'] == 'Lakers']['L'].values[0]) + int(NBA[NBA['team'] == 'Clippers']['L'].values[0])
    WLratio = float(Wins) / (float(Wins) + float(Loss))

    LakersClippers = {'team' : 'LakersClippers',
              'W' : Wins ,
              'L' : Loss,
              'W/L%' : WLratio,
              'year' : '2018'}


    NBA = NBA.append(KnicksNets,ignore_index=True)
    NBA = NBA.append(LakersClippers,ignore_index=True)
    NBA.drop([10,11,24,25], inplace=True)
    NBA.reset_index(inplace=True)
    del NBA['index']

    merge = pd.merge(NBA,Pop, how='outer' , on='team')

    merge = merge.astype({'Population':float,
                      'W/L%' : float})

    merge=merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})
  
    
    population_by_region = merge['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = merge['W/L%'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
    #For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the MLB using 2018 data.
    
    import pandas as pd
import numpy as np
import scipy.stats as stats
import re

#mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
df=cities.iloc[:-1,[0,3,5,6,7,8]]
    

def mlb_correlation(): 
   
    Pop = df[['Metropolitan area','Population (2016 est.)[8]','MLB']].copy()
    Pop['MLB'] = Pop['MLB'].str.replace(r"\[.*\]" , "")
    Pop.rename(columns={'Population (2016 est.)[8]' : 'Population'}, inplace=True)
    Pop['MLB'].replace('—', np.nan, inplace=True)
    Pop['MLB'].replace('',np.nan,inplace=True)
    Pop.dropna(subset=['MLB'], inplace=True)
    Pop.rename(columns={'MLB' : 'team'}, inplace=True)
    Pop.replace(['CubsWhite Sox'], 'CubsWhiteSox', inplace=True)
    Pop.replace(['Red Sox'], 'Sox', inplace=True)
    Pop.replace(['Blue Jays'], 'Jays', inplace=True)


    MLB = pd.read_csv('assets/mlb.csv')
    MLB = MLB[['team','W','L','W-L%','year']]
    MLB = MLB[MLB['year'] == 2018]
    Wins = int(MLB[MLB['team'] == 'New York Yankees']['W'].values[0]) + int(MLB[MLB['team'] == 'New York Mets']['W'].values[0])
    Loss = int(MLB[MLB['team'] == 'New York Yankees']['L'].values[0]) + int(MLB[MLB['team'] == 'New York Mets']['L'].values[0])
    WLratio = float(Wins) / (float(Wins) + float(Loss))

    YankeesMets = {'team' : 'YankeesMets',
              'W' : Wins ,
              'L' : Loss,
              'W-L%' : WLratio,
              'year' : '2018'}

    MLB = MLB.append(YankeesMets,ignore_index=True)

    Wins = int(MLB[MLB['team'] == 'Los Angeles Dodgers']['W'].values[0]) + int(MLB[MLB['team'] == 'Los Angeles Angels']['W'].values[0])
    Loss = int(MLB[MLB['team'] == 'Los Angeles Dodgers']['L'].values[0]) + int(MLB[MLB['team'] == 'Los Angeles Angels']['L'].values[0])
    WLratio = float(Wins) / (float(Wins) + float(Loss))

    DodgersAngels = {'team' : 'DodgersAngels',
              'W' : Wins ,
              'L' : Loss,
              'W-L%' : WLratio,
              'year' : '2018'}

    MLB = MLB.append(DodgersAngels,ignore_index=True)

    Wins = int(MLB[MLB['team'] == 'San Francisco Giants']['W'].values[0]) + int(MLB[MLB['team'] == 'Oakland Athletics']['W'].values[0])
    Loss = int(MLB[MLB['team'] == 'San Francisco Giants']['L'].values[0]) + int(MLB[MLB['team'] == 'Oakland Athletics']['L'].values[0])
    WLratio = float(Wins) / (float(Wins) + float(Loss))

    GiantsAthletics = {'team' : 'GiantsAthletics',
              'W' : Wins ,
              'L' : Loss,
              'W-L%' : WLratio,
              'year' : '2018'}

    MLB = MLB.append(GiantsAthletics,ignore_index=True)

    Wins = int(MLB[MLB['team'] == 'Chicago White Sox']['W'].values[0]) + int(MLB[MLB['team'] == 'Chicago Cubs']['W'].values[0])
    Loss = int(MLB[MLB['team'] == 'Chicago White Sox']['L'].values[0]) + int(MLB[MLB['team'] == 'Chicago Cubs']['L'].values[0])
    WLratio = float(Wins) / (float(Wins) + float(Loss))

    CubsWhiteSox = {'team' : 'CubsWhiteSox',
              'W' : Wins ,
              'L' : Loss,
              'W-L%' : WLratio,
              'year' : '2018'}

    MLB = MLB.append(CubsWhiteSox,ignore_index=True)
    MLB = MLB.drop([1,18,25,28,11,21,8])
    MLB['team'] = MLB['team'].str.replace(r'[\*]', '')
    MLB['team'] = MLB['team'].str.replace(r'\(\d*\)', '')
    MLB['team'] = MLB['team'].str.replace(r'[\xa0]', '')
    MLB['team'] = MLB['team'].str.replace('[\w.]* ', '')
    MLB.reset_index(inplace=True)
    del MLB['index']

    merge = pd.merge(MLB,Pop, how='outer' , on='team')
    merge = merge.astype({'Population':float,
                      'W-L%' : float})
    merge=merge.groupby('Metropolitan area').agg({'W-L%': np.nanmean, 'Population': np.nanmean})
    
    population_by_region = merge['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = merge['W-L%'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
    #For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NFL using 2018 data.
    
    import pandas as pd
import numpy as np
import scipy.stats as stats
import re

#nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
df=cities.iloc[:-1,[0,3,5,6,7,8]]

def nfl_correlation(): 
    Pop = df[['Metropolitan area','Population (2016 est.)[8]','NFL']].copy()
    Pop['NFL'] = Pop['NFL'].str.replace(r"\[.*\]" , "")
    Pop['NFL'].replace("—",np.nan,inplace=True)
    Pop['NFL'].replace("",np.nan,inplace=True)
    Pop['NFL'].replace("— ",np.nan,inplace=True)
    Pop.dropna(inplace=True)
    Pop.rename(columns={'Population (2016 est.)[8]' : 'Population'}, inplace=True)
    Pop.rename(columns={'NFL' : 'team'}, inplace=True)


    NFL=pd.read_csv('assets/nfl.csv')
    NFL=NFL[['W-L%','team','year']]
    NFL=NFL[NFL['year']==2018]
    NFL.drop([0,5,10,15,20,25,30,35], inplace=True)
    NFL['team'] = NFL['team'].str.replace(r'[\*]', '')
    NFL['team'] = NFL['team'].str.replace(r'[\+]', '')
    NFL['team'] = NFL['team'].str.replace(r'\(\d*\)', '')
    NFL['team'] = NFL['team'].str.replace(r'[\xa0]', '')
    NFL['team'] = NFL['team'].str.replace('[\w.]* ', '')

    Wins = float(NFL[NFL['team'] == 'Giants']['W-L%'].values[0]) + float(NFL[NFL['team'] == 'Jets']['W-L%'].values[0])
    WLratio = Wins/2

    GiantsJets = {'team' : 'GiantsJets',
              'W-L%' : WLratio,
              'year' : '2018'}

    NFL = NFL.append(GiantsJets,ignore_index=True)

    Wins = float(NFL[NFL['team'] == 'Rams']['W-L%'].values[0]) + float(NFL[NFL['team'] == 'Chargers']['W-L%'].values[0])
    WLratio = Wins/2

    RamsChargers = {'team' : 'RamsChargers',
              'W-L%' : WLratio,
              'year' : '2018'}

    NFL = NFL.append(RamsChargers,ignore_index=True)

    Wins = float(NFL[NFL['team'] == '49ers']['W-L%'].values[0]) + float(NFL[NFL['team'] == 'Raiders']['W-L%'].values[0])
    WLratio = Wins/2

    ersRaiders = {'team' : '49ersRaiders',
              'W-L%' : WLratio,
              'year' : '2018'}

    NFL = NFL.append(ersRaiders,ignore_index=True)
    NFL.drop([19,3,28,13,30,15], inplace=True)
    NFL.reset_index(inplace=True)
    del NFL['index']

    merge = pd.merge(NFL,Pop, how='outer' , on='team')
    merge = merge.astype({'Population':float,
                      'W-L%' : float})
    merge=merge.groupby('Metropolitan area').agg({'W-L%': np.nanmean, 'Population': np.nanmean})
    #raise NotImplementedError()
    
    population_by_region = merge['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = merge['W-L%'] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
