# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 17:23:57 2022

@author: santi
"""

import pandas as pd
doc=pd.read_csv("A00572499_EtiquetasNutrimentales (1) - Copy.csv")#IMPORTAMOS EL DOCUMENTO
doc.info()#DESPLEGAMOS LA INFORMACION DEL DOCUMENTO}
doc.corr()#DESPLEGAMOS INDICES DE CORRELACION
import statsmodels.formula.api as sm 
import pandas_datareader as pdr
start=pd.to_datetime("2020-02-01")#Declaramos fecha 
end= pd.to_datetime("2020-04-01")
acciones=pdr.get_data_yahoo("WMT",start,end)
acciones[["Open","Close"]].plot()
acciones.info()

resultado=sm.ols(formula="calorias~carbohidratos+grasas+proteinas",data=doc).fit()