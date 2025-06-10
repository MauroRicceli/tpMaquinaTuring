CREATE OR REPLACE FUNCTION simuladorMT(input_string TEXT)
RETURNS TEXT[][] AS $$
DECLARE
    longitud INTEGER := LENGTH(input_string);
    columnas INTEGER := longitud + 2;  -- B al inicio y B al final
    matriz TEXT[][];
    fila1 TEXT[];
    fila2 TEXT[];
    i INTEGER;
BEGIN
    -- Construyo primera fila: B + caracteres + B
    fila1 := ARRAY['B'];
    FOR i IN 1..longitud LOOP
        fila1 := array_append(fila1, SUBSTRING(input_string FROM i FOR 1));
    END LOOP;
    fila1 := array_append(fila1, 'B');

    -- lleno la segunda fila de 'B'
    fila2 := ARRAY[]::TEXT[];
    FOR i IN 1..columnas LOOP
        fila2 := array_append(fila2, 'B');
    END LOOP;

    -- formo la matriz
    matriz := ARRAY[fila1, fila2];

    RETURN matriz;
END;
$$ LANGUAGE plpgsql;