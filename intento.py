# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:24:19 2022

@author: santi
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
url="/content/ModeloRegresionTec.csv"
df=pd.read_csv("MisDatosSolo.csv")
df.shape
df.boxplot()

def outliers(df,ft):
    Q1 = df[ft].quantile(0.25)
    Q3 = df[ft].quantile(0.75)
    IQR= Q3-Q1
    lower_bound = Q1 -1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    ls = df.index[ (df[ft] < lower_bound  )  | (df[ft] > upper_bound) ]
    
    return ls

index_list = []
for feature in ["Calorias", "Carbohidratos", "Lipidos", "Proteínas", "Sodio"]:
    index_list.extend(outliers(df, feature))

index_list
def remove(df, ls):
    ls = sorted(set(ls))
    df = df.drop(ls)
    return df
df_cleaned = remove(df, index_list)
df_cleaned.shape

df.shape
df_cleaned.boxplot()
modelo=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas+Sodio-1",data=df_cleaned).fit()
residuos=modelo.resid
print(residuos.describe())


index_list = []
for feature in ["Calorias", "Carbohidratos", "Lipidos", "Proteínas", "Sodio", ]:
    index_list.extend(outliers(df_cleaned, feature))

index_list

df_cleaned2 = remove(df_cleaned, index_list)
df_cleaned2.shape

df.shape
df_cleaned2.boxplot()
modelo2=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas+Sodio-1",data=df_cleaned2).fit()
residuos2=modelo2.resid
print(residuos2.describe())
