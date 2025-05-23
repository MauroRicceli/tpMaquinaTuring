import sys
import os
import numpy

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator

#REALIZAR SUMA DE UN NUMERO BINARIO Y X CANTIDAD DE 1'S BINARIOS

class maquina_turing_ej1:

    def __crear_multicinta(self):
        aux = generator(2,2,"01","+","=", "suma")
        aux.comenzar_generacion()
        return aux.multicinta
    
    def __init__(self):
        self.multicinta = self.__crear_multicinta()
        self.estados = []
        self.alfabeto = "01+="
        self.cache_actual = 'B'
        self.columna = 0
        self.estado_actual = 'q0'
    
    #Q0 SE MUEVE A LA DERECHA HASTA LLEGAR AL IGUAL
    def __estado_q0(self):
        self.estado_actual = 'q0'

        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print("")
        print("XDD")

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
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q0()
            return

        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q2()
            return
        
    #BUSCA Y VA MARCANDO LOS 1'S, CUANDO MARCA UNO VA A QR1
    def __estado_q2(self):
        self.estado_actual = 'q2'

        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print("")
        print("")
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.columna = self.columna - 1
            self.__estado_q2()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            print("Estado Final")
            return

    #MARCA EL PRIMER DIGITO DEL RESULTADO PARA NO PISARLO
    def __estado_qS(self):
        self.estado_actual = 'qS'

        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'R'
            self.columna = self.columna + 1
            self.__estado_q4()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'R'
            self.columna = self.columna + 1
            self.__estado_q4()
            return


    #VUELVE A BUSCAR EL FIN DEL STRING Y VA A Q7
    def __estado_q4(self):
        self.estado_actual = 'q4'

        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print("")
        print("")
        
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
            self.__estado_q7()
            return


    #VERIFICA QUE EL PRIMER DIGITO DEL RESULTADO NO SEA TAMBIEN EL ULTIMO, SI LO ES LO MARCA NUEVAMENTE CON F PARA DISTINGUIRLO, SI NO, NO HACE NADA. LUEGO SE VA A Q6
    def __estado_q7(self):
        self.estado_actual = 'q7'

        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'R'):
            self.multicinta[1][self.columna] = 'F'
            self.columna = self.columna + 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.multicinta[1][self.columna] = 'F'
            self.columna = self.columna + 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_q6()
            return


    #SE ENCARGA DE REALIZAR LA SUMA, BUSCAR DONDE PONER EL 1, SI NO HAY LUGAR SE MUEVE Y PONE ESE 1 EN 0 Y ASI... SI NO ENCUENTRA NINGUN ESPACIO Y LLEGA AL MARCADO,
    #LLAMA AL ESTADO ENCARGADO DE MANEJAR EL OVERFLOW, SI LO ENCUENTRA, PASA AL SIGUIENTE 1 DE LA SUMA
    def __estado_q6(self):
        self.estado_actual = 'q6'

        print(self.multicinta)
        print(self.estado_actual)
        print(self.columna)
        print("")
        print("")

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'F'):
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'F'):
            self.columna = self.columna - 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna - 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.columna = self.columna - 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna - 1
            self.__estado_q6()
            return

    #SE ENCARGA DE MANEJAR EL OVERFLOW, Y LUEGO RESETEA
    def __estado_overflow(self):
        self.estado_actual = 'overflow'

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna + 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.__estado_overflow()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'F'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.__estado_overflow()
            return

        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna - 1

            nueva_columna = numpy.array([['B'],['B']])

            self.multicinta = numpy.hstack((self.multicinta, nueva_columna))

            self.__estado_reset()
            return
    
    #VA HACIA EL PRINCIPIO DEL RESULTADO (=), PARA COMENZAR A REALIZAR LA SUMA, LUEGO LLAMA A qS
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
            self.__estado_qS()
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
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna - 1
            self.__estado_reset()
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