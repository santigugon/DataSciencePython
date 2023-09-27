import pandas as pd
import seaborn as sns #IMPORTAMOS LIBRERIA PARA GRAFICAS
import statsmodels.formula.api as sm

df=pd.read_csv("Problema3.csv")#CARGAMOS EL DATAFRAME
df.info()#MOSTRAMOS INFORMACION, COLUMNAS Y TIPO DE VARIABLES 
df.describe()#MOSTRAMOS INFORMACION DE DESV ESTANDAR ADEMAS, DE PROMEDIO, CUANTILES, ETC
df.head()#MOSTRAMOS LAS PRIMERAS 5 LINEAS APROX.
df.head(10)#MOSTRAMOS LAS PRIMERAS 10 LINEAS, GRACIAS AL PARAMETRO

(df.hist())#NOS GENERA UN HISTOGRAMA
A=df.corr()#NOS MUESTRA LA MATRIZ DE CORRELACION

print(df.corr())

(sns.heatmap(A,annot=True,cmap="YlGnBu"))#CREAMOS UN MAPA DE CALOR DE LA CORRELACION QUE NOS MUESTRA LA CORR.
#ANNOT Permite mostrar numeros cmap, cambia los colores, todo puede ser consultado en las librerias

sns.pairplot(df) #NOS IMPRIME UNA NUBE DE DISPERSION, DONDE AL DIBUJAR LA RECTA DEBEMOS DE SER CAPACES DE VER SI NO ESTAN MUY DISPERSOS LOS PUNTOS
#A SU VEZ GENERA UN HISTOGRAMA DE CADA VARIABLE


type(A)#NOS MOSTRARA QUE A ES UN DATAFRAME

resultado= sm.ols(formula="Y~X_1+X_2+X_3+X_4-1",data=df).fit()#USAMOS OLS. Porque es el metodo de minimizar con la suma de errores al cuadrado
#.fit se ajusta a el tipo de ecuacion, datos. Primero ponemos var. dep~var.ind.+var.ind

resultado.summary()
print(resultado.summary())#MUESTRA EL RESUMEN, TOMAMOS LA R AJUSTADA YA QUE PENALIZA PROBLEMAS DE MULTICOLINEALIDAD Y LA R CUADRADA NO
#COLINEALIDAD= LA INFORMACION QUE SE CONSTRUYO A PARTIR DE LA INFORMACION DE OTRAS VARIABLES, SU CORRELACION ESTA MUY CERCANA A 1
#LA CORRELACION ENTRE VARIABLES INDEPENDIENTES NO DEBE SER CERCANA A 1 NI -1
#AGREGAMOS UN SIGNO NEGATIVO -1 PARA QUITAR LA CONSTANTE A NUESTRO MODELO YA QUE SI NO CONSUMIMOS NO HAY CALORIAS

resultado2= sm.ols(formula="Y~X_2+X_3+X_4-1",data=df).fit()#Quitamos la x1 por su correlacion con x2
print(resultado2.summary())#Imprimimos el nuevo modelo con su resumen
