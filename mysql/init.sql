-- mysql/init.sql
CREATE DATABASE IF NOT EXISTS tarjetas_db;
USE tarjetas_db;

-- Tabla para almacenar la información de clientes y sus tarjetas de crédito
CREATE TABLE tarjetas (
    id_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    pan VARCHAR(16) NOT NULL UNIQUE, -- Número de tarjeta de crédito
    nombre VARCHAR(100) NOT NULL,    -- Nombre del cliente
    apellidos VARCHAR(100) NOT NULL, -- Apellidos del cliente
    edad INT NOT NULL,               -- Edad del cliente
    direccion VARCHAR(255) NOT NULL, -- Dirección del cliente
    no_telefono VARCHAR(10) NOT NULL, -- Teléfono del cliente
    datos_laborales TEXT,            -- Información laboral del cliente
    datos_beneficiarios TEXT,        -- Información de beneficiarios del cliente
    dpi VARCHAR(13) NOT NULL UNIQUE, -- DPI único del cliente
    fecha_vencimiento DATE NOT NULL, -- Fecha de vencimiento de la tarjeta
    estado VARCHAR(50) NOT NULL,     -- Estado de la tarjeta (activo, bloqueado, etc.)
    id_replica VARCHAR(50)           -- ID de réplica para sincronización
);

-- Tabla para almacenar el balance de las tarjetas
CREATE TABLE balances (
    pan VARCHAR(16),
    limite DECIMAL(10,2),
    actual DECIMAL(10,2),
    id_replica VARCHAR(50),
    FOREIGN KEY (pan) REFERENCES tarjetas(pan)
);

-- Tabla para almacenar los mensajes de mensajería
CREATE TABLE mensajeria (
    id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
    numero_telefono VARCHAR(15) NOT NULL,
    texto TEXT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_envio DATETIME NOT NULL,
    id_tarjeta INT NOT NULL,
    FOREIGN KEY (id_tarjeta) REFERENCES tarjetas(id_tarjeta)
);
