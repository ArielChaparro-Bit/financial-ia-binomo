#!/usr/bin/env python3
"""
Script para generar aplicación Android desde la web app
Usando Apache Cordova o similar
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def check_requirements():
    """Verificar requisitos para generar APK"""
    requirements = {
        'node': 'Node.js',
        'npm': 'npm',
        'cordova': 'Apache Cordova',
        'android': 'Android SDK'
    }
    
    missing = []
    
    for cmd, name in requirements.items():
        try:
            subprocess.run([cmd, '--version'], 
                         capture_output=True, check=True)
            print(f"✅ {name} encontrado")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(name)
            print(f"❌ {name} no encontrado")
    
    return missing

def create_cordova_project():
    """Crear proyecto Cordova"""
    print("🏗️ Creando proyecto Cordova...")
    
    try:
        # Crear proyecto Cordova
        subprocess.run([
            'cordova', 'create', 'ia-financiera-app', 
            'com.iafinanciera.binomo', 'IA Financiera'
        ], check=True)
        
        print("✅ Proyecto Cordova creado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando proyecto: {e}")
        return False

def copy_web_files():
    """Copiar archivos de la web app al proyecto Cordova"""
    print("📁 Copiando archivos web...")
    
    try:
        # Crear directorio www si no existe
        www_dir = Path("ia-financiera-app/www")
        www_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar archivos de la app móvil
        mobile_app_dir = Path("mobile_app")
        
        # Copiar templates
        templates_dir = www_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        for template in mobile_app_dir.glob("templates/*.html"):
            subprocess.run([
                'cp', str(template), str(templates_dir)
            ])
        
        # Copiar static files
        static_dir = www_dir / "static"
        static_dir.mkdir(exist_ok=True)
        
        if (mobile_app_dir / "static").exists():
            subprocess.run([
                'cp', '-r', str(mobile_app_dir / "static/*"), str(static_dir)
            ])
        
        print("✅ Archivos web copiados")
        return True
    except Exception as e:
        print(f"❌ Error copiando archivos: {e}")
        return False

def create_index_html():
    """Crear index.html principal para la app"""
    print("📄 Creando index.html...")
    
    index_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Financiera Binomo</title>
    <link rel="manifest" href="static/manifest.json">
    <link rel="stylesheet" href="static/css/style.css">
    <meta name="theme-color" content="#00d4aa">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
</head>
<body>
    <div id="app">
        <header class="app-header">
            <h1>🤖 IA Financiera</h1>
            <p>Sistema de predicción de mercados</p>
        </header>
        
        <main class="app-main">
            <div class="status-card">
                <h2>Estado del Sistema</h2>
                <div id="status-content">
                    <p>Conectando...</p>
                </div>
            </div>
            
            <div class="action-buttons">
                <button onclick="getPrediction()" class="btn-primary">
                    🔮 Obtener Predicción
                </button>
                <button onclick="runBacktest()" class="btn-secondary">
                    📈 Ejecutar Backtest
                </button>
            </div>
            
            <div id="results" class="results-container">
                <!-- Resultados aquí -->
            </div>
        </main>
        
        <footer class="app-footer">
            <p>IA Financiera Binomo v2.0</p>
        </footer>
    </div>
    
    <script src="static/js/app.js"></script>
    <script>
        // Código JavaScript para la app
        document.addEventListener('DOMContentLoaded', function() {
            checkStatus();
        });
        
        function checkStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status-content').innerHTML = 
                        `<p>API: ${data.api_connected ? '✅ Conectado' : '❌ Desconectado'}</p>`;
                })
                .catch(error => {
                    document.getElementById('status-content').innerHTML = 
                        '<p>❌ Error de conexión</p>';
                });
        }
        
        function getPrediction() {
            fetch('/api/predict')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('results').innerHTML = 
                            `<div class="prediction-result">
                                <h3>Predicción: ${data.data.signal}</h3>
                                <p>Confianza: ${data.data.confidence}</p>
                                <p>Precio: $${data.data.current_price}</p>
                            </div>`;
                    } else {
                        document.getElementById('results').innerHTML = 
                            `<div class="error">Error: ${data.error}</div>`;
                    }
                });
        }
        
        function runBacktest() {
            fetch('/api/backtest')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('results').innerHTML = 
                            `<div class="backtest-result">
                                <h3>Resultados Backtest</h3>
                                <p>Predicciones: ${data.data.total_predictions}</p>
                                <p>Subidas: ${data.data.up_percentage}%</p>
                                <p>Bajadas: ${data.data.down_percentage}%</p>
                            </div>`;
                    } else {
                        document.getElementById('results').innerHTML = 
                            `<div class="error">Error: ${data.error}</div>`;
                    }
                });
        }
    </script>
</body>
</html>
"""
    
    try:
        with open("ia-financiera-app/www/index.html", "w", encoding="utf-8") as f:
            f.write(index_content)
        
        print("✅ index.html creado")
        return True
    except Exception as e:
        print(f"❌ Error creando index.html: {e}")
        return False

def configure_cordova():
    """Configurar proyecto Cordova"""
    print("⚙️ Configurando Cordova...")
    
    try:
        os.chdir("ia-financiera-app")
        
        # Agregar plataforma Android
        subprocess.run(['cordova', 'platform', 'add', 'android'], check=True)
        
        # Agregar plugins necesarios
        plugins = [
            'cordova-plugin-device',
            'cordova-plugin-network-information',
            'cordova-plugin-splashscreen',
            'cordova-plugin-statusbar'
        ]
        
        for plugin in plugins:
            subprocess.run(['cordova', 'plugin', 'add', plugin], check=True)
        
        print("✅ Cordova configurado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configurando Cordova: {e}")
        return False

def build_apk():
    """Generar APK"""
    print("📱 Generando APK...")
    
    try:
        # Construir APK
        subprocess.run(['cordova', 'build', 'android'], check=True)
        
        print("✅ APK generado exitosamente")
        print("📁 Ubicación: ia-financiera-app/platforms/android/app/build/outputs/apk/debug/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generando APK: {e}")
        return False

def main():
    """Función principal"""
    print("🤖 Generador de APK - IA Financiera")
    print("=" * 50)
    
    # Verificar requisitos
    missing = check_requirements()
    if missing:
        print(f"\n❌ Faltan requisitos: {', '.join(missing)}")
        print("💡 Instala los requisitos faltantes y vuelve a intentar")
        return
    
    # Crear proyecto
    if not create_cordova_project():
        return
    
    # Copiar archivos
    if not copy_web_files():
        return
    
    # Crear index.html
    if not create_index_html():
        return
    
    # Configurar Cordova
    if not configure_cordova():
        return
    
    # Generar APK
    if build_apk():
        print("\n🎉 ¡APK generado exitosamente!")
        print("📱 Instala el APK en tu dispositivo Android")
        print("🔗 Compártelo con otros usuarios")

if __name__ == '__main__':
    main() 