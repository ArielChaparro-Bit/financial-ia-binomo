#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del sistema de IA Financiera
"""

import os
import sys
import subprocess
import requests
import time
from datetime import datetime, timedelta

def print_step(step, message):
    """Imprime un paso del proceso de prueba"""
    print(f"\n{'='*50}")
    print(f"🔍 PASO {step}: {message}")
    print(f"{'='*50}")

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"❌ {message}")

def print_warning(message):
    """Imprime un mensaje de advertencia"""
    print(f"⚠️ {message}")

def check_python_version():
    """Verifica la versión de Python"""
    print_step(1, "Verificando versión de Python")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
        return False

def check_dependencies():
    """Verifica las dependencias instaladas"""
    print_step(2, "Verificando dependencias")
    
    required_packages = [
        'numpy', 'pandas', 'scikit-learn', 'tensorflow', 
        'flask', 'flask-cors', 'matplotlib', 'joblib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} - OK")
        except ImportError:
            print_error(f"{package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"Instala las dependencias faltantes: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_file_structure():
    """Verifica la estructura de archivos"""
    print_step(3, "Verificando estructura de archivos")
    
    required_files = [
        'src/api_server.py',
        'src/model_train.py',
        'src/data_processing.py',
        'src/features.py',
        'src/generate_sample_data.py',
        'data/price_data.csv',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path} - OK")
        else:
            print_error(f"{file_path} - NO ENCONTRADO")
            missing_files.append(file_path)
    
    if missing_files:
        print_warning("Algunos archivos están faltando")
        return False
    
    return True

def generate_sample_data():
    """Genera datos de ejemplo"""
    print_step(4, "Generando datos de ejemplo")
    
    try:
        # Cambiar al directorio src
        os.chdir('src')
        
        # Ejecutar el generador de datos
        result = subprocess.run([sys.executable, 'generate_sample_data.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print_success("Datos de ejemplo generados correctamente")
            print(result.stdout)
            return True
        else:
            print_error("Error al generar datos de ejemplo")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout al generar datos")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    finally:
        # Volver al directorio raíz
        os.chdir('..')

def train_model():
    """Entrena el modelo"""
    print_step(5, "Entrenando modelo (esto puede tomar varios minutos)")
    
    try:
        # Cambiar al directorio src
        os.chdir('src')
        
        # Ejecutar el entrenamiento
        print("🔄 Iniciando entrenamiento...")
        result = subprocess.run([sys.executable, 'model_train.py'], 
                              capture_output=True, text=True, timeout=600)  # 10 minutos timeout
        
        if result.returncode == 0:
            print_success("Modelo entrenado correctamente")
            print(result.stdout)
            return True
        else:
            print_error("Error al entrenar el modelo")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout al entrenar el modelo")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    finally:
        # Volver al directorio raíz
        os.chdir('..')

def test_api():
    """Prueba la API"""
    print_step(6, "Probando API")
    
    try:
        # Cambiar al directorio src
        os.chdir('src')
        
        # Iniciar el servidor en segundo plano
        print("🚀 Iniciando servidor API...")
        server_process = subprocess.Popen([sys.executable, 'api_server.py'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        
        # Esperar a que el servidor inicie
        time.sleep(5)
        
        # Probar endpoints
        base_url = "http://localhost:8080"
        
        # Probar endpoint de salud
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            if response.status_code == 200:
                print_success("Endpoint /health - OK")
                health_data = response.json()
                print(f"   Modelo cargado: {health_data.get('model_loaded', False)}")
                print(f"   Datos disponibles: {health_data.get('data_points', 0)}")
            else:
                print_error(f"Endpoint /health - Error {response.status_code}")
        except Exception as e:
            print_error(f"Error al probar /health: {e}")
        
        # Probar endpoint principal
        try:
            response = requests.get(f"{base_url}/", timeout=10)
            if response.status_code == 200:
                print_success("Endpoint / - OK")
            else:
                print_error(f"Endpoint / - Error {response.status_code}")
        except Exception as e:
            print_error(f"Error al probar /: {e}")
        
        # Probar predicción
        try:
            test_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response = requests.get(f"{base_url}/predict?date={test_date}", timeout=10)
            if response.status_code == 200:
                print_success("Endpoint /predict - OK")
                pred_data = response.json()
                print(f"   Señal: {pred_data.get('signal', 'N/A')}")
                print(f"   Confianza: {pred_data.get('confidence', 'N/A')}")
            else:
                print_error(f"Endpoint /predict - Error {response.status_code}")
                print(f"   Respuesta: {response.text}")
        except Exception as e:
            print_error(f"Error al probar /predict: {e}")
        
        # Terminar el servidor
        server_process.terminate()
        server_process.wait()
        
        return True
        
    except Exception as e:
        print_error(f"Error al probar API: {e}")
        return False
    finally:
        # Volver al directorio raíz
        os.chdir('..')

def main():
    """Función principal de pruebas"""
    print("🧪 SISTEMA DE PRUEBAS - IA FINANCIERA BINOMO")
    print("=" * 60)
    
    tests = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Estructura de archivos", check_file_structure),
        ("Generación de datos", generate_sample_data),
        ("Entrenamiento del modelo", train_model),
        ("Prueba de API", test_api)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print_success("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
    else:
        print_warning("⚠️ Algunas pruebas fallaron. Revisa los errores anteriores.")
    
    print("\n💡 Próximos pasos:")
    print("1. Si todas las pruebas pasaron, tu sistema está listo para usar")
    print("2. Si algunas fallaron, revisa los errores y corrige los problemas")
    print("3. Para usar en producción, considera usar datos reales en lugar de simulados")

if __name__ == "__main__":
    main() 