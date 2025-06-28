#!/usr/bin/env python3
"""
Script simple para probar el servidor API
"""

import requests
import time

def test_server():
    """Prueba el servidor API"""
    print("🧪 Probando servidor API...")
    
    # Esperar un poco para que el servidor inicie
    time.sleep(3)
    
    try:
        # Probar endpoint de salud
        print("📋 Probando /health...")
        response = requests.get('http://localhost:8080/health', timeout=10)
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            print(f"📊 Respuesta: {response.json()}")
        else:
            print(f"❌ Error en servidor: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de que el servidor esté ejecutándose")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_server() 