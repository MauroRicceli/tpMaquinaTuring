import sys
import os

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator

#REALIZAR SUMAS DE 2 NUMEROS BINARIOS

class maquina_turing_ej1:

    def crear_multicinta(self):
        aux = generator(2,3,"01","+")
        aux.comenzar_generacion()
        return aux.multicinta
    
    def __init__(self):
        self.multicinta = self.crear_multicinta()
        self.estados = []
        self.alfabeto = "01+"

prueba = maquina_turing_ej1()

print(prueba.multicinta)