# Importa los módulos necesarios para escribir las pruebas
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Configura el cliente de prueba para llamar a las rutas del controlador
client = TestClient(app)

# Define tus pruebas
def test_login_success():
    # Simula una solicitud de inicio de sesión exitosa
    response = client.post("/auth/login", json={"email": "dleo@test.com", "password": "test123"})

    # Verifica que la respuesta tenga un código de estado 200 (éxito)
    assert response.status_code == 200

    # Verifica que los datos de respuesta sean los esperados
    assert "jwt" in response.json()

def test_login_invalid_credentials():
    # Simula una solicitud de inicio de sesión con credenciales inválidas
    response = client.post("/auth/login", json={"email": "testuser@test.com", "password": "wrongpass"})

    # Verifica que la respuesta tenga un código de estado 401 (no autorizado)
    assert response.status_code == 401

    # Verifica que los datos de respuesta sean los esperados
    assert "detail" in response.json()

# Ejecuta las pruebas con pytest
if __name__ == "__main__":
    pytest.main()
