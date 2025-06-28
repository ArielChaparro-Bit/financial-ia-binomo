#!/usr/bin/env python3
"""
Script para corregir automáticamente todos los puertos restantes
"""

import os
import glob
import re

def fix_all_ports():
    """Corrige todos los puertos de 5000 a 8080 en todos los archivos"""
    print("🔧 Corrigiendo todos los puertos de 5000 a 8080...")
    
    # Buscar todos los archivos
    all_files = []
    
    # Archivos Python
    all_files.extend(glob.glob("*.py"))
    all_files.extend(glob.glob("**/*.py", recursive=True))
    
    # Archivos de documentación
    all_files.extend(glob.glob("*.md"))
    all_files.extend(glob.glob("**/*.md", recursive=True))
    
    # Archivos HTML
    all_files.extend(glob.glob("**/*.html", recursive=True))
    
    # Archivos JSON (excepto config.json que ya está corregido)
    json_files = glob.glob("*.json")
    json_files.extend(glob.glob("**/*.json", recursive=True))
    all_files.extend([f for f in json_files if f != "config.json"])
    
    # Archivos de texto
    all_files.extend(glob.glob("*.txt"))
    all_files.extend(glob.glob("**/*.txt", recursive=True))
    
    fixed_files = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Reemplazos específicos
            replacements = [
                (':5000', ':8080'),
                ('port=5000', 'port=8080'),
                ('localhost:5000', 'localhost:8080'),
                ('192.168.100.17:5000', '192.168.100.17:8080'),
                ('http://localhost:5000', 'http://localhost:8080'),
                ('http://192.168.100.17:5000', 'http://192.168.100.17:8080'),
                ('API_PORT = 5000', 'API_PORT = 8080'),
                ('"port": 5000', '"port": 8080'),
                ('puerto 5000', 'puerto 8080'),
                ('port 5000', 'port 8080')
            ]
            
            for old, new in replacements:
                content = content.replace(old, new)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ {file_path}")
                
        except Exception as e:
            print(f"❌ Error en {file_path}: {e}")
    
    return fixed_files

def create_unified_runner():
    """Crea un script unificado para ejecutar el sistema"""
    print("🚀 Creando script unificado...")
    
    runner_script = '''#!/usr/bin/env python3
"""
IA Financiera Binomo - Ejecutor Unificado
=========================================

Este script ejecuta el sistema completo desde cualquier ubicación.
"""

import os
import sys
import subprocess
import json
import time

def load_config():
    """Carga la configuración"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return None

def main():
    """Función principal"""
    print("🚀 IA FINANCIERA BINOMO - SISTEMA UNIFICADO")
    print("=" * 50)
    
    config = load_config()
    if config:
        print(f"📋 Puerto API: {config['api']['port']}")
        print(f"📋 Host: {config['api']['host']}")
        print(f"📋 URL Base: {config['api']['base_url']}")
    
    print("\\n🎯 ¿Qué quieres ejecutar?")
    print("1. Servidor API")
    print("2. Aplicación móvil")
    print("3. Ambos servicios")
    print("4. Salir")
    
    choice = input("\\nSelecciona una opción (1-4): ").strip()
    
    if choice == '1':
        print("\\n🚀 Iniciando servidor API...")
        subprocess.run([sys.executable, 'start_api.py'])
        
    elif choice == '2':
        print("\\n📱 Iniciando aplicación móvil...")
        os.chdir('mobile_app')
        subprocess.run([sys.executable, 'app.py'])
        
    elif choice == '3':
        print("\\n🚀 Iniciando ambos servicios...")
        print("⚠️ Ejecutando servidor API en segundo plano...")
        
        # Iniciar API en segundo plano
        api_process = subprocess.Popen([sys.executable, 'start_api.py'])
        
        # Esperar a que inicie
        time.sleep(3)
        
        print("📱 Iniciando aplicación móvil...")
        os.chdir('mobile_app')
        subprocess.run([sys.executable, 'app.py'])
        
        # Terminar API
        api_process.terminate()
        
    elif choice == '4':
        print("👋 ¡Hasta luego!")
        
    else:
        print("❌ Opción inválida")

if __name__ == '__main__':
    main()
'''
    
    with open('run_unified.py', 'w', encoding='utf-8') as f:
        f.write(runner_script)
    
    print("   ✅ run_unified.py creado")

