import sys
import os

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generador_multicinta import generador_multicintas as generator
from db_conn.connector import db_connector as db

#REALIZAR SUMA DE UN NUMERO BINARIO Y X CANTIDAD DE 1'S BINARIOS

class maquina_turing_ej1:

    def __crear_multicinta(self):
        aux = generator(2,2,"01","=","", "igualdad")
        aux.comenzar_generacion()
        return aux.multicinta
    
    def __init__(self):
        self.multicinta = self.__crear_multicinta()
        self.estados = []
        self.alfabeto = "01=XY"
        self.columna = 0
        self.cache = ""
        self.estado_actual = 'q0'
        self.db_conex = db()

    def iniciar(self):
        
        self.cargarEstados()
        if(self.multicinta[0][self.columna] == 'B'):
            self.columna = self.columna + 1
            self.q0()
            return
    

    #BUSCA EL PRIMER NUMERO POSIBLE QUE NO ESTE MARCADO CON X DEL NUMERO A LA IZQUIERDA DEL IGUAL.
    #SI ENCUENTRA ALGUNO VALIDO LO MARCA CON X, LO GUARDA EN CACHE PARA SU USO POSTERIOR Y CAMBIA DE ESTADO
    #SI LLEGA AL IGUAL VERIFICA QUE EL CARACTER DEL OTRO NUMERO SEA EL BLANCO, SI NO LO ES, SON DE DISTINTA LONGITUD, por lo tanto distintos
    def q0(self):
        self.estado_actual = 'q0'

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'qDer', '1X','d',self.columna ,str(self.multicinta))
            self.cache = '1'
            self.multicinta[1][self.columna] = 'X'
            self.columna = self.columna + 1
            self.qDer()
            return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'qDer', '0X','d',self.columna ,str(self.multicinta))
            self.cache = '0'
            self.multicinta[1][self.columna] = 'X'
            self.columna = self.columna + 1
            self.qDer()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.db_conex.update_mt(self.estado_actual, '1X', 'q0', '1X','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.q0()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.db_conex.update_mt(self.estado_actual, '0X', 'q0', '0X','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.q0()
            return

        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'q1', '=B','d',self.columna ,str(self.multicinta))
            self.cache = '='
            self.columna = self.columna + 1
            self.q1()
            return
        

    #SE MUEVE A LA DERECHA HASTA ENCONTRAR EL IGUAL, LA IDEA ES LLEGAR AL SEGUNDO NUMERO PARA HACER LA COMPARATIVA
    def qDer(self):
        self.estado_actual = 'qDer'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'qDer', '0B','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.qDer()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'qDer', '1B','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.qDer()
            return
        
        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.db_conex.update_mt(self.estado_actual, '0X', 'qDer', '0X','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.qDer()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.db_conex.update_mt(self.estado_actual, '1X', 'qDer', '1X','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.qDer()
            return

        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'q1', '=B','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.q1()
            return
    
    #CON EL VALOR GUARDADO EN CACHE EN Q0, SE VERIFICA QUE EL PRIMER NUMERO NO MARCADO ENCONTRADO TENGA EL MISMO VALOR
    #SI NO LO TIENE, NO ES IGUAL, Y SE TERMINA SIN ESTADO VALIDO
    #SI ES IGUAL SE CONTINUA.
    def q1(self):
        self.estado_actual = 'q1'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            if(self.cache != '0'):
                self.db_conex.update_mt(self.estado_actual, '0B', 'distintos', '0Y','i',self.columna ,str(self.multicinta))
                self.distintos()
                return
            self.db_conex.update_mt(self.estado_actual, '0B', 'qIzq', '0Y','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            if(self.cache != '1'):
                self.db_conex.update_mt(self.estado_actual, '1B', 'distintos', '1Y','i',self.columna ,str(self.multicinta))
                self.distintos()
                return
            self.db_conex.update_mt(self.estado_actual, '1B', 'qIzq', '1Y','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '0Y', 'q1', '0Y','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.q1()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '1Y', 'q1', '1Y','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.q1()
            return

        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.multicinta[1][self.columna] = 'Y'
            if(self.cache != '='):
                self.db_conex.update_mt(self.estado_actual, '0B', 'distintos', 'BY','i',self.columna ,str(self.multicinta))
                self.distintos()
                return
            self.db_conex.update_mt(self.estado_actual, 'BB', 'qIguales', 'BY','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIguales()
            return

    #TE MOVES A LA IZQUIERDA PARA LLEGAR HASTA EL BB DE LA IZQUIERDA Y VOLVER A CALCULAR Q0 CON EL PROXIMO VALOR SIN MARCAR
    def qIzq(self):
        self.estado_actual = 'qIzq'

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '0B', 'qIzq', '0B','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '1B', 'qIzq', '1B','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '0Y', 'qIzq', '0Y','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return

        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'Y'):
            self.db_conex.update_mt(self.estado_actual, '1Y', 'qIzq', '1Y','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return

        if(self.multicinta[0][self.columna] == '0' and self.multicinta[1][self.columna] == 'X'):
            self.db_conex.update_mt(self.estado_actual, '0X', 'qIzq', '0X','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '1' and self.multicinta[1][self.columna] == 'X'):
            self.db_conex.update_mt(self.estado_actual, '1X', 'qIzq', '1X','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return
        
        if(self.multicinta[0][self.columna] == '=' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, '=B', 'qIzq', '=B','i',self.columna ,str(self.multicinta))
            self.columna = self.columna - 1
            self.qIzq()
            return
        
        if(self.multicinta[0][self.columna] == 'B' and self.multicinta[1][self.columna] == 'B'):
            self.db_conex.update_mt(self.estado_actual, 'BB', 'q0', 'BB','d',self.columna ,str(self.multicinta))
            self.columna = self.columna + 1
            self.q0()
            return

    def distintos(self):
        self.db_conex.update_mt('Los numeros son distintos','','','','','','')
        self.db_conex.exportar_datos()
        return

    def qIguales(self):
        self.db_conex.update_mt('Los numeros son iguales','','','','','','')
        self.db_conex.exportar_datos()
        return
    
    def cargarEstados(self):
        self.db_conex.iniciar_programa('q0','1B','qDer','1X','d')
        self.db_conex.iniciar_programa('q0','0B','qDer','0X','d')
        self.db_conex.iniciar_programa('q0','1X','q0','1X','d')
        self.db_conex.iniciar_programa('q0','0X','q0','0X','d')
        self.db_conex.iniciar_programa('q0','=B','q1','=B','d')

        self.db_conex.iniciar_programa('qDer','0B','qDer','0B','d')
        self.db_conex.iniciar_programa('qDer','1B','qDer','1B','d')
        self.db_conex.iniciar_programa('qDer','0X','qDer','0X','d')
        self.db_conex.iniciar_programa('qDer','=B','q1','=B','d')

        self.db_conex.iniciar_programa('q1[0]','0B','qIzq','0Y','i')
        self.db_conex.iniciar_programa('q1[1]','0B','distintos','0Y','i')
        self.db_conex.iniciar_programa('q1[1]','1B','qIzq','1Y','i')
        self.db_conex.iniciar_programa('q1[0]','1B','distintos','1Y','i')

        self.db_conex.iniciar_programa('q1[0]','1Y','q1[0]','1Y','d')
        self.db_conex.iniciar_programa('q1[1]','1Y','q1[1]','1Y','d')
        self.db_conex.iniciar_programa('q1[0]','0Y','q1[0]','0Y','d')
        self.db_conex.iniciar_programa('q1[1]','0Y','q1[0]','0Y','d')

        self.db_conex.iniciar_programa('q1[0]','BB','distintos','BY','i')
        self.db_conex.iniciar_programa('q1[1]','BB','distintos','BY','i')
        self.db_conex.iniciar_programa('q1[=]','BB','iguales','BY','i')

        self.db_conex.iniciar_programa('qIzq','0B','qIzq','0B','i')
        self.db_conex.iniciar_programa('qIzq','1B','qIzq','1B','i')
        self.db_conex.iniciar_programa('qIzq','0Y','qIzq','0Y','i')
        self.db_conex.iniciar_programa('qIzq','1Y','qIzq','1Y','i')
        self.db_conex.iniciar_programa('qIzq','0X','qIzq','0X','i')
        self.db_conex.iniciar_programa('qIzq','1X','qIzq','1X','i')
        self.db_conex.iniciar_programa('qIzq','=B','qIzq','=B','i')
        self.db_conex.iniciar_programa('qIzq','BB','q0','BB','d')


aux = maquina_turing_ej1()
aux.iniciar()