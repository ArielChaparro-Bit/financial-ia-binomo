#!/usr/bin/env python3
"""
Instalador automático de dependencias para IA Financiera
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {package} instalado")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error instalando {package}")
        return False

def main():
    """Función principal"""
    print("🔧 INSTALADOR AUTOMÁTICO - IA FINANCIERA")
    print("=" * 50)
    
    # Dependencias básicas (esenciales)
    basic_packages = [
        "numpy",
        "pandas", 
        "scikit-learn",
        "matplotlib",
        "joblib",
        "seaborn",
        "plotly",
        "yfinance",
        "ta"
    ]
    
    # Dependencias avanzadas (opcionales)
    advanced_packages = [
        "tensorflow",
        "flask",
        "flask-cors"
    ]
    
    print("📋 Instalando dependencias básicas...")
    
    success_basic = 0
    for package in basic_packages:
        if install_package(package):
            success_basic += 1
    
    print(f"\n✅ Dependencias básicas: {success_basic}/{len(basic_packages)}")
    
    print("\n📋 Instalando dependencias avanzadas...")
    
    success_advanced = 0
    for package in advanced_packages:
        if install_package(package):
            success_advanced += 1
    
    print(f"\n✅ Dependencias avanzadas: {success_advanced}/{len(advanced_packages)}")
    
    total_success = success_basic + success_advanced
    total_packages = len(basic_packages) + len(advanced_packages)
    
    print(f"\n🎉 Instalación completada!")
    print(f"   Total: {total_success}/{total_packages} paquetes instalados")
    
    if total_success >= len(basic_packages):
        print("✅ Sistema listo para usar")
        print("\n🚀 Ejecuta: python simple_test.py")
    else:
        print("⚠️ Algunas dependencias básicas faltan")
        print("   Revisa los errores anteriores")

if __name__ == "__main__":
    main() 