CREATE OR REPLACE FUNCTION insertar_alfabeto1()
RETURNS VOID AS $$
BEGIN
    DELETE FROM alfabeto;

    INSERT INTO alfabeto (alfabeto) VALUES
    ('1'),
    ('0'),
    ('B'),
    ('X'),
    ('Y'),
    ('=');
END;
$$ LANGUAGE plpgsql;