#!/usr/bin/env python3
"""
IA Financiera Móvil - Versión Servidor Externo
Optimizada para Render, Heroku, Railway, etc.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime, timedelta
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = 'ia_financiera_2025'

class ServerIA:
    """IA optimizada para servidor externo"""
    
    def __init__(self):
        self.db_path = "user_data.db"
        self.model_path = "mobile_model.pkl"
        self.scaler_path = "mobile_scaler.pkl"
        
        # Crear directorios si no existen
        os.makedirs("static", exist_ok=True)
        os.makedirs("templates", exist_ok=True)
        
        # Inicializar base de datos
        self.init_database()
        
        # Cargar o crear modelo
        self.load_or_create_model()
    
    def init_database(self):
        """Inicializa la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de predicciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                prediction TEXT,
                confidence REAL,
                user_input TEXT,
                actual_result TEXT,
                timestamp DATETIME,
                is_correct BOOLEAN
            )
        ''')
        
        # Tabla de feedback de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_id INTEGER,
                user_rating INTEGER,
                user_comment TEXT,
                timestamp DATETIME,
                FOREIGN KEY (prediction_id) REFERENCES predictions (id)
            )
        ''')
        
        # Tabla de estadísticas globales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_predictions INTEGER DEFAULT 0,
                correct_predictions INTEGER DEFAULT 0,
                total_users INTEGER DEFAULT 0,
                last_updated DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_or_create_model(self):
        """Carga o crea un modelo nuevo"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print("✅ Modelo cargado desde servidor")
            else:
                self.create_new_model()
        except:
            self.create_new_model()
    
    def create_new_model(self):
        """Crea un modelo nuevo"""
        self.model = RandomForestClassifier(
            n_estimators=50,
            max_depth=8,
            random_state=42
        )
        self.scaler = MinMaxScaler()
        print("🆕 Modelo nuevo creado en servidor")
    
    def get_simple_features(self, data):
        """Obtiene características simples"""
        features = []
        
        if len(data) >= 5:
            # Precios recientes
            features.extend([
                data['close'].iloc[-1],
                data['close'].iloc[-2],
                data['close'].iloc[-3],
                data['close'].iloc[-4],
                data['close'].iloc[-5],
            ])
            
            # Cambios de precio
            features.extend([
                data['close'].iloc[-1] - data['close'].iloc[-2],
                data['close'].iloc[-2] - data['close'].iloc[-3],
                data['close'].iloc[-3] - data['close'].iloc[-4],
            ])
            
            # Volatilidad y tendencia
            recent_prices = data['close'].tail(5)
            features.append(recent_prices.std())
            features.append(recent_prices.iloc[-1] - recent_prices.iloc[0])
            features.append(data['volume'].iloc[-1])
            
        else:
            features = [1.0] * 12
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, symbol, market_data):
        """Realiza predicción"""
        try:
            features = self.get_simple_features(market_data)
            features_scaled = self.scaler.fit_transform(features)
            prediction_proba = self.model.predict_proba(features_scaled)[0]
            
            if prediction_proba[1] > 0.5:
                signal = "COMPRAR"
                confidence = prediction_proba[1]
            else:
                signal = "VENDER"
                confidence = prediction_proba[0]
            
            return {
                'signal': signal,
                'confidence': confidence,
                'prob_up': prediction_proba[1],
                'prob_down': prediction_proba[0]
            }
            
        except Exception as e:
            return {
                'signal': 'NEUTRAL',
                'confidence': 0.5,
                'prob_up': 0.5,
                'prob_down': 0.5,
                'error': str(e)
            }
    
    def learn_from_feedback(self, prediction_id, actual_result, user_rating=None):
        """Aprende del feedback"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Actualizar predicción
            is_correct = (actual_result == 'COMPRAR' or actual_result == 'VENDER')
            cursor.execute('''
                UPDATE predictions 
                SET actual_result = ?, is_correct = ?
                WHERE id = ?
            ''', (actual_result, is_correct, prediction_id))
            
            # Guardar feedback
            if user_rating:
                cursor.execute('''
                    INSERT INTO user_feedback (prediction_id, user_rating, timestamp)
                    VALUES (?, ?, ?)
                ''', (prediction_id, user_rating, datetime.now()))
            
            # Reentrenar si hay suficientes datos
            self.retrain_model()
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error aprendiendo: {e}")
            return False
    
    def retrain_model(self):
        """Reentrena el modelo"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT prediction, actual_result, confidence
                FROM predictions 
                WHERE actual_result IS NOT NULL
                ORDER BY timestamp DESC
                LIMIT 1000
            '''
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if len(df) < 20:
                return
            
            X = []
            y = []
            
            for _, row in df.iterrows():
                features = [
                    float(row['confidence']),
                    1.0 if row['prediction'] == 'COMPRAR' else 0.0,
                ]
                
                X.append(features)
                y.append(1 if row['actual_result'] == 'COMPRAR' else 0)
            
            X = np.array(X)
            y = np.array(y)
            
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            self.model.fit(X_scaled, y)
            
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            print(f"🔄 Modelo reentrenado con {len(df)} predicciones")
            
        except Exception as e:
            print(f"Error reentrenando: {e}")
    
    def get_global_stats(self):
        """Obtiene estadísticas globales"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de predicciones
            cursor.execute('SELECT COUNT(*) FROM predictions')
            total_predictions = cursor.fetchone()[0]
            
            # Predicciones correctas
            cursor.execute('SELECT COUNT(*) FROM predictions WHERE is_correct = 1')
            correct_predictions = cursor.fetchone()[0]
            
            # Precisión
            accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
            
            # Últimas predicciones
            cursor.execute('''
                SELECT symbol, prediction, confidence, actual_result, timestamp
                FROM predictions 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''')
            recent_predictions = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_predictions': total_predictions,
                'correct_predictions': correct_predictions,
                'accuracy': accuracy,
                'recent_predictions': recent_predictions,
                'server_status': 'online',
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy': 0,
                'recent_predictions': [],
                'server_status': 'error',
                'error': str(e)
            }

