-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS obligatoriobd2;
USE obligatoriobd2;

-- Crear tablas
CREATE TABLE Circuito (
    numero_circuito INT PRIMARY KEY,
    cerrado BOOLEAN DEFAULT FALSE
);

CREATE TABLE Eleccion (
    id_eleccion INT PRIMARY KEY,
    fecha DATE,
    tipo VARCHAR(50),
    status BOOLEAN DEFAULT TRUE
);

CREATE TABLE Ciudadano (
    numero_credencial VARCHAR(10) PRIMARY KEY,
    CI VARCHAR(20),
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    edad INT
);

CREATE TABLE Acto_Electoral (
    numero_credencial VARCHAR(10),
    id_eleccion INT,
    numero_circuito INT,
    voto_emitido BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (numero_credencial, id_eleccion),
    FOREIGN KEY (numero_credencial) REFERENCES Ciudadano(numero_credencial),
    FOREIGN KEY (id_eleccion) REFERENCES Eleccion(id_eleccion),
    FOREIGN KEY (numero_circuito) REFERENCES Circuito(numero_circuito)
);

CREATE TABLE Lista (
    id INT PRIMARY KEY
);

CREATE TABLE Papeleta (
    id INT PRIMARY KEY,
    opcion VARCHAR(100),
    FOREIGN KEY (id) REFERENCES Lista(id)
);

CREATE TABLE Lista_Presidencial (
    id INT PRIMARY KEY,
    presidente VARCHAR(100),
    vicepresidente VARCHAR(100),
    senadores TEXT,
    diputados TEXT,
    FOREIGN KEY (id) REFERENCES Lista(id)
);

CREATE TABLE Lista_Ballotage (
    id INT PRIMARY KEY,
    candidato VARCHAR(100),
    FOREIGN KEY (id) REFERENCES Lista(id)
);

CREATE TABLE Lista_Municipal (
    id INT PRIMARY KEY,
    candidato VARCHAR(100),
    FOREIGN KEY (id) REFERENCES Lista(id)
);

CREATE TABLE Voto (
    id_voto INT PRIMARY KEY AUTO_INCREMENT,
    id_lista INT,
    fecha DATE,
    condicion VARCHAR(50),
    numero_circuito INT,
    FOREIGN KEY (id_lista) REFERENCES Lista(id),
    FOREIGN KEY (numero_circuito) REFERENCES Circuito(numero_circuito)
);

CREATE TABLE Admin (
    usuario VARCHAR(50) PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL
);