# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:07:34 2021

@author: Alkan
"""

from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
url='https://raw.githubusercontent.com/carlson9/KocPythonFall2021/main/inclass/10ML/cses4_cut.csv'
df=pd.read_csv(url)
print(df.isnull().values.any())
X=df.drop(['voted','age'],axis=1)
Y=df['voted']
age=df['age'] #before replacing missing valuees with NaN I seperated age column since it does not contain any missing values
#to replace all the missing values with NaN (missing,refuse to answer,don't know)
x=X.replace([7,8,9,97,98,99,997,998,999,9997,9998,9999],np.NaN)
x=pd.concat([x,age],axis=1) 
print(x)
X1 = x.fillna(x.mode().iloc[0]) #replaced the NaN with most frequent value of each column
X2=X1[['age','D2002','D2003','D2012','D2020','D2025','D2031']]
X2=X2.copy()
X2[['D2002','D2012','D2031']]=X2[['D2002','D2012','D2031']].astype(str) #changed categorical variables to string
X2['D2003']=X2['D2003'].replace(96,0) #96 refers to non-educated, so I replacced it with 0 to put education level in an order
X3=X2.to_dict('records')
vec = DictVectorizer(sparse=True, dtype=int)
V=vec.fit_transform(X3)
X4=pd.DataFrame(V.toarray(), columns=vec.get_feature_names())
Xtrain, Xtest, ytrain, ytest = train_test_split(X4, Y)

from sklearn.naive_bayes import GaussianNB 
model = GaussianNB() 
model.fit(Xtrain, ytrain) 
y_model = model.predict(Xtest)
from sklearn.metrics import accuracy_score
print(accuracy_score(ytest, y_model))
print(confusion_matrix(ytest, y_model))

from sklearn.ensemble import RandomForestClassifier

rmodel=RandomForestClassifier()
rmodel.fit(Xtrain,ytrain)
ymodel=rmodel.predict(Xtest)
from sklearn.metrics import accuracy_score
print('Accuracy rate with Random Forest Classifier is ' + str(accuracy_score(ytest, ymodel)))
from sklearn.model_selection import GridSearchCV
parameters = dict(n_estimators = [100,300,500,800,1200], max_depth = [5, 8, 15, 25, 30],  
              min_samples_split = [2, 5, 10, 15, 100], 
             min_samples_leaf = [1, 2, 5, 10])



from sklearn.metrics import classification_report

gridmodelrf = GridSearchCV(rmodel, parameters, cv = 3,n_jobs=-1)
gridmodelrf.fit(Xtrain, ytrain)
grmodel=gridmodelrf.predict(Xtest)
print('After optimization: '+ str(accuracy_score(ytest, grmodel)))
print(gridmodelrf.best_params_)
print(classification_report(ytest,grmodel))
mat=confusion_matrix(ytest, grmodel)
print(mat)




from sklearn.svm import SVC

smodel=SVC()
smodel.fit(Xtrain, ytrain)
symodel=smodel.predict(Xtest)
svc_parameters=dict(C= [0.1, 1, 10, 100, 1000],
              gamma= [1, 0.1, 0.01, 0.001, 0.0001],
              kernel= ['rbf'])
gridmodelsvc = GridSearchCV(smodel, svc_parameters, cv = 3,n_jobs=-1)
gridmodelsvc.fit(Xtrain, ytrain)
svcmodel=gridmodelsvc.predict(Xtest)

print('Accuracy with SVC is: '+ str (accuracy_score(ytest, symodel)))

print(gridmodelsvc.best_params_)
print('After optimization: '+ str(accuracy_score(ytest, svcmodel)))
print(classification_report(ytest,svcmodel))
mat2=confusion_matrix(ytest, svcmodel)
print(mat2)

from sklearn.neighbors import KNeighborsClassifier
kmodel = KNeighborsClassifier()
kmodel.fit(Xtrain,ytrain)
kymodel=kmodel.predict(Xtest)
kn_parameters=dict(n_neighbors=[3,5,11,19,26,30,40,45,60,100],weights=['uniform','distance'],
                   metric=['euclidean','manhattan','cosine'])
print('Accuracy with KNeighbors is: '+str(accuracy_score(ytest, kymodel)))
gridmodelkn = GridSearchCV(kmodel, kn_parameters, cv = 3,n_jobs=-1)
gridmodelkn.fit(Xtrain, ytrain)

knmodel=gridmodelkn.predict(Xtest)
print(gridmodelkn.best_params_)
print('After optimization: ' + str(accuracy_score(ytest, knmodel)))
print(classification_report(ytest,knmodel))
mat3=confusion_matrix(ytest, knmodel)
print(mat3)

