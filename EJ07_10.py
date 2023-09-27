# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 17:17:48 2022

@author: santi
"""

import pandas as pd
import seaborn as sns #IMPORTAMOS LIBRERIA PARA GRAFICAS
import statsmodels.formula.api as sm
import statsmodels.api as sm2
import numpy as np
import scipy.stats as st
from scipy.stats import anderson
from scipy.stats import shapiro
from scipy.stats import kstest
import statsmodels.stats.diagnostic as smd
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson

df=pd.read_csv("low_birth_weight_infants-1.txt", sep="\s+")#Con esto indicamos que lo que separa el archivo son espacios
df.corr()
a=df["headcirc"]
sns.heatmap(df.corr(),annot=True,cmap="YlGnBu")
st.t.interval(0.99, len(a)-1, loc=np.mean(a), scale= st.sem(a))#GENERAMOS UN INTERVALO DE CONFIANZA

sns.pairplot(df) #GEneramos nuestro histograma
df.info()
resultado=sm.ols(formula="headcirc~gestage-1",data=df).fit()#Generamos nuestra ecuacion del modelo y agregamos al -1 porque no hay constante
resultado.summary()
P=resultado.predict()#NUESTRO MODELO GENERA PREDICCIONES
e=a-P #El resultado son el parametro

sumaerroresc=sum(e**2)
print(sumaerroresc)

resultado.params

o=resultado.predict({"gestage":[20,25,29,33]}) #EN EL INTERIOR PONEMOS UN DICCIONARIO PARA IDENTIFICAR EL TIPO DE VARIABLE
#En el ejemplo de arriba tenemos el diccionario gestage que esta prediciendo la headcirc para la semana de gestacion 20
print("La prediccion es de",o)

sns.pairplot(df, diag_kind="kde")#ESTA OPCION NOS PERMITE ESTIMAR LA FUNCION DE DISTRIBUCION DE PROBABILIDAD, usando el diag kind de= kde
modelo2=sm.ols(formula="headcirc~gestage+birthwt-1",data=df).fit()
residuos=modelo2.resid#Vammos a guardar una variable con los residuos
residuos.describe()#Usamos la funcion describe la cual se caracteriza por darnos la media,desv. est, max ,etc...
#El error tiene que estar lo mas cercano a 0 posible
sm2.qqplot(residuos, fit=True, line="45")#Esto nos genera un grafico que busca que veamos cual es el dato generando el error, es la diagonal 
anderson(residuos)#Generamos la prueba de anderson para probar la normalidad
#Aqui se genera el Zp y la ZAlpha, para que podamos comprobar si la ZAlpha esta o no dentro de la region de rechazo
sns.boxplot(residuos) #Generamos un grafica de diagrama caja y bigote
#Los valores fuera del bigote son los datos atipicos , nos muestra a su vez el maximo y el minimo
e=residuos.drop([30],axis=0)#Sabiendo que el dato atipico esta en el indice 30 lo sacamos, usamos eje=0 porque esto quiere decir renglon, si fuera renglon=1 seria una columna
anderson(e)#VOLVEMOS A HACER EL ANALIS ANDERSOn
#Ahora anderson nos demuestra que el dato atipico estaba evitando la normlidad y generaba que el zp estuviera en la zona de rechazo, produciendo que desecharamos nuestra hipotesis nula

l= pd.concat([residuos, e],axis=1)
sns.histplot(data=l,alpha=0.7, kde=True)#Graficamos para ver nuevamente la campana de normalidad con ambos datos y ver los que escapan de la normalidad
l.columns=["residuo","e"]#Renombramos las columnas
print(l)

#EN ESTA PARTE CHECAMOS SI QUITANDO ERROR PASAMOS NORMALIDAD
#Recordemos que la hipotesis nula es que los errores se ajustan a la normalidad

#Prueba shapiro
print(shapiro(residuos))
print(shapiro(e))
#Estos dos pruebas nos muestran el p valor para ver si pasamos y en caso de hacerlo podemos rechazar la hipotesis nula
#Recuerda si el p valor es menor que .05 rechazamos la hipotesis nula

#Esta es la prueba de kolmovorov
print(kstest(residuos,"norm"))
print(kstest(e,"norm"))
#En ambos caso pasamos la prueba con una p valor mayor a .05 determinando que para kolmovorov si hay normalidad

#Parte 3 buscamos si la varianza es constante
#Verificamos el p valor en este caso que buscamos ver si el p valor es menor 
plt.scatter(modelo2.predict(),residuos) 
plt.axhline(0, color="red")
plt.xlabel("Valores Predictivos")
plt.ylabel("Residuales")
#VERIFICAMOS EL P VALOR PARA RECHAZAR HIPOTESIS NULA O NO
breush_pagan_p = smd.het_breuschpagan(modelo2.resid, modelo2.model.exog)[1]
print(breush_pagan_p) #El valor si es menor a .05 por lo que si podemos rechazar la hipotesis nula y determinar que nuestra varianza es constante

#4 Busqueda de autocorrelacion
print(durbin_watson (modelo2.resid))
print(durbin_watson (e))
#En esta parte buscamos que el valor sea entre 1.5-2.5 siendo que si no fuera por esto significaria que podemos predecir el error
#NUEVO DATA FRAME
df2=df.drop([30], axis=0)
modelo2=sm.ols(formula= 'headcirc ~ gestage + birthwt -1', data=df2).fit()
print(modelo2.summary())