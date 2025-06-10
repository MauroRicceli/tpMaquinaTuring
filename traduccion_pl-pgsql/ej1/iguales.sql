--se confirma que los numeros son iguales
CREATE OR REPLACE FUNCTION iguales()
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO traza_ejecucion(estado_origen) VALUES ('Los numeros son iguales');
END;
$$;