#!/usr/bin/env python3
"""
Verificador de Preparación para Render
"""

import os
import sys

def check_file_exists(filepath, description):
    """Verifica que un archivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NO ENCONTRADO")
        return False

def check_directory_structure():
    """Verifica la estructura de directorios"""
    print("📁 Verificando estructura de directorios...")
    
    required_dirs = [
        ("mobile_app", "Directorio de la app móvil"),
        ("mobile_app/templates", "Plantillas HTML"),
        ("mobile_app/static", "Archivos estáticos"),
    ]
    
    all_good = True
    for dir_path, description in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {description}: {dir_path}/")
        else:
            print(f"❌ {description}: {dir_path}/ - NO ENCONTRADO")
            all_good = False
    
    return all_good

def check_required_files():
    """Verifica archivos requeridos"""
    print("\n📄 Verificando archivos requeridos...")
    
    required_files = [
        ("requirements_server.txt", "Dependencias para servidor"),
        ("render.yaml", "Configuración de Render"),
        ("mobile_app/server_app.py", "App principal para servidor"),
        ("mobile_app/templates/index.html", "Página principal"),
        ("mobile_app/templates/learn.html", "Página de aprendizaje"),
        ("README.md", "Documentación del proyecto"),
    ]
    
    all_good = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    return all_good

def check_python_syntax():
    """Verifica sintaxis de Python"""
    print("\n🐍 Verificando sintaxis de Python...")
    
    python_files = [
        "mobile_app/server_app.py",
        "mobile_app/app.py",
    ]
    
    all_good = True
    for filepath in python_files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, filepath, 'exec')
                print(f"✅ Sintaxis correcta: {filepath}")
            except SyntaxError as e:
                print(f"❌ Error de sintaxis en {filepath}: {e}")
                all_good = False
            except Exception as e:
                print(f"⚠️ Error verificando {filepath}: {e}")
        else:
            print(f"⚠️ Archivo no encontrado: {filepath}")
    
    return all_good

def check_requirements():
    """Verifica archivo de dependencias"""
    print("\n📦 Verificando dependencias...")
    
    if not os.path.exists("requirements_server.txt"):
        print("❌ requirements_server.txt no encontrado")
        return False
    
    try:
        with open("requirements_server.txt", 'r') as f:
            requirements = f.read().strip()
        
        if not requirements:
            print("❌ requirements_server.txt está vacío")
            return False
        
        required_packages = [
            "Flask",
            "pandas", 
            "numpy",
            "scikit-learn",
            "joblib",
            "gunicorn"
        ]
        
        missing_packages = []
        for package in required_packages:
            if package.lower() not in requirements.lower():
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Paquetes faltantes: {', '.join(missing_packages)}")
            return False
        else:
            print("✅ Todas las dependencias están incluidas")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando dependencias: {e}")
        return False

def check_render_config():
    """Verifica configuración de Render"""
    print("\n⚙️ Verificando configuración de Render...")
    
    if not os.path.exists("render.yaml"):
        print("❌ render.yaml no encontrado")
        return False
    
    try:
        with open("render.yaml", 'r') as f:
            config = f.read()
        
        required_configs = [
            "buildCommand",
            "startCommand",
            "gunicorn"
        ]
        
        missing_configs = []
        for config_item in required_configs:
            if config_item not in config:
                missing_configs.append(config_item)
        
        if missing_configs:
            print(f"❌ Configuraciones faltantes: {', '.join(missing_configs)}")
            return False
        else:
            print("✅ Configuración de Render correcta")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def generate_summary():
    """Genera resumen de verificación"""
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    checks = [
        ("Estructura de directorios", check_directory_structure()),
        ("Archivos requeridos", check_required_files()),
        ("Sintaxis de Python", check_python_syntax()),
        ("Dependencias", check_requirements()),
        ("Configuración de Render", check_render_config()),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, result in checks:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("\n🎉 ¡TODO LISTO PARA RENDER!")
        print("💡 Próximos pasos:")
        print("   1. Sube tu código a GitHub")
        print("   2. Ve a render.com")
        print("   3. Sigue la guía en GUIA_RENDER_PASO_A_PASO.md")
        
    else:
        print("\n⚠️ Hay problemas que resolver antes de desplegar")
        print("💡 Revisa los errores anteriores y corrígelos")
    
    return passed == total

def main():
    """Función principal"""
    print("🚀 VERIFICADOR DE PREPARACIÓN PARA RENDER")
    print("=" * 60)
    
    # Ejecutar todas las verificaciones
    generate_summary()
    
    print(f"\n📚 Documentación disponible:")
    print("   - GUIA_RENDER_PASO_A_PASO.md (Guía visual)")
    print("   - DEPLOY_GUIDE.md (Guía técnica)")
    print("   - README.md (Documentación general)")

if __name__ == "__main__":
    main() 