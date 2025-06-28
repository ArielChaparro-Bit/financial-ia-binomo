#!/usr/bin/env python3
"""
🎯 EJECUTAR SISTEMA IA FINANCIERA
Script simple para ejecutar todo el sistema
"""

import os
import sys
import subprocess
import time

def main():
    print("🎯 EJECUTANDO SISTEMA IA FINANCIERA")
    print("=" * 50)
    
    # Paso 1: Recrear modelo
    print("\n📋 PASO 1: Recreando modelo...")
    try:
        subprocess.run([sys.executable, "recreate_model.py"], check=True)
        print("✅ Modelo recreado correctamente")
    except:
        print("❌ Error recreando modelo")
        return
    
    # Paso 2: Iniciar servidor
    print("\n📋 PASO 2: Iniciando servidor API...")
    try:
        process = subprocess.Popen([sys.executable, "start_api.py"])
        print("✅ Servidor iniciado")
        print("🔄 Esperando 5 segundos...")
        time.sleep(5)
        
        # Paso 3: Probar API
        print("\n📋 PASO 3: Probando API...")
        subprocess.run([sys.executable, "test_api.py"], check=True)
        
        print("\n🎉 ¡SISTEMA LISTO!")
        print("📊 URLs:")
        print("   • Local: http://localhost:8080")
        print("   • Red: http://192.168.100.17:8080")
        print("\n⚠️ NO cierres esta ventana")
        print("🛑 Para detener: Ctrl+C")
        
        # Mantener corriendo
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        process.terminate()
    except:
        print("❌ Error iniciando servidor")

if __name__ == "__main__":
    main() 