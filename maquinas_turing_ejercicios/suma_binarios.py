import sys
import os
import numpy

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator

#REALIZAR SUMAS DE 2 NUMEROS BINARIOS

#Q0 ESTADO INICIAL, BUSCA UN NUMERO SIN MARCAR DE LA PRIMERA PARTE DE LA SUMA DE IZQ A DER Y LO GUARDA EN CACHE
#Q1 UNA VEZ QUE ENCUENTRA UN NUMERO SIN MARCAR Y SE MUEVE A LA DERECHA HASTA ENCONTRAR EL = PARA BUSCAR EL 2DO NUMERO
#Q2 BUSCA UN NUMERO SIN MARCAR DE LA SEGUNDA PARTE DE LA SUMA Y SEGUN CUAL ES LLAMA A QR1 O QR0
#Q3 SI EL NUMERO DE LA SEGUNDA PARTE marcada ES 0, SE LLAMA A ESTE ESTADO Y SE DIRIGE HASTA EL FINAL DEL RESULTADO
#Q4 IGUAL QUE Q3 PERO LA SEGUNDA PARTE ES 1
#Q5 ES CUANDO PASO EL = Y EMPIEZO A BUSCAR EL RESULTADO PARA SUMAR UN 1 EN ALGUN ESPACIO, SI NO SE ENCUENTRA SE LLEGA AL = Y SE LLAMA A Q10, SI LO ENCUENTRA PONE EL PRIMER 0 QUE ENCUENTRE EN 1 
#Q10 BUSCA EL PRIMER 1 DEL RESULTADO, Y LLAMA A QA
#QA PONE TOD EL RESULTADO EN 0 MENOS EL PRIMER 1 PARA VER QUE AGREGAMOS UN NUMERO MAS CON EL ACARREO, EXPANDE LOS BLANCOS.
#QR1 SE ENCARGA DE MANEJAR BUSCAR EL = SABIENDO QUE EL MARCADO DE LA SEGUNDA PARTE ES 1
#QR0 IGUAL QUE QR1 PERO CON 0

#CAMBIAR PARA CALCULAR DE DERECHA A IZQUIERDA.
#Q0 DEBE EMPEZAR A LA IZQUIERDA DEL +
#Q2 DEBE EMPEZAR A LA IZQUIERDA DEL =

class maquina_turing_ej1:

    def __crear_multicinta(self):
        aux = generator(2,2,"01","+","=0")
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
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q16()
            return
        
        

    def __estado_q16(self):
        self.estado_actual = 'q16'

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
            self.__estado_q16()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_q16()
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
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_q1()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
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

        if(self.cache_actual == '0'): #si tomaste 0 de ambos numeros la suma es 0, no hacer nada y volver.
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q3()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q3()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q5()
            return


    def __estado_q4(self):
        self.estado_actual = 'q4'

        if(self.cache_actual == '0'): #ES LO MISMO QUE MANEJA Q3, SOLO QUE EN VEZ DE TENER 0 EN CACHE Y TOMAR 1, TIENE 1 EN CACHE Y TOMA 0
            self.__estado_q3()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q4()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q4()
            return
            
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q6()
            return

    def __estado_q5(self):
        self.estado_actual = 'q5'

        print(self.multicinta)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna + 1
            self.__estado_q9()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q5()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q10()
            return
    

    def __estado_q6(self):
        self.estado_actual = 'q6'

        print(self.multicinta)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Z'
            self.columna = self.columna - 1
            self.__estado_q7()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Z'
            self.columna = self.columna - 1
            self.__estado_q7()
            return
    
    def __estado_q7(self):
        self.estado_actual = 'q7'

        print(self.multicinta)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna + 1
            
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna - 1
            self.__estado_q7()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q12()
            return

    def __estado_q9(self):
        self.estado_actual = 'q9'

        print(self.multicinta)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna + 1
            self.__estado_q9()
            return

        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return

    def __estado_q10(self):
        self.estado_actual = 'q10'

        print(self.multicinta)
        print("")
        print("")
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_qA()
            return

    def __estado_q11(self):
        self.estado_actual = 'q11'
        
        print(self.multicinta)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q11()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q11()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Z'):
            self.multicinta[0][self.columna] = '1'
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.cache_actual = '0'
            self.__estado_qB()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Z'):
            self.multicinta[1][self.columna] = 'B'
            self.cache_actual = '1'
            self.columna = self.columna + 1
            self.__estado_qB()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna - 1
            self.__estado_q13()
            return

    def __estado_q12(self):
        self.estado_actual = 'q12'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Z'):
            self.cache_actual = '0'
            self.multicinta[0][self.columna] = '1'
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.__estado_q11()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Z'):
            self.multicinta[1][self.columna] = 'B'
            self.cache_actual = '1'
            self.columna = self.columna + 1
            self.__estado_qB()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna + 1
            self.__estado_q11()
            return


    def __estado_q13(self):
        self.estado_actual = 'q13'

        print(self.multicinta)
        print("")
        print("")

        self.columna = self.columna - 1

        nueva_columna = numpy.array([['B'],['B']])

        self.multicinta = numpy.hstack((self.multicinta, nueva_columna))

        self.__estado_reset()
        return



    def __estado_qA(self):
        self.estado_actual = 'qA'

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna + 1
            self.__estado_qA()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna - 1

            nueva_columna = numpy.array([['B'],['B']])

            self.multicinta = numpy.hstack((self.multicinta, nueva_columna))

            self.__estado_reset()
            return
        
    def __estado_qB(self):
        self.estado_actual = 'qB'

        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = self.cache_actual
            self.columna = self.columna - 1

            nueva_columna = numpy.array([['B'],['B']])

            self.multicinta = numpy.hstack((self.multicinta, nueva_columna))

            self.__estado_reset()
            return

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
            self.columna = self.columna + 1
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
            self.columna = self.columna + 1
            self.__estado_q4()
            return
    

    def __estado_reset(self):
        self.estado_actual = 'reset'

        self.cache_actual = 'B'
        
        print(self.multicinta)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return


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
print(prueba.columna)
print(prueba.multicinta)