#!/usr/bin/env python3
"""
Script para probar el servidor API
"""

import requests
import time

def test_api():
    """Prueba los endpoints de la API"""
    base_url = "http://localhost:8080"
    
    print("🧪 Probando servidor API...")
    print("=" * 50)
    
    # Probar health
    try:
        print("📋 Probando /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health OK")
            print(f"   • Status: {data.get('status')}")
            print(f"   • Modelo cargado: {data.get('model_loaded')}")
            print(f"   • Tipo de modelo: {data.get('model_type')}")
            print(f"   • Datos: {data.get('data_points')} registros")
            print(f"   • Features: {data.get('features_count')} indicadores")
        else:
            print(f"❌ Health Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False
    
    print()
    
    # Probar predict
    try:
        print("📊 Probando /predict...")
        response = requests.get(f"{base_url}/predict", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Predict OK")
            print(f"   • Señal: {data.get('signal')}")
            print(f"   • Confianza: {data.get('confidence')}")
            print(f"   • Precio actual: {data.get('current_price')}")
            print(f"   • RSI: {data.get('technical_indicators', {}).get('RSI')}")
            print(f"   • MACD: {data.get('technical_indicators', {}).get('MACD')}")
        else:
            print(f"❌ Predict Error: {response.status_code}")
            print(f"   • Error: {response.text}")
    except Exception as e:
        print(f"❌ Error en predict: {e}")
    
    print()
    
    # Probar backtest
    try:
        print("📈 Probando /backtest...")
        response = requests.get(f"{base_url}/backtest", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backtest OK")
            print(f"   • Predicciones totales: {data.get('total_predictions')}")
            print(f"   • Predicciones SUBE: {data.get('up_predictions')} ({data.get('up_percentage')}%)")
            print(f"   • Predicciones BAJA: {data.get('down_predictions')} ({data.get('down_percentage')}%)")
            print(f"   • Confianza promedio: {data.get('average_confidence')}")
        else:
            print(f"❌ Backtest Error: {response.status_code}")
            print(f"   • Error: {response.text}")
    except Exception as e:
        print(f"❌ Error en backtest: {e}")
    
    print()
    
    # Probar página principal
    try:
        print("🏠 Probando /...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Página principal OK")
            print(f"   • Mensaje: {data.get('message')}")
            print(f"   • Versión: {data.get('version')}")
            print(f"   • Estado: {data.get('status')}")
        else:
            print(f"❌ Página principal Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en página principal: {e}")
    
    print()
    print("🎉 Pruebas completadas!")
    return True

if __name__ == "__main__":
    # Esperar un poco para que el servidor inicie
    print("⏳ Esperando que el servidor inicie...")
    time.sleep(3)
    
    test_api() 