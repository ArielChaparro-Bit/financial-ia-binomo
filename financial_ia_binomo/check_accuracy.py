#!/usr/bin/env python3
"""
Verificador de Precisión de IA Financiera
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_fix_data():
    """Carga y arregla los datos"""
    print("📊 Cargando y arreglando datos...")
    
    try:
        # Cargar datos
        data_path = "data/price_data.csv"
        if not os.path.exists(data_path):
            print("❌ Archivo de datos no encontrado")
            return None
        
        # Cargar con formato flexible
        df = pd.read_csv(data_path)
        
        # Arreglar formato de fechas
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], format='mixed')
        except:
            # Si falla, intentar con formato ISO
            df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601')
        
        print(f"✅ Datos cargados: {len(df):,} registros")
        print(f"   Rango: {df['datetime'].min()} a {df['datetime'].max()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None

def add_technical_indicators(df):
    """Agrega indicadores técnicos"""
    try:
        # Medias móviles
        df['SMA_5'] = df['close'].rolling(window=5).mean()
        df['SMA_10'] = df['close'].rolling(window=10).mean()
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['EMA_12'] = df['close'].ewm(span=12).mean()
        df['EMA_26'] = df['close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_histogram'] = df['MACD'] - df['MACD_signal']
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        df['BB_width'] = df['BB_upper'] - df['BB_lower']
        df['BB_position'] = (df['close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower'])
        
        # Stochastic
        low_min = df['low'].rolling(window=14).min()
        high_max = df['high'].rolling(window=14).max()
        df['Stoch_K'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
        df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()
        
        # Volumen
        df['Volume_SMA'] = df['volume'].rolling(window=20).mean()
        df['Volume_ratio'] = df['volume'] / df['Volume_SMA']
        
        # Momentum
        df['ROC'] = ((df['close'] - df['close'].shift(10)) / df['close'].shift(10)) * 100
        df['MOM'] = df['close'] - df['close'].shift(10)
        
        # ATR
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        df['ATR'] = true_range.rolling(window=14).mean()
        
        # Williams %R
        highest_high = df['high'].rolling(window=14).max()
        lowest_low = df['low'].rolling(window=14).min()
        df['Williams_R'] = ((highest_high - df['close']) / (highest_high - lowest_low)) * -100
        
        return df
        
    except Exception as e:
        print(f"❌ Error agregando indicadores: {e}")
        return df

def get_feature_columns():
    """Retorna las columnas de características"""
    return [
        'open', 'high', 'low', 'close', 'volume',
        'SMA_5', 'SMA_10', 'SMA_20', 'EMA_12', 'EMA_26',
        'MACD', 'MACD_signal', 'MACD_histogram',
        'RSI_14', 'BB_width', 'BB_position',
        'Stoch_K', 'Stoch_D', 'Volume_ratio',
        'ROC', 'MOM', 'ATR', 'Williams_R'
    ]

def load_model():
    """Carga el modelo entrenado"""
    print("🤖 Cargando modelo entrenado...")
    
    try:
        model_path = "models/best_model.pkl"
        scaler_path = "models/scaler.pkl"
        features_path = "models/features.pkl"
        
        if not all(os.path.exists(p) for p in [model_path, scaler_path, features_path]):
            print("❌ Modelo no encontrado. Ejecuta train_ai.py primero")
            return None, None, None
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        features = joblib.load(features_path)
        
        print("✅ Modelo cargado exitosamente")
        return model, scaler, features
        
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return None, None, None

def evaluate_model(model, scaler, features, df):
    """Evalúa el modelo actual"""
    print("\n📊 Evaluando modelo actual...")
    
    try:
        # Agregar indicadores
        df = add_technical_indicators(df)
        
        # Obtener características disponibles
        available_features = [f for f in features if f in df.columns]
        
        if len(available_features) < 5:
            print("❌ Pocas características disponibles")
            return None
        
        # Preparar datos
        X = df[available_features].values
        
        # Crear etiquetas
        y = []
        for i in range(len(X) - 1):
            if df['close'].iloc[i+1] > df['close'].iloc[i]:
                y.append(1)
            else:
                y.append(0)
        
        X = X[:-1]
        y = np.array(y)
        
        # Eliminar filas con NaN
        mask = ~np.isnan(X).any(axis=1)
        X = X[mask]
        y = y[mask]
        
        if len(X) < 1000:
            print("❌ Pocos datos para evaluación")
            return None
        
        # Normalizar datos
        X_scaled = scaler.transform(X)
        
        # Predicciones
        y_pred = model.predict(X_scaled)
        y_pred_proba = model.predict_proba(X_scaled)
        
        # Métricas
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
        
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred, zero_division=0)
        recall = recall_score(y, y_pred, zero_division=0)
        f1 = f1_score(y, y_pred, zero_division=0)
        
        # Matriz de confusión
        cm = confusion_matrix(y, y_pred)
        
        # Probabilidad promedio de acierto
        confidence_scores = np.max(y_pred_proba, axis=1)
        avg_confidence = np.mean(confidence_scores)
        
        # Resultados
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'avg_confidence': avg_confidence,
            'confusion_matrix': cm,
            'total_predictions': len(y),
            'correct_predictions': np.sum(y == y_pred),
            'wrong_predictions': np.sum(y != y_pred)
        }
        
        return results
        
    except Exception as e:
        print(f"❌ Error evaluando modelo: {e}")
        return None

def show_results(results):
    """Muestra los resultados de precisión"""
    if results is None:
        return
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DE PRECISIÓN ACTUAL")
    print("=" * 60)
    
    print(f"\n🎯 MÉTRICAS PRINCIPALES:")
    print(f"   Precisión (Accuracy): {results['accuracy']:.3f} ({results['accuracy']*100:.1f}%)")
    print(f"   Precision: {results['precision']:.3f} ({results['precision']*100:.1f}%)")
    print(f"   Recall: {results['recall']:.3f} ({results['recall']*100:.1f}%)")
    print(f"   F1-Score: {results['f1_score']:.3f} ({results['f1_score']*100:.1f}%)")
    
    print(f"\n📈 PROBABILIDAD DE ACIERTO:")
    print(f"   Confianza promedio: {results['avg_confidence']:.3f} ({results['avg_confidence']*100:.1f}%)")
    
    print(f"\n📊 PREDICCIONES:")
    print(f"   Total de predicciones: {results['total_predictions']:,}")
    print(f"   Predicciones correctas: {results['correct_predictions']:,}")
    print(f"   Predicciones incorrectas: {results['wrong_predictions']:,}")
    
    # Matriz de confusión
    cm = results['confusion_matrix']
    print(f"\n🔍 MATRIZ DE CONFUSIÓN:")
    print(f"   Verdaderos Positivos: {cm[1,1]:,}")
    print(f"   Verdaderos Negativos: {cm[0,0]:,}")
    print(f"   Falsos Positivos: {cm[0,1]:,}")
    print(f"   Falsos Negativos: {cm[1,0]:,}")
    
    # Análisis de rentabilidad
    print(f"\n💰 ANÁLISIS DE RENTABILIDAD:")
    
    # Simular trading simple
    correct_rate = results['accuracy']
    risk_reward = 0.8  # Ratio riesgo/beneficio típico
    
    expected_value = (correct_rate * 1) - ((1 - correct_rate) * risk_reward)
    
    print(f"   Tasa de acierto: {correct_rate*100:.1f}%")
    print(f"   Valor esperado por trade: {expected_value:.3f}")
    
    if expected_value > 0:
        print(f"   ✅ ESTRATEGIA RENTABLE")
        print(f"   💡 Recomendación: Usar la IA para trading")
    else:
        print(f"   ❌ ESTRATEGIA NO RENTABLE")
        print(f"   💡 Recomendación: Mejorar el modelo")
    
    print(f"\n📋 RESUMEN:")
    if results['accuracy'] > 0.6:
        print(f"   🎉 EXCELENTE: Precisión superior al 60%")
    elif results['accuracy'] > 0.5:
        print(f"   ✅ BUENA: Precisión superior al 50%")
    else:
        print(f"   ⚠️ MEJORABLE: Precisión inferior al 50%")

def test_recent_predictions(model, scaler, features, df):
    """Prueba predicciones recientes"""
    print(f"\n🔮 Probando predicciones recientes...")
    
    try:
        # Agregar indicadores
        df = add_technical_indicators(df)
        
        # Obtener datos más recientes
        recent_data = df.tail(10)
        
        available_features = [f for f in features if f in recent_data.columns]
        X_recent = recent_data[available_features].values
        
        # Eliminar filas con NaN
        mask = ~np.isnan(X_recent).any(axis=1)
        X_recent = X_recent[mask]
        
        if len(X_recent) == 0:
            print("❌ No hay datos recientes válidos")
            return
        
        # Normalizar y predecir
        X_recent_scaled = scaler.transform(X_recent)
        predictions = model.predict_proba(X_recent_scaled)
        
        print(f"   Últimas {len(predictions)} predicciones:")
        
        for i, pred in enumerate(predictions):
            prob_up = pred[1]
            prob_down = pred[0]
            signal = "COMPRAR" if prob_up > 0.5 else "VENDER"
            confidence = abs(prob_up - 0.5) * 2
            
            print(f"   {i+1}. {signal} - Subida: {prob_up:.3f}, Bajada: {prob_down:.3f}, Confianza: {confidence:.3f}")
        
    except Exception as e:
        print(f"❌ Error en predicciones recientes: {e}")

def main():
    """Función principal"""
    print("🎯 VERIFICADOR DE PRECISIÓN DE IA FINANCIERA")
    print("=" * 60)
    
    # 1. Cargar datos
    df = load_and_fix_data()
    if df is None:
        return
    
    # 2. Cargar modelo
    model, scaler, features = load_model()
    if model is None:
        return
    
    # 3. Evaluar modelo
    results = evaluate_model(model, scaler, features, df)
    
    # 4. Mostrar resultados
    show_results(results)
    
    # 5. Probar predicciones recientes
    test_recent_predictions(model, scaler, features, df)
    
    print(f"\n🕐 Verificación completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 