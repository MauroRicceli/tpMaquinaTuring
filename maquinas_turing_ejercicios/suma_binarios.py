import sys
import os

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator

#REALIZAR SUMAS DE 2 NUMEROS BINARIOS

#Q0 ESTADO INICIAL, BUSCA UN NUMERO SIN MARCAR DE LA PRIMERA PARTE DE LA SUMA DE IZQ A DER Y LO GUARDA EN CACHE
#Q1 UNA VEZ QUE ENCUENTRA UN NUMERO SIN MARCAR Y SE MUEVE A LA DERECHA HASTA ENCONTRAR EL = PARA BUSCAR EL 2DO NUMERO
#Q2 BUSCA UN NUMERO SIN MARCAR DE LA SEGUNDA PARTE DE LA SUMA Y SEGUN CUAL ES LLAMA A QR1 O QR0
#Q3 SI EL NUMERO DE LA SEGUNDA PARTE marcada ES 0, SE LLAMA A ESTE ESTADO
#Q4 IGUAL QUE Q3 PERO LA SEGUNDA PARTE ES 1
#QR1 SE ENCARGA DE MANEJAR BUSCAR EL = SABIENDO QUE EL MARCADO DE LA SEGUNDA PARTE ES 1
#QR0 IGUAL QUE QR1 PERO CON 0

#CAMBIAR PARA CALCULAR DE DERECHA A IZQUIERDA.
#Q0 DEBE EMPEZAR A LA IZQUIERDA DEL +
#Q2 DEBE EMPEZAR A LA IZQUIERDA DEL =

class maquina_turing_ej1:

    def __crear_multicinta(self):
        aux = generator(2,2,"01","+","=")
        aux.comenzar_generacion()
        return aux.multicinta
    
    def __init__(self):
        self.multicinta = self.__crear_multicinta()
        self.estados = []
        self.alfabeto = "01+"
        self.cache_actual = 'B'
        self.columna = 0
        self.estado_actual = 'q0'
    

    def __estado_q0(self):
        self.estado_actual = 'q0'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'X'
            self.columna = self.columna + 1
            self.cache_actual = '0'
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'X'
            self.columna = self.columna + 1
            self.cache_actual = '1'
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            #self.__estado_qALGO() definir luego, si llega a BB el primer numero ya esta completamente marcado.
            return


        
    def __estado_q1(self):
        self.estado_actual = 'q1'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q2()
            return
    
    def __estado_q2(self):
        self.estado_actual = 'q2'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            self.columna = self.columna + 1
            self.__estado_qr0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_q2()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_q2()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            #self.__estado_qr() SI LLEGA AL +B YA SE ACABO EL NUMERO 2, manejar
            return

    def __estado_q3(self):
        self.estado_actual = 'q3'

    def __estado_q4(self):
        self.estado_actual = 'q4'

    def __estado_qr0(self):
        self.estado_actual = 'qr0'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qr0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qr0()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_qr0()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_qr0()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q3()
            return
    
    def __estado_qr1(self):
        self.estado_actual = 'qr1'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_qr1()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q4()
            return
    

    def __estado_q3(self):
        self.estado_actual = 'q3'

        if(self.cache_actual == '0'):
            #con len(multicinta[][]) verificar si el siguiente es un blanco para ver si hay espacio, si no lo es y no hay nada agregar 1 blanco en fila 1 y fila 2 


    def realizar_solucion(self):
        self.__ir_al_comienzo_string()
        self.__estado_q0()

    def __ir_al_comienzo_string(self):
        for i in range(len(self.multicinta[0])-1):
            if(self.multicinta[0][i] == '+'):
                self.columna = i-1
                return
    


prueba = maquina_turing_ej1()

print(prueba.multicinta)
prueba.realizar_solucion()
print(prueba.estado_actual)
print(prueba.cache_actual)
print(prueba.multicinta)