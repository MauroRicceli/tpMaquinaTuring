
from psycopg2 import pool

class db:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(minconn=1, maxconn = 2,database="", user="", password="",host="", port="")
        self.__iniciardb()

    def __iniciardb(self):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE programa")
        cursor.execute("DROP TABLE traza_ejecucion")
        cursor.execute("CREATE TABLE IF NOT EXISTS programa(estado_ori VARCHAR(20), caracter_ori VARCHAR(20), estado_nue VARCHAR(20), caracter_nue VARCHAR(20), desplazamiento CHAR(1))")
        cursor.execute("CREATE TABLE IF NOT EXISTS traza_ejecucion(estado_ori VARCHAR(20), caracter_ori VARCHAR(20), estado_nue VARCHAR(20), caracter_nue VARCHAR(20), desplazamiento CHAR(1), columna_actual VARCHAR(400),estado_string VARCHAR(1000))")
        cursor.execute("CREATE TABLE IF NOT EXISTS alfabeto(alf VARCHAR(200))")
        conn.commit()

        self.__release_connection(conn)

    def iniciar_programa(self, estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO programa(estado_ori, caracter_ori, estado_nue, caracter_nue, desplazamiento) VALUES (%s, %s, %s, %s, %s)",(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo,desplazamiento))
        conn.commit()
        self.__release_connection(conn)
        #self.__mostrar_carga()

    def update_mt(self, estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual,estado_string):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO traza_ejecucion(estado_ori, caracter_ori, estado_nue, caracter_nue, desplazamiento, columna_actual, estado_string) VALUES (%s, %s, %s, %s, %s, %s, %s)",(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo,desplazamiento, columna_actual,estado_string))
        conn.commit()
        self.__release_connection(conn)
    
    def insertar_alfabeto(self, alfabeto):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alfabeto(alf) VALUES (%s)",(alfabeto,))
        conn.commit()
        self.__release_connection(conn)

    #def __mostrar_carga(self):
    #    conn = self.__get_connection()
    #    cursor = conn.cursor()
    #    cursor.execute("SELECT * FROM programa")
    #    aux = cursor.fetchall()
    #    print(aux)
    #    self.__release_connection(conn)

    def __get_connection(self):
        return self.connection_pool.getconn()
    
    def __release_connection(self, conn):
        self.connection_pool.putconn(conn)