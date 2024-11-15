from flask import Flask, request, jsonify, request, abort
import json 
import os
import pika
import random


app = Flask(__name__)

estudiantes = {}

identificador_estudiante = 1
#variables de enterno de mysql
mysql_host = os.environ['MYSQL_HOST']
mysql_db = os.environ['MYSQL_DATABASE']
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']

# Simulación de base de datos
tarjetas = {}


@app.route('/health', methods=['GET'])
def obtener_estado():
    id_contenedor = os.environ.get('HOSTNAME')
    return jsonify({
        'status': 'ok',
        'idContenedor': id_contenedor,
        'mysql_host': mysql_host,
        'mysql_db': mysql_db
    })

# Función para enviar mensajes a RabbitMQ
def enviar_notificacion_sms(mensaje):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-sabados'))
        canal = connection.channel()
        canal.queue_declare(queue='notificaciones-sms')
        
        canal.basic_publish(
            exchange='',
            routing_key='notificaciones-sms',
            body=json.dumps(mensaje),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        return True
    except pika.exceptions.AMQPError as error:
        print(f"Error al enviar a RabbitMQ: {error}")
        return False

# Ruta para obtener todas las tarjetas de crédito
@app.route('/tarjeta-credito', methods=['GET'])
def obtener_tarjetas():
    return jsonify(tarjetas)

# Ruta para obtener una tarjeta específica por PAN
@app.route('/tarjeta-credito/<string:pan>', methods=['GET'])
def obtener_tarjeta(pan):
    tarjeta = tarjetas.get(pan)
    if tarjeta:
        return jsonify(tarjeta)
    else:
        return jsonify({"error": "Tarjeta no encontrada"}), 404
    

# Ruta para crear una nueva tarjeta de crédito
@app.route('/tarjeta-credito', methods=['POST'])
def crear_tarjeta():
    data = request.get_json()
    pan = f"6800{random.randint(100000000000, 999999999999)}"
    data['pan'] = pan
    data['balance'] = {
        "limite": 5000,  # Limite de ejemplo, puedes modificarlo según necesidad
        "actual": 0
    }
    tarjetas[pan] = data
    return jsonify({"mensaje": "Tarjeta creada", "pan": pan}), 201

# Ruta para actualizar una tarjeta
@app.route('/tarjeta-credito/<string:pan>', methods=['PUT'])
def actualizar_tarjeta(pan):
    data = request.get_json()
    tarjeta = tarjetas.get(pan)
    if tarjeta:
        tarjeta.update(data)
        return jsonify({"mensaje": "Tarjeta actualizada"})
    else:
        return jsonify({"error": "Tarjeta no encontrada"}), 404

# Ruta para eliminar una tarjeta
@app.route('/tarjeta-credito/<string:pan>', methods=['DELETE'])
def eliminar_tarjeta(pan):
    if pan in tarjetas:
        del tarjetas[pan]
        return jsonify({"mensaje": "Tarjeta eliminada"})
    else:
        return jsonify({"error": "Tarjeta no encontrada"}), 404

# Ruta para obtener el balance de una tarjeta
@app.route('/tarjeta-credito/balance/<string:pan>', methods=['GET'])
def obtener_balance(pan):
    tarjeta = tarjetas.get(pan)
    if tarjeta:
        return jsonify(tarjeta['balance'])
    else:
        return jsonify({"error": "Tarjeta no encontrada"}), 404

# Ruta para realizar un cargo
@app.route('/tarjeta-credito/procesamiento/<string:pan>', methods=['POST'])
def realizar_cargo(pan):
    tarjeta = tarjetas.get(pan)
    if tarjeta:
        monto = request.json.get('monto')
        if monto and tarjeta['balance']['actual'] + monto <= tarjeta['balance']['limite']:
            tarjeta['balance']['actual'] += monto
            enviar_notificacion_sms({
                "mensaje": f"Se ha realizado un cargo a su tarjeta {pan[-4:]} por {monto}",
                "pan": pan
            })
            return jsonify({"mensaje": "Cargo realizado"})
        else:
            return jsonify({"error": "Monto supera el límite de crédito"}), 400
    else:
        return jsonify({"error": "Tarjeta no encontrada"}), 404

# Ruta para realizar un abono
@app.route('/tarjeta-credito/abono/<string:pan>', methods=['POST'])
def realizar_abono(pan):
    tarjeta = tarjetas.get(pan)
    if tarjeta:
        monto = request.json.get('monto')
        if monto:
            tarjeta['balance']['actual'] -= monto
            enviar_notificacion_sms({
                "mensaje": f"Se ha realizado un abono a su tarjeta {pan[-4:]} por {monto}",
                "pan": pan
            })
            return jsonify({"mensaje": "Abono realizado"})
        else:
            return jsonify({"error": "Monto inválido"}), 400
    else:
        return jsonify({"error": "Tarjeta no encontrada"}), 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
            
 
   

