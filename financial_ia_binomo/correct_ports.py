import os
import glob

def fix_ports():
    """Corrige todos los puertos de 5000 a 8080"""
    print("🔧 Corrigiendo puertos de 5000 a 8080...")
    
    # Buscar todos los archivos
    files = []
    for ext in ['*.py', '*.md', '*.json', '*.html', '*.txt']:
        files.extend(glob.glob(ext))
        files.extend(glob.glob(f'**/{ext}', recursive=True))
    
    fixed_count = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Reemplazos
            content = content.replace(':5000', ':8080')
            content = content.replace('port=5000', 'port=8080')
            content = content.replace('localhost:5000', 'localhost:8080')
            content = content.replace('192.168.100.17:5000', '192.168.100.17:8080')
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {file_path}")
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ Error en {file_path}: {e}")
    
    print(f"\n🎉 Corrección completada: {fixed_count} archivos corregidos")

if __name__ == '__main__':
    fix_ports() 