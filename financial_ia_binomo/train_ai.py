#!/usr/bin/env python3
"""
Entrenamiento de IA Financiera - Script Completo
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Carga y prepara los datos para entrenamiento"""
    print("📊 Cargando y preparando datos...")
    
    try:
        # Cargar datos
        data_path = "data/price_data.csv"
        if not os.path.exists(data_path):
            print("❌ Archivo de datos no encontrado")
            return None, None, None
        
        df = pd.read_csv(data_path)
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        print(f"✅ Datos cargados: {len(df):,} registros")
        print(f"   Rango: {df['datetime'].min()} a {df['datetime'].max()}")
        
        # Agregar indicadores técnicos
        df = add_technical_indicators(df)
        
        # Obtener características
        features = get_feature_columns()
        available_features = [f for f in features if f in df.columns]
        
        print(f"✅ Indicadores técnicos agregados: {len(available_features)} características")
        
        # Preparar datos
        X = df[available_features].values
        y = []
        
        # Crear etiquetas: 1 si el precio sube, 0 si baja
        for i in range(len(X) - 1):
            if df['close'].iloc[i+1] > df['close'].iloc[i]:
                y.append(1)
            else:
                y.append(0)
        
        # Ajustar X para que coincida con y
        X = X[:-1]
        y = np.array(y)
        
        # Eliminar filas con valores NaN
        mask = ~np.isnan(X).any(axis=1)
        X = X[mask]
        y = y[mask]
        
        print(f"✅ Datos finales: {len(X):,} muestras, {len(available_features)} características")
        print(f"   Distribución: {np.sum(y)} subidas, {len(y) - np.sum(y)} bajadas")
        
        return X, y, available_features
        
    except Exception as e:
        print(f"❌ Error preparando datos: {e}")
        return None, None, None

def add_technical_indicators(df):
    """Agrega indicadores técnicos al DataFrame"""
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
        
        # ATR (Average True Range)
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

def train_models(X, y, features):
    """Entrena múltiples modelos"""
    print("\n🤖 Entrenando modelos de IA...")
    
    # Normalizar datos
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    print(f"   Datos de entrenamiento: {len(X_train):,} muestras")
    print(f"   Datos de validación: {len(X_test):,} muestras")
    
    models = {}
    results = {}
    
    # 1. Random Forest
    print("\n🌲 Entrenando Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    results['RandomForest'] = {
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf, zero_division=0),
        'recall': recall_score(y_test, y_pred_rf, zero_division=0),
        'f1': f1_score(y_test, y_pred_rf, zero_division=0)
    }
    
    models['RandomForest'] = rf_model
    
    # 2. Gradient Boosting
    print("🚀 Entrenando Gradient Boosting...")
    gb_model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    
    results['GradientBoosting'] = {
        'accuracy': accuracy_score(y_test, y_pred_gb),
        'precision': precision_score(y_test, y_pred_gb, zero_division=0),
        'recall': recall_score(y_test, y_pred_gb, zero_division=0),
        'f1': f1_score(y_test, y_pred_gb, zero_division=0)
    }
    
    models['GradientBoosting'] = gb_model
    
    # Evaluar modelos
    print("\n📊 Resultados de los modelos:")
    print("=" * 60)
    
    best_model = None
    best_f1 = 0
    
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"   Precisión: {metrics['accuracy']:.3f}")
        print(f"   Precision: {metrics['precision']:.3f}")
        print(f"   Recall: {metrics['recall']:.3f}")
        print(f"   F1-Score: {metrics['f1']:.3f}")
        
        if metrics['f1'] > best_f1:
            best_f1 = metrics['f1']
            best_model = name
    
    print(f"\n🏆 Mejor modelo: {best_model} (F1: {best_f1:.3f})")
    
    return models[best_model], scaler, features, results

def save_model(model, scaler, features, results):
    """Guarda el modelo entrenado"""
    print("\n💾 Guardando modelo...")
    
    try:
        os.makedirs("models", exist_ok=True)
        
        # Guardar modelo
        model_path = "models/best_model.pkl"
        joblib.dump(model, model_path)
        
        # Guardar scaler
        scaler_path = "models/scaler.pkl"
        joblib.dump(scaler, scaler_path)
        
        # Guardar características
        features_path = "models/features.pkl"
        joblib.dump(features, features_path)
        
        # Guardar resultados
        results_path = "models/training_results.pkl"
        joblib.dump(results, results_path)
        
        print(f"✅ Modelo guardado en: {model_path}")
        print(f"✅ Scaler guardado en: {scaler_path}")
        print(f"✅ Características guardadas en: {features_path}")
        print(f"✅ Resultados guardados en: {results_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error guardando modelo: {e}")
        return False

def test_prediction(model, scaler, features):
    """Prueba una predicción"""
    print("\n🔮 Probando predicción...")
    
    try:
        # Crear datos de prueba
        test_data = np.random.rand(1, len(features))
        test_scaled = scaler.transform(test_data)
        
        # Predicción
        prediction = model.predict_proba(test_scaled)[0]
        
        print(f"   Probabilidad de subida: {prediction[1]:.3f}")
        print(f"   Probabilidad de bajada: {prediction[0]:.3f}")
        print(f"   Señal: {'COMPRAR' if prediction[1] > 0.5 else 'VENDER'}")
        print(f"   Confianza: {abs(prediction[1] - 0.5) * 2:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return False

def main():
    """Función principal"""
    print("🤖 ENTRENAMIENTO DE IA FINANCIERA")
    print("=" * 50)
    print(f"🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Cargar y preparar datos
    X, y, features = load_and_prepare_data()
    if X is None:
        print("❌ No se pudieron cargar los datos")
        return
    
    # 2. Entrenar modelos
    model, scaler, features, results = train_models(X, y, features)
    
    # 3. Guardar modelo
    if save_model(model, scaler, features, results):
        print("\n✅ Modelo entrenado y guardado exitosamente!")
    else:
        print("\n❌ Error guardando modelo")
        return
    
    # 4. Probar predicción
    test_prediction(model, scaler, features)
    
    print(f"\n🎉 ¡Entrenamiento completado!")
    print(f"🕐 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n💡 Próximos pasos:")
    print("   1. Ejecutar: cd src && python api_server.py")
    print("   2. Probar predicciones en: http://localhost:8080")
    print("   3. Revisar resultados en: models/training_results.pkl")

if __name__ == "__main__":
    main() 