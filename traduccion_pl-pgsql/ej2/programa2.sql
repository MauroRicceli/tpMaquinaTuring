CREATE OR REPLACE FUNCTION programa2(input_string TEXT)
RETURNS TEXT AS $$
DECLARE
    longitud INTEGER := LENGTH(input_string);
    caracter TEXT;
    i INTEGER;
    resultado1 TEXT[];
    resultado2 TEXT[];
BEGIN
	--RECIBE STRING CON NUMERO INICIAL IGUAL AL QUE ESTA AL FINAL DEL IGUAL PARA HACER LA RESTA, EJEMPLO: 100-11=100 ES VALIDO COMO INPUT.
    -- limpio el alfabeto y lo inserto para el programa 1 (IGUALDAD ENTRE 2 BINARIOS) 1 0 B X Y =
    DELETE FROM alfabeto;
    INSERT INTO alfabeto (alfabeto) VALUES
    ('1'),
    ('0'),
    ('B'),
    ('X'),
    ('Y'),
	('-'),
	('R'),
    ('=');

    -- limpio la tabla programa y cargo los datos
    DELETE FROM programa;
    DELETE FROM traza_ejecucion;

    INSERT INTO programa (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento) VALUES
	('q0[]', '0B', 'qDer[0]', '0X', 'd'),
	('q0[R]', '0B', 'qDer[R]', '0X', 'd'),
	
	('q0[]', '1B', 'qDer[1]', '1X', 'd'),
	('q0[R]', '1B', 'qDer[R]', '1X', 'd'),
	
	('q0', '0X', 'q0', '0X', 'd'),
	('q0', '1X', 'q0', '1X', 'd'),
	
	('q0[]', '-B', 'restable[]', '-B', 'i'),
	('q0[R]', '-B', 'qDer[-]', '-B', 'S'),
	
	('qDer', '0B', 'qDer', '0B', 'd'),
	('qDer', '1B', 'qDer', '1B', 'd'),
	('qDer', '0X', 'qDer', '0X', 'd'),
	('qDer', '1X', 'qDer', '1X', 'd'),
	('qDer', '-B', 'q1', '-B', 'd'),
	
	('q1[0]', '0B', 'retry[]', '0Y', 'i'),
	('q1[1]', '0B', 'retry[R]', '0B', 'i'),
	('q1[R]', '0B', 'retry[R]', '0Y', 'i'),
	('q1[-]', '0B', 'numeroIzqMenor[-]', '0B', 'i'),
	
	('q1[0]', '1B', 'retry[]', 'Y', 'i'),
	
	('q1', '0Y', 'q1', '0Y', 'd'),
	('q1', '1Y', 'q1', '1Y', 'd'),
	
	('q1', '1B', 'retry', 'Y', 'i'), 
	
	('retry', '0B', 'retry', '0B', 'i'),
	('retry', '1B', 'retry', '1B', 'i'),
	('retry', '0Y', 'retry', '0Y', 'i'),
	('retry', '1Y', 'retry', '1Y', 'i'),
	('retry', '0X', 'retry', '0X', 'i'),
	('retry', '1X', 'retry', '1X', 'i'),
	('retry', '-B', 'retry', '-B', 'i'),
	('retry', 'BB', 'q0', 'BB', 'd'),
	
	('restable', '0B', 'restable', '0B', 'd'),
	('restable', '1B', 'restable', '1B', 'd'),
	('restable', '0Y', 'restable', '0Y', 'd'),
	('restable', '1Y', 'restable', '1Y', 'd'),
	('restable', '0X', 'restable', '0X', 'd'),
	('restable', '1X', 'restable', '1X', 'd'),
	('restable', '-B', 'restable', '-B', 'd'),
	('restable', '=B', 'reiniciarMarcado', '=B', 'i'),
	
	('reiniciarMarcado', '0B', 'reiniciarMarcado', '0B', 'i'),
	('reiniciarMarcado', '1B', 'reiniciarMarcado', '1B', 'i'),
	('reiniciarMarcado', '0Y', 'reiniciarMarcado', '0B', 'i'),
	('reiniciarMarcado', '1Y', 'reiniciarMarcado', '1B', 'i'),
	('reiniciarMarcado', '0X', 'reiniciarMarcado', '0B', 'i'),
	('reiniciarMarcado', '1X', 'reiniciarMarcado', '1B', 'i'),
	('reiniciarMarcado', '-B', 'reiniciarMarcado', '-B', 'i'),
	('reiniciarMarcado', 'BB', 'iniciarResta', 'BB', 'd'),
	
	('numeroIzqMenor', '', 'numeroIzqMenor', '', ''), 
	
	('iniciarResta', '0B', 'iniciarResta', '0B', 'd'),
	('iniciarResta', '1B', 'iniciarResta', '1B', 'd'),
	('iniciarResta', '0Y', 'iniciarResta', '0Y', 'd'),
	('iniciarResta', '1Y', 'iniciarResta', '1Y', 'd'),
	('iniciarResta', '-B', 'iniciarResta', '-B', 'd'),
	('iniciarResta', '=B', 'q10', '=B', 'i'),
	
	('q10', '0B', 'qDerResta', '0Y', 'i'),
	('q10', '1B', 'qDerResta', '1Y', 'i'),
	('q10', '0Y', 'q10', '0Y', 'i'),
	('q10', '1Y', 'q10', '1Y', 'i'),
	('q10', '-B', 'qFinal', '-B', 'i'),
	
	('qDerResta', '0B', 'qDerResta', '0B', 'd'),
	('qDerResta', '1B', 'qDerResta', '1B', 'd'),
	('qDerResta', '0Y', 'qDerResta', '0Y', 'd'),
	('qDerResta', '1Y', 'qDerResta', '1Y', 'd'),
	('qDerResta', '1X', 'qDerResta', '1X', 'd'),
	('qDerResta', '0X', 'qDerResta', '0X', 'd'),
	('qDerResta', '-B', 'qDerResta', '-B', 'd'),
	('qDerResta', '=B', 'qDerResta', '=B', 'd'),
	('qDerResta', 'BB', 'q11', 'BB', 'i'),
	
	('q11', '1B', 'qIzq', 'X', 'i'),
	('q11[0]', '1B', 'qIzq', 'X', 'i'),
	('q11[1]', '1B', 'qIzq', '0X', 'i'),
	
	('q11[0]', '0B', 'qIzq', 'X', 'i'),
	('q11[1]', '0B', 'qPrestamo', '1X', 'i'),
	
	('q11', '0X', 'q11', '0X', 'i'),
	('q11', '1X', 'q11', '1X', 'i'),
	
	('q11', '=B', 'qFinal', '=B', 'i'),
	
	('qIzq', '0B', 'qIzq', '0B', 'i'),
	('qIzq', '1B', 'qIzq', '1B', 'i'),
	('qIzq', '0Y', 'qIzq', '0Y', 'i'),
	('qIzq', '1Y', 'qIzq', '1Y', 'i'),
	('qIzq', '1X', 'qIzq', '1X', 'i'),
	('qIzq', '0X', 'qIzq', '0X', 'i'),
	('qIzq', '-B', 'iniciarResta', '-B', 'i'),
	('qIzq', '=B', 'qIzq', '=B', 'i'),
	
	('qPrestamo', '0B', 'qPrestamo', 'R', 'i'),
	('qPrestamo', '1B', 'qRealizarPrestamo', '0B', 'd'),
	
	('qRealizarPrestamo', '0R', 'qRealizarPrestamo', '1B', 'd'),
	('qRealizarPrestamo', '1B', 'qRealizarPrestamo', '1B', 'd'),
	('qRealizarPrestamo', '0X', 'qRealizarPrestamo', '0X', 'd'),
	('qRealizarPrestamo', '1X', 'qRealizarPrestamo', '1X', 'd'),
	('qRealizarPrestamo', 'BB', 'qIzq', 'BB', 'i'),
	
	('qFinal', '', 'qFinal', '', '');
	
	
	
    

    -- VERIFICO QUE LOS CARACTERES ENVIADOS SEAN PARTE DEL ALFABETO
    FOR i IN 1..longitud LOOP
        caracter := SUBSTRING(input_string FROM i FOR 1);
        IF NOT EXISTS (SELECT 1 FROM alfabeto WHERE alfabeto = caracter) THEN
            RAISE EXCEPTION 'Carácter "%" no permitido en el alfabeto', caracter;
        END IF;
    END LOOP;

    -- CONSTRUYO LA MATRIZ CON EL SIMULADORMT Y LUEGO EJECUTO EL PROGRAMA CON ESA MATRIZ
    SELECT fila1, fila2 INTO resultado1, resultado2 FROM simuladorMT(input_string);
	PERFORM programa_ej2(resultado1, resultado2);
	RETURN 'fin';
END;
$$ LANGUAGE plpgsql;