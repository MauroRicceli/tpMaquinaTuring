CREATE OR REPLACE FUNCTION finalizar_maquina_menor()
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO traza_ejecucion(estado_origen, caracter_origen, estado_nuevo, caracter_nuevo, desplazamiento, columna_actual, estado_string) VALUES
				('Máquina finalizada. Numero izquierdo menor al que le esta restando. Fin prematuro', '','','','','','');
END;
$$;