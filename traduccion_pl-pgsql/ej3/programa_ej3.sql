CREATE OR REPLACE FUNCTION programa_ej3(fila1 TEXT[], fila2 TEXT[])
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    columna INTEGER := 2;
    cache CHAR;
    estado_actual TEXT := 'q0';
BEGIN
    LOOP
        RAISE NOTICE 'Estado: %, Columna: %', estado_actual, columna;
        RAISE NOTICE 'Cache: %', cache;
        RAISE NOTICE 'Fila 1: %', array_to_string(fila1, '');
        RAISE NOTICE 'Fila 2: %', array_to_string(fila2, '');

        IF estado_actual = 'q0' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','q0','0B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','q0','1B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','q0','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','q0','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            ELSIF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','q1','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'q1';
                CONTINUE;
        END IF;

        ELSIF estado_actual = 'q1' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'X';
                estado_actual := 'qDer';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qDer','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                cache := '0';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qDer','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                fila2[columna] := 'X';
                estado_actual := 'qDer';
                columna := columna + 1;
                cache := '1';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','q1','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'q1';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','q1','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'q1';
                CONTINUE;
            ELSIF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, 'BB','fin','BB','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'fin';
                CONTINUE;
            END IF;

        ELSIF estado_actual = 'qDer' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qDer','0B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qDer','1B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qDer','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qDer','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));  
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','q2','=B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q2';
                CONTINUE;
            END IF;

        ELSIF estado_actual = 'q2' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qIzq',cache || 'Y' ,'i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                fila1[columna] := cache;
                fila2[columna] := 'Y';
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','q2','0Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q2';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','q2','1Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q2';
                CONTINUE;
            ELSIF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, 'BB','qIzq','BB','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            END IF;

        ELSIF estado_actual = 'qIzq' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qIzq','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qIzq','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qIzq','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qIzq','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','qIzq','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','qIzq','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','qIzq','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            ELSIF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, 'BB','q0','BB','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            END IF;

        ELSIF estado_actual = 'fin' THEN
            INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
			(estado_actual,'','','','', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
            RAISE NOTICE 'Fin de la ejecución';
            EXIT;
        END IF;

    END LOOP;
END;
$$;