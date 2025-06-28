#!/usr/bin/env python3
"""
Aplicación Móvil IA Financiera Binomo
Configurada para IP específica: 192.168.100.17:8080
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import requests
import json
import os
import sys
from datetime import datetime
import threading
import time

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# Configuración específica para tu red
LOCAL_IP = "192.168.100.17"
API_PORT = 8080
MOBILE_PORT = 8080

# Configuración de la API
API_BASE_URL = f"http://{LOCAL_IP}:{API_PORT}"
API_ENDPOINTS = {
    'health': f"{API_BASE_URL}/health",
    'predict': f"{API_BASE_URL}/predict",
    'backtest': f"{API_BASE_URL}/backtest",
    'home': f"{API_BASE_URL}/"
}

# Estado de la aplicación
app_status = {
    'api_connected': False,
    'last_prediction': None,
    'last_backtest': None,
    'server_status': 'Desconectado',
    'api_url': API_BASE_URL,
    'mobile_url': f"http://{LOCAL_IP}:{MOBILE_PORT}"
}

def check_api_status():
    """Verifica el estado de la API"""
    try:
        response = requests.get(API_ENDPOINTS['health'], timeout=5)
        if response.status_code == 200:
            app_status['api_connected'] = True
            app_status['server_status'] = 'Conectado'
            return True
        else:
            app_status['api_connected'] = False
            app_status['server_status'] = 'Error'
            return False
    except requests.exceptions.ConnectionError:
        app_status['api_connected'] = False
        app_status['server_status'] = 'Desconectado'
        return False
    except Exception as e:
        app_status['api_connected'] = False
        app_status['server_status'] = f'Error: {str(e)}'
        return False

@app.route('/')
def index():
    """Página principal de la aplicación móvil"""
    # Verificar estado de la API
    check_api_status()
    
    return render_template('index.html', 
                         status=app_status,
                         title="IA Financiera Binomo",
                         mobile_url=app_status['mobile_url'])

@app.route('/predict')
def predict_page():
    """Página de predicciones"""
    check_api_status()
    return render_template('predict.html', 
                         status=app_status,
                         title="Predicciones",
                         mobile_url=app_status['mobile_url'])

@app.route('/backtest')
def backtest_page():
    """Página de backtesting"""
    check_api_status()
    return render_template('backtest.html', 
                         status=app_status,
                         title="Backtesting",
                         mobile_url=app_status['mobile_url'])

@app.route('/learn')
def learn_page():
    """Página de aprendizaje"""
    return render_template('learn.html', 
                         title="Aprende Trading",
                         mobile_url=app_status['mobile_url'])

@app.route('/qr')
def qr_page():
    """Página con código QR"""
    return render_template('qr.html', 
                         title="Código QR",
                         mobile_url=app_status['mobile_url'])

@app.route('/api/status')
def api_status():
    """Endpoint para obtener el estado de la API"""
    check_api_status()
    return jsonify(app_status)

@app.route('/api/predict', methods=['GET', 'POST'])
def get_prediction():
    """Obtener predicción desde la API"""
    try:
        response = requests.get(API_ENDPOINTS['predict'], timeout=10)
        if response.status_code == 200:
            prediction = response.json()
            app_status['last_prediction'] = {
                'data': prediction,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify({
                'success': True,
                'data': prediction
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error API: {response.status_code}',
                'api_url': API_BASE_URL
            })
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'No se puede conectar al servidor API',
            'api_url': API_BASE_URL,
            'tip': 'Asegúrate de que el servidor API esté ejecutándose'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error de conexión: {str(e)}',
            'api_url': API_BASE_URL
        })

@app.route('/api/backtest', methods=['GET', 'POST'])
def get_backtest():
    """Obtener resultados de backtest desde la API"""
    try:
        response = requests.get(API_ENDPOINTS['backtest'], timeout=15)
        if response.status_code == 200:
            backtest = response.json()
            app_status['last_backtest'] = {
                'data': backtest,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify({
                'success': True,
                'data': backtest
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error API: {response.status_code}',
                'api_url': API_BASE_URL
            })
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'No se puede conectar al servidor API',
            'api_url': API_BASE_URL,
            'tip': 'Asegúrate de que el servidor API esté ejecutándose'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error de conexión: {str(e)}',
            'api_url': API_BASE_URL
        })

@app.route('/api/start-server')
def start_server():
    """Iniciar el servidor API"""
    try:
        # Intentar iniciar el servidor API
        import subprocess
        import os
        
        # Cambiar al directorio del proyecto
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_dir)
        
        # Iniciar servidor en segundo plano
        subprocess.Popen([sys.executable, 'start_api.py'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Esperar un poco para que inicie
        time.sleep(3)
        
        # Verificar si se inició correctamente
        if check_api_status():
            return jsonify({
                'success': True,
                'message': 'Servidor iniciado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo iniciar el servidor'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al iniciar servidor: {str(e)}'
        })

@app.route('/api/health')
def health_check():
    """Verificar salud de la aplicación móvil"""
    return jsonify({
        'status': 'OK',
        'app': 'IA Financiera Móvil',
        'version': '2.0',
        'api_connected': app_status['api_connected'],
        'api_url': API_BASE_URL,
        'mobile_url': app_status['mobile_url'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/manifest.json')
def manifest():
    """Manifest para PWA (Progressive Web App)"""
    manifest_data = {
        "name": "IA Financiera Binomo",
        "short_name": "IA Binomo",
        "description": "Sistema de IA para análisis y predicción de mercados financieros",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a1a1a",
        "theme_color": "#00d4aa",
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    return jsonify(manifest_data)

@app.route('/sw.js')
def service_worker():
    """Service Worker para PWA"""
    sw_content = """
    const CACHE_NAME = 'ia-financiera-v1';
    const urlsToCache = [
        '/',
        '/static/css/style.css',
        '/static/js/app.js'
    ];

    self.addEventListener('install', event => {
        event.waitUntil(
            caches.open(CACHE_NAME)
                .then(cache => cache.addAll(urlsToCache))
        );
    });

    self.addEventListener('fetch', event => {
        event.respondWith(
            caches.match(event.request)
                .then(response => response || fetch(event.request))
        );
    });
    """
    return app.response_class(sw_content, mimetype='application/javascript')

if __name__ == '__main__':
    print("📱 Iniciando IA Financiera Móvil...")
    print(f"🔗 API URL: {API_BASE_URL}")
    print(f"📱 App URL: http://{LOCAL_IP}:{MOBILE_PORT}")
    print(f"🌐 Puerto: {MOBILE_PORT}")
    print("📱 Accede desde tu móvil usando la URL de arriba")
    print("🔗 Código QR disponible en /qr")
    
    # Verificar API al inicio
    check_api_status()
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=MOBILE_PORT, debug=False) 