#!/usr/bin/env python3
"""
Script para instalar dependencias del sistema IA Financiera
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 INSTALADOR DE DEPENDENCIAS - IA FINANCIERA")
    print("=" * 50)
    
    # Lista de dependencias básicas
    packages = [
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "joblib>=1.1.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "yfinance>=0.1.70",
        "ta>=0.10.0"
    ]
    
    # Dependencias opcionales (más pesadas)
    optional_packages = [
        "tensorflow>=2.8.0",
        "flask>=2.0.0",
        "flask-cors>=3.0.0"
    ]
    
    print("📋 Instalando dependencias básicas...")
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n✅ Dependencias básicas: {success_count}/{total_count} instaladas")
    
    # Preguntar por dependencias opcionales
    print("\n🤔 ¿Instalar TensorFlow y Flask? (puede tomar tiempo)")
    print("   - TensorFlow: Para el modelo LSTM")
    print("   - Flask: Para la API web")
    
    response = input("   Continuar? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\n📋 Instalando dependencias opcionales...")
        
        for package in optional_packages:
            if install_package(package):
                success_count += 1
            total_count += 1
    
    print(f"\n🎉 Instalación completada!")
    print(f"   Paquetes instalados: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ Todas las dependencias instaladas correctamente")
        print("\n🚀 Ahora puedes ejecutar:")
        print("   python simple_test.py")
    else:
        print("⚠️ Algunas dependencias no se pudieron instalar")
        print("   Revisa los errores anteriores")

if __name__ == "__main__":
    main() 