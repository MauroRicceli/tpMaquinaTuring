CREATE OR REPLACE FUNCTION programa_ej1(fila1 TEXT[], fila2 TEXT[])
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
            IF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                cache := '1';
                fila2[columna] := 'X';
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                cache := '0';
                fila2[columna] := 'X';
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                cache := '=';
                columna := columna + 1;
                estado_actual := 'q1';
                CONTINUE;
            ELSE
                EXIT;
            END IF;

        ELSIF estado_actual = 'qDer' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                columna := columna + 1;
                estado_actual := 'q1';
                CONTINUE;
            ELSE
                EXIT;
            END IF;

        ELSIF estado_actual = 'q1' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'Y';
                IF cache = '0' THEN
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                ELSE
                    PERFORM distintos();
                    EXIT;
                END IF;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'Y';
                IF cache = '1' THEN
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                ELSE
                    PERFORM distintos();
                    EXIT;
                END IF;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                fila2[columna] := 'Y';
                IF cache = '=' THEN
                    PERFORM iguales();
                    EXIT;
                ELSE
                    PERFORM distintos();
                    EXIT;
                END IF;
            ELSE
                EXIT;
            END IF;

        ELSIF estado_actual = 'qIzq' THEN
            IF fila1[columna] = '0' AND fila2[columna] = 'B' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'B' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'Y' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'Y' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = '0' AND fila2[columna] = 'X' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = '1' AND fila2[columna] = 'X' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = '=' AND fila2[columna] = 'B' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF fila1[columna] = 'B' AND fila2[columna] = 'B' THEN
                columna := columna + 1;
                estado_actual := 'q0';
                CONTINUE;
            ELSE
                EXIT;
            END IF;

        ELSE
            EXIT;
        END IF;
    END LOOP;
END;
$$;