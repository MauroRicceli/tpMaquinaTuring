CREATE OR REPLACE FUNCTION programa1(input_string TEXT)
RETURNS TEXT AS $$
DECLARE
    longitud INTEGER := LENGTH(input_string);
    caracter TEXT;
    i INTEGER;
    resultado TEXT[][];
BEGIN
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

    INSERT INTO programa (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento) VALUES
    ('q0', '1B', 'qDer', '1X', 'd'),
    ('q0', '0B', 'qDer', '0X', 'd'),
    ('q0', '1X', 'q0', '1X', 'd'),
    ('q0', '0X', 'q0', '0X', 'd'),
    ('q0', '=B', 'q1', '=B', 'd'),

    ('qDer', '0B', 'qDer', '0B', 'd'),
    ('qDer', '1B', 'qDer', '1B', 'd'),
    ('qDer', '0X', 'qDer', '0X', 'd'),
    ('qDer', '=B', 'q1', '=B', 'd'),

    ('q1[0]', '0B', 'qIzq', '0Y', 'i'),
    ('q1[1]', '0B', 'distintos', '0Y', 'i'),
    ('q1[1]', '1B', 'qIzq', '1Y', 'i'),
    ('q1[0]', '1B', 'distintos', '1Y', 'i'),

    ('q1[0]', '1Y', 'q1[0]', '1Y', 'd'),
    ('q1[1]', '1Y', 'q1[1]', '1Y', 'd'),
    ('q1[0]', '0Y', 'q1[0]', '0Y', 'd'),
    ('q1[1]', '0Y', 'q1[0]', '0Y', 'd'),

    ('q1[0]', 'BB', 'distintos', 'BY', 'i'),
    ('q1[1]', 'BB', 'distintos', 'BY', 'i'),
    ('q1[=]', 'BB', 'iguales', 'BY', 'i'),

    ('qIzq', '0B', 'qIzq', '0B', 'i'),
    ('qIzq', '1B', 'qIzq', '1B', 'i'),
    ('qIzq', '0Y', 'qIzq', '0Y', 'i'),
    ('qIzq', '1Y', 'qIzq', '1Y', 'i'),
    ('qIzq', '0X', 'qIzq', '0X', 'i'),
    ('qIzq', '1X', 'qIzq', '1X', 'i'),
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
    resultado := simuladorMT(input_string);
	PERFORM programa_ej1(resultado);
	RETURN 'fin';
END;
$$ LANGUAGE plpgsql;