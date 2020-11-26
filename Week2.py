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
