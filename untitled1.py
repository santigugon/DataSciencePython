# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:23:13 2023

@author: santi
"""

import math as m
def serie(nserie):
  acumulador=0
  i=1
  valorserie=0
  valorsumatoria=0
  for x in range(1,nserie+1,1):
    if(i==1):
      valorunico=-1
      acumulador+=valorunico
      print(valorunico,end= " ")
    elif(i>1):
      valorserie+=2
      valorsumatoria=valorserie/m.factorial(valorserie)
      if i%2==0:
        print("+",valorserie,"/",m.factorial(valorserie),end= " ")
        acumulador+=valorsumatoria
      elif i%2!=0:
        acumulador-=valorsumatoria
        print("-",valorserie,"/",m.factorial(valorserie),end= " ")
    i+=1
  print("= ",round(acumulador,2))
  return(acumulador)

def main():
  nserie=int(input("Ingresa el numero de elementos de la serie "))
  serie(nserie)

main()  