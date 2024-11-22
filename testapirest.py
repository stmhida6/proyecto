import requests

# URL base del API
BASE_URL = "http://localhost:3000"

# Endpoints de la API
CARD_ENDPOINT = "/tarjeta-credito"
BALANCE_ENDPOINT = "/tarjeta-credito/balance"
PROCESS_ENDPOINT = "/tarjeta-credito/procesamiento"
ABONO_ENDPOINT = "/tarjeta-credito/abono"

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
    }
]



# Flujo de prueba
if __name__ == "__main__":
    # Crear tarjetas
    print("Creando tarjetas de crédito:")
    for cliente in clientes:
        crear_tarjeta(cliente)
    
  