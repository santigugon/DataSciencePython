# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:25:31 2023

@author: santi
"""

import numpy as np
import matplotlib.pyplot as plt

def create_bridge_points(width, height):
    x = np.linspace(0, width, 100)
    y = height * np.sin((x - width / 2) * np.pi / width)
    return x, y

def plot_bridge(width, height, terrain_height, river_width):
    x, y = create_bridge_points(width, height)
    
    plt.figure(figsize=(12, 6))
    
    # Dibujar el terreno
    plt.fill_between([0, river_width], -terrain_height, terrain_height, color='sandybrown', alpha=0.6, label='Terreno árido')
    
    # Dibujar el río
    plt.fill_between([0, river_width], -terrain_height, -terrain_height * 0.5, color='blue', alpha=0.5, label='Río')
    
    # Dibujar el puente
    plt.plot(x, y + terrain_height * 0.5, label='Puente peatonal', linewidth=3, color='black')
    plt.plot(x + river_width, y + terrain_height * 0.5, linewidth=3, color='black')
    
    plt.ylim(-terrain_height * 2, terrain_height * 2)
    plt.xlim(-width, river_width + width)
    
    plt.title('Modelo de puente peatonal sobre río de 200 metros de ancho')
    plt.legend()
    plt.grid()
    plt.show()

# Configurar parámetros del puente
bridge_width = 10
bridge_height = 5
terrain_height = 20
river_width = 200

plot_bridge(bridge_width, bridge_height, terrain_height, river_width)