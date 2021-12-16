# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 19:02:03 2021

@author: Alkan
"""

import wbdata 
import datetime
import LRegression


print(wbdata.get_source())
print(wbdata.get_indicator(source=40))
print(wbdata.search_indicators('enrollment'))
print(wbdata.search_indicators('gdp'))
years = (datetime.datetime(2018, 1, 1), datetime.datetime(2018, 1, 1))
indicators = {"SP.DYN.LE00.IN":"lifeexpectancy", 'SE.SEC.ENRR' :"schoolenrollment", 'NY.GDP.PCAP.PP.KD': "GDP" }
lifeexp = wbdata.get_dataframe(indicators, country='all', data_date=years)
lifeexp.to_csv("C:/Users/Alkan/.spyder-py3/WBLifeexp.csv")
y=lifeexp['lifeexpectancy']
x=lifeexp[['schoolenrollment','GDP']]
LRegression.regression(y,x)