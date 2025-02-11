"""Script para testar o login da API."""
import requests

def test_login():
    """Testa o endpoint de login."""
    url = "http://localhost:8000/api/v1/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Tenant-ID": "1"
    }
    data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_login()
