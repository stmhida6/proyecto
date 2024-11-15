-- mysql/init.sql
CREATE DATABASE IF NOT EXISTS tarjetas_db;
USE tarjetas_db;

-- Tabla para almacenar la información del cliente
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    datos_laborales TEXT,
    datos_beneficiarios TEXT,
    dpi VARCHAR(13) NOT NULL UNIQUE
);

-- Tabla para almacenar las tarjetas de crédito
CREATE TABLE tarjetas_credito (
    pan VARCHAR(16) PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Tabla para almacenar el balance de las tarjetas de crédito
CREATE TABLE balances (
    pan VARCHAR(16),
    limite DECIMAL(10,2),
    actual DECIMAL(10,2),
    FOREIGN KEY (pan) REFERENCES tarjetas_credito(pan)
);
