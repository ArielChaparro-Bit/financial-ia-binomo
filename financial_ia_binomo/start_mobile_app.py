#!/usr/bin/env python3
"""
Script para iniciar la aplicación móvil IA Financiera
Configurado para IP específica: 192.168.100.17:8080
"""

import os
import sys
import subprocess
import time
import requests
import socket
from datetime import datetime

# Configuración específica para tu red
LOCAL_IP = "192.168.100.17"
API_PORT = 8080
MOBILE_PORT = 8080

def get_local_ip():
    """Obtener la IP local de la máquina"""
    try:
        # Conectar a un servidor externo para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def check_api_server():
    """Verificar si el servidor API está ejecutándose"""
    try:
        response = requests.get(f"http://{LOCAL_IP}:{API_PORT}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Iniciar el servidor API si no está ejecutándose"""
    if not check_api_server():
        print("🚀 Iniciando servidor API...")
        try:
            # Iniciar servidor API en segundo plano
            subprocess.Popen([sys.executable, 'start_api.py'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            # Esperar a que inicie
            for i in range(10):
                time.sleep(1)
                if check_api_server():
                    print("✅ Servidor API iniciado correctamente")
                    return True
                print(f"⏳ Esperando servidor API... ({i+1}/10)")
            
            print("❌ No se pudo iniciar el servidor API")
            return False
        except Exception as e:
            print(f"❌ Error al iniciar servidor API: {e}")
            return False
    else:
        print("✅ Servidor API ya está ejecutándose")
        return True

def start_mobile_app():
    """Iniciar la aplicación móvil"""
    print("📱 Iniciando Aplicación Móvil IA Financiera...")
    
    # Cambiar al directorio de la app móvil
    mobile_app_dir = os.path.join(os.path.dirname(__file__), 'mobile_app')
    os.chdir(mobile_app_dir)
    
    print(f"🌐 Aplicación disponible en:")
    print(f"   • Local: http://localhost:{MOBILE_PORT}")
    print(f"   • Red: http://{LOCAL_IP}:{MOBILE_PORT}")
    print(f"   • API: http://{LOCAL_IP}:{API_PORT}")
    print(f"📱 Accede desde tu móvil usando: http://{LOCAL_IP}:{MOBILE_PORT}")
    print(f"🔗 Código QR disponible en: http://{LOCAL_IP}:{MOBILE_PORT}/qr")
    print(f"📊 API Status: http://{LOCAL_IP}:{MOBILE_PORT}/api/status")
    print(f"⏰ Iniciado: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    print(f"🎯 URL para móvil: http://{LOCAL_IP}:{MOBILE_PORT}")
    print("=" * 60)
    
    # Iniciar aplicación móvil
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Aplicación móvil detenida")
    except Exception as e:
        print(f"❌ Error al iniciar aplicación móvil: {e}")

def main():
    """Función principal"""
    print("🤖 IA Financiera Binomo - Aplicación Móvil")
    print("=" * 60)
    print(f"📍 IP Configurada: {LOCAL_IP}")
    print(f"🔌 Puerto API: {API_PORT}")
    print(f"📱 Puerto Móvil: {MOBILE_PORT}")
    print("=" * 60)
    
    # Verificar e iniciar servidor API
    if not start_api_server():
        print("⚠️  Continuando sin servidor API...")
        print("💡 Ejecuta 'python start_api.py' en otra terminal")
    
    # Iniciar aplicación móvil
    start_mobile_app()

if __name__ == '__main__':
    main() 