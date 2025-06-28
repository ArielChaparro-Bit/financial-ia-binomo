#!/usr/bin/env python3
"""
Script para desplegar IA Financiera a la nube automáticamente
"""

import os
import subprocess
import sys
import json
from datetime import datetime

def check_git():
    """Verificar si Git está instalado"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print("✅ Git encontrado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git no encontrado")
        print("💡 Instala Git desde: https://git-scm.com/")
        return False

def check_heroku():
    """Verificar si Heroku CLI está instalado"""
    try:
        subprocess.run(['heroku', '--version'], capture_output=True, check=True)
        print("✅ Heroku CLI encontrado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Heroku CLI no encontrado")
        print("💡 Instala Heroku CLI desde: https://devcenter.heroku.com/articles/heroku-cli")
        return False

def create_heroku_app():
    """Crear aplicación en Heroku"""
    print("🚀 Creando aplicación en Heroku...")
    
    try:
        # Crear app en Heroku
        result = subprocess.run([
            'heroku', 'create', 'ia-financiera-binomo'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Aplicación Heroku creada")
            return True
        else:
            print("⚠️ Aplicación ya existe o error")
            return True
    except Exception as e:
        print(f"❌ Error creando app: {e}")
        return False

def deploy_to_heroku():
    """Desplegar a Heroku"""
    print("📤 Desplegando a Heroku...")
    
    try:
        # Agregar archivos
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit
        subprocess.run([
            'git', 'commit', '-m', f'Deploy {datetime.now().strftime("%Y-%m-%d %H:%M")}'
        ], check=True)
        
        # Push a Heroku
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        print("✅ Desplegado exitosamente a Heroku")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en despliegue: {e}")
        return False

def deploy_to_render():
    """Instrucciones para Render"""
    print("🌐 Para desplegar en Render:")
    print("1. Ve a https://render.com")
    print("2. Conecta tu repositorio de GitHub")
    print("3. Selecciona 'Web Service'")
    print("4. Build Command: pip install -r requirements.txt")
    print("5. Start Command: python mobile_app/app_cloud.py")
    print("6. ¡Listo! Tu app estará disponible en la nube")

def create_deployment_guide():
    """Crear guía de despliegue"""
    guide = """
# 🚀 Guía de Despliegue - IA Financiera

## Opción 1: Render (Recomendado)

1. **Ve a Render.com** y crea una cuenta
2. **Conecta tu repositorio** de GitHub
3. **Crea un Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python mobile_app/app_cloud.py`
4. **¡Listo!** Tu app estará disponible en la nube

## Opción 2: Heroku

1. **Instala Heroku CLI**
2. **Ejecuta**: `python deploy_to_cloud.py`
3. **O manualmente**:
   ```bash
   heroku create ia-financiera-binomo
   git push heroku main
   ```

## Opción 3: Vercel

1. **Ve a Vercel.com**
2. **Importa tu repositorio**
3. **Configura como Python app**
4. **¡Listo!**

## URLs de Acceso

Después del despliegue, tu app estará disponible en:
- **Render**: https://tu-app.onrender.com
- **Heroku**: https://tu-app.herokuapp.com
- **Vercel**: https://tu-app.vercel.app

## Características Cloud

✅ **Sin IP local** - Acceso desde cualquier lugar
✅ **Siempre disponible** - 24/7 online
✅ **Escalable** - Se adapta al tráfico
✅ **Seguro** - HTTPS automático
✅ **Móvil** - PWA instalable

## Próximos Pasos

1. **Sube tu código a GitHub**
2. **Conecta a Render/Heroku**
3. **Comparte la URL** con otros
4. **¡Disfruta tu app en la nube!**
"""
    
    with open('GUIA_DESPLIEGUE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Guía de despliegue creada: GUIA_DESPLIEGUE.md")

def main():
    """Función principal"""
    print("🌐 Desplegador Cloud - IA Financiera")
    print("=" * 50)
    
    # Verificar herramientas
    if not check_git():
        return
    
    # Crear guía de despliegue
    create_deployment_guide()
    
    # Opciones de despliegue
    print("\n🎯 Opciones de despliegue:")
    print("1. Render (Recomendado - Gratis)")
    print("2. Heroku (Requiere CLI)")
    print("3. Vercel (Alternativa)")
    
    choice = input("\nSelecciona opción (1-3): ").strip()
    
    if choice == "1":
        deploy_to_render()
    elif choice == "2":
        if check_heroku():
            if create_heroku_app():
                deploy_to_heroku()
    elif choice == "3":
        print("🌐 Para Vercel:")
        print("1. Ve a vercel.com")
        print("2. Importa tu repositorio")
        print("3. Configura como Python app")
    else:
        print("❌ Opción no válida")
    
    print("\n📚 Consulta GUIA_DESPLIEGUE.md para más detalles")

if __name__ == '__main__':
    main() 