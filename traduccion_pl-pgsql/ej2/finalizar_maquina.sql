CREATE OR REPLACE FUNCTION finalizar_maquina()
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				('Máquina finalizada para ejercicio 2', '','','','','','');
END;
$$;