def update_documentation():
    """Actualiza la documentación principal"""
    print("📚 Actualizando documentación...")
    
    # Actualizar README.md
    readme_content = '''# 🤖 IA Financiera Binomo

Sistema completo de inteligencia artificial para trading en Binomo con modelo Random Forest optimizado.

## 🚀 Inicio Rápido

### 1. Instalación
```bash
pip install -r requirements.txt
```

### 2. Ejecución
```bash
# Opción 1: Script unificado (recomendado)
python run_unified.py

# Opción 2: Servidor API directamente
python start_api.py

# Opción 3: Aplicación móvil
python mobile_app/app.py
```

### 3. Acceso
- **API Local**: http://localhost:8080
- **API Red**: http://192.168.100.17:8080
- **App Móvil**: http://192.168.100.17:8080

## 📊 Endpoints Disponibles

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

## ⚙️ Configuración

El sistema usa `config.json` para toda la configuración:
- Puerto API: 8080
- IP Local: 192.168.100.17
- Modelo: Random Forest

## 🛠️ Solución de Problemas

### Error: "No module named..."
```bash
pip install -r requirements.txt
```

### Error: "Modelo no cargado"
```bash
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

## 📱 Aplicación Móvil

La aplicación móvil incluye:
- Interfaz responsive
- Predicciones en tiempo real
- Backtesting visual
- Código QR para acceso móvil
- PWA (Progressive Web App)

## 🔧 Desarrollo

### Estructura del Proyecto
```
financial_ia_binomo/
├── start_api.py          # Servidor API principal
├── mobile_app/           # Aplicación móvil
├── src/                  # Código fuente
├── models/               # Modelos entrenados
├── data/                 # Datos de mercado
├── config.json           # Configuración centralizada
└── requirements.txt      # Dependencias
```

### Scripts Disponibles
- `start_api.py` - Servidor API
- `mobile_app/app.py` - Aplicación móvil
- `run_unified.py` - Ejecutor unificado
- `recreate_model.py` - Recrear modelo
- `test_api.py` - Probar API

## 📈 Características

- ✅ Modelo Random Forest optimizado
- ✅ API REST completa
- ✅ Aplicación móvil responsive
- ✅ Backtesting automático
- ✅ Gestión de riesgo
- ✅ Configuración centralizada
- ✅ Documentación completa

## ⚠️ Advertencias

- Este sistema es para fines educativos
- No garantiza ganancias en trading real
- Siempre prueba en demo antes de usar dinero real

## 📞 Soporte

- Revisa los logs en `logs/`
- Consulta la documentación
- Verifica `config.json` para ajustes

---
**Desarrollado con ❤️ para análisis financiero**
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("   ✅ README.md actualizado")

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN COMPLETA DEL SISTEMA")
    print("=" * 50)
    
    # Corregir puertos
    fixed_files = fix_all_ports()
    
    # Crear script unificado
    create_unified_runner()
    
    # Actualizar documentación
    update_documentation()
    
    print("\n✅ CORRECCIÓN COMPLETADA")
    print("=" * 50)
    print(f"📝 Archivos corregidos: {len(fixed_files)}")
    print("🚀 Script unificado creado: run_unified.py")
    print("📚 Documentación actualizada")
    
    print("\n🎯 Próximos pasos:")
    print("1. Ejecutar: python run_unified.py")
    print("2. O directamente: python start_api.py")
    print("3. Acceder a: http://localhost:8080")
    print("4. Probar endpoints: /health, /predict, /backtest")
    
    print("\n📱 Para la app móvil:")
    print("1. Ejecutar: python mobile_app/app.py")
    print("2. Acceder desde móvil: http://192.168.100.17:8080")
    print("3. Escanear código QR en: http://192.168.100.17:8080/qr")

if __name__ == '__main__':
    main() 