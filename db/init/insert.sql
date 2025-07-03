-- CIRCUITOS
INSERT INTO Circuito (numero_circuito, cerrado) VALUES
(1, FALSE),
(2, FALSE),
(3, FALSE),
(4, FALSE),
(5, FALSE);

-- CIUDADANOS
INSERT INTO Ciudadano (numero_credencial, CI, nombre, apellido, edad) VALUES
('ABC1234', '45678901', 'Laura', 'Pérez', 30),
('DEF5678', '56789012', 'Martín', 'Díaz', 35),
('GHI9012', '67890123', 'María', 'González', 28),
('JKL3456', '78901234', 'Juan', 'Torres', 40),
('MNO7890', '89012345', 'Ana', 'Fernández', 22),
('PQR2345', '90123456', 'Sofía', 'Suárez', 33),
('STU6789', '34567890', 'Diego', 'Castro', 27),
('VWX1234', '23456789', 'Lucía', 'Ramos', 31),
('YZA5678', '12345678', 'Carlos', 'López', 38),
('BCD9012', '01234567', 'Valentina', 'Silva', 29); -- ESTE NO SE LE ASIGNARÁ NINGUNA ELECCIÓN

-- ELECCIONES
INSERT INTO Eleccion (id_eleccion, fecha, tipo, status) VALUES
(1, '2025-10-01', 'Presidencial', TRUE),
(2, '2025-11-01', 'Municipal', TRUE),
(3, '2025-12-01', 'Ballotage', TRUE),
(4, '2025-09-15', 'Plebiscito', TRUE),
(5, '2025-09-20', 'Referendum', TRUE);

-- ACTOS ELECTORALES (para todos menos 'BCD9012')
INSERT INTO Acto_Electoral (numero_credencial, id_eleccion, numero_circuito, voto_emitido) VALUES
-- ABC1234
('ABC1234', 1, 1, FALSE),
('ABC1234', 2, 2, FALSE),
('ABC1234', 3, 3, FALSE),
('ABC1234', 4, 4, FALSE),
('ABC1234', 5, 5, FALSE),
-- DEF5678
('DEF5678', 1, 1, FALSE),
('DEF5678', 2, 2, FALSE),
('DEF5678', 3, 3, FALSE),
('DEF5678', 4, 4, FALSE),
('DEF5678', 5, 5, FALSE),
-- GHI9012
('GHI9012', 1, 1, FALSE),
('GHI9012', 2, 2, FALSE),
('GHI9012', 3, 3, FALSE),
('GHI9012', 4, 4, FALSE),
('GHI9012', 5, 5, FALSE),
-- JKL3456
('JKL3456', 1, 1, FALSE),
('JKL3456', 2, 2, FALSE),
('JKL3456', 3, 3, FALSE),
('JKL3456', 4, 4, FALSE),
('JKL3456', 5, 5, FALSE),
-- MNO7890
('MNO7890', 1, 1, FALSE),
('MNO7890', 2, 2, FALSE),
('MNO7890', 3, 3, FALSE),
('MNO7890', 4, 4, FALSE),
('MNO7890', 5, 5, FALSE),
-- PQR2345
('PQR2345', 1, 1, FALSE),
('PQR2345', 2, 2, FALSE),
('PQR2345', 3, 3, FALSE),
('PQR2345', 4, 4, FALSE),
('PQR2345', 5, 5, FALSE),
-- STU6789
('STU6789', 1, 1, FALSE),
('STU6789', 2, 2, FALSE),
('STU6789', 3, 3, FALSE),
('STU6789', 4, 4, FALSE),
('STU6789', 5, 5, FALSE),
-- VWX1234
('VWX1234', 1, 1, FALSE),
('VWX1234', 2, 2, FALSE),
('VWX1234', 3, 3, FALSE),
('VWX1234', 4, 4, FALSE),
('VWX1234', 5, 5, FALSE),
-- YZA5678
('YZA5678', 1, 1, FALSE),
('YZA5678', 2, 2, FALSE),
('YZA5678', 3, 3, FALSE),
('YZA5678', 4, 4, FALSE),
('YZA5678', 5, 5, FALSE);

-- LISTAS PARA CADA TIPO
-- Presidenciales
INSERT INTO Lista (id) VALUES (1), (2), (3), (4);
INSERT INTO Lista_Presidencial (id, presidente, vicepresidente, senadores, diputados) VALUES
(1, 'Laura Pérez', 'Martín Díaz', 'Senador A, Senador B', 'Diputado A, Diputado B'),
(2, 'Martín Díaz', 'Laura Pérez', 'Senador C, Senador D', 'Diputado C, Diputado D'),
(3, 'María González', 'Juan Torres', 'Senador E, Senador F', 'Diputado E, Diputado F'),
(4, 'Juan Torres', 'María González', 'Senador G, Senador H', 'Diputado G, Diputado H');

-- Municipales
INSERT INTO Lista (id) VALUES (5), (6), (7), (8);
INSERT INTO Lista_Municipal (id, candidato) VALUES
(5, 'María González'),
(6, 'Juan Torres'),
(7, 'Lucía Ramos'),
(8, 'Carlos López');

-- Ballotage
INSERT INTO Lista (id) VALUES (9), (10), (11), (12);
INSERT INTO Lista_Ballotage (id, candidato) VALUES
(9, 'Laura Pérez'),
(10, 'Martín Díaz'),
(11, 'María González'),
(12, 'Juan Torres');

-- Plebiscito y Referendum
INSERT INTO Lista (id) VALUES (13), (14);
INSERT INTO Papeleta (id, opcion) VALUES
(13, 'Si'),
(14, 'No');

-- ADMIN
INSERT INTO Admin (usuario, contrasena) VALUES ('admin1', 'admin1');