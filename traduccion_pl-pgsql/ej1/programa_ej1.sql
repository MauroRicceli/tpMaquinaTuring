CREATE OR REPLACE FUNCTION programa_ej1(multicinta TEXT[][])
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    columna INTEGER := 2;  -- arrays empiezan en 1 en plpgsql
    cache CHAR;
    estado_actual TEXT := 'q0';

BEGIN
    LOOP
		RAISE NOTICE 'Estado: %, Columna: %', estado_actual, columna;
		
		--BUSCA EL PRIMER NUMERO POSIBLE QUE NO ESTE MARCADO CON X DEL NUMERO A LA IZQUIERDA DEL IGUAL.
    	--SI ENCUENTRA ALGUNO VALIDO LO MARCA CON X, LO GUARDA EN CACHE PARA SU USO POSTERIOR Y CAMBIA DE ESTADO
    	--SI LLEGA AL IGUAL VERIFICA QUE EL CARACTER DEL OTRO NUMERO SEA EL BLANCO, SI NO LO ES, SON DE DISTINTA LONGITUD, por lo tanto distintos
        IF estado_actual = 'q0' THEN
            IF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'B' THEN
                cache := '1';
                multicinta[2][columna] := 'X';
                INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1B', 'qDer', '1X', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
                estado_actual := 'qDer';
				CONTINUE;

            ELSIF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'B' THEN
                cache := '0';
                multicinta[2][columna] := 'X';
                INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0B', 'qDer', '0X', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
				columna := columna + 1;
                estado_actual := 'qDer';
				CONTINUE;

            ELSIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'X' THEN
                INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1X', 'q0', '1X', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
				columna := columna + 1;
				CONTINUE;

            ELSIF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'X' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0X', 'q0', '0X', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
				CONTINUE;

            ELSIF multicinta[1][columna] = '=' AND multicinta[2][columna] = 'B' THEN
                cache := '=';
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '=B', 'q1', '=B', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
                estado_actual := 'q1';
				CONTINUE;

            END IF;
		
		--SE MUEVE A LA DERECHA HASTA ENCONTRAR EL IGUAL, LA IDEA ES LLEGAR AL SEGUNDO NUMERO PARA HACER LA COMPARATIVA
        ELSIF estado_actual = 'qDer' THEN
            IF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'B' THEN
                INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0B', 'qDer', '0B', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
				columna := columna + 1;
				CONTINUE;

            ELSIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'B' THEN
                INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1B', 'qDer', '1B', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
				columna := columna + 1;
				CONTINUE;
			
			ELSIF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'X' THEN
                INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0X', 'qDer', '0X', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
				columna := columna + 1;
				CONTINUE;

			ELSIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'X' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1X', 'qDer', '1X', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
				CONTINUE;

            ELSIF multicinta[1][columna] = '=' AND multicinta[2][columna] = 'B' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '=B', 'q1', '=B', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
                estado_actual := 'q1';
				CONTINUE;

            END IF;

		--CON EL VALOR GUARDADO EN CACHE EN Q0, SE VERIFICA QUE EL PRIMER NUMERO NO MARCADO ENCONTRADO TENGA EL MISMO VALOR
    	--SI NO LO TIENE, NO ES IGUAL, Y SE TERMINA SIN ESTADO VALIDO
    	--SI ES IGUAL SE CONTINUA.
        ELSIF estado_actual = 'q1' THEN

            IF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'B' THEN
				multicinta[2][columna] := 'Y';
                IF cache = '0' THEN
					INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0B', 'qIzq', '0Y', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
	                columna := columna - 1;
	                estado_actual := 'qIzq';
					CONTINUE;
                ELSE
					INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0B', 'distintos', '0Y', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                    columna := columna - 1;
					PERFORM distintos();
                    EXIT;	
                END IF;


            ELSIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'B' THEN
				multicinta[2][columna] := 'Y';
                IF cache = '1' THEN
					INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1B', 'qIzq', '1Y', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
	                columna := columna - 1;
	                estado_actual := 'qIzq';
					CONTINUE;
                ELSE
					INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1B', 'distintos', '1Y', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                    columna := columna - 1;
					PERFORM distintos();
                    EXIT;	
                END IF;

			ELSIF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'Y' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0Y', 'q1', '0Y', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
                estado_actual := 'q1';
				CONTINUE;

			ELSIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'Y' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1Y', 'q1', '1Y', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
                estado_actual := 'q1';
				CONTINUE;

			ELSIF multicinta[1][columna] = 'B' AND multicinta[2][columna] = 'B' THEN
				multicinta[2][columna] := 'Y';
                IF cache = '=' THEN
					INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, 'BB', 'iguales', 'BY', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
	                columna := columna - 1;
	                PERFORM iguales();
					EXIT;
                ELSE
					INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, 'BB', 'distintos', 'BY', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                    columna := columna - 1;
					PERFORM distintos();
                    EXIT;	
                END IF;
			END IF;
		
		--TE MOVES A LA IZQUIERDA PARA LLEGAR HASTA EL BB DE LA IZQUIERDA Y VOLVER A CALCULAR Q0 CON EL PROXIMO VALOR SIN MARCAR
        ELSIF estado_actual = 'qIzq' THEN
            IF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'B' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0B', 'qIzq', '0B', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;

			ELSEIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'B' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1B', 'qIzq', '1B', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;

			ELSEIF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'Y' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1Y', 'qIzq', '1Y', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;

			ELSEIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'Y' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1Y', 'qIzq', '1Y', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;
			
			ELSEIF multicinta[1][columna] = '0' AND multicinta[2][columna] = 'X' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '0X', 'qIzq', '0X', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;

			ELSEIF multicinta[1][columna] = '1' AND multicinta[2][columna] = 'X' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '1X', 'qIzq', '1X', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;

			ELSEIF multicinta[1][columna] = '=' AND multicinta[2][columna] = 'B' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, '=B', 'qIzq', '=B', 'i', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna - 1;
				CONTINUE;

			ELSEIF multicinta[1][columna] = 'B' AND multicinta[2][columna] = 'B' THEN
				INSERT INTO traza_ejecucion (estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES (estado_actual, 'BB', 'q0', 'BB', 'd', columna, array_to_string(multicinta[1]::TEXT[], '') || '|' || array_to_string(multicinta[2]::TEXT[], ''));
                columna := columna + 1;
				estado_actual := 'q0';
				CONTINUE;

            END IF;

        END IF;
    END LOOP;
END;
$$;