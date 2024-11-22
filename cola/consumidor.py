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


def guardar_en_bd(mensaje, telefono, pan,fecha_envio,estado,id_tarjeta):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_root,
            password=mysql_root_password,
            database=mysql_db
        )
        print("Conexión a base de datos exitosa")
        print(f"Mensaje: {mensaje}, Telefono: {telefono}, Fecha de envio: {fecha_envio}, Estado: {estado}, Id tarjeta: {id_tarjeta}")
        cursor = connection.cursor()
        query = "INSERT INTO mensajeria (texto, numero_telefono, fecha_envio, estado, id_tarjeta) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (mensaje, telefono, fecha_envio, estado, id_tarjeta))
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Requerimiento guardado en la base de datos: {mensaje}, {telefono},  {fecha_envio}, {estado}, {id_tarjeta}")
    except mysql.connector.Error as err:
        print(f"Error al guardar en base de datos: {err}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-sabados'))
    canal = connection.channel()
    canal.queue_declare(queue='app-sabados-queue')

    def callback(ch, method, properties, body):
        print(f"Mensaje recibido: {body}")
        try:
            fecha_envio= time.strftime("%Y-%m-%d %H:%M:%S")
            estado= "enviado"
            id_tarjeta=1
            mensaje = json.loads(body)
            # Guardar en base de datos
            guardar_en_bd(mensaje['mensaje'], mensaje['no_telefono'], mensaje['pan'],fecha_envio,estado,id_tarjeta)
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
