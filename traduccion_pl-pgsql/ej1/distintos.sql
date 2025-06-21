-- se sabe que el numero es distinto al otro, se sale
CREATE OR REPLACE FUNCTION distintos()
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO traza_ejecucion(estado_origen) VALUES ('Los numeros son distintos');
END;
$$;