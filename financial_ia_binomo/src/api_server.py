from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from data_processing import load_data
from features import add_technical_indicators, get_feature_columns
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import os
import joblib

app = Flask(__name__)
CORS(app)

# Variables globales
model = None
scaler = None
features = None
df = None
data = None
seq_length = 30
model_loaded = False

def load_model_and_data():
    """Carga el modelo y los datos necesarios"""
    global model, scaler, features, df, data, model_loaded
    
    try:
        # Cargar datos
        df = load_data('../data/price_data.csv')
        df = add_technical_indicators(df)
        
        # Cargar características guardadas o usar por defecto
        features_path = '../models/features.pkl'
        if os.path.exists(features_path):
            features = joblib.load(features_path)
        else:
            features = get_feature_columns()
        
        # Verificar características disponibles
        features = [f for f in features if f in df.columns]
        
        # Cargar scaler guardado o crear nuevo
        scaler_path = '../models/scaler.pkl'
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
        else:
            scaler = MinMaxScaler()
            data_temp = scaler.fit_transform(df[features])
        
        # Preparar datos
        data = scaler.transform(df[features])
        
        # Cargar modelo
        model_path = '../models/lstm_model.h5'
        if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
            model = load_model(model_path)
            model_loaded = True
            print("✅ Modelo cargado exitosamente")
        else:
            model_loaded = False
            print("⚠️ Modelo no encontrado. Ejecuta primero model_train.py")
            
    except Exception as e:
        print(f"❌ Error al cargar modelo y datos: {e}")
        model_loaded = False

def get_sequence(idx):
    """Obtiene la secuencia de datos para predicción"""
    return data[idx-seq_length:idx]

@app.route('/predict', methods=['GET'])
def predict():
    """Endpoint para predicciones"""
    if not model_loaded:
        return jsonify({
            'error': 'Modelo no entrenado', 
            'message': 'Ejecuta model_train.py primero'
        }), 500
    
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Parámetro date requerido'}), 400
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({
            'error': 'Formato de fecha inválido', 
            'format': 'YYYY-MM-DD HH:MM:SS'
        }), 400

    try:
        # Buscar la fecha más cercana
        df['datetime'] = pd.to_datetime(df['datetime'])
        exact_match = df[df['datetime'] == date]
        
        if len(exact_match) == 0:
            # Buscar la fecha más cercana
            df['time_diff'] = abs(df['datetime'] - date)
            closest_idx = df['time_diff'].idxmin()
            idx = closest_idx
            actual_date = df.loc[idx, 'datetime']
            used_closest = True
        else:
            idx = exact_match.index[0]
            actual_date = date
            used_closest = False
        
        if idx < seq_length:
            return jsonify({
                'error': 'Datos insuficientes para predicción',
                'required': seq_length,
                'available': idx
            }), 400
            
        # Obtener secuencia y predecir
        seq = get_sequence(idx)
        pred = model.predict(np.expand_dims(seq, axis=0), verbose=0)[0][0]
        
        # Calcular confianza
        confidence = abs(pred - 0.5) * 2  # Normalizar a 0-1
        
        # Obtener datos actuales
        current_price = float(df.loc[idx, 'close'])
        current_rsi = float(df.loc[idx, 'RSI_14']) if 'RSI_14' in df.columns else None
        current_macd = float(df.loc[idx, 'MACD']) if 'MACD' in df.columns else None
        
        # Análisis técnico adicional
        technical_analysis = {}
        if 'RSI_14' in df.columns:
            if current_rsi > 70:
                technical_analysis['RSI'] = 'Sobrecomprado'
            elif current_rsi < 30:
                technical_analysis['RSI'] = 'Sobreventa'
            else:
                technical_analysis['RSI'] = 'Neutral'
        
        if 'MACD' in df.columns and 'MACD_signal' in df.columns:
            macd_signal = float(df.loc[idx, 'MACD_signal'])
            if current_macd > macd_signal:
                technical_analysis['MACD'] = 'Alcista'
            else:
                technical_analysis['MACD'] = 'Bajista'
        
        return jsonify({
            'signal': 'SUBE' if pred > 0.5 else 'BAJA',
            'confidence': round(float(confidence), 3),
            'prediction_value': round(float(pred), 3),
            'date_requested': date_str,
            'date_used': actual_date.strftime('%Y-%m-%d %H:%M:%S'),
            'used_closest_date': used_closest,
            'current_price': current_price,
            'technical_indicators': {
                'RSI': current_rsi,
                'MACD': current_macd
            },
            'technical_analysis': technical_analysis,
            'model_info': {
                'features_used': len(features),
                'sequence_length': seq_length
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
        'data_points': len(df) if df is not None else 0,
        'features_count': len(features) if features is not None else 0,
        'sequence_length': seq_length
    })

@app.route('/data_info', methods=['GET'])
def data_info():
    """Información sobre los datos disponibles"""
    if df is None:
        return jsonify({'error': 'Datos no cargados'}), 500
    
    return jsonify({
        'total_records': len(df),
        'date_range': {
            'start': df['datetime'].min().strftime('%Y-%m-%d %H:%M:%S'),
            'end': df['datetime'].max().strftime('%Y-%m-%d %H:%M:%S')
        },
        'features_available': list(df.columns),
        'features_used': features if features else []
    })

@app.route('/', methods=['GET'])
def home():
    """Página principal de la API"""
    return jsonify({
        'message': 'IA Financiera Binomo API',
        'version': '2.0',
        'endpoints': {
            'predict': 'GET /predict?date=YYYY-MM-DD HH:MM:SS',
            'health': 'GET /health',
            'data_info': 'GET /data_info'
        },
        'features': {
            'technical_indicators': 'RSI, MACD, Bollinger Bands, Stochastic, etc.',
            'prediction_type': 'Binary (SUBE/BAJA)',
            'model': 'LSTM Neural Network'
        }
    })

# Cargar modelo al iniciar
print("🚀 Iniciando IA Financiera Binomo API...")
load_model_and_data()

if __name__ == '__main__':
    print("📊 Endpoints disponibles:")
    print("   - GET /predict?date=YYYY-MM-DD HH:MM:SS")
    print("   - GET /health")
    print("   - GET /data_info")
    print("   - GET /")
    app.run(debug=True, host='0.0.0.0', port=8080)
    