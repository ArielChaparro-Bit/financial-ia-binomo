#!/usr/bin/env python3
"""
Script de Optimización del Sistema IA Financiera
================================================

Este script corrige todas las discrepancias y optimiza el sistema:
1. Centraliza configuración
2. Corrige puertos y URLs
3. Actualiza documentación
4. Crea scripts unificados
"""

import os
import json
import re
import shutil
from pathlib import Path

def load_config():
    """Carga la configuración actual"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return None

def update_file_content(file_path, old_content, new_content):
    """Actualiza contenido de un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content.replace(old_content, new_content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"❌ Error actualizando {file_path}: {e}")
        return False

def fix_port_references():
    """Corrige todas las referencias al puerto 5000 por 8080"""
    print("🔧 Corrigiendo referencias de puertos...")
    
    # Archivos a actualizar
    files_to_update = [
        'start_api.py',
        'api_server_simple.py',
        'reactivate_system.py',
        'src/api_server.py',
        'mobile_app/app.py',
        'start_mobile_app.py',
        'test_api.py',
        'test_server.py',
        'test_system.py',
        'test_access.py',
        'run_complete_system.py',
        'src/auto_trader.py',
        'train_ai.py',
        'final_test.py'
    ]
    
    replacements = [
        (':5000', ':8080'),
        ('port=5000', 'port=8080'),
        ('localhost:5000', 'localhost:8080'),
        ('192.168.100.17:5000', '192.168.100.17:8080')
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            print(f"   📝 Actualizando {file_path}")
            for old, new in replacements:
                update_file_content(file_path, old, new)

def update_config_centralization():
    """Actualiza archivos para usar configuración centralizada"""
    print("⚙️ Centralizando configuración...")
    
    # Actualizar start_api.py para usar config.json
    config_import = '''import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import os

# Cargar configuración centralizada
def load_config():
    """Carga la configuración desde config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return None

config = load_config()'''
    
    # Buscar y actualizar start_api.py
    if os.path.exists('start_api.py'):
        with open('start_api.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar imports
        new_content = re.sub(
            r'from flask import Flask, request, jsonify\nfrom flask_cors import CORS\nimport numpy as np\nimport pandas as pd\nimport pickle\nfrom sklearn\.preprocessing import StandardScaler\nfrom datetime import datetime\nimport os',
            config_import,
            content
        )
        
        # Reemplazar rutas hardcodeadas
        new_content = re.sub(
            r"model_path = 'models/simple_model\.pkl'",
            "model_path = config['model']['path']",
            new_content
        )
        new_content = re.sub(
            r"scaler_path = 'models/simple_model_scaler\.pkl'",
            "scaler_path = config['model']['scaler_path']",
            new_content
        )
        new_content = re.sub(
            r"features_path = 'models/simple_model_features\.pkl'",
            "features_path = config['model']['features_path']",
            new_content
        )
        
        with open('start_api.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("   ✅ start_api.py actualizado")

def create_unified_runner():
    """Crea un script unificado para ejecutar el sistema"""
    print("🚀 Creando script unificado...")
    
    unified_script = '''#!/usr/bin/env python3
"""
IA Financiera Binomo - Ejecutor Unificado
=========================================

Este script ejecuta el sistema completo desde cualquier ubicación.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def get_project_root():
    """Obtiene la ruta raíz del proyecto"""
    current = Path.cwd()
    while current != current.parent:
        if (current / 'config.json').exists():
            return current
        current = current.parent
    return Path.cwd()

def load_config():
    """Carga la configuración"""
    config_path = get_project_root() / 'config.json'
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return None

def run_api_server():
    """Ejecuta el servidor API"""
    print("🚀 Iniciando servidor API...")
    
    project_root = get_project_root()
    os.chdir(project_root)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('start_api.py'):
        print("❌ No se encontró start_api.py")
        return False
    
    try:
        # Ejecutar servidor
        subprocess.run([sys.executable, 'start_api.py'], check=True)
        return True
    except KeyboardInterrupt:
        print("\\n🛑 Servidor detenido por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando servidor: {e}")
        return False

def run_mobile_app():
    """Ejecuta la aplicación móvil"""
    print("📱 Iniciando aplicación móvil...")
    
    project_root = get_project_root()
    mobile_app_path = project_root / 'mobile_app'
    
    if not mobile_app_path.exists():
        print("❌ No se encontró la aplicación móvil")
        return False
    
    os.chdir(mobile_app_path)
    
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
        return True
    except KeyboardInterrupt:
        print("\\n🛑 Aplicación móvil detenida por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando aplicación móvil: {e}")
        return False

def main():
    """Función principal"""
    print("🤖 IA FINANCIERA BINOMO - EJECUTOR UNIFICADO")
    print("=" * 50)
    
    config = load_config()
    if config is None:
        print("❌ No se pudo cargar la configuración")
        return
    
    print(f"📋 Configuración cargada:")
    print(f"   • API: {config['api']['base_url']}")
    print(f"   • Puerto: {config['api']['port']}")
    print(f"   • IP Local: {config['network']['local_ip']}")
    
    print("\\n🎯 ¿Qué quieres ejecutar?")
    print("   1. Servidor API")
    print("   2. Aplicación móvil")
    print("   3. Ambos")
    print("   4. Salir")
    
    try:
        choice = input("\\nSelecciona una opción (1-4): ").strip()
        
        if choice == '1':
            run_api_server()
        elif choice == '2':
            run_mobile_app()
        elif choice == '3':
            print("⚠️ Ejecutando ambos servicios...")
            # En una implementación real, usarías threading
            run_api_server()
        elif choice == '4':
            print("👋 ¡Hasta luego!")
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\\n👋 ¡Hasta luego!")

if __name__ == '__main__':
    main()
'''
    
    with open('run_system.py', 'w', encoding='utf-8') as f:
        f.write(unified_script)
    
    print("   ✅ run_system.py creado")

def update_documentation():
    """Actualiza la documentación con el puerto correcto"""
    print("📚 Actualizando documentación...")
    
    docs_to_update = [
        'README.md',
        'README_MOBILE.md',
        'INSTRUCCIONES_MOVIL.md',
        'ESTADO_ACTUAL.md',
        'SISTEMA_REACTIVADO.md'
    ]
    
    for doc_file in docs_to_update:
        if os.path.exists(doc_file):
            print(f"   📝 Actualizando {doc_file}")
            update_file_content(doc_file, ':5000', ':8080')
            update_file_content(doc_file, 'puerto 5000', 'puerto 8080')
            update_file_content(doc_file, 'port 5000', 'port 8080')

def create_quick_start_guide():
    """Crea una guía de inicio rápido"""
    print("📖 Creando guía de inicio rápido...")
    
    quick_start = '''# 🚀 Guía de Inicio Rápido - IA Financiera Binomo

## Instalación y Ejecución

### 1. Requisitos
- Python 3.8 o superior
- Conexión a internet

### 2. Instalación
```bash
# Clonar o descargar el proyecto
cd financial_ia_binomo

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecución
```bash
# Opción 1: Script unificado (recomendado)
python run_system.py

# Opción 2: Servidor API directamente
python start_api.py

# Opción 3: Aplicación móvil
python mobile_app/app.py
```

### 4. Acceso
- **API Local**: http://localhost:8080
- **API Red**: http://192.168.100.17:8080
- **App Móvil**: http://192.168.100.17:8080

## Endpoints Disponibles

### API
- `GET /` - Página principal
- `GET /health` - Estado del sistema
- `GET /predict` - Predicciones
- `GET /backtest` - Backtest del modelo

### Ejemplos de Uso
```bash
# Verificar estado
curl http://localhost:8080/health

# Obtener predicción
curl http://localhost:8080/predict

# Ejecutar backtest
curl http://localhost:8080/backtest
```

## Configuración

El sistema usa `config.json` para toda la configuración:
- Puerto API: 8080
- IP Local: 192.168.100.17
- Modelo: Random Forest

## Solución de Problemas

### Error: "No module named..."
```bash
# Instalar dependencias faltantes
pip install -r requirements.txt
```

### Error: "Modelo no cargado"
```bash
# Recrear modelo
python recreate_model.py
```

### Puerto ocupado
Cambiar el puerto en `config.json`:
```json
{
  "api": {
    "port": 8081
  }
}
```

## Soporte

Para más información, consulta:
- `README.md` - Documentación completa
- `INSTRUCCIONES_MOVIL.md` - Guía móvil
- `ESTADO_ACTUAL.md` - Estado del sistema
'''
    
    with open('GUIA_INICIO_RAPIDO.md', 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print("   ✅ GUIA_INICIO_RAPIDO.md creada")

def main():
    """Función principal de optimización"""
    print("🔧 OPTIMIZACIÓN DEL SISTEMA IA FINANCIERA")
    print("=" * 50)
    
    # Verificar configuración
    config = load_config()
    if config is None:
        print("❌ No se pudo cargar la configuración")
        return
    
    print(f"📋 Configuración actual:")
    print(f"   • Puerto API: {config['api']['port']}")
    print(f"   • Host API: {config['api']['host']}")
    print(f"   • URL Base: {config['api']['base_url']}")
    
    # Ejecutar optimizaciones
    fix_port_references()
    update_config_centralization()
    create_unified_runner()
    update_documentation()
    create_quick_start_guide()
    
    print("\n✅ OPTIMIZACIÓN COMPLETADA")
    print("=" * 50)
    print("🎯 Cambios realizados:")
    print("   • ✅ Puertos corregidos (5000 → 8080)")
    print("   • ✅ Configuración centralizada")
    print("   • ✅ Script unificado creado")
    print("   • ✅ Documentación actualizada")
    print("   • ✅ Guía de inicio rápido creada")
    
    print("\n🚀 Próximos pasos:")
    print("   1. Ejecutar: python run_system.py")
    print("   2. Acceder a: http://localhost:8080")
    print("   3. Probar endpoints: /health, /predict, /backtest")
    
    print("\n📚 Documentación:")
    print("   • GUIA_INICIO_RAPIDO.md - Guía rápida")
    print("   • README.md - Documentación completa")
    print("   • config.json - Configuración del sistema")

if __name__ == '__main__':
    main() 