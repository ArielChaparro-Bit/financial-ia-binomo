import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from data_processing import load_data
from features import add_technical_indicators, get_feature_columns
import os

def create_sequences(data, seq_length=30):
    X, y = [], []
    for i in range(len(data) - seq_length - 1):
        X.append(data[i:i+seq_length])
        # Predicción: 1 si el precio sube, 0 si baja
        y.append(1 if data[i+seq_length][0] > data[i+seq_length-1][0] else 0)
    return np.array(X), np.array(y)

def main():
    print("🤖 Iniciando entrenamiento del modelo LSTM...")
    
    # Cargar y preparar datos
    print("📊 Cargando datos...")
    df = load_data('../data/price_data.csv')
    print(f"   Datos cargados: {len(df)} registros")
    
    df = add_technical_indicators(df)
    print("   Indicadores técnicos calculados")
    
    # Usar características mejoradas
    features = get_feature_columns()
    print(f"   Usando {len(features)} características técnicas")
    
    # Verificar que todas las características existan
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        print(f"⚠️ Características faltantes: {missing_features}")
        # Usar solo características disponibles
        features = [f for f in features if f in df.columns]
        print(f"   Usando {len(features)} características disponibles")
    
    scaler = MinMaxScaler()
    data = scaler.fit_transform(df[features])
    print(f"   Datos normalizados con {len(features)} características")
    
    # Crear secuencias
    print("🔄 Creando secuencias de entrenamiento...")
    X, y = create_sequences(data)
    print(f"   Secuencias creadas: {len(X)} muestras")
    
    if len(X) < 50:
        print("⚠️ ADVERTENCIA: Pocos datos para entrenamiento. Se recomiendan al menos 1000 registros.")
        print("   Considera agregar más datos históricos para mejor rendimiento.")
    
    # Dividir datos
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    print(f"   Datos de entrenamiento: {len(X_train)} muestras")
    print(f"   Datos de validación: {len(X_test)} muestras")
    
    # Crear modelo mejorado
    print("🏗️ Construyendo modelo LSTM...")
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.3),
        LSTM(64, return_sequences=True),
        Dropout(0.3),
        LSTM(32),
        Dropout(0.3),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam', 
        loss='binary_crossentropy', 
        metrics=['accuracy', 'precision', 'recall']
    )
    
    print("📈 Arquitectura del modelo:")
    model.summary()
    
    # Entrenar modelo
    print("🎯 Iniciando entrenamiento...")
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=100,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=1
    )
    
    # Evaluar modelo
    print("📊 Evaluando modelo...")
    test_loss, test_acc, test_precision, test_recall = model.evaluate(X_test, y_test, verbose=0)
    print(f"   Precisión: {test_acc:.3f}")
    print(f"   Precisión (precision): {test_precision:.3f}")
    print(f"   Sensibilidad (recall): {test_recall:.3f}")
    
    # Calcular F1-Score
    f1_score = 2 * (test_precision * test_recall) / (test_precision + test_recall) if (test_precision + test_recall) > 0 else 0
    print(f"   F1-Score: {f1_score:.3f}")
    
    # Guardar modelo
    print("💾 Guardando modelo...")
    os.makedirs('../models', exist_ok=True)
    model.save('../models/lstm_model.h5')
    print("✅ Modelo guardado exitosamente en models/lstm_model.h5")
    
    # Guardar scaler para uso futuro
    import joblib
    joblib.dump(scaler, '../models/scaler.pkl')
    print("✅ Scaler guardado en models/scaler.pkl")
    
    # Guardar lista de características
    joblib.dump(features, '../models/features.pkl')
    print("✅ Lista de características guardada en models/features.pkl")
    
    print("🎉 Entrenamiento completado!")
    print("\n📋 Resumen del modelo:")
    print(f"   - Características utilizadas: {len(features)}")
    print(f"   - Secuencias de entrada: {X.shape[1]} timesteps")
    print(f"   - Precisión final: {test_acc:.3f}")
    print(f"   - F1-Score: {f1_score:.3f}")

if __name__ == "__main__":
    main()
    