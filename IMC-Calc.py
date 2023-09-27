# -*- coding: utf-8 -*-
yo= ["Santiago,","Gutierrez Gonzalez",19,1.82,74]
#Nombre, Apellido, edad, altura en metros, peso en kg
def imc(lista): #Definimos esta funcion para poder calcular el IMC de cualquier lista con la estructura mencionada anterior
   imc=lista[4]/(lista[3]**2)#Escribimos la formula del IMC
   print("“Peso inferior al normal: Menos de 18.5 Normal: 18.5 – 24.9 \n Peso superior al normal: 25.0 – 29.9 Obesidad: Más de 30.0 \n IMC de ",lista[0],lista[1],"Es =",imc)

imc(yo)# Mandamos llamar la funcion con la lista YO