# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 21:54:39 2022

@author: Alkan
"""

import pandas as pd
import numpy as np
import wbdata
import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns

#### DATA FOR COVID-19 CASES, POPULATION AND POPULATION DENSITY FROM OURWORLDINDATA

url = 'C:/Users/Alkan/.spyder-py3/owid-covid-data.csv'
df = pd.read_csv(url)
print(df.columns)
x = df[['location', 'date', 'total_cases', 'population', 'population_density']]
x = x.rename(columns={"location": "country"})
x1 = x[x['date'] == '2021-12-31'] ## Total cases are cumulative, so the last row is selected
print(x1)

##### DATA FOR DEMOCRACY INDEX of ECONOMIC INTELLIGENCE UNIT (eiu)

url2 = 'https://raw.githubusercontent.com/xmarquez/democracyData/master/data-raw/EIU%20Democracy%20Index%202020.csv'
df2 = pd.read_csv(url2)
democracy = df2[df2['year'] == 2019]
print(democracy.columns)
democracy = democracy.drop('year', axis=1)
print(democracy)
df1 = pd.merge(x1, democracy)
df1['infectionrate'] = df1['total_cases']/df1['population']
print(df1)
####### DATA FOR GINI INDEX FROM WORLD BANK DATA
url3 = 'C:/Users/Alkan/.spyder-py3/gini.csv'
gini = pd.read_csv(url3)
print(gini.head())
giniwb = gini[['country', 'giniWB']].dropna()

##### DATA FOR EDUCATION, GDP AND URBAN POPULATION FROM WB API
years = (datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 1))
indicators = {'SE.SEC.CMPT.LO.ZS': "SecondarySchoolCompletionRate", 'NY.GDP.PCAP.PP.KD': "GDP",
              'SP.URB.TOTL': 'Urbanpop'}
countries = wbdata.get_dataframe(indicators, country='all', data_date=years)
countries = countries.dropna()
countries = countries.reset_index()

countries.to_csv("C:/Users/Alkan/.spyder-py3/WorldBank.csv")

##### MERGE DATA
df2 = pd.merge(df1, countries)
print(df2)
df2.to_csv("C:/Users/Alkan/.spyder-py3/df2.csv")
df3=pd.merge(df2,giniwb)


sns.regplot(df2["SecondarySchoolCompletionRate"],df2['infectionrate'])
plt.clf()
df2['ln(infectionrate)'] = np.log(df2['infectionrate'])
df2['ln(SecondarySchoolCompletionRate'] = np.log(
    df2['SecondarySchoolCompletionRate'])

sns.regplot(df2['ln(SecondarySchoolCompletionRate'],df2['ln(infectionrate)'])
plt.clf()
df3.to_csv("C:/Users/Alkan/.spyder-py3/finaldata.csv")

### Taking log of the variables
x = np.log(df3[['SecondarySchoolCompletionRate', 'GDP',
            'eiu', 'Urbanpop', 'population_density','giniWB']])
y = np.log(df3['infectionrate'])



x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
print(model.summary())
print(model.resid)
print(model.params)
print(model.conf_int(alpha=0.05, cols=None))
plt.hist(model.resid)
plt.xlabel("residuals(model)")
plt.ylabel('frequency')
plt.title('Distribution of Residuals')
sm.qqplot(model.resid)
fig = plt.figure(figsize=(12, 8))

#to  produce regression plots
fig = sm.graphics.plot_regress_exog(
   model, 'SecondarySchoolCompletionRate', fig=fig)
sm.graphics.plot_regress_exog(model, 'SecondarySchoolCompletionRate',fig=fig)

from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

vifs = [vif(x.values, i) for i in range(len(x.columns))]
v=pd.DataFrame(data=vifs, index=x.columns)
v.columns=["VIFS"]
print(v)