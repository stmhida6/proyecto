from flask import Flask, request, jsonify, request, abort
import json 
import os
import pika


app = Flask(__name__)

estudiantes = {}

identificador_estudiante = 1

@app.route('/health', methods=['GET'])
def obtener_estado():
    id_contenedor = os.environ.get('HOSTNAME')
    return jsonify({'status': 'ok', 'idContenedor': id_contenedor})    

def enviar_a_rabbitmq(nombre, telefono, requerimiento):
    try:
        body=request.get_json()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-sabados'))
        canal=connection.channel()
        canal.queue_declare(queue='app-sabados-queue')

        nombre = body['nombre']
        telefono = body['telefono']
        requerimiento = body['requerimiento']

      
        canal.basic_publish(exchange='', routing_key='app-sabados-queue', body=json.dumps(body), properties=pika.BasicProperties(delivery_mode=2))
    
        connection.close()
        return True
    except pika.exceptions.AMQPError as error:
        print(f"Error al enviar a RabbitMQ: {error}")
        return False
    

@app.route('/soporte', methods=['POST'])
def soporte():
    data = request.get_json()
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    requerimiento = data.get('requerimiento')

    if not nombre or not telefono or not requerimiento:
        return jsonify({'error': 'Faltan datos'}), 400

    # Intentar enviar el mensaje a RabbitMQ
    resultado = enviar_a_rabbitmq(nombre, telefono, requerimiento)
    print(f"Resultado de enviar_a_rabbitmq: {resultado}")  # Línea para verificar el resultado

    if resultado:
        respuesta = {
            'mensaje': 'Solicitud de soporte recibida',
            'nombre': nombre,
            'telefono': telefono,
            'requerimiento': requerimiento
        }
        return jsonify(respuesta), 200
    else:
        return jsonify({'error': 'Error al enviar la solicitud de soporte'}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
            
 
   

