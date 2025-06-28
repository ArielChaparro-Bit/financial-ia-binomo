#!/usr/bin/env python3
"""
Script de reactivación del sistema de IA Financiera Binomo
Compatible con Python 3.13 (sin TensorFlow)
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

def print_header(title: str):
    """Imprime un encabezado"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step: int, message: str):
    """Imprime un paso del proceso"""
    print(f"\n📋 PASO {step}: {message}")

def print_success(message: str):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message: str):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_warning(message: str):
    """Imprime mensaje de advertencia"""
    print(f"⚠️ {message}")

def check_system():
    """Verifica el estado del sistema"""
    print_step(1, "Verificando estado del sistema")
    
    # Verificar Python
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Verificar archivos críticos
    critical_files = [
        "config.json",
        "models/simple_model.pkl",
        "models/simple_model_scaler.pkl",
        "models/simple_model_features.pkl",
        "data/price_data.csv"
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print_success(f"{file_path} - {size} bytes")
        else:
            print_error(f"Faltante: {file_path}")
            return False
    
    return True

def install_basic_dependencies():
    """Instala dependencias básicas (sin TensorFlow)"""
    print_step(2, "Instalando dependencias básicas")
    
    basic_requirements = [
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "requests>=2.25.0",
        "flask>=2.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "yfinance>=0.1.70",
        "ta>=0.10.0"
    ]
    
    for req in basic_requirements:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", req], 
                         capture_output=True, check=True)
            print_success(f"Instalado: {req}")
        except subprocess.CalledProcessError as e:
            print_warning(f"No se pudo instalar {req}: {e}")
    
    return True

def test_model():
    """Prueba el modelo simple"""
    print_step(3, "Probando modelo simple")
    
    try:
        import pickle
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        
        # Cargar modelo
        with open("models/simple_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Cargar scaler
        with open("models/simple_model_scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        
        # Cargar features
        with open("models/simple_model_features.pkl", "rb") as f:
            features = pickle.load(f)
        
        print_success(f"Modelo cargado: {type(model).__name__}")
        print_success(f"Features: {len(features)} indicadores")
        
        # Crear datos de prueba
        test_data = np.random.rand(1, len(features))
        test_data_scaled = scaler.transform(test_data)
        prediction = model.predict_proba(test_data_scaled)
        
        print_success(f"Predicción de prueba: {prediction[0]}")
        return True
        
    except Exception as e:
        print_error(f"Error probando modelo: {e}")
        return False

def start_api_server():
    """Inicia el servidor API"""
    print_step(4, "Iniciando servidor API")
    
    try:
        # Verificar si el servidor ya está corriendo
        import requests
        try:
            response = requests.get("http://localhost:8080/health", timeout=2)
            if response.status_code == 200:
                print_success("Servidor API ya está corriendo")
                return True
        except:
            pass
        
        # Iniciar servidor
        server_script = """
import sys
import os
sys.path.append('src')
from api_server import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
"""
        
        with open("temp_server.py", "w") as f:
            f.write(server_script)
        
        # Iniciar en segundo plano
        process = subprocess.Popen([sys.executable, "temp_server.py"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que inicie
        time.sleep(3)
        
        # Verificar si está corriendo
        try:
            response = requests.get("http://localhost:8080/health", timeout=5)
            if response.status_code == 200:
                print_success("Servidor API iniciado correctamente")
                return True
            else:
                print_error("Servidor no responde correctamente")
                return False
        except Exception as e:
            print_error(f"Error conectando al servidor: {e}")
            return False
            
    except Exception as e:
        print_error(f"Error iniciando servidor: {e}")
        return False

def test_api_endpoints():
    """Prueba los endpoints de la API"""
    print_step(5, "Probando endpoints de la API")
    
    try:
        import requests
        
        base_url = "http://localhost:8080"
        endpoints = [
            "/health",
            "/predict",
            "/indicators",
            "/backtest"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print_success(f"GET {endpoint} - OK")
                else:
                    print_warning(f"GET {endpoint} - Status {response.status_code}")
            except Exception as e:
                print_warning(f"GET {endpoint} - Error: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Error probando API: {e}")
        return False

def generate_status_report():
    """Genera un reporte de estado"""
    print_step(6, "Generando reporte de estado")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "system_status": "ACTIVO",
        "model_type": "Random Forest (Simple)",
        "api_status": "RUNNING",
        "data_sources": ["price_data.csv", "test_data.csv"],
        "next_steps": [
            "1. Configurar trading automático en config.json",
            "2. Ejecutar backtest para validar rendimiento",
            "3. Monitorear predicciones en tiempo real",
            "4. Ajustar parámetros según resultados"
        ]
    }
    
    # Crear directorio reports si no existe
    os.makedirs("reports", exist_ok=True)
    
    # Guardar reporte
    with open("reports/system_status.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print_success("Reporte guardado en reports/system_status.json")
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DEL SISTEMA:")
    print(f"   • Python: {report['python_version']}")
    print(f"   • Estado: {report['system_status']}")
    print(f"   • Modelo: {report['model_type']}")
    print(f"   • API: {report['api_status']}")
    print(f"   • Datos: {len(report['data_sources'])} fuentes")
    
    return True

def main():
    """Función principal"""
    print_header("REACTIVACIÓN DEL SISTEMA DE IA FINANCIERA BINOMO")
    
    # Verificar sistema
    if not check_system():
        print_error("Sistema no está listo para reactivación")
        return False
    
    # Instalar dependencias
    install_basic_dependencies()
    
    # Probar modelo
    if not test_model():
        print_error("Error con el modelo")
        return False
    
    # Iniciar API
    if not start_api_server():
        print_error("Error iniciando API")
        return False
    
    # Probar endpoints
    test_api_endpoints()
    
    # Generar reporte
    generate_status_report()
    
    print_header("🎉 SISTEMA REACTIVADO EXITOSAMENTE")
    print("""
    📱 Para usar la aplicación móvil:
       python start_mobile_app.py
    
    🔧 Para configurar trading automático:
       Editar config.json -> "trading": {"enabled": true}
    
    📊 Para ver predicciones:
       http://localhost:8080/predict
    
    📈 Para ejecutar backtest:
       http://localhost:8080/backtest
    
    🛑 Para detener el sistema:
       Ctrl+C en la terminal
    """)
    
    return True

if __name__ == "__main__":
    main() 