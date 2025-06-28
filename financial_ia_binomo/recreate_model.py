#!/usr/bin/env python3
"""
Script para recrear el modelo simple de IA Financiera
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def print_step(step: int, message: str):
    """Imprime un paso del proceso"""
    print(f"\n📋 PASO {step}: {message}")

def print_success(message: str):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message: str):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def generate_sample_data():
    """Genera datos de muestra realistas"""
    print_step(1, "Generando datos de muestra")
    
    np.random.seed(42)
    n_samples = 10000
    
    # Generar datos de precios simulados
    dates = pd.date_range('2023-01-01', periods=n_samples, freq='1min')
    
    # Precio base
    base_price = 100.0
    prices = [base_price]
    
    # Generar precios con tendencia y volatilidad
    for i in range(1, n_samples):
        # Tendencia aleatoria
        trend = np.random.normal(0, 0.001)
        # Volatilidad
        volatility = np.random.normal(0, 0.005)
        # Cambio de precio
        price_change = trend + volatility
        new_price = prices[-1] * (1 + price_change)
        prices.append(max(new_price, 0.1))  # Precio mínimo
    
    # Crear DataFrame
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.002))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.002))) for p in prices],
        'close': prices,
        'volume': np.random.randint(1000, 10000, n_samples)
    })
    
    # Asegurar que high >= close >= low
    df['high'] = df[['open', 'high', 'close']].max(axis=1)
    df['low'] = df[['open', 'low', 'close']].min(axis=1)
    
    print_success(f"Generados {n_samples} registros de datos")
    return df

def calculate_technical_indicators(df):
    """Calcula indicadores técnicos"""
    print_step(2, "Calculando indicadores técnicos")
    
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
    
    # ATR (Average True Range)
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    df['atr'] = true_range.rolling(window=14).mean()
    
    # Williams %R
    highest_high = df['high'].rolling(window=14).max()
    lowest_low = df['low'].rolling(window=14).min()
    df['williams_r'] = -100 * ((highest_high - df['close']) / (highest_high - lowest_low))
    
    print_success("Indicadores técnicos calculados")
    return df

def create_features_and_targets(df):
    """Crea features y targets para el modelo"""
    print_step(3, "Creando features y targets")
    
    # Features técnicos
    feature_columns = [
        'sma_5', 'sma_20', 'ema_12', 'ema_26',
        'rsi', 'macd', 'macd_signal', 'macd_histogram',
        'bb_width', 'bb_position', 'stoch_k', 'stoch_d',
        'volume_ratio', 'momentum', 'rate_of_change',
        'atr', 'williams_r'
    ]
    
    # Crear features adicionales
    df['price_change'] = df['close'].pct_change()
    df['price_change_5'] = df['close'].pct_change(5)
    df['price_change_10'] = df['close'].pct_change(10)
    
    # Agregar a features
    feature_columns.extend(['price_change', 'price_change_5', 'price_change_10'])
    
    # Crear target (dirección del precio)
    df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    
    # Eliminar filas con NaN
    df_clean = df.dropna()
    
    # Preparar features y target
    X = df_clean[feature_columns]
    y = df_clean['target']
    
    print_success(f"Features: {X.shape[1]} columnas, {X.shape[0]} muestras")
    print_success(f"Target balance: {y.value_counts().to_dict()}")
    
    return X, y, feature_columns

def train_model(X, y):
    """Entrena el modelo"""
    print_step(4, "Entrenando modelo Random Forest")
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Escalar features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar modelo
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluar modelo
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print_success(f"Precisión del modelo: {accuracy:.4f}")
    print("\n📊 Reporte de clasificación:")
    print(classification_report(y_test, y_pred))
    
    return model, scaler, X.columns.tolist()

def save_model(model, scaler, features):
    """Guarda el modelo y componentes"""
    print_step(5, "Guardando modelo")
    
    # Crear directorio models si no existe
    os.makedirs("models", exist_ok=True)
    
    # Guardar modelo
    with open("models/simple_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    # Guardar scaler
    with open("models/simple_model_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    # Guardar features
    with open("models/simple_model_features.pkl", "wb") as f:
        pickle.dump(features, f)
    
    print_success("Modelo guardado en models/simple_model.pkl")
    print_success("Scaler guardado en models/simple_model_scaler.pkl")
    print_success("Features guardadas en models/simple_model_features.pkl")

def test_model():
    """Prueba el modelo guardado"""
    print_step(6, "Probando modelo guardado")
    
    try:
        # Cargar modelo
        with open("models/simple_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Cargar scaler
        with open("models/simple_model_scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        
        # Cargar features
        with open("models/simple_model_features.pkl", "rb") as f:
            features = pickle.load(f)
        
        # Crear datos de prueba
        test_data = np.random.rand(1, len(features))
        test_data_scaled = scaler.transform(test_data)
        prediction = model.predict_proba(test_data_scaled)
        
        print_success(f"Modelo cargado correctamente")
        print_success(f"Features: {len(features)} indicadores")
        print_success(f"Predicción de prueba: {prediction[0]}")
        
        return True
        
    except Exception as e:
        print_error(f"Error probando modelo: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 RECREACIÓN DEL MODELO SIMPLE DE IA FINANCIERA")
    print("=" * 60)
    
    # Generar datos
    df = generate_sample_data()
    
    # Calcular indicadores
    df = calculate_technical_indicators(df)
    
    # Crear features y targets
    X, y, features = create_features_and_targets(df)
    
    # Entrenar modelo
    model, scaler, feature_names = train_model(X, y)
    
    # Guardar modelo
    save_model(model, scaler, feature_names)
    
    # Probar modelo
    test_model()
    
    print("\n🎉 MODELO RECREADO EXITOSAMENTE")
    print("=" * 60)
    print("""
    📁 Archivos creados:
       • models/simple_model.pkl
       • models/simple_model_scaler.pkl
       • models/simple_model_features.pkl
    
    🔧 Próximos pasos:
       1. Ejecutar reactivate_system.py
       2. Probar predicciones en tiempo real
       3. Configurar trading automático
    """)

if __name__ == "__main__":
    main() 