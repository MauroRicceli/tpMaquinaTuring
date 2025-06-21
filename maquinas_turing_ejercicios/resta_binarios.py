import sys
import os
import numpy

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator
from db_conn.connector import db_connector as db

#REALIZAR SUMA DE UN NUMERO BINARIO Y X CANTIDAD DE 1'S BINARIOS

class maquina_turing_ej2:

    def __crear_multicinta(self):
        aux = generator(2,2,"01","-","=", "resta")
        aux.comenzar_generacion()
        return aux.multicinta
    
    def __init__(self):
        self.multicinta = self.__crear_multicinta()
        self.estados = []
        self.alfabeto = "01-=XY"
        self.columna = 1
        self.estado_actual = 'q0'
        self.cache_actual = ''
        self.db_conex = db()

    #TOMA EL PRIMER CARACTER DEL PRIMER NUMERO Y LO MARCA, PASA A QDER
    def __estado_q0(self):
        self.estado_actual = 'q0'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'X'
            if self.cache_actual != 'R':
                self.cache_actual = '0'
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'X'
            if self.cache_actual != 'R':
                self.cache_actual = '1'
            self.columna = self.columna + 1
            self.__estado_qDer()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return

        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            if self.cache_actual != 'R':
                self.columna = self.columna - 1
                self.__estado_Restable()
            else:
                self.cache_actual = '-'
                self.__estado_qDer()
            return

    #ESTADO QDER, MUEVE A LA DERECHA HASTA ENCONTRAR EL - Y EMPEZAR CON EL SEGUNDO NUMERO, LLAMA A Q1    
    def __estado_qDer(self):
        self.estado_actual = 'qDer'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
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

        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
    #VERIFICA QUE EL NUMERO EN CACHE SEA MAYOR O IGUAL AL PRIMER NO MARCADO, SI EL NUMERO EN CACHE ES MAYOR ES RESTABLE
    #SI NO LO ES,
    #SI ES IGUAL, MARCA EL NUMERO Y VUELVE A HACER EL PROCESO CON EL SIGUIENTE NUMERO DESDE Q0
    #SI ES MENOR, VERIFICA QUE EL NUMERO DERECHO SEA MAS CORTO QUE EL DE LA IZQUIERDA CON QVERIFICARLONGITUD
    def __estado_q1(self):
        self.estado_actual = 'q1'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            if(self.cache_actual == '0'):
                self.multicinta[1][self.columna] = 'Y'
                self.columna = self.columna - 1
                self.cache_actual = ''     
                self.__estado_qRetry()
                return
            if(self.cache_actual == '1'):
                self.columna = self.columna - 1
                self.cache_actual = 'R'     
                self.__estado_qRetry()
                return
            if(self.cache_actual == 'R'):
                self.multicinta[1][self.columna] = 'Y'
                self.columna = self.columna - 1     
                self.__estado_qRetry()
                return
            if(self.cache_actual == '-'):
                self.columna = self.columna - 1     
                self.__estado_numero_izq_menor()
                return
            
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'): 
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            if(self.cache_actual == '0'):
                self.multicinta[1][self.columna] = 'Y'
                self.columna = self.columna - 1
                self.cache_actual = 'R'     
                self.__estado_qRetry()
                return
            if(self.cache_actual == '1'):
                self.multicinta[1][self.columna] = 'Y'
                self.columna = self.columna - 1
                self.cache_actual = ''     
                self.__estado_qRetry()
                return
            if(self.cache_actual == 'R'):
                self.multicinta[1][self.columna] = 'Y'
                self.columna = self.columna - 1     
                self.__estado_qRetry()
                return
            if(self.cache_actual == '-'):
                self.columna = self.columna - 1     
                self.__estado_numero_izq_menor()
                return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'): 
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            if(self.cache_actual != '-'): 
                self.columna = self.columna - 1
                self.__estado_Restable()
            else:
                self.__estado_numero_izq_menor()
            return
    
    #SE MUEVE HACIA EL BB DEL INICIO PARA VOLVER A INICIAR EL PROCESO DE COMPROBACION, LUEGO LLAMA A Q0
    def __estado_qRetry(self):
        self.estado_actual = 'qRetry'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return

        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qRetry()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
    
    #SE MUEVE A LA DERECHA DE TODO EL STRING PARA LLAMAR A REINICIAR MARCADO
    def __estado_Restable(self):
        self.estado_actual = 'qRestable'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_Restable()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
    
    #RECORRE TODO EL STRING DE DERECHA A IZQUIERDA REINICIANDO TODOS LOS MARCADOS, LUEGO LLAMA A INICIAR RESTA
    def __estado_reiniciar_marcado(self):
        self.estado_actual = 'reiniciar_marcado'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return

        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reiniciar_marcado()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_iniciarResta()
            return
    
    def __estado_numero_izq_menor(self):
        self.estado_actual = 'numero_izq_menor'
        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()
    
    #ESTADO INICIAR RESTA, SE LLAMA LUEGO DE LA COMPROBACION Y SE MUEVE HASTA EL PRIMER NUMERO (DESDE LA DERECHA) A RESTAR.
    #CUANDO LLEGA AL = SIGNIFICA QUE YA PUEDO VER EL NUMERO QUE RESTA, POR LO TANTO PASO A Q10
    def __estado_iniciarResta(self):
        self.estado_actual = 'iniciarResta'
        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_iniciarResta()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_iniciarResta()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_iniciarResta()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_iniciarResta()
            return
        
        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_iniciarResta()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q10()
            return

    #BUSCO DE DERECHA A IZQUIERDA LOS NUMEROS DEL NUMERO QUE ESTA RESTANDO. SI ENCUENTRO UN 0 SIN MARCAR LO MARCO Y SIGO BUSCANDO UN 1 YA QUE NO ME AFECTA EN LA RESTA.
    #SI ENCUENTRO UN 1 SIN MARCAR, LO MARCO Y LLAMO A QDER RESTA, QUE SE ENCARGA DE IR HASTA EL FINAL DEL STRING.
    def __estado_q10(self):
        self.estado_actual = 'q10'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            self.cache_actual = '0'
            self.columna = self.columna - 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            self.cache_actual = '1'
            self.columna = self.columna - 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_q10()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_q10()
            return
        
        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qFinal()
            return

    #SE MUEVE HASTA EL FINAL DEL STRING.
    def __estado_qDerResta(self):
        self.estado_actual = 'qDerResta'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return

        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'P'):
            self.columna = self.columna + 1
            self.__estado_qDerResta()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q11()
            return

    #HACE LA RESTA EN ORDEN DE DERECHA A IZQUIERDA.
    def __estado_q11(self):
        self.estado_actual = 'q11'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print(self.cache_actual)
        print()

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            if(self.cache_actual == '0'):
                self.multicinta[1][self.columna] = 'X'
                self.columna = self.columna - 1
                self.__estado_qIzq()
                return
            if(self.cache_actual == '1'):
                self.multicinta[0][self.columna] = '0'
                self.multicinta[1][self.columna] = 'X'
                self.columna = self.columna - 1
                self.__estado_qIzq()
                return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            if(self.cache_actual == '0'):
                self.multicinta[1][self.columna] = 'X'
                self.columna = self.columna - 1
                self.__estado_qIzq()
                return
            if(self.cache_actual == '1'):
                self.multicinta[0][self.columna] = '1'
                self.multicinta[1][self.columna] = 'X'
                self.columna = self.columna - 1
                self.__estado_qPrestamo()
                return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q11()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q11()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'P'):
            self.columna = self.columna - 1
            self.__estado_q11()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qFinal()
            return

    def __estado_qIzq(self):
        self.estado_actual = 'qIzq'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'P'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
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
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '-' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_iniciarResta()
            return

        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return
    
    def __estado_qPrestamo(self):
        self.estado_actual = 'qPrestamo'
        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'R'
            self.columna = self.columna - 1
            self.__estado_qPrestamo()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna + 1
            self.__estado_qrealizar_prestamo()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'P'):
            self.columna = self.columna - 1
            self.__estado_qPrestamo()
            return
        
    def __estado_qrealizar_prestamo(self):
        self.estado_actual = 'qRealizarPrestamo'
        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'R'):
            self.multicinta[0][self.columna] = '1'
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.__estado_qrealizar_prestamo()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qrealizar_prestamo()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_qrealizar_prestamo()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_qrealizar_prestamo()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'P'):
            self.columna = self.columna + 1
            self.__estado_qrealizar_prestamo()
            return

        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_qIzq()
            return

    def __estado_qFinal(self):
        self.estado_actual = 'qFinal'

        print(self.multicinta)
        print(self.columna)
        print(self.estado_actual)
        print()

        print("fin")

    def iniciar_maquina(self):
        self.__estado_q0()

prueba = maquina_turing_ej2()
prueba.iniciar_maquina()


        