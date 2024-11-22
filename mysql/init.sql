-- mysql/init.sql
CREATE DATABASE IF NOT EXISTS tarjetas_db;
USE tarjetas_db;

-- Tabla para almacenar la información de clientes y sus tarjetas de crédito
CREATE TABLE tarjetas (
    id_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    pan VARCHAR(16) NOT NULL UNIQUE, 
    nombre VARCHAR(100) NOT NULL,   
    apellidos VARCHAR(100) NOT NULL, 
    edad INT NOT NULL,              
    direccion VARCHAR(255) NOT NULL, 
    no_telefono VARCHAR(10) NOT NULL, 
    datos_laborales TEXT,            
    datos_beneficiarios TEXT,        
    dpi VARCHAR(13) NOT NULL UNIQUE, 
    fecha_vencimiento DATE NOT NULL, 
    estado VARCHAR(50) NOT NULL,     
    id_replica VARCHAR(50)           
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
