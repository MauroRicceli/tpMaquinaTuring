import sys
import os
import numpy

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator
from db_conn.postgres_connector import db

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
        self.columna = 0
        self.estado_actual = 'q0'
        self.db_conex = db()
    
    #Q0 SE MUEVE A LA DERECHA HASTA LLEGAR AL IGUAL
    def __estado_q0(self):
        self.estado_actual = 'q0'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'q0', '0B','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'q0', '1B','d',self.columna , str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '0Y', 'q0', '0Y','d',self.columna, str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '1Y', 'q0', '1Y','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '+B', 'q0', '+B','d', self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q0()
            return

        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'q2', '=B','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_q2()
            return
        
    #BUSCA Y VA MARCANDO LOS 1'S, CUANDO MARCA UNO VA A QR1
    def __estado_q2(self):
        self.estado_actual = 'q2'
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'qr1', '1Y','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'Y'
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '1Y', 'q2', '1Y','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_q2()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '+B', 'estado final', '+B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.db_conex.update_mt('Maquina apagada', '', '', '','','')
            return

    #MARCA EL PRIMER DIGITO DEL RESULTADO PARA NO PISARLO
    def __estado_qS(self):
        self.estado_actual = 'qS'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'q4', '0R','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'R'
            self.columna = self.columna + 1
            self.__estado_q4()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'q4', '1R','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'R'
            self.columna = self.columna + 1
            self.__estado_q4()
            return


    #VUELVE A BUSCAR EL FIN DEL STRING Y VA A Q7
    def __estado_q4(self):
        self.estado_actual = 'q4'
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'q4', '0B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q4()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'q4', '1B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q4()
            return
            
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, 'BB', 'q7', 'BB','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_q7()
            return


    #VERIFICA QUE EL PRIMER DIGITO DEL RESULTADO NO SEA TAMBIEN EL ULTIMO, SI LO ES LO MARCA NUEVAMENTE CON F PARA DISTINGUIRLO, SI NO, NO HACE NADA. LUEGO SE VA A Q6
    def __estado_q7(self):
        self.estado_actual = 'q7'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'R'):
            self.db_conex.update_mt(self.estado_actual, '0R', 'q6', '0F','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'F'
            self.columna = self.columna + 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.db_conex.update_mt(self.estado_actual, '1R', 'q6', '1F','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'F'
            self.columna = self.columna + 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'q6', '0B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'q6', '1B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q6()
            return


    #SE ENCARGA DE REALIZAR LA SUMA, BUSCAR DONDE PONER EL 1, SI NO HAY LUGAR SE MUEVE Y PONE ESE 1 EN 0 Y ASI... SI NO ENCUENTRA NINGUN ESPACIO Y LLEGA AL MARCADO,
    #LLAMA AL ESTADO ENCARGADO DE MANEJAR EL OVERFLOW, SI LO ENCUENTRA, PASA AL SIGUIENTE 1 DE LA SUMA
    def __estado_q6(self):
        self.estado_actual = 'q6'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'reset', '1B','i',self.columna,str(self.multicinta))
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'F'):
            self.db_conex.update_mt(self.estado_actual, '0F', 'reset', '1F','i',self.columna,str(self.multicinta))
            self.multicinta[0][self.columna] = '1'
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'F'):
            self.db_conex.update_mt(self.estado_actual, '1F', 'overflow', '1F','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'q6', '0B','i',self.columna,str(self.multicinta))
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna - 1
            self.__estado_q6()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.db_conex.update_mt(self.estado_actual, '1R', 'overflow', '1R','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, 'BB', 'q6', 'BB','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_q6()
            return

    #SE ENCARGA DE MANEJAR EL OVERFLOW, Y LUEGO RESETEA
    def __estado_overflow(self):
        self.estado_actual = 'overflow'

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'overflow', '0B','d',self.columna,str(self.multicinta))
            self.multicinta[0][self.columna] = '0'
            self.columna = self.columna + 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'overflow', '0B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'overflow', '=B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_overflow()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'F'):
            self.db_conex.update_mt(self.estado_actual, '1F', 'overflow', '1B','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.__estado_overflow()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.db_conex.update_mt(self.estado_actual, '1R', 'overflow', '1B','d',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna + 1
            self.__estado_overflow()
            return

        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, 'BB', 'reset', '0B','i',self.columna,str(self.multicinta))
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
            self.db_conex.update_mt(self.estado_actual, '0B', 'qr1', '0B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'qr1', '1B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '0Y', 'qr1', '0Y','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_qr1()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '1Y', 'qr1', '1Y','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_qr1()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'qS', '=B','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_qS()
            return
    

    def __estado_reset(self):
        self.estado_actual = 'reset'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'reset', '0B','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_reset()
            return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '0Y', 'reset', '0Y','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'reset', '1B','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '1Y', 'reset', '1Y','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '+' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '+B', 'reset', '+B','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'reset', '=B','i',self.columna,str(self.multicinta))
            self.columna = self.columna - 1
            self.__estado_reset()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, 'BB', 'q0', 'BB','d',self.columna,str(self.multicinta))
            self.columna = self.columna + 1
            self.__estado_q0()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'R'):
            self.db_conex.update_mt(self.estado_actual, '1R', 'reset', '1B','i',self.columna,str(self.multicinta))
            self.multicinta[1][self.columna] = 'B'
            self.columna = self.columna - 1
            self.__estado_reset()
            return


    def realizar_solucion(self):
        self.__cargar_programa()
        self.__ir_al_comienzo_string()
        self.__estado_q0()

    def __ir_al_comienzo_string(self):
        for i in range(len(self.multicinta[0])-1):
            if(self.multicinta[0][i] == '+'):
                self.columna = i-1
                return
            
    def __cargar_programa(self):
        self.db_conex.iniciar_programa('q0', '0B', 'q0','0B','d')
        self.db_conex.iniciar_programa('q0', '1B', 'q0','1B','d')
        self.db_conex.iniciar_programa('q0', '0Y', 'q0','0Y','d')
        self.db_conex.iniciar_programa('q0', '1Y', 'q0','1Y','d')
        self.db_conex.iniciar_programa('q0', '+B', 'q0','+B','d')
        self.db_conex.iniciar_programa('q0', '=Y', 'q2','=Y','i')

        self.db_conex.iniciar_programa('q2', '1B', 'qr1','1Y','d')
        self.db_conex.iniciar_programa('q2', '1Y', 'q2','1Y','i')
        self.db_conex.iniciar_programa('q2', '+B', 'fin','+B','d')

        self.db_conex.iniciar_programa('qS', '0B', 'q4','0R','d')
        self.db_conex.iniciar_programa('qS', '1B', 'q4','1R','d')

        self.db_conex.iniciar_programa('q4', '0B', 'q4','0B','d')
        self.db_conex.iniciar_programa('q4', '1B', 'q4','1B','d')
        self.db_conex.iniciar_programa('q4', 'BB', 'q7','BB','i')

        self.db_conex.iniciar_programa('q7', '0R', 'q6','0F','d')
        self.db_conex.iniciar_programa('q7', '1R', 'q6','1F','d')
        self.db_conex.iniciar_programa('q7', '0B', 'q6','0B','d')
        self.db_conex.iniciar_programa('q7', '1B', 'q6','1B','d')

        self.db_conex.iniciar_programa('q6', '0B', 'reset','1B','i')
        self.db_conex.iniciar_programa('q6', '0F', 'reset','1F','i')
        self.db_conex.iniciar_programa('q6', '1F', 'overflow','1F','i')
        self.db_conex.iniciar_programa('q6', '1B', 'q6','0B','i')
        self.db_conex.iniciar_programa('q6', '1R', 'overflow','1R','i')
        self.db_conex.iniciar_programa('q6', 'BB', 'q6','BB','i')

        self.db_conex.iniciar_programa('overflow', '1B', 'overflow','0B','d')
        self.db_conex.iniciar_programa('overflow', '0B', 'overflow','0B','d')
        self.db_conex.iniciar_programa('overflow', '=B', 'overflow','=B','d')
        self.db_conex.iniciar_programa('overflow', '1F', 'overflow','1B','d')
        self.db_conex.iniciar_programa('overflow', '1R', 'overflow','1B','d')
        self.db_conex.iniciar_programa('overflow', 'BB', 'reset','0B','i')

        self.db_conex.iniciar_programa('qr1', '0B', 'qr1','0B','d')
        self.db_conex.iniciar_programa('qr1', '1B', 'qr1','1B','d')
        self.db_conex.iniciar_programa('qr1', '0Y', 'qr1','0Y','d')
        self.db_conex.iniciar_programa('qr1', '1Y', 'qr1','1Y','d')
        self.db_conex.iniciar_programa('qr1', '=B', 'qS','=B','d')

        self.db_conex.iniciar_programa('reset', '0B', 'reset','0B','i')
        self.db_conex.iniciar_programa('reset', '0Y', 'reset','0Y','i')
        self.db_conex.iniciar_programa('reset', '1B', 'reset','1B','i')
        self.db_conex.iniciar_programa('reset', '1Y', 'reset','1Y','i')
        self.db_conex.iniciar_programa('reset', '+B', 'reset','+B','i')
        self.db_conex.iniciar_programa('reset', '=B', 'reset','=B','i')
        self.db_conex.iniciar_programa('reset', '1R', 'reset','1B','i')
        self.db_conex.iniciar_programa('reset', 'BB', 'q0','BB','d')

        self.db_conex.insertar_alfabeto(self.alfabeto)

    


prueba = maquina_turing_ej1()
prueba.realizar_solucion()
