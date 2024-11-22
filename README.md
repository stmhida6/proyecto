
# Sistema Distribuido de Procesamiento de Tarjeta de Crédito

## Descripción
Este proyecto implementa el backend para un procesador distribuido de tarjetas de crédito. Su objetivo principal es migrar de un sistema monolítico a una arquitectura distribuida, mejorando la eficiencia y escalabilidad. El sistema incluye:

- Una API REST para creación y procesamiento de tarjetas de crédito.
- Balanceo de carga con NGINX utilizando el algoritmo ROUND-ROBIN.
- Sistema desacoplado de mensajería asíncrona mediante RabbitMQ.
- Base de datos MySQL desacoplada del núcleo principal.

## Características Principales
- Creación, consulta, modificación y eliminación de tarjetas de crédito.
- Procesamiento de cargos y abonos con validación de límites de crédito.
- Envío de notificaciones por SMS simuladas al realizar transacciones.
- Sistema de mensajería basado en colas para manejo asíncrono de eventos.
- Integración con Docker para despliegue y contenedorización.

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/proyecto.git
   cd proyecto
   ```



2. Configura Docker para los servicios del sistema:
   ```bash
   docker-compose up --build
   ```

3. Asegúrate de tener configurados NGINX y RabbitMQ.

## Uso
1. Inicia el proyecto:
   ```bash
   npm start
   ```

2. Accede a la API REST en `http://localhost:3000`.

3. Endpoints principales:
   - **Tarjetas de Crédito**:
     - `GET /tarjeta-credito`: Obtiene todas las tarjetas.
     - `POST /tarjeta-credito`: Crea una tarjeta nueva.
     - `GET /tarjeta-credito/:id`: Consulta por PAN.
     - `PUT /tarjeta-credito/:id`: Actualiza datos de la tarjeta.
     - `DELETE /tarjeta-credito/:id`: Elimina tarjeta (validando saldo).
   - **Procesamiento**:
     - `POST /tarjeta-credito/procesamiento/:id`: Realiza un cargo.
     - `POST /tarjeta-credito/abono/:id`: Realiza un abono.
   - **Mensajería**:
     - Los SMS simulados se registran en la tabla de mensajería.

## Tecnologías Utilizadas
- **Lenguaje**: Python (Flask).
- **Base de Datos**: MySQL.
- **Balanceador de Carga**: NGINX.
- **Mensajería Asíncrona**: RabbitMQ.
- **Contenedores**: Docker.

## Contribución
¡Contribuciones son bienvenidas! Sigue estos pasos para colaborar:

1. Haz un fork del repositorio.
2. Crea una rama para tu feature:
   ```bash
   git checkout -b feature/nueva-feature
   ```
3. Realiza tus cambios y haz commit:
   ```bash
   git commit -am "Añadir nueva feature"
   ```
4. Sube tus cambios:
   ```bash
   git push origin feature/nueva-feature
   ```
5. Abre un Pull Request para revisión.

## Licencia
Este proyecto está licenciado bajo [MIT License](LICENSE).

