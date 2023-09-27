# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:53:35 2022

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

import matplotlib.pyplot as plt

df=pd.read_csv("MisDatosSolo.csv")
df.info()
modelo=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas+Sodio-1",data=df).fit()
print(modelo.summary())



residuos=modelo.resid
print(shapiro(residuos))
print(kstest(residuos,"norm"),"\n")
print(residuos.max())
print(anderson(residuos))

l=residuos==residuos.max()

s=residuos.index[l]

print(s)
sns.boxplot(modelo.resid)

#Limpieza de datos parte 2
Q1 = residuos.quantile(0.25)#Generamos los quartiles 1 y 3
Q3 = residuos.quantile(0.75)
IQR= Q3-Q1#Formula para conocer lo que que abarcan estos cuartiles
Maximum = Q3 + 1.5 * IQR
Minimum = Q1 - 1.5 * IQR
residuos > Maximum #Si residuo mayor que el maximo
l=((residuos<Minimum) | (residuos > Maximum)) #Guardamos todos los errores en esta variablee que sean mayores al maximo o menos al minimo
print(type(l))
l.info()

s=residuos.index[l] #Buscamos indices de los errores    
s=list(s)
print(s)

e=residuos.drop(s,axis=0)#Eliminamos  los elementos de s en el eje x
sns.boxplot(e)#Al graficar aun nos salen nuevos datos atipicos pero estos ya son en relacion a los nuevos datos, por lo tanto nuestros datos son correctos, por lo que podemos quedar satisfechos con nuestros nuevos datos
print(e)
