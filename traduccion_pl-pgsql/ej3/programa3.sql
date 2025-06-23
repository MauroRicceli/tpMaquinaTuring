CREATE OR REPLACE FUNCTION programa3(input_string TEXT)
RETURNS TEXT AS $$
DECLARE
    longitud INTEGER := LENGTH(input_string);
    caracter TEXT;
    i INTEGER;
    resultado1 TEXT[];
    resultado2 TEXT[];
BEGIN

    --RECIBE STRING CON IGUAL CANTIDAD DE 0 QUE EL BINARIO QUE INVERTIS, POR EJEMPLO: 1001=0000 ES VALIDO COMO INPUT.
    -- limpio el alfabeto y lo inserto para el programa 1 (IGUALDAD ENTRE 2 BINARIOS) 1 0 B X Y =
    DELETE FROM alfabeto;
    INSERT INTO alfabeto (alfabeto) VALUES
    ('1'),
    ('0'),
    ('B'),
    ('X'),
    ('Y'),
    ('=');

    -- limpio la tabla programa y cargo los datos
    DELETE FROM programa;
    DELETE FROM traza_ejecucion;

    INSERT INTO programa (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento) VALUES
    ('q0', '0B', 'q0', '0B', 'd'),
    ('q0', '1B', 'q0', '1B', 'd'),
    ('q0', '0X', 'q0', '0X', 'd'),
    ('q0', '1X', 'q0', '1X', 'd'),
    ('q0', '=B', 'q1', '=B', 'i'),
    ('q1', '0B', 'qDer', '0X', 'd'),
    ('q1', '1B', 'qDer', '1X', 'd'),
    ('q1', '0X', 'q1', '0X', 'i'),
    ('q1', '1X', 'q1', '1X', 'i'),
    ('q1', 'BB', 'fin', 'BB', 'd'),
    ('qDer', '0B', 'qDer', '0B', 'd'),
    ('qDer', '1B', 'qDer', '1B', 'd'),
    ('qDer', '0X', 'qDer', '0X', 'd'),
    ('qDer', '1X', 'qDer', '1X', 'd'),
    ('qDer', '=B', 'q2', '=B', 'd'),
    ('q2[0]', '0B', 'qIzq', '0Y', 'i'),
    ('q2[1]', '0B', 'qIzq', '1Y', 'i'),
    ('q2', '0Y', 'q2', '0Y', 'd'),
    ('q2', '1Y', 'q2', '1Y', 'd'),
    ('q2', 'BB', 'qIzq', 'BB', 'i'),
    ('qIzq', '0B', 'qIzq', '0B', 'i'),
    ('qIzq', '1B', 'qIzq', '1B', 'i'),
    ('qIzq', '0X', 'qIzq', '0X', 'i'),
    ('qIzq', '1X', 'qIzq', '1X', 'i'),
    ('qIzq', '0Y', 'qIzq', '0Y', 'i'),
    ('qIzq', '1Y', 'qIzq', '1Y', 'i'),
    ('qIzq', '=B', 'qIzq', '=B', 'i'),
    ('qIzq', 'BB', 'q0', 'BB', 'd');


    -- VERIFICO QUE LOS CARACTERES ENVIADOS SEAN PARTE DEL ALFABETO
    FOR i IN 1..longitud LOOP
        caracter := SUBSTRING(input_string FROM i FOR 1);
        IF NOT EXISTS (SELECT 1 FROM alfabeto WHERE alfabeto = caracter) THEN
            RAISE EXCEPTION 'Carácter "%" no permitido en el alfabeto', caracter;
        END IF;
    END LOOP;

    -- CONSTRUYO LA MATRIZ CON EL SIMULADORMT Y LUEGO EJECUTO EL PROGRAMA CON ESA MATRIZ
    SELECT fila1, fila2 INTO resultado1, resultado2 FROM simuladorMT(input_string);
	PERFORM programa_ej3(resultado1, resultado2);
	RETURN 'fin';
END;
$$ LANGUAGE plpgsql;