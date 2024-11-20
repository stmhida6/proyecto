import pika
import mysql.connector
import time
import json
import os

#variables de enterno de mysql
mysql_host = os.environ['MYSQL_HOST']
mysql_db = os.environ['MYSQL_DATABASE']
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_root_password = os.environ['MYSQL_ROOT_PASSWORD']
mysql_root= 'root'


def guardar_en_bd(nombre, telefono, requerimiento):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            database=mysql_db,
            user=mysql_user,
            password=mysql_password
        )
        cursor = connection.cursor()
        query = "INSERT INTO REQUERIMIENTO (nombre, telefono, requerimiento) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, telefono, requerimiento))
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Requerimiento guardado en la base de datos: {nombre}, {telefono}, {requerimiento}")
    except mysql.connector.Error as err:
        print(f"Error al guardar en base de datos: {err}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-sabados'))
    canal = connection.channel()
    canal.queue_declare(queue='app-sabados-queue')

    def callback(ch, method, properties, body):
        print(f"Mensaje recibido: {body}")
        try:
            mensaje = json.loads(body)
            guardar_en_bd(mensaje['nombre'], mensaje['telefono'], mensaje['requerimiento'])
            #print deliver tag
            print("deliver tag " + str(method.delivery_tag))
            #ch.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError:
            print("Error al decodificar el mensaje")
        except KeyError:
            print("Error al obtener los datos del mensaje")

    canal.basic_consume(
        queue='app-sabados-queue', on_message_callback=callback, auto_ack=True
    )

    print("Esperando mensajes en la cola 'app-sabados-queue'. Para salir, presiona CTRL+C")
    canal.start_consuming()

if __name__ == "__main__":
    while True:
        try:
            main()
        except pika.exceptions.AMQPConnectionError:
            print("Intentando reconectar a RabbitMQ...")
            time.sleep(5)
