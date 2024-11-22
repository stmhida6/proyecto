# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos a la imagen del contenedor
COPY . /app

# Instala las dependencias
RUN pip install flask pika mysql-connector-python

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python","-u","app.py"]