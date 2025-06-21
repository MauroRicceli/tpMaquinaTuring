CREATE OR REPLACE FUNCTION programa_ej2(fila1 TEXT[], fila2 TEXT[])
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    columna INTEGER := 2;  -- arrays empiezan en 1 en plpgsql
    cache TEXT := '';
    estado_actual TEXT := 'q0';
BEGIN
    LOOP
        RAISE NOTICE 'Estado: %, Columna: %', estado_actual, columna;
        RAISE NOTICE 'Cache: %', cache;
        RAISE NOTICE 'Fila 1: %', array_to_string(fila1, '');
        RAISE NOTICE 'Fila 2: %', array_to_string(fila2, '');

        --TOMA EL PRIMER CARACTER DEL PRIMER NUMERO Y LO MARCA, PASA A QDER
        IF estado_actual = 'q0' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'X';
                IF cache <> 'R' THEN
                    cache := '0';
                END IF;
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qDer','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'X';
                IF cache <> 'R' THEN
                    cache := '1';
                END IF;
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qDer','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','q0','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','q0','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                IF cache <> 'R' THEN
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '-B','restable','-B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'restable';
                ELSE
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '-B','qDer','-B','S', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    cache := '-';
                    estado_actual := 'qDer';
                END IF;
                CONTINUE;
            END IF;

        --ESTADO QDER, MUEVE A LA DERECHA HASTA ENCONTRAR EL - Y EMPEZAR CON EL SEGUNDO NUMERO, LLAMA A Q1 
        ELSIF estado_actual = 'qDer' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qDer','0B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qDer','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qDer','1B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qDer','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','q1','-B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q1';
                CONTINUE;
            END IF;

        --VERIFICA QUE EL NUMERO EN CACHE SEA MAYOR O IGUAL AL PRIMER NO MARCADO, SI EL NUMERO EN CACHE ES MAYOR ES RESTABLE
        --SI NO LO ES,
        --SI ES IGUAL, MARCA EL NUMERO Y VUELVE A HACER EL PROCESO CON EL SIGUIENTE NUMERO DESDE Q0
        --SI ES MENOR, VERIFICA QUE EL NUMERO DERECHO SEA MAS CORTO QUE EL DE LA IZQUIERDA CON QVERIFICARLONGITUD
        ELSIF estado_actual = 'q1' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                IF cache = '0' THEN
                    fila2[columna] := 'Y';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '0B','qRetry','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    cache := '';
                    estado_actual := 'qRetry';
                    CONTINUE;
                END IF;

                IF cache = '1' THEN
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '0B','qRetry','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    cache := 'R';
                    estado_actual := 'qRetry';
                    CONTINUE;
                END IF;

                IF cache = 'R' THEN
                    fila2[columna] := 'Y';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '0B','qRetry','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'qRetry';
                    CONTINUE;
                END IF;

                IF cache = '-' THEN
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '0B','numero_izq_menor','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'numero_izq_menor';
                    CONTINUE;
                END IF;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','q1','0Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                IF cache = '0' THEN
                    fila2[columna] := 'Y';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '1B','qRetry','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    cache := 'R';
                    estado_actual := 'qRetry';
                    CONTINUE;
                END IF;

                IF cache = '1' THEN
                    fila2[columna] := 'Y';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '1B','qRetry','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    cache := '';
                    estado_actual := 'qRetry';
                    CONTINUE;
                END IF;

                IF cache = 'R' THEN
                    fila2[columna] := 'Y';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '1B','qRetry','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'qRetry';
                    CONTINUE;
                END IF;

                IF cache = '-' THEN
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '1B','numero_izq_menor','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'numero_izq_menor';
                    CONTINUE;
                END IF;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','q1','1Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                IF cache <> '-' THEN
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '=B','restable','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'restable';
                    CONTINUE;
                ELSE
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '=B','numero_izq_menor','=B','S', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    estado_actual := 'numero_izq_menor';
                    CONTINUE;
                END IF;
            END IF;
        

        ELSIF estado_actual = 'numero_izq_menor' THEN
            PERFORM finalizar_maquina_menor();
            EXIT;

        --SE MUEVE HACIA EL BB DEL INICIO PARA VOLVER A INICIAR EL PROCESO DE COMPROBACION, LUEGO LLAMA A Q0
        ELSIF estado_actual = 'qRetry' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qRetry','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qRetry','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','qRetry','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','qRetry','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qRetry','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qRetry','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','qRetry','-B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, 'BB','q0','BB','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            END IF;


        --SE MUEVE A LA DERECHA DE TODO EL STRING PARA LLAMAR A REINICIAR MARCADO
        ELSIF estado_actual = 'restable' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','restable','0B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','restable','0Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','restable','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','restable','1B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','restable','1Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','restable','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','restable','-B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','reiniciar_marcado','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'reiniciar_marcado';
                CONTINUE;
            END IF;


        --RECORRE TODO EL STRING DE DERECHA A IZQUIERDA REINICIANDO TODOS LOS MARCADOS, LUEGO LLAMA A INICIAR RESTA
        ELSIF estado_actual = 'reiniciar_marcado' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','reiniciar_marcado','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','reiniciar_marcado','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                fila2[columna] := 'B';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','reiniciar_marcado','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                fila2[columna] := 'B';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','reiniciar_marcado','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                fila2[columna] := 'B';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','reiniciar_marcado','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                fila2[columna] := 'B';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','reiniciar_marcado','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','reiniciar_marcado','-B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, 'BB','iniciarResta','BB','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'iniciarResta';
                CONTINUE;
            END IF;


        --ESTADO INICIAR RESTA, SE LLAMA LUEGO DE LA COMPROBACION Y SE MUEVE HASTA EL PRIMER NUMERO (DESDE LA DERECHA) A RESTAR.
        --CUANDO LLEGA AL = SIGNIFICA QUE YA PUEDO VER EL NUMERO QUE RESTA, POR LO TANTO PASO A Q10
        ELSIF estado_actual = 'iniciarResta' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','iniciarResta','0B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','iniciarResta','1B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','iniciarResta','0Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','iniciarResta','1Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','iniciarResta','-B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','q10','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'q10';
                CONTINUE;
            END IF;

        --BUSCO DE DERECHA A IZQUIERDA LOS NUMEROS DEL NUMERO QUE ESTA RESTANDO. SI ENCUENTRO UN 0 SIN MARCAR LO MARCO Y SIGO BUSCANDO UN 1 YA QUE NO ME AFECTA EN LA RESTA.
        --SI ENCUENTRO UN 1 SIN MARCAR, LO MARCO Y LLAMO A QDER RESTA, QUE SE ENCARGA DE IR HASTA EL FINAL DEL STRING.
        ELSIF estado_actual = 'q10' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'Y';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qDerResta','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                cache := '0';
                columna := columna - 1;
                estado_actual := 'qDerResta';
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'Y';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qDerResta','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                cache := '1';
                columna := columna - 1;
                estado_actual := 'qDerResta';
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','q10','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','q10','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','qFinal','-B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qFinal';
                CONTINUE;
            END IF;


        --SE MUEVE HASTA EL FINAL DEL STRING.
        ELSIF estado_actual = 'qDerResta' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qDerResta','0B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qDerResta','1B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','qDerResta','0Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','qDerResta','1Y','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qDerResta','1X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qDerResta','0X','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','qDerResta','-B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','qDerResta','=B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, 'BB','q11','BB','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'q11';
                CONTINUE;
            END IF;


        --HACE LA RESTA EN ORDEN DE DERECHA A IZQUIERDA.
        ELSIF estado_actual = 'q11' THEN
            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                IF cache = '0' THEN
                    fila2[columna] := 'X';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '1B','qIzq','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                END IF;

                IF cache = '1' THEN
                    fila1[columna] := '0';
                    fila2[columna] := 'X';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '1B','qIzq','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                END IF;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                IF cache = '0' THEN
                    fila2[columna] := 'X';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '0B','qIzq','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                END IF;

                IF cache = '1' THEN
                    fila1[columna] := '1';
                    fila2[columna] := 'X';
                    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				    (estado_actual, '0B','qPrestamo','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                    columna := columna - 1;
                    estado_actual := 'qPrestamo';
                    CONTINUE;
                END IF;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','q11','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','q11','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','qFinal','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qFinal';
                CONTINUE;
            END IF;


        --LLEGA HASTA EL PRINCIPIO DEL SEGUNDO NUMERO (EL QUE ESTA LUEGO DEL -), Y LLAMA A INICIAR RESTA.
        ELSIF estado_actual = 'qIzq' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qIzq','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qIzq','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0Y','qIzq','0Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1Y','qIzq','1Y','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qIzq','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qIzq','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','qIzq','=B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '-' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '-B','iniciarResta','-B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'iniciarResta';
                CONTINUE;
            END IF;


        --CONVIERTE TODOS LOS 0 QUE ENCUENTRA EN EL CAMINO A 1, CUANDO ENCUENTRA UN 1 PARA PRESTAR QUE NO ESTE MARCADO, LO PONE EN 0 Y LLAMA A QIZQ
        ELSIF estado_actual = 'qPrestamo' THEN
            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                fila1[columna] := '0';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1B','qIzq','0B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                estado_actual := 'qIzq';
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                fila1[columna] := '1';
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0B','qPrestamo','1B','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '1X','qPrestamo','1X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '0X','qPrestamo','0X','i', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna - 1;
                CONTINUE;
            END IF;

            IF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				(estado_actual, '=B','q10','=B','d', columna, array_to_string(fila1, '') || E'\n' || array_to_string(fila2, ''));
                columna := columna + 1;
                estado_actual := 'q10';
                CONTINUE;
            END IF;

        ELSIF estado_actual = 'qFinal' THEN
            PERFORM finalizar_maquina();
            EXIT;
        END IF;
    END LOOP;
END;
$$;
