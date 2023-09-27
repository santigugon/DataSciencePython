# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 14:47:41 2022

@author: santi
"""

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as sm
import statsmodels.api as sm2
from scipy.stats import anderson
from scipy.stats import shapiro
from scipy.stats import kstest
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import statsmodels.stats.diagnostic as smd
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm2 
df=pd.read_csv("Bitacoracomida2.csv")


df.info()
modelo=sm.ols(formula="calorias~carbohidratos + lipidos + proteina", data=df).fit()
print(modelo.resid)
residuos=modelo.resid

Q1= residuos.quantile(0.25)
Q3= residuos.quantile(.75)
IQR=Q3-Q1
Maximum=Q3+1.5*IQR
Minimum=Q1-1.5*IQR

l=(residuos<Minimum)| (residuos>Maximum)

s=residuos.index[l]
e=residuos.drop(s, axis=0)

df2=df.drop(s,axis=0)
df2.info()

#sns.pairplot(df2, diag_kind="kde")
#sns.pairplot(df2)

modelo=sm.ols(formula="calorias~carbohidratos +lipidos+ proteina+sodio-1", data=df2).fit()
print(modelo.resid)
residuos=modelo.resid

print(residuos.describe())

#sm2.qqplot(residuos, fit=True , line="45")
print(anderson(residuos))
print(shapiro(residuos))
print(kstest(residuos,"norm"),"\n")
#residuos.hist()

plt.scatter(modelo.predict(),residuos) 
plt.axhline(0, color="yellow")
plt.xlabel("Valores Predictivos")
plt.ylabel("Residuales")

breush_pagan_p = smd.het_breuschpagan(modelo.resid, modelo.model.exog)[1]
print(breush_pagan_p)
print(durbin_watson (modelo.resid))

print(modelo.summary())



#Limpieza de datos 