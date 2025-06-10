-- Las funciones distintas() y qIguales() igual que antes
CREATE OR REPLACE FUNCTION distintos()
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO traza_ejecucion(estado_origen) VALUES ('Los numeros son distintos');
END;
$$;