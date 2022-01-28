# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 06:31:17 2022


@author: Alkan
"""

import pandas as pd
import numpy as np
import wbdata 
import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns

url3='C:/Users/Alkan/.spyder-py3/gini.csv'
gini=pd.read_csv(url3)
print(gini.head())
giniwb=gini[['country','giniWB']].dropna()



url='C:/Users/Alkan/.spyder-py3/owid-covid-data.csv'
df=pd.read_csv(url)
print(df.columns)
x=df[['location','date','total_cases','population','population_density']]
x = x.rename(columns={"location":"country"})
x1=x[x['date']=='2021-12-31']
print(x1)


url2='https://raw.githubusercontent.com/xmarquez/democracyData/master/data-raw/EIU%20Democracy%20Index%202020.csv'
df2=pd.read_csv(url2)
democracy=df2[df2['year']==2019]
print(democracy.columns)
democracy=democracy.drop('year',axis=1)
print(democracy)
df1=pd.merge(x1,democracy)
df1['infectionrate']=df1['total_cases']/df1['population']
print(df1)


years = (datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 1))
indicators = {'SE.TER.ENRR' :"SchoolEnrolment(tertiary)", 'NY.GDP.PCAP.PP.KD': "GDP",
              'SP.URB.TOTL':'Urbanpop'}
countries = wbdata.get_dataframe(indicators, country='all', data_date=years)
countries=countries.dropna()
countries=countries.reset_index()

print(countries)

df2=pd.merge(df1,countries)

print(df2)
df3=pd.merge(df2,giniwb)
sns.regplot(df2["SchoolEnrolment(tertiary)"],df2['infectionrate'])
plt.clf()
x=np.log(df3[['SchoolEnrolment(tertiary)','GDP','eiu','Urbanpop','population_density','giniWB']])
y=np.log(df3['infectionrate'])
df2['ln(infectionrate)']=np.log(df2['infectionrate'])
df2["ln(SchoolEnrolment(tertiary))"]=np.log(df2["SchoolEnrolment(tertiary)"])

sns.regplot(df2['ln(SchoolEnrolment(tertiary))'],df2['ln(infectionrate)'])
plt.clf()
x=sm.add_constant(x)
model3 = sm.OLS(y, x).fit()
print(model3.summary())
print(model3.resid)
print(model3.params)
print(model3.conf_int(alpha=0.05, cols=None))
plt.hist(model3.resid)
plt.xlabel("residuals(model)")
plt.ylabel('frequency')
plt.title('Distribution of Residuals (model3)')
sm.qqplot(model3.resid)
fig = plt.figure(figsize=(12,8))
sm.graphics.plot_regress_exog(model3, 'SchoolEnrolment(tertiary)', fig=fig)
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

vifs = [vif(x.values, i) for i in range(len(x.columns))]
v=pd.DataFrame(data=vifs, index=x.columns)
v.columns=["VIFS"]
print(v)