#!/usr/bin/env python3
"""
Script para iniciar el servidor API con el modelo simple
"""

import json
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

config = load_config()

app = Flask(__name__)
CORS(app)

# Variables globales
model = None
scaler = None
features = None
df = None
model_loaded = False

def load_model_and_data():
    """Carga el modelo simple y los datos necesarios"""
    global model, scaler, features, df, model_loaded
    
    try:
        # Usar rutas de configuración
        model_path = config['model']['path']
        scaler_path = config['model']['scaler_path']
        features_path = config['model']['features_path']
        
        if not all(os.path.exists(p) for p in [model_path, scaler_path, features_path]):
            print("❌ Archivos del modelo simple no encontrados")
            model_loaded = False
            return
        
        # Cargar modelo
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Cargar scaler
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # Cargar features
        with open(features_path, 'rb') as f:
            features = pickle.load(f)
        
        # Cargar datos
        data_path = 'data/price_data.csv'
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            # Convertir timestamp a datetime si existe
            if 'timestamp' in df.columns:
                df['datetime'] = pd.to_datetime(df['timestamp'])
            elif 'datetime' in df.columns:
                df['datetime'] = pd.to_datetime(df['datetime'])
            else:
                # Crear datetime si no existe
                df['datetime'] = pd.date_range('2023-01-01', periods=len(df), freq='1min')
        
        model_loaded = True
        print("✅ Modelo simple cargado exitosamente")
        print(f"   • Features: {len(features)}")
        print(f"   • Datos: {len(df) if df is not None else 0} registros")
        
    except Exception as e:
        print(f"❌ Error al cargar modelo y datos: {e}")
        model_loaded = False

