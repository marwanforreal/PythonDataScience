#Write a function called proportion_of_education which returns the proportion of children in the dataset who had a mother with the education levels equal to less than high school (<12), high school (12), more than high school but not a college graduate (>12) and college degree.

#This function should return a dictionary in the form of (use the correct numbers, do not round numbers):

  #  {"less than high school":0.2,
   #"high school":0.4,
    #"more than high school but not college":0.2,
    #"college":0.2}

    #SOLUTION
    import pandas as pd
def proportion_of_education():
    #x=y=z=t=0

    data = pd.read_csv('assets/NISPUF17.csv')
    S = pd.Series(data['EDUC1'])

    sum = len(S)
    
    x = data[data['EDUC1'] == 1]
    y = data[data['EDUC1'] == 1]
    z = data[data['EDUC1'] == 1]
    t = data[data['EDUC1'] == 1]

#print(len(h))

#for index,value in S.items():
    #if value == 1 :
        #x+=1
    #elif value == 2 :
        #y+=1
    #elif value == 3:
        #z+=1
    #else:
        #t+=1

    myDict={"less than high school" : x/sum,
            "high school" : y/sum,
            "more than high school but not college" : z/sum,
            "college" : t/sum}
    return myDict
  
  
  #question TWO
  
 # Question 2
#Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza vaccine from a healthcare provider. Return a tuple of the average number of influenza vaccines for those children we know received breastmilk as a child and those who know did not.

#This function should return a tuple in the form (use the correct numbers:

#(2.5, 0.1)

import pandas as pd

data = pd.read_csv('datafile.csv')

BR=data.loc[data['CBF_01']==1]
NoBR=data.loc[data['CBF_01']==2]

x=BR['P_NUMFLU'].mean()
y=NoBR['P_NUMFLU'].mean()

result=(x,y)

#question THREE
#Question 3
#It would be interesting to see if there is any evidence of a link between vaccine effectiveness and sex of the child. Calculate the ratio of the number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose) versus those who were vaccinated but did not contract chicken pox. Return results by sex.

#This function should return a dictionary in the form of (use the correct numbers):

 #   {"male":0.2,
  #  "female":0.4}
#Note: To aid in verification, the chickenpox_by_sex()['female'] value the autograder is looking for starts with the digits 0.0077.

import pandas as pd


data = pd.read_csv('datafile.csv')

Q = data[['SEX','P_NUMVRC','HAD_CPOX']]
X = data['HAD_CPOX']

MalesVacWithCPOX = data.loc[(data['SEX']==1) & (data['P_NUMVRC'] > 0) & (data['HAD_CPOX'] == 1)]
MalesVacNoCPOX = data.loc[(data['SEX']==1) & (data['P_NUMVRC'] > 0) & (data['HAD_CPOX'] == 2)]

FeVacWithCPOX = data.loc[(data['SEX']==2) & (data['P_NUMVRC'] > 0) & (data['HAD_CPOX'] == 1)]
FeVacNoCPOX = data.loc[(data['SEX']==2) & (data['P_NUMVRC'] > 0) & (data['HAD_CPOX'] == 2)]

x = len(MalesVacWithCPOX.index)/len(MalesVacNoCPOX.index)

y = len(FeVacWithCPOX.index)/len(FeVacNoCPOX.index)

#print(len(FeVacNoCPOX.index)/len(FeVacWithCPOX.index))
#print(len(MalesVacNoCPOX.index)/len(MalesVacWithCPOX.index))

myDict={'male' : x,
        'female': y}

#print(myDict)

#print(MalesVacWithCPOX[['SEX','P_NUMVRC','HAD_CPOX']])

#questionFOUR


#Question 4
#A correlation is a statistical relationship between two variables. If we wanted to know if vaccines work, we might look at the correlation between the use of the vaccine and whether it results in prevention of the infection or disease [1]. In this question, you are to see if there is a correlation between having had the chicken pox and the number of chickenpox vaccine doses given (varicella).

#Some notes on interpreting the answer. The had_chickenpox_column is either 1 (for yes) or 2 (for no), and the num_chickenpox_vaccine_column is the number of doses a child has been given of the varicella vaccine. A positive correlation (e.g., corr > 0) means that an increase in had_chickenpox_column (which means more no’s) would also increase the values of num_chickenpox_vaccine_column (which means more doses of vaccine). If there is a negative correlation (e.g., corr < 0), it indicates that having had chickenpox is related to an increase in the number of vaccine doses.

#Also, pval is the probability that we observe a correlation between had_chickenpox_column and num_chickenpox_vaccine_column which is greater than or equal to a particular value occurred by chance. A small pval means that the observed correlation is highly unlikely to occur by chance. In this case, pval should be very small (will end in e-18 indicating a very small number).

#[1] This isn’t really the full picture, since we are not looking at when the dose was given. It’s possible that children had chickenpox and then their parents went to get them the vaccine. Does this dataset have the data we would need to investigate the timing of the dose?

import scipy.stats as stats
import numpy as np
import pandas as pd

data = pd.read_csv('datafile.csv')

# this is just an example dataframe
CP = data[['HAD_CPOX','P_NUMVRC']].copy()
CP.dropna(subset=['P_NUMVRC'],inplace=True)
#print(CP)
HadCP=CP.loc[(data['HAD_CPOX']<=2)]
#print(HadCP)
#print(HadCP[['HAD_CPOX','P_NUMVRC']].dropna().head())
# here is some stub code to actually run the correlation
corr, pval = stats.pearsonr(HadCP['P_NUMVRC'], HadCP['HAD_CPOX'])

print(corr)
