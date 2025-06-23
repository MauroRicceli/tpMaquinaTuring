import sys
import os
import numpy

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator
from db_conn.connector import db_connector as db

#REALIZAR SUMA DE UN NUMERO BINARIO Y X CANTIDAD DE 1'S BINARIOS

class maquina_turing_ej3:

    def __crear_multicinta(self):
        aux = generator(2,2,"01","=","", "invertir")
        aux.comenzar_generacion()
        return aux.multicinta
    
    def __init__(self):
        self.multicinta = self.__crear_multicinta()
        self.estados = []
        self.alfabeto = "01=XY"
        self.columna = 1
        self.cache = ''
        self.estado_actual = 'q0'

    #SE MUEVE HACIA LA DERECHA HASTA LLEGAR AL IGUAL Y PASA A Q1
    def __estado_q0(self):
        self.estado_actual = 'q0'
        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q1()
            return
    
    #ENCUENTRA EL PRIMER NUMERO SIN MARCAR Y LO MARCA, LO GUARDA EN CACHE, SE MUEVE A LA DERECHA Y VA A QDER
    def __estado_q1(self):
        self.estado_actual = 'q1'
        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.cache = '0'
            self.multicinta[1][self.columna] = 'X'
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.cache = '1'
            self.multicinta[1][self.columna] = 'X'
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_fin()
            return
    
    #VUELVE A BUSCAR EL =, Y LUEGO PASA A Q2
    def __estado_qDer(self):
        self.estado_actual = 'qDer'
        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_qDer()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q2()
            return


    def __estado_q2(self):
        self.estado_actual = 'q2'
        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = self.cache
            self.multicinta[1][self.columna] = 'Y'
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_q2()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_q2()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
    def __estado_qIzq(self):
        self.estado_actual = 'qIzq'
        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return

    def iniciar(self):
        self.__estado_q0()
        return

    def __estado_fin(self):
        print("fin")


aux = maquina_turing_ej3()
aux.iniciar()
