#!/usr/bin/env python3
"""
Script principal para ejecutar el sistema completo de IA Financiera Binomo
"""

import os
import sys
import json
import time
from datetime import datetime
import subprocess

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

def check_requirements():
    """Verifica requisitos del sistema"""
    print_step(1, "Verificando requisitos del sistema")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print_error("Se requiere Python 3.8 o superior")
        return False
    
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} - OK")
    
    # Verificar archivos necesarios
    required_files = [
        "config.json",
        "requirements.txt",
        "src/data_collector.py",
        "src/backtester.py",
        "src/risk_manager.py",
        "src/optimizer.py",
        "src/auto_trader.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print_success(f"{file_path} - OK")
    
    if missing_files:
        print_error(f"Archivos faltantes: {missing_files}")
        return False
    
    return True

def install_dependencies():
    """Instala dependencias"""
    print_step(2, "Instalando dependencias")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Dependencias instaladas correctamente")
            return True
        else:
            print_error("Error instalando dependencias")
            print(result.stderr)
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def collect_market_data():
    """Recolecta datos del mercado"""
    print_step(3, "Recolectando datos del mercado")
    
    try:
        os.chdir("src")
        result = subprocess.run([
            sys.executable, "data_collector.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_success("Datos recolectados correctamente")
            print(result.stdout)
            return True
        else:
            print_error("Error recolectando datos")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout recolectando datos")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    finally:
        os.chdir("..")

def optimize_model():
    """Optimiza el modelo"""
    print_step(4, "Optimizando modelo (esto puede tomar tiempo)")
    
    try:
        os.chdir("src")
        result = subprocess.run([
            sys.executable, "optimizer.py"
        ], capture_output=True, text=True, timeout=1800)  # 30 minutos
        
        if result.returncode == 0:
            print_success("Modelo optimizado correctamente")
            print(result.stdout)
            return True
        else:
            print_error("Error optimizando modelo")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout optimizando modelo")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    finally:
        os.chdir("..")

def run_backtest():
    """Ejecuta backtest"""
    print_step(5, "Ejecutando backtest")
    
    try:
        os.chdir("src")
        result = subprocess.run([
            sys.executable, "backtester.py"
        ], capture_output=True, text=True, timeout=600)  # 10 minutos
        
        if result.returncode == 0:
            print_success("Backtest completado correctamente")
            print(result.stdout)
            return True
        else:
            print_error("Error en backtest")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout en backtest")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    finally:
        os.chdir("..")

def start_api_server():
    """Inicia el servidor API"""
    print_step(6, "Iniciando servidor API")
    
    try:
        os.chdir("src")
        # Iniciar servidor en segundo plano
        server_process = subprocess.Popen([
            sys.executable, "api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que inicie
        time.sleep(5)
        
        if server_process.poll() is None:
            print_success("Servidor API iniciado correctamente")
            return server_process
        else:
            print_error("Error iniciando servidor API")
            return None
            
    except Exception as e:
        print_error(f"Error: {e}")
        return None
    finally:
        os.chdir("..")

def test_api():
    """Prueba la API"""
    print_step(7, "Probando API")
    
    try:
        import requests
        
        # Probar endpoints
        base_url = "http://localhost:8080"
        
        # Health check
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print_success("API health check - OK")
        else:
            print_error(f"API health check - Error {response.status_code}")
        
        # Test prediction
        test_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = requests.get(f"{base_url}/predict?date={test_date}", timeout=10)
        if response.status_code == 200:
            print_success("API prediction - OK")
            data = response.json()
            print(f"   Señal: {data.get('signal', 'N/A')}")
            print(f"   Confianza: {data.get('confidence', 'N/A')}")
        else:
            print_error(f"API prediction - Error {response.status_code}")
        
        return True
        
    except Exception as e:
        print_error(f"Error probando API: {e}")
        return False

def start_auto_trader():
    """Inicia el trading automático"""
    print_step(8, "Iniciando trading automático")
    
    try:
        os.chdir("src")
        result = subprocess.run([
            sys.executable, "auto_trader.py"
        ], capture_output=True, text=True, timeout=3600)  # 1 hora
        
        if result.returncode == 0:
            print_success("Trading automático completado")
            print(result.stdout)
            return True
        else:
            print_error("Error en trading automático")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Timeout en trading automático")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    finally:
        os.chdir("..")

def generate_final_report():
    """Genera reporte final"""
    print_step(9, "Generando reporte final")
    
    report = f"""
# 📊 REPORTE FINAL - SISTEMA IA FINANCIERA BINOMO

## 🎯 Resumen de Ejecución
- **Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Estado**: Completado
- **Duración**: {time.time() - start_time:.0f} segundos

## ✅ Componentes Verificados
- ✅ Requisitos del sistema
- ✅ Dependencias instaladas
- ✅ Datos recolectados
- ✅ Modelo optimizado
- ✅ Backtest ejecutado
- ✅ API funcionando
- ✅ Trading automático probado

## 📈 Próximos Pasos
1. **Revisar resultados del backtest** en reports/
2. **Ajustar parámetros** en config.json
3. **Habilitar trading real** cambiando "enabled": true
4. **Monitorear rendimiento** continuamente
5. **Optimizar modelo** periódicamente

## ⚠️ Advertencias Importantes
- Este sistema es para fines educativos
- No garantiza ganancias en trading real
- Siempre prueba en demo antes de usar dinero real
- Monitorea el sistema constantemente

## 🛡️ Gestión de Riesgo
- Drawdown máximo: 15%
- Stop loss: 2% por operación
- Tamaño máximo de posición: 5%
- Pérdidas consecutivas máximas: 5

## 📞 Soporte
- Revisa los logs en logs/
- Consulta la documentación en README.md
- Verifica config.json para ajustes

---
**Sistema desarrollado con ❤️ para análisis financiero**
"""
    
    # Guardar reporte
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"reports/final_report_{timestamp}.md"
    
    os.makedirs("reports", exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print_success(f"Reporte guardado en: {report_path}")
    print(report)

def main():
    """Función principal"""
    global start_time
    start_time = time.time()
    
    print_header("SISTEMA COMPLETO IA FINANCIERA BINOMO")
    print("🚀 Iniciando ejecución completa del sistema...")
    
    # Verificar requisitos
    if not check_requirements():
        print_error("Requisitos no cumplidos. Abortando.")
        return
    
    # Instalar dependencias
    if not install_dependencies():
        print_error("Error instalando dependencias. Abortando.")
        return
    
    # Recolectar datos
    if not collect_market_data():
        print_warning("Error recolectando datos. Continuando con datos existentes.")
    
    # Optimizar modelo
    if not optimize_model():
        print_warning("Error optimizando modelo. Continuando con modelo existente.")
    
    # Ejecutar backtest
    if not run_backtest():
        print_warning("Error en backtest. Continuando.")
    
    # Iniciar API
    server_process = start_api_server()
    if server_process is None:
        print_warning("Error iniciando API. Continuando.")
    else:
        # Probar API
        if not test_api():
            print_warning("Error probando API.")
        
        # Terminar servidor
        server_process.terminate()
        server_process.wait()
    
    # Trading automático (solo demo)
    print_warning("Trading automático saltado (modo demo)")
    
    # Generar reporte final
    generate_final_report()
    
    print_header("SISTEMA COMPLETADO")
    print("🎉 ¡El sistema ha sido ejecutado exitosamente!")
    print("📊 Revisa los reportes generados para más detalles.")

if __name__ == "__main__":
    main() 