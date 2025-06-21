CREATE TABLE programa(id SERIAL PRIMARY KEY, estado_origen VARCHAR(100), caracter_origen VARCHAR(10), estado_nuevo VARCHAR(100), caracter_nuevo VARCHAR(10), desplazamiento CHAR(1));

CREATE TABLE traza_ejecucion(id SERIAL PRIMARY KEY, estado_origen VARCHAR(100), caracter_origen VARCHAR(10), estado_nuevo VARCHAR(100), caracter_nuevo VARCHAR(10), desplazamiento CHAR(1), columna_actual VARCHAR(100),estado_string VARCHAR (1000));

CREATE TABLE alfabeto(id SERIAL PRIMARY KEY, alfabeto VARCHAR(100));