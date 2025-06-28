#!/usr/bin/env python3
"""
Aplicación Móvil IA Financiera - Versión Cloud
Optimizada para despliegue en la nube sin dependencias de IP local
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# Configuración para la nube
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://ia-financiera-api.onrender.com')
PORT = int(os.environ.get('PORT', 8080))

# Endpoints de la API
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
    'api_url': API_BASE_URL
}

def check_api_status():
    """Verifica el estado de la API"""
    try:
        response = requests.get(API_ENDPOINTS['health'], timeout=10)
        if response.status_code == 200:
            app_status['api_connected'] = True
            app_status['server_status'] = 'Conectado'
            return True
        else:
            app_status['api_connected'] = False
            app_status['server_status'] = 'Error'
            return False
    except Exception as e:
        app_status['api_connected'] = False
        app_status['server_status'] = f'Desconectado: {str(e)}'
        return False

@app.route('/')
def index():
    """Página principal de la aplicación móvil"""
    check_api_status()
    
    return render_template('index.html', 
                         status=app_status,
                         title="IA Financiera Binomo - Cloud")

@app.route('/predict')
def predict_page():
    """Página de predicciones"""
    check_api_status()
    return render_template('predict.html', 
                         status=app_status,
                         title="Predicciones")

@app.route('/backtest')
def backtest_page():
    """Página de backtesting"""
    check_api_status()
    return render_template('backtest.html', 
                         status=app_status,
                         title="Backtesting")

@app.route('/learn')
def learn_page():
    """Página de aprendizaje"""
    return render_template('learn.html', 
                         title="Aprende Trading")

@app.route('/qr')
def qr_page():
    """Página con código QR"""
    return render_template('qr.html', 
                         title="Código QR")

@app.route('/api/status')
def api_status():
    """Endpoint para obtener el estado de la API"""
    check_api_status()
    return jsonify(app_status)

@app.route('/api/predict', methods=['GET', 'POST'])
def get_prediction():
    """Obtener predicción desde la API"""
    try:
        response = requests.get(API_ENDPOINTS['predict'], timeout=15)
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
        response = requests.get(API_ENDPOINTS['backtest'], timeout=20)
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
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error de conexión: {str(e)}',
            'api_url': API_BASE_URL
        })

@app.route('/api/health')
def health_check():
    """Verificar salud de la aplicación móvil"""
    return jsonify({
        'status': 'OK',
        'app': 'IA Financiera Móvil - Cloud',
        'version': '2.0',
        'api_connected': app_status['api_connected'],
        'api_url': API_BASE_URL,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/manifest.json')
def manifest():
    """Manifest para PWA (Progressive Web App)"""
    manifest_data = {
        "name": "IA Financiera Binomo - Cloud",
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
    const CACHE_NAME = 'ia-financiera-cloud-v1';
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

@app.route('/demo')
def demo():
    """Página de demostración sin API"""
    return render_template('demo.html', 
                         title="Demo - IA Financiera")

if __name__ == '__main__':
    print("🌐 Iniciando IA Financiera Móvil - Cloud...")
    print(f"🔗 API URL: {API_BASE_URL}")
    print(f"🌍 Puerto: {PORT}")
    print("📱 Aplicación disponible en la nube")
    print("🔗 Accede desde cualquier dispositivo sin IP local")
    
    # Verificar API al inicio
    check_api_status()
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=PORT, debug=False) 