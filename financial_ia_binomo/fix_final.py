#!/usr/bin/env python3
"""
Script final para corregir todos los puertos restantes
"""

import os
import glob

def fix_remaining_ports():
    """Corrige todos los puertos restantes de 5000 a 8080"""
    print("🔧 Corrigiendo puertos restantes...")
    
    # Archivos específicos que necesitan corrección
    files_to_fix = [
        'final_test.py',
        'create_sample_data.py', 
        'mobile_app/server_app.py',
        'mobile_app/templates/qr.html',
        'README.md',
        'README_MOBILE.md',
        'INSTRUCCIONES_MOVIL.md',
        'SISTEMA_REACTIVADO.md',
        'ESTADO_ACTUAL.md',
        'mobile_app/README.md'
    ]
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Reemplazos
                content = content.replace(':5000', ':8080')
                content = content.replace('port=5000', 'port=8080')
                content = content.replace('localhost:5000', 'localhost:8080')
                content = content.replace('192.168.100.17:5000', '192.168.100.17:8080')
                content = content.replace('http://localhost:5000', 'http://localhost:8080')
                content = content.replace('http://192.168.100.17:5000', 'http://192.168.100.17:8080')
                content = content.replace('"port": 5000', '"port": 8080')
                content = content.replace('puerto 5000', 'puerto 8080')
                content = content.replace('port 5000', 'port 8080')
                content = content.replace('API_PORT = 5000', 'API_PORT = 8080')
                
                if content != original:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ {file_path}")
                    fixed_count += 1
                    
            except Exception as e:
                print(f"❌ Error en {file_path}: {e}")
    
    return fixed_count

def create_run_script():
    """Crea un script de ejecución simple"""
    print("🚀 Creando script de ejecución...")
    
    script = '''#!/usr/bin/env python3
"""
IA Financiera Binomo - Ejecutor Simple
"""

import os
import sys
import subprocess

def main():
    print("🚀 IA FINANCIERA BINOMO")
    print("=" * 30)
    
    print("\\n🎯 ¿Qué quieres ejecutar?")
    print("1. Servidor API")
    print("2. Aplicación móvil") 
    print("3. Salir")
    
    choice = input("\\nSelecciona (1-3): ").strip()
    
    if choice == '1':
        print("\\n🚀 Iniciando servidor API...")
        subprocess.run([sys.executable, 'start_api.py'])
        
    elif choice == '2':
        print("\\n📱 Iniciando aplicación móvil...")
        os.chdir('mobile_app')
        subprocess.run([sys.executable, 'app.py'])
        
    elif choice == '3':
        print("👋 ¡Hasta luego!")
        
    else:
        print("❌ Opción inválida")

if __name__ == '__main__':
    main()
'''
    
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("   ✅ run.py creado")

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN FINAL DE PUERTOS")
    print("=" * 40)
    
    # Corregir puertos
    fixed_count = fix_remaining_ports()
    
    # Crear script de ejecución
    create_run_script()
    
    print("\\n✅ CORRECCIÓN COMPLETADA")
    print("=" * 40)
    print(f"📝 Archivos corregidos: {fixed_count}")
    print("🚀 Script de ejecución creado: run.py")
    
    print("\\n🎯 Tu sistema está listo:")
    print("1. Ejecutar: python run.py")
    print("2. O directamente: python start_api.py")
    print("3. Acceder a: http://localhost:8080")
    print("4. App móvil: http://192.168.100.17:8080")
    
    print("\\n📊 Endpoints disponibles:")
    print("   • GET /health - Estado del sistema")
    print("   • GET /predict - Predicciones")
    print("   • GET /backtest - Backtest")
    print("   • GET / - Página principal")

if __name__ == '__main__':
    main() 