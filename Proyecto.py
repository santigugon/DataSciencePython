# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 17:21:20 2022

@author: santi
"""


import pandas as pd
import seaborn as sns #IMPORTAMOS LIBRERIA PARA GRAFICAS
import statsmodels.formula.api as sm
import numpy as np
import scipy.stats as st
from scipy.stats import anderson
from scipy.stats import shapiro
from scipy.stats import kstest
from statsmodels.stats.outliers_influence import variance_inflation_factor

df=pd.read_csv("MisDatosSolo.csv")
df.info()

print(df.corr());
modelo=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas+Sodio+Azucar-1",data=df).fit()
print(modelo.summary())
print(sns.heatmap(df.corr(),annot=True,cmap="hot"))
X= df[['Carbohidratos','Lipidos','Proteínas','Sodio','Azucar']]
variables=['Constant','Carbohidratos','Lipidos','Proteínas','Sodio','Azucar']
df['Constant']=1
Constante=df["Constant"]
dfX=pd.concat([Constante,X],axis=1)
for i in range(5):
    print(variables[i],variance_inflation_factor(dfX.values, i+1))
#print(variance_inflation_factor(dfX.values, 1))

sns.pairplot(df)

#LOS 4 Supuestos del error

residuos=modelo.resid
print(residuos.describe())