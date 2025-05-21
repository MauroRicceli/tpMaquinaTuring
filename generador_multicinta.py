import numpy
import re

#OBJETO RECIBE CANTIDAD DE STRINGS QUE QUERES MANEJAR, CUANTAS CINTAS TENDRÁ LA MT (DE 1 A +INF), EL ALFABETO COMO STRING "01" SIN CONTAR LOS SEPARADORES,
#Y UN SEPARADOR OPCIONAL (NONE, '+', '-', ETC)
class generador_multicintas:
    def __init__(self, cant_strings, cant_cintas, alfabeto, separador_strings):
        self.cant_strings = cant_strings
        self.cant_cintas = cant_cintas
        self.alfabeto = alfabeto.upper()
        self.multicinta = None
        self.string_analizar = None
        self.separador_strings = separador_strings

    #UNE TODOS LOS STRINGS DE LOS INPUTS TENIENDO EN CUENTA EL POSIBLE SEPARADOR
    def generar_string_unico(self, array_inputs):
        string_unico = ""+array_inputs[0]
        array_inputs.pop(0)
        for i in range(len(array_inputs)):
            if(self.separador_strings != None):
                string_unico += self.separador_strings
            string_unico += array_inputs[i]
        
        self.string_analizar = string_unico

        return self.generar_multicinta()
                
    #MANEJA LOS INPUTS DE TODOS LOS STRINGS Y VERIFICA QUE ESTEN DENTRO DEL ALFABETO
    def comenzar_generacion(self):
        i = 0
        inputs = []
        while (i!=self.cant_strings):
            aux = input("Ingrese el string "+str(i+1)+" a considerar: ").upper()
            patron = f"[{self.alfabeto}]+"
            if re.fullmatch(patron, aux) != None:
                inputs.append(aux)
                i += 1
            else:
                print("Ingrese un string válido dentro del alfabeto ("+self.alfabeto+")")
        return self.generar_string_unico(inputs)    
    
    #GENERA LAS CINTAS POSIBLES DEJANDO TDO EN BLANCOS Y LUEGO UBICA EL STRING CON UNA COLUMNA DE BLANCOS A CADA LADO PARA MARCAR INICIO Y FIN
    def generar_multicinta(self):
        self.multicinta = numpy.full((self.cant_cintas, len(self.string_analizar)+2), 'B')

        for i in range(len(self.string_analizar)):
            self.multicinta[0, i+1] = self.string_analizar[i]
    
        return


    def __str__(self):
        return f"Multicinta:\n{self.multicinta}"
#EJ
#prueba = generador_multicintas(4, 3, "ABC1", "+")
#prueba.comenzar_generacion()
#print(prueba.multicinta)