def calculate_technical_indicators(df):
    """Calcula indicadores técnicos básicos"""
    # Medias móviles
    df['sma_5'] = df['close'].rolling(window=5).mean()
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']
    
    # Bollinger Bands
    df['bb_middle'] = df['close'].rolling(window=20).mean()
    bb_std = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
    df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
    df['bb_width'] = df['bb_upper'] - df['bb_lower']
    df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
    
    # Stochastic
    low_min = df['low'].rolling(window=14).min()
    high_max = df['high'].rolling(window=14).max()
    df['stoch_k'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
    df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
    
    # Volumen
    df['volume_sma'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_sma']
    
    # Momentum
    df['momentum'] = df['close'] - df['close'].shift(4)
    df['rate_of_change'] = ((df['close'] - df['close'].shift(10)) / df['close'].shift(10)) * 100
    
    # ATR
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    df['atr'] = true_range.rolling(window=14).mean()
    
    # Williams %R
    highest_high = df['high'].rolling(window=14).max()
    lowest_low = df['low'].rolling(window=14).min()
    df['williams_r'] = -100 * ((highest_high - df['close']) / (highest_high - lowest_low))
    
    # Cambios de precio
    df['price_change'] = df['close'].pct_change()
    df['price_change_5'] = df['close'].pct_change(5)
    df['price_change_10'] = df['close'].pct_change(10)
    
    return df

@app.route('/predict', methods=['GET'])
def predict():
    """Endpoint para predicciones"""
    if not model_loaded:
        return jsonify({
            'error': 'Modelo no cargado', 
            'message': 'Ejecuta recreate_model.py primero'
        }), 500
    
    try:
        # Calcular indicadores si no existen
        if 'sma_5' not in df.columns:
            df = calculate_technical_indicators(df)
        
        # Usar el último registro
        idx = len(df) - 1
        
        # Obtener features del índice actual
        feature_data = []
        for feature in features:
            if feature in df.columns:
                feature_data.append(df.iloc[idx][feature])
            else:
                feature_data.append(0.0)  # Valor por defecto
        
        feature_data = np.array(feature_data).reshape(1, -1)
        
        # Escalar features
        feature_data_scaled = scaler.transform(feature_data)
        
        # Predecir
        prediction_proba = model.predict_proba(feature_data_scaled)[0]
        prediction = model.predict(feature_data_scaled)[0]
        
        # Calcular confianza
        confidence = max(prediction_proba)
        
        # Obtener datos actuales
        current_price = float(df.iloc[idx]['close'])
        current_rsi = float(df.iloc[idx]['rsi']) if 'rsi' in df.columns else None
        current_macd = float(df.iloc[idx]['macd']) if 'macd' in df.columns else None
        
        return jsonify({
            'signal': 'SUBE' if prediction == 1 else 'BAJA',
            'confidence': round(float(confidence), 3),
            'prediction_value': round(float(prediction_proba[1]), 3),
            'current_price': current_price,
            'technical_indicators': {
                'RSI': current_rsi,
                'MACD': current_macd
            },
            'model_info': {
                'type': 'Random Forest',
                'features_used': len(features),
                'model_loaded': model_loaded
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en predicción: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de estado del sistema"""
    return jsonify({
        'status': 'OK',
        'model_loaded': model_loaded,
        'model_type': 'Random Forest (Simple)',
        'data_points': len(df) if df is not None else 0,
        'features_count': len(features) if features is not None else 0
    })

@app.route('/backtest', methods=['GET'])
def run_backtest():
    """Endpoint para ejecutar backtest simple"""
    if not model_loaded or df is None:
        return jsonify({'error': 'Modelo o datos no cargados'}), 500
    
    try:
        # Calcular indicadores si no existen
        if 'sma_5' not in df.columns:
            df = calculate_technical_indicators(df)
        
        # Preparar features para todo el dataset
        feature_data = []
        for idx in range(len(df)):
            features_row = []
            for feature in features:
                if feature in df.columns:
                    features_row.append(df.iloc[idx][feature])
                else:
                    features_row.append(0.0)
            feature_data.append(features_row)
        
        feature_data = np.array(feature_data)
        
        # Eliminar filas con NaN
        valid_indices = ~np.isnan(feature_data).any(axis=1)
        feature_data_clean = feature_data[valid_indices]
        
        if len(feature_data_clean) == 0:
            return jsonify({'error': 'No hay datos válidos para backtest'}), 500
        
        # Escalar features
        feature_data_scaled = scaler.transform(feature_data_clean)
        
        # Predecir
        predictions = model.predict(feature_data_scaled)
        probabilities = model.predict_proba(feature_data_scaled)
        
        # Calcular métricas
        total_predictions = len(predictions)
        up_predictions = np.sum(predictions == 1)
        down_predictions = np.sum(predictions == 0)
        
        avg_confidence = np.mean(np.max(probabilities, axis=1))
        
        results = {
            'total_predictions': total_predictions,
            'up_predictions': int(up_predictions),
            'down_predictions': int(down_predictions),
            'up_percentage': round(float(up_predictions / total_predictions * 100), 2),
            'down_percentage': round(float(down_predictions / total_predictions * 100), 2),
            'average_confidence': round(float(avg_confidence), 3),
            'model_type': 'Random Forest (Simple)',
            'features_used': len(features)
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Error en backtest: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def home():
    """Página principal de la API"""
    return jsonify({
        'message': 'IA Financiera Binomo API (Modelo Simple)',
        'version': '2.0',
        'model_type': 'Random Forest',
        'endpoints': {
            '/health': 'Estado del sistema',
            '/predict': 'Predicciones',
            '/backtest': 'Backtest simple del modelo'
        },
        'status': 'ACTIVO' if model_loaded else 'MODELO NO CARGADO'
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor API (Modelo Simple)...")
    
    if config is None:
        print("❌ No se pudo cargar la configuración")
        exit(1)
    
    load_model_and_data()
    
    # Usar configuración centralizada
    host = config['api']['host']
    port = config['api']['port']
    base_url = config['api']['base_url']
    
    print(f"🌐 Servidor disponible en: {base_url}")
    print(f"📊 Endpoints disponibles:")
    print("   • GET / - Página principal")
    print("   • GET /health - Estado del sistema")
    print("   • GET /predict - Predicciones")
    print("   • GET /backtest - Backtest")
    print(f"\n🔗 Accede desde:")
    print(f"   • Local: {base_url}")
    print(f"   • Red: http://{config['network']['local_ip']}:{port}")
    
    app.run(host=host, port=port, debug=config['api']['debug']) 
