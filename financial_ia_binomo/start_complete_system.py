#!/usr/bin/env python3
"""
🎯 SISTEMA COMPLETO IA FINANCIERA - INICIO AUTOMÁTICO
============================================================
Script que automatiza todo el proceso de inicio del sistema:
1. Recrear modelo
2. Iniciar servidor API
3. Probar que todo funcione
"""

import os
import sys
import time
import subprocess
import requests
import json
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step, message):
    print(f"\n📋 PASO {step}: {message}")
    print("-" * 40)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️ {message}")

def check_python_version():
    """Verificar versión de Python"""
    print_step(1, "Verificando versión de Python")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
        return False

def check_files():
    """Verificar archivos necesarios"""
    print_step(2, "Verificando archivos del sistema")
    
    required_files = [
        "config.json",
        "recreate_model.py",
        "start_api.py",
        "test_api.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print_success(f"{file} - OK")
        else:
            print_error(f"{file} - NO ENCONTRADO")
            missing_files.append(file)
    
    if missing_files:
        print_error(f"Faltan {len(missing_files)} archivos necesarios")
        return False
    
    return True

def recreate_model():
    """Recrear el modelo"""
    print_step(3, "Recreando modelo de IA")
    
    try:
        result = subprocess.run([sys.executable, "recreate_model.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print_success("Modelo recreado correctamente")
            return True
        else:
            print_error(f"Error recreando modelo: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout recreando modelo")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False

def start_api_server():
    """Iniciar servidor API"""
    print_step(4, "Iniciando servidor API")
    
    try:
        # Iniciar servidor en background
        process = subprocess.Popen([sys.executable, "start_api.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Esperar a que el servidor inicie
        time.sleep(5)
        
        # Verificar si el proceso sigue corriendo
        if process.poll() is None:
            print_success("Servidor API iniciado correctamente")
            return process
        else:
            stdout, stderr = process.communicate()
            print_error(f"Error iniciando servidor: {stderr}")
            return None
            
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return None

def test_api():
    """Probar la API"""
    print_step(5, "Probando API")
    
    try:
        # Esperar un poco más para asegurar que el servidor esté listo
        time.sleep(3)
        
        # Probar endpoint de salud
        response = requests.get("http://localhost:8080/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success("API respondiendo correctamente")
            print_info(f"Status: {data.get('status', 'N/A')}")
            print_info(f"Modelo cargado: {data.get('model_loaded', False)}")
            print_info(f"Datos: {data.get('data_count', 0)} registros")
            return True
        else:
            print_error(f"API no responde correctamente: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar a la API")
        return False
    except Exception as e:
        print_error(f"Error probando API: {e}")
        return False

def test_predictions():
    """Probar predicciones"""
    print_step(6, "Probando predicciones")
    
    try:
        response = requests.get("http://localhost:8080/predict", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Predicciones funcionando correctamente")
            print_info(f"Predicción: {data.get('prediction', 'N/A')}")
            print_info(f"Confianza: {data.get('confidence', 'N/A')}")
            return True
        else:
            print_error(f"Error en predicciones: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error probando predicciones: {e}")
        return False

def show_final_status(api_process):
    """Mostrar estado final"""
    print_header("SISTEMA COMPLETAMENTE FUNCIONANDO")
    
    print_success("🎉 ¡Todo listo! El sistema está funcionando correctamente")
    
    print("\n📊 URLs disponibles:")
    print("   • Local: http://localhost:8080")
    print("   • Red: http://192.168.100.17:8080")
    
    print("\n🔗 Endpoints disponibles:")
    print("   • GET / - Página principal")
    print("   • GET /health - Estado del sistema")
    print("   • GET /predict - Predicciones")
    print("   • GET /backtest - Backtest")
    
    print("\n📱 Para usar desde móvil:")
    print("   • Abre tu navegador móvil")
    print("   • Ve a: http://192.168.100.17:8080")
    print("   • O escanea el QR en la página principal")
    
    print("\n⚠️ IMPORTANTE:")
    print("   • NO cierres esta ventana de PowerShell")
    print("   • El servidor seguirá corriendo hasta que lo cierres")
    print("   • Para detener: presiona Ctrl+C")
    
    if api_process:
        print(f"\n🔄 Servidor API corriendo (PID: {api_process.pid})")
    
    return True

def main():
    """Función principal"""
    print_header("SISTEMA COMPLETO IA FINANCIERA - INICIO AUTOMÁTICO")
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Verificar archivos
    if not check_files():
        return False
    
    # Recrear modelo
    if not recreate_model():
        return False
    
    # Iniciar servidor API
    api_process = start_api_server()
    if not api_process:
        return False
    
    # Probar API
    if not test_api():
        print_error("API no responde correctamente")
        api_process.terminate()
        return False
    
    # Probar predicciones
    if not test_predictions():
        print_error("Predicciones no funcionan")
        api_process.terminate()
        return False
    
    # Mostrar estado final
    show_final_status(api_process)
    
    try:
        # Mantener el servidor corriendo
        print("\n🔄 Manteniendo servidor activo... (Ctrl+C para detener)")
        api_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        api_process.terminate()
        print_success("Servidor detenido correctamente")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ El sistema no pudo iniciarse correctamente")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1) 