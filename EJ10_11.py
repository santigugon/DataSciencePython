# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:10:18 2022

@author: santi
"""

import pandas as pd
import seaborn as sns #IMPORTAMOS LIBRERIA PARA GRAFICAS
import statsmodels.formula.api as sm
import numpy as np
import scipy.stats as st
from statsmodels.stats.outliers_influence import variance_inflation_factor

url="https://reneshbedre.github.io/assets/posts/reg/bp.csv"#Cargamos la liga donde esta nuestra base de datos
df=pd.read_csv(url)
df.info()
print(df.describe())#Despliega toda la informacion estadistica
print(sns.heatmap(df.corr(),annot=True,cmap="Blues_r"))
modelo=sm.ols(formula=" Age~Weight+BSA+Dur+Pulse+Stress", data=df).fit()
r=modelo.rsquared
print(1/(1-r))#Este valor nos arroja el VIF para saber si existe un problema de multicolinealidad
modelo2=sm.ols(formula=" Weight~Age+BSA+Dur+Pulse+Stress", data=df).fit()
r2=modelo2.rsquared
print(1/(1-r2))
modelo3=sm.ols(formula=" BSA~Weight+Age+Dur+Pulse+Stress", data=df).fit()
r3=modelo3.rsquared
print(1/(1-r3))#NOS DA MAYOR QUE 2 MOSTRANDO UN GRAVE PROBLEMA DE MULTI...
#Tenemos 3 opciones, combinarlas, eliminarlas o buscar nuevos datos
df["Constant"]=1 #Agregamos una constante
X=df[['Age', 'Weight', 'BSA', 'Dur', 'Pulse', 'Stress']]#Creamos una variable conteniendo las sig. variables
Constante=df["Constant"]
dfX=pd.concat([Constante, X],axis=1)
print(dfX)
Constante=df["Constant"]

VIF=[]
for i in range(6):
    VIF.append(variance_inflation_factor(dfX.values,i+1))#CON ESTO REPRESENTAMOS EL VIF DE CADA VARIABLE
print(VIF) 
d={"Variables":['Age', 'Weight', 'BSA', 'Dur', 'Pulse', 'Stress'], "VIF":VIF}#Creamos un diccionario para guardar las variables,  y el VIF

ddf=pd.DataFrame(d)#transformarmos d en un DATAFRAME
print(ddf)#Al imprimirlo somos capaces de ver las variables y su respectivos VIF para poder tomar una decision sobre que debemos de hacer

df2=pd.read_csv("low_birth_weight_infants-1.txt", sep="\s+")
df2.info()
print(sns.heatmap(df2.corr(), annot=False, cmap=""))