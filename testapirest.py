import requests

# URL base del API
BASE_URL = "http://localhost:3000"

# Endpoints de la API
CARD_ENDPOINT = "/tarjeta-credito"
BALANCE_ENDPOINT = "/tarjeta-credito/balance"
PROCESS_ENDPOINT = "/tarjeta-credito/procesamiento"
ABONO_ENDPOINT = "/tarjeta-credito/abono"
ALL_CARDS_ENDPOINT = "/tarjeta-credito/"

# Función para crear tarjetas de crédito
def crear_tarjeta(cliente):
    url = f"{BASE_URL}{CARD_ENDPOINT}"
    try:
        response = requests.post(url, json=cliente)
        if response.status_code == 201:  # Código HTTP 201: Creado
            print(f"Tarjeta creada exitosamente: {response.json()}")
        else:
            print(f"Error al crear tarjeta: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


# Datos de prueba
clientes = [
    {
        "nombre": "Juan Pérez",
        "apellidos": "Pérez",
        "edad": 30,
        "direccion": "Calle 123, Ciudad, País",
        "no_telefono": "12345678",
        "datos_laborales": "Empleado en XYZ S.A.",
        "datos_beneficiarios": "Esposa, María López",
        "dpi": "1234567890123",
        "estado": "activo",     
    },
    {
        "nombre": "Ana García",
        "apellidos": "Lopez",
        "edad": 28,
        "direccion": "Avenida Central 45, Ciudad, País",
        "no_telefono": "22222222",
        "datos_laborales": "Independiente",
        "datos_beneficiarios": "Hijo, Carlos García",
        "dpi": "2345678901234",
        "estado": "activo"        
    },
    {
        "nombre": "Carlos Ramírez",
        "apellidos": "Ramírez",
        "edad": 35,
        "direccion": "Boulevard Norte 789, Ciudad, País",
        "no_telefono": "33333333",
        "datos_laborales": "Gerente en ABC Corp.",
        "datos_beneficiarios": "Padre, José Ramírez",
        "dpi": "3456789012345",
        "estado": "activo"      
    },
    {
        "nombre": "Laura Martínez",
        "apellidos": "Martínez",
        "edad": 40,
        "direccion": "Calle Sur 456, Ciudad, País",
        "no_telefono": "44444444",
        "datos_laborales": "Directora en DEF Ltd.",
        "datos_beneficiarios": "Hermano, Luis Martínez",
        "dpi": "4567890123456",
        "estado": "activo"        
    },
    {
        "nombre": "Miguel Torres",
        "apellidos": "Torres",
        "edad": 50,
        "direccion": "Avenida Este 123, Ciudad, País",
        "no_telefono": "55555555",
        "datos_laborales": "Consultor Independiente",
        "datos_beneficiarios": "Esposa, Clara Torres",
        "dpi": "5678901234567",
        "estado": "activo"        
    },
    {
        "nombre": "Sofia Hernández",
        "apellidos": "Hernández",
        "edad": 27,
        "direccion": "Calle Oeste 789, Ciudad, País",
        "no_telefono": "66666666",
        "datos_laborales": "Ingeniera en GHI Inc.",
        "datos_beneficiarios": "Madre, Rosa Hernández",
        "dpi": "6789012345678",
        "estado": "activo"
    },
    {
        "nombre": "David Gómez",
        "apellidos": "Gómez",
        "edad": 45,
        "direccion": "Avenida Sur 321, Ciudad, País",
        "no_telefono": "77777777",
        "datos_laborales": "Profesor en Universidad",
        "datos_beneficiarios": "Esposa, Laura Gómez",
        "dpi": "7890123456789",
        "estado": "activo"
    },
    {
        "nombre": "Elena Ruiz",
        "apellidos": "Ruiz",
        "edad": 32,
        "direccion": "Boulevard Este 654, Ciudad, País",
        "no_telefono": "88888888",
        "datos_laborales": "Doctora en Hospital",
        "datos_beneficiarios": "Padre, Juan Ruiz",
        "dpi": "8901234567890",
        "estado": "activo"
    }
]


def obtener_terjetas():
    url = f"{BASE_URL}{CARD_ENDPOINT}"
    try:
        response = requests.get(url)
        if response.status_code == 200:  # Código HTTP 200: OK
            print(f"Tarjetas obtenidas exitosamente: {response.json()}")
            return response.json()
        else:
            print(f"Error al obtener tarjetas: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return []

    

# Flujo de prueba
if __name__ == "__main__":
    # Crear tarjetas
    print("Creando tarjetas de crédito:")
    for cliente in clientes:
        crear_tarjeta(cliente)
    
    #lista de tarjetas
    tarjetas = obtener_terjetas()
    print(tarjetas)

    #obtener el pand e la primera tarjeta
    pan = tarjetas[0]['pan']
    print(pan)

    #obtener el balance de la primera tarjeta
    url = f"{BASE_URL}{BALANCE_ENDPOINT}/{pan}"

    try:
        response = requests.get(url)
        if response.status_code == 200:  # Código HTTP 200: OK
            print(f"Balance obtenido exitosamente: {response.json()}")
        else:
            print(f"Error al obtener balance: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

    #procesar una transacción
    url = f"{BASE_URL}{PROCESS_ENDPOINT}"
    transaccion = {   
        "monto": 100,
    }
    try:
        response = requests.post(url, json=transaccion)

        if response.status_code == 201:  # Código HTTP 201: Creado
            print(f"Transacción procesada exitosamente: {response.json()}")
        else:
            print(f"Error al procesar transacción: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

    #abonar a una tarjeta
    url = f"{BASE_URL}{ABONO_ENDPOINT}"
    abono = {   
        "monto": 100,
    }
    try:
        response = requests.post(url, json=abono)

        if response.status_code == 201:  # Código HTTP 201: Creado
            print(f"Abono realizado exitosamente: {response.json()}")
        else:
            print(f"Error al realizar abono: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

     #obtener el balance de la primera tarjeta
    url = f"{BASE_URL}{BALANCE_ENDPOINT}/{pan}"

    try:
        response = requests.get(url)
        if response.status_code == 200:  # Código HTTP 200: OK
            print(f"Balance obtenido exitosamente: {response.json()}")
        else:
            print(f"Error al obtener balance: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")










