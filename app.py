from flask import Flask, request, jsonify
import mysql.connector
import os
import json
import random
from datetime import datetime
import pika

app = Flask(__name__)

# Variables de entorno para la conexión MySQL
mysql_host = os.environ['MYSQL_HOST']
mysql_db = os.environ['MYSQL_DATABASE']
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_root_password = os.environ['MYSQL_ROOT_PASSWORD']
mysql_root = 'root'

# Establecer conexión con la base de datos MySQL
def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=mysql_host,
            user=mysql_root,
            password=mysql_root_password,
            database=mysql_db
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None

@app.route('/health', methods=['GET'])
def obtener_estado():
    id_contenedor = os.environ.get('HOSTNAME')
    return jsonify({
        'status': 'ok',
        'idContenedor': id_contenedor,
        'mensaje': 'API de tarjetas en Python'
    })

# Crear un cliente y tarjeta en la base de datos
def crear_tarjeta_db(data):
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            id_replica = os.environ.get('HOSTNAME')
            # Generar un PAN aleatorio de 16 dígitos con prefijo 6800
            pan = f"6800{random.randint(100000000000, 999999999999)}"
            fecha_vencimiento = datetime(2027, 12, 31)

            cursor.execute("""
                INSERT INTO tarjetas (pan, nombre, apellidos, edad, direccion, no_telefono, datos_laborales,
                                      datos_beneficiarios, dpi, fecha_vencimiento, estado, id_replica)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (pan, data['nombre'], data['apellidos'], data['edad'], data['direccion'], data['no_telefono'],
                 data.get('datos_laborales'), data.get('datos_beneficiarios'), data['dpi'], fecha_vencimiento,
                 data['estado'], id_replica))
            

            # Balance inicial con la nueva tarjeta (límite de Q5000 y saldo actual de Q0)
            cursor.execute("""
                INSERT INTO balances (pan, limite, actual, id_replica)
                VALUES (%s, %s, %s, %s)
            """, (pan, 5000, 0, id_replica))

            conexion.commit()
            cursor.close()
            conexion.close()
            return pan
        return None
    except mysql.connector.Error as err:
        print(f"Error al insertar tarjeta: {err}")
        return None

# Ruta para crear una nueva tarjeta con información del cliente
@app.route('/tarjeta-credito', methods=['POST'])
def crear_tarjeta():
    data = request.get_json()
    pan = crear_tarjeta_db(data)
    if pan:
        return jsonify({"mensaje": "Cliente y tarjeta creados", "pan": pan}), 201
    else:
        return jsonify({"error": "Error al crear el cliente y la tarjeta"}), 500

# Ruta para obtener todas las tarjetas
@app.route('/tarjeta-credito', methods=['GET'])
def obtener_tarjetas():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarjetas")
        tarjetas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(tarjetas)
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para obtener una tarjeta específica por PAN
@app.route('/tarjeta-credito/<string:pan>', methods=['GET'])
def obtener_tarjeta(pan):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarjetas WHERE pan = %s", (pan,))
        tarjeta = cursor.fetchone()
        cursor.close()
        conexion.close()
        if tarjeta:
            return jsonify(tarjeta)
        else:
            return jsonify({"error": "Tarjeta no encontrada"}), 404
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para actualizar una tarjeta
@app.route('/tarjeta-credito/<string:pan>', methods=['PUT'])
def actualizar_tarjeta(pan):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()

            # Generar dinámicamente la consulta de actualización
            campos = []
            valores = []

            for clave, valor in data.items():
                if clave in ['nombre', 'apellidos', 'edad', 'direccion', 'no_telefono', 'datos_laborales', 
                             'datos_beneficiarios', 'dpi', 'fecha_vencimiento', 'estado', 'id_replica']:
                    campos.append(f"{clave} = %s")
                    valores.append(valor)

            if not campos:
                return jsonify({"error": "No se proporcionaron campos válidos para actualizar"}), 400

            # Construir y ejecutar la consulta SQL
            consulta = f"UPDATE tarjetas SET {', '.join(campos)} WHERE pan = %s"
            valores.append(pan)  # Agregar el `pan` al final de los valores
            cursor.execute(consulta, valores)

            # Confirmar cambios y cerrar conexión
            conexion.commit()
            cursor.close()
            conexion.close()

            return jsonify({"mensaje": "Tarjeta actualizada exitosamente"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": f"Error al actualizar la tarjeta: {err}"}), 500
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500


# Ruta para obtener el balance de una tarjeta
@app.route('/tarjeta-credito/balance/<string:pan>', methods=['GET'])
def obtener_balance(pan):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM balances WHERE pan = %s", (pan,))
        balance = cursor.fetchone()
        cursor.close()
        conexion.close()
        if balance:
            balance['saldo_disponible'] = balance['limite'] - balance['actual']
            return jsonify(balance)
        else:
            return jsonify({"error": "Balance no encontrado"}), 404
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para eliminar una tarjeta
@app.route('/tarjeta-credito/<string:pan>', methods=['DELETE'])
def eliminar_tarjeta(pan):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT actual FROM balances WHERE pan = %s", (pan,))
        balance = cursor.fetchone()
        if balance and balance['actual'] == 0:
            # Elimina la tarjeta y el balance asociado
            cursor.execute("DELETE FROM balances WHERE pan = %s", (pan,))
            cursor.execute("DELETE FROM tarjetas WHERE pan = %s", (pan,))
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Tarjeta eliminada"})
        else:
            cursor.close()
            conexion.close()
            return jsonify({"error": "No se puede eliminar la tarjeta con saldo pendiente"}), 400
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500
    
# Función para enviar un mensaje de texto (SMS) a un número de teléfono
def enviar_sms(mensaje, no_telefono, pan):
    try:
        # Conexión con el servidor RabbitMQ
        body={
            "mensaje": mensaje,
            "no_telefono": no_telefono,
            "pan": pan
        }
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-sabados'))
        canal = connection.channel()
        canal.queue_declare(queue='app-sabados-queue')
        canal.basic_publish(exchange='', routing_key='app-sabados-queue', body=json.dumps(body), properties=pika.BasicProperties(delivery_mode=2))
        connection.close()
        return True
    except pika.exceptions.AMQPError as err:
        print(f"Error al enviar SMS: {err}")
        return False 

@app.route('/tarjeta-credito/procesamiento/<string:pan>', methods=['POST'])
def realizar_cargo(pan):
    data = request.get_json()
    monto = data.get('monto')

    if not monto or monto <= 0:
        return jsonify({"error": "Monto inválido"}), 400

    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)

            # Verificar si la tarjeta está activa
            #cursor.execute("SELECT estado FROM tarjetas WHERE pan = %s", (pan,))
            cursor.execute("SELECT estado, no_telefono FROM tarjetas WHERE pan = %s", (pan,))

            tarjeta = cursor.fetchone()
            if not tarjeta:
                return jsonify({"error": "Tarjeta no encontrada"}), 404
            if tarjeta['estado'] != 'activo':
                return jsonify({"error": "La tarjeta no está activa"}), 400
            
            no_telefono = tarjeta['no_telefono']

            # Verificar el balance de la tarjeta
            cursor.execute("SELECT actual, limite FROM balances WHERE pan = %s", (pan,))
            balance = cursor.fetchone()
            if not balance:
                return jsonify({"error": "Balance no encontrado"}), 404

            nuevo_balance = balance['actual'] + monto
            # Validar que el monto no exceda el límite de crédito
            if nuevo_balance > balance['limite']:
                return jsonify({"error": "Monto excede el límite de crédito"}), 400

            # Actualizar el saldo
            cursor.execute("UPDATE balances SET actual = %s WHERE pan = %s", (nuevo_balance, pan))
            conexion.commit()

            cursor.close()
            conexion.close()

            # Simulación de envío de notificación (puedes reemplazar con un servicio real de mensajería)
            mensaje = f"Se ha realizado un cargo de Q{monto:.2f} en la tarjeta {pan}"
            enviar_sms(mensaje, no_telefono, pan)
           # enviar_sms(f"Se ha realizado un cargo de Q{monto} en la tarjeta {pan}")

            return jsonify({"mensaje": "Cargo realizado con éxito", "nuevo_saldo": nuevo_balance})
        except mysql.connector.Error as err:
            print(f"Error al realizar el cargo: {err}")
            return jsonify({"error": "Error al procesar el cargo"}), 500
        finally:
            if conexion.is_connected():
                conexion.close()
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

@app.route('/tarjeta-credito/abono/<string:pan>', methods=['POST'])
def realizar_abono(pan):
    data = request.get_json()
    monto = data.get('monto')

    if not monto or monto <= 0:
        return jsonify({"error": "Monto inválido"}), 400

    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)

            # Verificar si la tarjeta existe
            cursor.execute("SELECT estado, no_telefono FROM tarjetas WHERE pan = %s", (pan,))
            tarjeta = cursor.fetchone()
            if not tarjeta:
                return jsonify({"error": "Tarjeta no encontrada"}), 404

            # Verificar el balance de la tarjeta
            cursor.execute("SELECT actual FROM balances WHERE pan = %s", (pan,))
            balance = cursor.fetchone()
            if not balance:
                return jsonify({"error": "Balance no encontrado"}), 404

            # Validar que el monto no exceda el saldo actual
            nuevo_balance = balance['actual'] - monto
            if nuevo_balance < 0:
                return jsonify({"error": "El abono excede el saldo actual"}), 400
            
            no_telefono = tarjeta['no_telefono']

            # Actualizar el saldo
            cursor.execute("UPDATE balances SET actual = %s WHERE pan = %s", (nuevo_balance, pan))
            conexion.commit()

            cursor.close()
            conexion.close()

            mensaje = f"Se ha realizado un abono a su tarjeta {pan} por Q{monto:.2f} "
            enviar_sms(mensaje, no_telefono, pan)

            # Simulación de envío de notificación (puedes reemplazar con un servicio real de mensajería)
            #enviar_sms(f"Se ha realizado un abono de Q{monto} a la tarjeta {pan}")

            return jsonify({"mensaje": "Abono realizado con éxito", "nuevo_saldo": nuevo_balance})
        except mysql.connector.Error as err:
            print(f"Error al realizar el abono: {err}")
            return jsonify({"error": "Error al procesar el abono"}), 500
        finally:
            if conexion.is_connected():
                conexion.close()
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500



if __name__ == '__main__':
    id_contenedor = os.environ.get('HOSTNAME')
    print(f"ID del contenedor: {id_contenedor}")
    app.run(host='0.0.0.0', port=5000, debug=True)
