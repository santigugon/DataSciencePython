# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 17:18:36 2022

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
from scipy.stats import anderson
import statsmodels.api as sm2
import statsmodels.stats.diagnostic as smd
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson


df=pd.read_csv("MisDatosSolo.csv")
df.info()
modelo=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas+Sodio-1",data=df).fit()
print(modelo.summary())


#Normalidad
residuos=modelo.resid
residuos.describe()#En esta parte comprobamos si los errores tienen una media de 0

sm2.qqplot(modelo.resid, fit=True , line="45")#Generamos un grafica para ver los errores comparados a una linea
residuos.hist()#Generamos histograma de los errores para poder observar si hay normlidad


#Normalidad
#Aqui tenemos tres de las pruebas que haremos para poder identificar si nuestro modelo tiene normalidad
print(shapiro(residuos))
print(kstest(residuos,"norm"),"\n")
print(anderson(residuos))



#Heterocedasticidad
plt.scatter(modelo.predict(),residuos)  #Aqui generamos el grafico usado para medir la varianza en nuestro modelo
plt.axhline(0, color="yellow")
plt.xlabel("Valores Predictivos")
plt.ylabel("Residuales")
breush_pagan_p = smd.het_breuschpagan(modelo.resid, modelo.model.exog)[1] #Declaramos el valor de breush pagan con la libreria
print("Aqui",breush_pagan_p) #Realizamos la prueba de breush pagan para ver si hay varianza constante en los errores

#Independencia de los errores
print(durbin_watson (modelo.resid))#Ponemos a prueba la independencia de los errores




#Realizamos estas lineas de codigo para poder generar una limpieza
l=residuos==residuos.max()

s=residuos.index[l]

print(s)
#sns.boxplot(df("Carbohidratos")) #Generamos nuestro grafico de caja de bigotes




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
#sns.boxplot(e)#Al graficar aun nos salen nuevos datos atipicos pero estos ya son en relacion a los nuevos datos, por lo tanto nuestros datos son correctos, por lo que podemos quedar satisfechos con nuestros nuevos datos
print(e)

#Valores=df.iloc[s]#Te muestra los datos eliminados


df2=df.drop(s,axis=0)
df2.info()

modelo2=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas+Sodio-1",data=df2).fit()
print(modelo2.summary())
residuos2=modelo2.resid


# modelo.predict(Valores)
residuos2.hist()
sm2.qqplot(modelo2.resid, fit=True , line="45")
#Normalidad
print(shapiro(residuos2))
print(kstest(residuos2,"norm"),"\n")
print(anderson(residuos2))


breush_pagan_p = smd.het_breuschpagan(modelo2.resid, modelo2.model.exog)[1]

#Grafica para la igualdad de la varianza
plt.scatter(modelo.predict(),residuos) 
plt.axhline(0, color="red")
plt.xlabel("Valores Predictivos")
plt.ylabel("Residuales")


#Prueba de breush pagan para verificar la igualdad de la varianza
print(breush_pagan_p)




print(durbin_watson (modelo2.resid)) #Prueba Durbin Watson con la cual determinamos la independencia de los errores



sns.pairplot(df2)#Grafico de dispersion para analizar la linealidad

#Limpieza de datos 2
def outliers(df,ft):
    Q1 = df[ft].quantile(0.25)
    Q3 = df[ft].quantile(0.75)
    IQR= Q3-Q1
    lower_bound = Q1 -1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    ls = df.index[ (df[ft] < lower_bound  )  | (df[ft] > upper_bound) ]
    
    return ls

index_list = []
for feature in ["Calorias", "Carbohidratos", "Lipidos", "Proteínas", "Sodio" ]:
    index_list.extend(outliers(df2, feature))

index_list
def remove(df, ls):
    ls = sorted(set(ls))
    df = df.drop(ls)
    return df

df_cleaned = remove(df2, index_list)
#df_cleaned.shape
#df_cleaned.boxplot()
modelo3=sm.ols(formula="Calorias~Carbohidratos+Lipidos+Proteínas-1",data=df_cleaned).fit()
residuos3=modelo3.resid
residuos3.describe()