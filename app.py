from flask import Flask, request, jsonify
import mysql.connector
import os
import random
from datetime import datetime

app = Flask(__name__)

# Variables de entorno para la conexión MySQL
mysql_host = os.environ['MYSQL_HOST']
mysql_db = os.environ['MYSQL_DATABASE']
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_root_password = os.environ['MYSQL_ROOT_PASSWORD']
mysql_root= 'root'

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
        'mysql_host': mysql_host,
        'mysql_db': mysql_db,
        'mysql_user': mysql_user,
        'mysql_password': mysql_password

    })

# Crear un cliente en la base de datos
def crear_cliente_db(data):
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, apellidos, edad, direccion, datos_laborales, datos_beneficiarios, dpi)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data['nombre'], data['apellidos'], data['edad'], data['direccion'], 
                  data['datos_laborales'], data['datos_beneficiarios'], data['dpi']))
            conexion.commit()
            cliente_id = cursor.lastrowid  # Obtener el ID del cliente insertado
            cursor.close()
            conexion.close()
            return cliente_id
        return None
    except mysql.connector.Error as err:
        print(f"Error al insertar cliente: {err}")
        return None

# Crear una nueva tarjeta de crédito y asociarla al cliente
def crear_tarjeta_db(cliente_id):
    # Generar un PAN aleatorio comenzando con 6800
    pan = f"6800{random.randint(100000000000, 999999999999)}"
    fecha_vencimiento = datetime(2027, 12, 31)  # Establecer una fecha de vencimiento predeterminada (por ejemplo, 31/12/2027)
    
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO tarjetas_credito (pan, id_cliente, fecha_vencimiento, estado)
                VALUES (%s, %s, %s, %s)
            """, (pan, cliente_id, fecha_vencimiento, 'activa'))
            cursor.execute("""
                INSERT INTO balances (pan, limite, actual)
                VALUES (%s, %s, %s)
            """, (pan, 5000, 0))  # Limite de crédito de 5000 y saldo actual 0
            conexion.commit()
            cursor.close()
            conexion.close()
            return pan
        return None
    except mysql.connector.Error as err:
        print(f"Error al insertar tarjeta: {err}")
        return None

# Ruta para obtener todas las tarjetas de crédito
@app.route('/tarjeta-credito', methods=['GET'])
def obtener_tarjetas():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        #cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarjetas_credito")
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
        cursor.execute("SELECT * FROM tarjetas_credito WHERE pan = %s", (pan,))
        tarjeta = cursor.fetchone()
        cursor.close()
        conexion.close()
        if tarjeta:
            return jsonify(tarjeta)
        else:
            return jsonify({"error": "Tarjeta no encontrada"}), 404
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para crear un nuevo cliente y tarjeta de crédito
@app.route('/tarjeta-credito', methods=['POST'])
def crear_cliente_y_tarjeta():
    data = request.get_json()

    # Primero, creamos el cliente
    cliente_id = crear_cliente_db(data)
    if cliente_id:
        # Luego, creamos la tarjeta de crédito asociada al cliente
        pan = crear_tarjeta_db(cliente_id)
        if pan:
            return jsonify({"mensaje": "Cliente y tarjeta creados", "pan": pan}), 201
        else:
            return jsonify({"error": "Error al crear la tarjeta de crédito"}), 500
    else:
        return jsonify({"error": "Error al crear el cliente"}), 500

# Ruta para actualizar una tarjeta
@app.route('/tarjeta-credito/<string:pan>', methods=['PUT'])
def actualizar_tarjeta(pan):
    data = request.get_json()
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("UPDATE tarjetas_credito SET estado = %s WHERE pan = %s", (data['estado'], pan))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "Tarjeta actualizada"})
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para eliminar una tarjeta
@app.route('/tarjeta-credito/<string:pan>', methods=['DELETE'])
def eliminar_tarjeta(pan):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT actual FROM balances WHERE pan = %s", (pan,))
        balance = cursor.fetchone()
        if balance and balance['actual'] == 0:  # Verificamos que el balance actual sea 0
            cursor.execute("DELETE FROM tarjetas_credito WHERE pan = %s", (pan,))
            cursor.execute("DELETE FROM balances WHERE pan = %s", (pan,))
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
            # Calculamos el saldo disponible
            balance['saldo_disponible'] = balance['limite'] - balance['actual']
            return jsonify(balance)
        else:
            return jsonify({"error": "Tarjeta no encontrada"}), 404
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para realizar un cargo a la tarjeta de crédito
@app.route('/tarjeta-credito/procesamiento/<string:pan>', methods=['POST'])
def realizar_cargo(pan):
    data = request.get_json()
    monto = data.get('monto')
    if monto is None or monto <= 0:
        return jsonify({"error": "Monto inválido"}), 400

    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT actual, limite FROM balances WHERE pan = %s", (pan,))
        balance = cursor.fetchone()
        if balance and balance['actual'] + monto <= balance['limite']:
            nuevo_balance = balance['actual'] + monto
            cursor.execute("UPDATE balances SET actual = %s WHERE pan = %s", (nuevo_balance, pan))
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Cargo realizado"})
        else:
            cursor.close()
            conexion.close()
            return jsonify({"error": "Monto supera el límite de crédito"}), 400
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500

# Ruta para realizar un abono a la tarjeta de crédito
@app.route('/tarjeta-credito/abono/<string:pan>', methods=['POST'])
def realizar_abono(pan):
    data = request.get_json()
    monto = data.get('monto')
    if monto is None or monto <= 0:
        return jsonify({"error": "Monto inválido"}), 400

    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT actual FROM balances WHERE pan = %s", (pan,))
        balance = cursor.fetchone()
        if balance:
            nuevo_balance = balance['actual'] - monto
            if nuevo_balance < 0:
                cursor.close()
                conexion.close()
                return jsonify({"error": "El abono supera el saldo actual"}), 400
            cursor.execute("UPDATE balances SET actual = %s WHERE pan = %s", (nuevo_balance, pan))
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Abono realizado"})
        else:
            cursor.close()
            conexion.close()
            return jsonify({"error": "Tarjeta no encontrada"}), 404
    else:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
            
 
   

