CREATE OR REPLACE FUNCTION programa_ej1(cinta1 TEXT[], cinta2 TEXT[])
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    columna INTEGER := 2;
    cache CHAR;
    estado_actual TEXT := 'q0';
BEGIN
    LOOP
        RAISE NOTICE 'Estado: %, Columna: %', estado_actual, columna;
        RAISE NOTICE 'Cache: %', cache;
        RAISE NOTICE 'Fila 1: %', array_to_string(cinta1, '');
        RAISE NOTICE 'Fila 2: %', array_to_string(cinta2, '');

        IF estado_actual = 'q0' THEN
            IF cinta1[columna] = '1' AND cinta2[columna] = 'B' THEN
                cache := '1';
                cinta2[columna] := 'X';
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF cinta1[columna] = '0' AND cinta2[columna] = 'B' THEN
                cache := '0';
                cinta2[columna] := 'X';
                columna := columna + 1;
                estado_actual := 'qDer';
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '0' AND cinta2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '=' AND cinta2[columna] = 'B' THEN
                cache := '=';
                columna := columna + 1;
                estado_actual := 'q1';
                CONTINUE;
            ELSE
                EXIT;
            END IF;

        ELSIF estado_actual = 'qDer' THEN
            IF cinta1[columna] = '0' AND cinta2[columna] = 'B' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'B' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '0' AND cinta2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'X' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '=' AND cinta2[columna] = 'B' THEN
                columna := columna + 1;
                estado_actual := 'q1';
                CONTINUE;
            ELSE
                EXIT;
            END IF;

        ELSIF estado_actual = 'q1' THEN
            IF cinta1[columna] = '0' AND cinta2[columna] = 'B' THEN
                cinta2[columna] := 'Y';
                IF cache = '0' THEN
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                ELSE
                    PERFORM distintos();
                    EXIT;
                END IF;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'B' THEN
                cinta2[columna] := 'Y';
                IF cache = '1' THEN
                    columna := columna - 1;
                    estado_actual := 'qIzq';
                    CONTINUE;
                ELSE
                    PERFORM distintos();
                    EXIT;
                END IF;
            ELSIF cinta1[columna] = '0' AND cinta2[columna] = 'Y' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'Y' THEN
                columna := columna + 1;
                CONTINUE;
            ELSIF cinta1[columna] = 'B' AND cinta2[columna] = 'B' THEN
                cinta2[columna] := 'Y';
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
            IF cinta1[columna] = '0' AND cinta2[columna] = 'B' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'B' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = '0' AND cinta2[columna] = 'Y' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'Y' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = '0' AND cinta2[columna] = 'X' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = '1' AND cinta2[columna] = 'X' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = '=' AND cinta2[columna] = 'B' THEN
                columna := columna - 1;
                CONTINUE;
            ELSIF cinta1[columna] = 'B' AND cinta2[columna] = 'B' THEN
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