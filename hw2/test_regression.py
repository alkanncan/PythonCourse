# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:37:58 2021

@author: Alkan

"""
import unittest
import LRegression
import pandas as pd


#Tests TypeError for columns including string


dictionary={'A':[1,2,'a',4,5],'B':[9,8,1,2,1]}
df=pd.DataFrame(dictionary)
print(df)
class regressionTest(unittest.TestCase):
   def test_input_value(self):
       with self.assertRaises(TypeError):
           LRegression.regression(df['A'], df['B'])
           
    