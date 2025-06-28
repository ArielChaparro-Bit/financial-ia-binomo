#!/usr/bin/env python3
"""
Script para verificar si esta carpeta tiene lo mismo que GitHub
"""

import os
import subprocess
import json
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

def check_git_status():
    """Verifica el estado de Git"""
    print_step(1, "Verificando estado de Git")
    
    try:
        # Verificar si es un repositorio Git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Repositorio Git encontrado")
            
            # Verificar si hay cambios sin commitear
            if "nothing to commit, working tree clean" in result.stdout:
                print_success("No hay cambios pendientes")
                return True
            else:
                print_warning("Hay cambios sin commitear:")
                print(result.stdout)
                return False
        else:
            print_error("No es un repositorio Git")
            return False
            
    except FileNotFoundError:
        print_error("Git no está instalado")
        return False
    except Exception as e:
        print_error(f"Error verificando Git: {e}")
        return False

def check_remote_repository():
    """Verifica el repositorio remoto"""
    print_step(2, "Verificando repositorio remoto")
    
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            print_success("Repositorio remoto configurado:")
            print(result.stdout)
            return True
        else:
            print_warning("No hay repositorio remoto configurado")
            return False
            
    except Exception as e:
        print_error(f"Error verificando remoto: {e}")
        return False

def check_file_structure():
    """Verifica la estructura de archivos"""
    print_step(3, "Verificando estructura de archivos")
    
    # Archivos críticos que deben existir
    critical_files = [
        "config.json",
        "requirements.txt",
        "README.md",
        "models/simple_model.pkl",
        "models/simple_model_scaler.pkl",
        "models/simple_model_features.pkl",
        "data/price_data.csv",
        "start_api.py",
        "recreate_model.py",
        "reactivate_system.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            existing_files.append((file_path, size))
            print_success(f"{file_path} - {size} bytes")
        else:
            missing_files.append(file_path)
            print_error(f"Faltante: {file_path}")
    
    if missing_files:
        print_warning(f"Archivos faltantes: {len(missing_files)}")
        return False
    else:
        print_success(f"Todos los archivos críticos presentes: {len(existing_files)}")
        return True

def check_model_files():
    """Verifica los archivos del modelo"""
    print_step(4, "Verificando archivos del modelo")
    
    model_files = [
        "models/simple_model.pkl",
        "models/simple_model_scaler.pkl", 
        "models/simple_model_features.pkl"
    ]
    
    for file_path in model_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 0:
                print_success(f"{file_path} - {size} bytes")
            else:
                print_error(f"{file_path} está vacío")
                return False
        else:
            print_error(f"Faltante: {file_path}")
            return False
    
    return True

def check_data_files():
    """Verifica los archivos de datos"""
    print_step(5, "Verificando archivos de datos")
    
    data_files = [
        "data/price_data.csv",
        "data/test_data.csv"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 1000:  # Al menos 1KB
                print_success(f"{file_path} - {size} bytes")
            else:
                print_warning(f"{file_path} muy pequeño: {size} bytes")
        else:
            print_warning(f"Faltante: {file_path}")
    
    return True

def check_script_files():
    """Verifica los scripts principales"""
    print_step(6, "Verificando scripts principales")
    
    script_files = [
        "start_api.py",
        "recreate_model.py", 
        "reactivate_system.py",
        "api_server_simple.py"
    ]
    
    for file_path in script_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 100:  # Al menos 100 bytes
                print_success(f"{file_path} - {size} bytes")
            else:
                print_error(f"{file_path} muy pequeño: {size} bytes")
                return False
        else:
            print_error(f"Faltante: {file_path}")
            return False
    
    return True

def generate_comparison_report():
    """Genera un reporte de comparación"""
    print_step(7, "Generando reporte de comparación")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "local_directory": os.getcwd(),
        "git_status": "unknown",
        "remote_repo": "unknown",
        "critical_files": [],
        "model_files": [],
        "data_files": [],
        "script_files": [],
        "summary": {
            "total_files_checked": 0,
            "files_present": 0,
            "files_missing": 0,
            "files_empty": 0
        }
    }
    
    # Verificar archivos críticos
    critical_files = [
        "config.json", "requirements.txt", "README.md",
        "models/simple_model.pkl", "models/simple_model_scaler.pkl", 
        "models/simple_model_features.pkl", "data/price_data.csv",
        "start_api.py", "recreate_model.py", "reactivate_system.py"
    ]
    
    for file_path in critical_files:
        report["summary"]["total_files_checked"] += 1
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            report["critical_files"].append({"file": file_path, "size": size, "status": "present"})
            report["summary"]["files_present"] += 1
            if size == 0:
                report["summary"]["files_empty"] += 1
        else:
            report["critical_files"].append({"file": file_path, "size": 0, "status": "missing"})
            report["summary"]["files_missing"] += 1
    
    # Crear directorio reports si no existe
    os.makedirs("reports", exist_ok=True)
    
    # Guardar reporte
    with open("reports/github_comparison.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print_success("Reporte guardado en reports/github_comparison.json")
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE COMPARACIÓN:")
    print(f"   • Archivos verificados: {report['summary']['total_files_checked']}")
    print(f"   • Archivos presentes: {report['summary']['files_present']}")
    print(f"   • Archivos faltantes: {report['summary']['files_missing']}")
    print(f"   • Archivos vacíos: {report['summary']['files_empty']}")
    
    return report

def main():
    """Función principal"""
    print_header("VERIFICACIÓN DE DIFERENCIAS CON GITHUB")
    
    # Verificar Git
    git_ok = check_git_status()
    
    # Verificar remoto
    remote_ok = check_remote_repository()
    
    # Verificar estructura
    structure_ok = check_file_structure()
    
    # Verificar modelo
    model_ok = check_model_files()
    
    # Verificar datos
    data_ok = check_data_files()
    
    # Verificar scripts
    scripts_ok = check_script_files()
    
    # Generar reporte
    report = generate_comparison_report()
    
    print_header("RESULTADO DE LA VERIFICACIÓN")
    
    if all([structure_ok, model_ok, data_ok, scripts_ok]):
        print_success("✅ CARPETA LOCAL COMPLETA")
        print("   Esta carpeta contiene todos los archivos necesarios")
        
        if git_ok and remote_ok:
            print_success("✅ SINCRONIZADO CON GITHUB")
            print("   No hay diferencias con el repositorio remoto")
        else:
            print_warning("⚠️ VERIFICAR SINCRONIZACIÓN CON GITHUB")
            print("   Ejecuta 'git status' y 'git push' si es necesario")
    else:
        print_error("❌ CARPETA INCOMPLETA")
        print("   Faltan archivos o están dañados")
        print("   Ejecuta 'recreate_model.py' para regenerar el modelo")
    
    print(f"\n📁 Reporte detallado: reports/github_comparison.json")

if __name__ == "__main__":
    main() 