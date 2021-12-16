# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 13:42:40 2021

@author: Alkan
"""
import pandas as pd
import numpy as np
import scipy.stats





def regression(dependent,independent):
##### To drop NaN values
    x=pd.DataFrame(independent)
    y=pd.DataFrame(dependent)
    dd=pd.concat([y,x],axis=1)
    ddp=dd.dropna()   
    x=ddp[x.columns]
    y=ddp[y.columns]

#####Matrix calculations
    x['constant']=1
    xm=np.array(x)
    ss=len(xm) #samplesize
    predictors=len(xm[1]) #number of predictors including "constant"
    xmt=xm.transpose()
    ym=np.array(y)
    beta=[]
    beta=np.dot(np.linalg.inv(np.dot(xmt,xm)),np.dot(xmt,ym))
    yhat=np.dot(xm,beta)
    e=ym-yhat
    et=e.transpose()
    mse=(np.dot(et,e))/(ss-predictors)
    var=mse*np.linalg.inv(np.dot(xmt,xm))
    diagonal=np.diagonal(var)
    se=np.sqrt(diagonal) #standart error for slope 
    betat=beta.transpose() ##### for element-wise calculations
    tvalues=betat/se
    criticalt=scipy.stats.t.ppf(q=1-0.05,df=ss-predictors)
    ME=criticalt*se #Margin of error
    credibleintr=betat+ME
    credibleintl=betat-ME
    credibleint=[] 
    for i in range(len(xm[1])):
        credibleint.append((str(credibleintl[:,i])+'-'+str(credibleintr[:,i])))
    
    ######## To Print Result
    table={'D':[],'IV':[],'Slope':[],'SE':[],'t':[],'CI':[],'criticalt':[]}
    for i in y.columns:
        table['D'].append(str(i))
    for i in x.columns:
        table['IV'].append(str(i))
    for i in beta:
        table['Slope'].append(str(i))
    for i in credibleint:
        table['CI'].append(str(i))
    for i in se:
        table['SE'].append(str(i))
    for i in tvalues:
        table['t'].append(str(i))
    table['criticalt']=criticalt
    print(str('Dependent Variables:'+str(table['D'])+
  '\nIndependent Variables:'+str(table['IV'])+'\nSlope Coefficients:'+str(table['Slope'])+
       '\nStandart Errors:'+str(table['SE'])+'\ntstats:'+str(table['t'])+
       '\nCredible Intervals(0.95):'+str(table['CI'])+'\nt value for 0.95:'+str(table['criticalt'])))