# Crear instancia de IA
server_ia = ServerIA()

@app.route('/')
def home():
    """Página principal"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para predicciones"""
    try:
        data = request.json
        symbol = data.get('symbol', 'EURUSD')
        
        # Simular datos de mercado
        market_data = pd.DataFrame({
            'close': [1.1000, 1.1005, 1.0998, 1.1002, 1.1008],
            'volume': [1000, 1200, 800, 1100, 1300]
        })
        
        # Realizar predicción
        result = server_ia.predict(symbol, market_data)
        
        # Guardar predicción
        conn = sqlite3.connect(server_ia.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (symbol, prediction, confidence, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (symbol, result['signal'], result['confidence'], datetime.now()))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'prediction_id': prediction_id,
            'symbol': symbol,
            'signal': result['signal'],
            'confidence': result['confidence'],
            'prob_up': result['prob_up'],
            'prob_down': result['prob_down'],
            'server': 'online'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'server': 'error'
        })

@app.route('/feedback', methods=['POST'])
def feedback():
    """Endpoint para feedback"""
    try:
        data = request.json
        prediction_id = data.get('prediction_id')
        actual_result = data.get('actual_result')
        user_rating = data.get('rating')
        
        success = server_ia.learn_from_feedback(prediction_id, actual_result, user_rating)
        
        return jsonify({
            'success': success,
            'message': 'Feedback guardado y modelo actualizado' if success else 'Error guardando feedback',
            'server': 'online'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'server': 'error'
        })

@app.route('/stats')
def stats():
    """Endpoint para estadísticas"""
    stats = server_ia.get_global_stats()
    return jsonify(stats)

@app.route('/health')
def health():
    """Endpoint de salud del servidor"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'server': 'IA Financiera Móvil',
        'version': '1.0.0'
    })

@app.route('/learn')
def learn_page():
    """Página de aprendizaje"""
    return render_template('learn.html')

if __name__ == '__main__':
    # Para desarrollo local
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
else:
    # Para servidor externo (Render, Heroku, etc.)
    app.debug = False 