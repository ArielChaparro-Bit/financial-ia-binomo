#!/usr/bin/env python3
"""
Script para probar acceso a la app móvil
"""

import requests
import socket
import webbrowser
import time
import os

def get_local_ip():
    """Obtiene la IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def test_local_access():
    """Prueba acceso local"""
    print("🔍 Probando acceso local...")
    
    urls = [
        "http://localhost:8080",
        f"http://{get_local_ip()}:8080"
    ]
    
    for url in urls:
        try:
            print(f"   Probando: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ FUNCIONA: {url}")
                return url
            else:
                print(f"   ❌ Error {response.status_code}: {url}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No conecta: {url}")
        except Exception as e:
            print(f"   ❌ Error: {url} - {e}")
    
    return None

def start_server():
    """Inicia el servidor"""
    print("🚀 Iniciando servidor...")
    
    # Cambiar al directorio de la app
    app_dir = os.path.join(os.path.dirname(__file__), "mobile_app")
    os.chdir(app_dir)
    
    # Iniciar servidor
    os.system("python app.py")

def main():
    """Función principal"""
    print("📱 TEST DE ACCESO - IA FINANCIERA MÓVIL")
    print("=" * 50)
    
    # Probar acceso existente
    working_url = test_local_access()
    
    if working_url:
        print(f"\n🎉 ¡La app está funcionando!")
        print(f"📱 URL de acceso: {working_url}")
        
        # Abrir en navegador
        print(f"\n🌐 Abriendo en navegador...")
        webbrowser.open(working_url)
        
        print(f"\n💡 Instrucciones:")
        print(f"   1. La app se abrió en tu navegador")
        print(f"   2. Para móvil, usa: {working_url}")
        print(f"   3. Asegúrate de estar en la misma red WiFi")
        
    else:
        print(f"\n❌ No se pudo acceder a la app")
        print(f"🔧 Iniciando servidor...")
        
        # Preguntar si iniciar servidor
        response = input("¿Iniciar servidor? (s/n): ").lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            start_server()
        else:
            print("❌ Servidor no iniciado")

if __name__ == "__main__":
    main() 