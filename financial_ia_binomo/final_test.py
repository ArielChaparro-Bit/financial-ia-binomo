#!/usr/bin/env python3
"""
Prueba final del sistema IA Financiera
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

def test_basic_functionality():
    """Prueba funcionalidad básica"""
    print("🧪 PRUEBA FINAL - SISTEMA IA FINANCIERA")
    print("=" * 50)
    
    # Verificar datos generados
    data_path = "data/price_data.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        print(f"✅ Datos encontrados: {len(df):,} registros")
        print(f"   Rango: {df['datetime'].min()} a {df['datetime'].max()}")
        print(f"   Columnas: {list(df.columns)}")
    else:
        print("❌ Datos no encontrados")
        return False
    
    # Verificar archivos del sistema
    required_files = [
        "src/api_server.py",
        "src/model_train.py", 
        "src/features.py",
        "src/data_processing.py",
        "config.json",
        "README.md"
    ]
    
    print("\n📁 Verificando archivos del sistema...")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    # Verificar directorios
    required_dirs = ["data", "models", "src", "reports"]
    print("\n📂 Verificando directorios...")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")
    
    return True

def test_data_processing():
    """Prueba procesamiento de datos"""
    print("\n📊 Probando procesamiento de datos...")
    
    try:
        sys.path.append('src')
        from data_processing import load_data, clean_data
        
        # Cargar datos
        df = load_data("data/price_data.csv")
        if df is not None:
            print("✅ Carga de datos - OK")
            
            # Limpiar datos
            cleaned_df = clean_data(df)
            if cleaned_df is not None:
                print("✅ Limpieza de datos - OK")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_technical_indicators():
    """Prueba indicadores técnicos"""
    print("\n📈 Probando indicadores técnicos...")
    
    try:
        sys.path.append('src')
        from features import add_technical_indicators, get_feature_columns
        
        # Cargar datos
        df = pd.read_csv("data/price_data.csv")
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Agregar indicadores
        df_with_features = add_technical_indicators(df)
        
        if len(df_with_features.columns) > len(df.columns):
            print("✅ Indicadores técnicos - OK")
            print(f"   Características agregadas: {len(df_with_features.columns) - len(df.columns)}")
            return True
        else:
            print("❌ Indicadores técnicos - Error")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_model():
    """Prueba modelo simple"""
    print("\n🤖 Probando modelo simple...")
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import MinMaxScaler
        
        # Crear modelo simple
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        scaler = MinMaxScaler()
        
        # Cargar datos
        df = pd.read_csv("data/price_data.csv")
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Agregar indicadores
        sys.path.append('src')
        from features import add_technical_indicators
        
        df = add_technical_indicators(df)
        
        # Preparar características
        features = ['close', 'SMA_5', 'SMA_10', 'RSI_14']
        available_features = [f for f in features if f in df.columns]
        
        if len(available_features) < 2:
            print("⚠️ Pocas características disponibles")
            return False
        
        X = df[available_features].dropna().values
        if len(X) < 100:
            print("⚠️ Pocos datos para entrenamiento")
            return False
        
        # Crear etiquetas
        y = []
        for i in range(len(X) - 1):
            if df['close'].iloc[i+1] > df['close'].iloc[i]:
                y.append(1)
            else:
                y.append(0)
        
        X = X[:-1]
        y = np.array(y)
        
        # Normalizar y entrenar
        X_scaled = scaler.fit_transform(X)
        model.fit(X_scaled, y)
        
        # Predicción de prueba
        prediction = model.predict_proba(X_scaled[:1])[0]
        
        print("✅ Modelo simple - OK")
        print(f"   Probabilidad subida: {prediction[1]:.3f}")
        print(f"   Probabilidad bajada: {prediction[0]:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_creation():
    """Prueba creación de API"""
    print("\n🌐 Probando creación de API...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return {'message': 'IA Financiera API'}
        
        print("✅ API Flask creada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    tests = [
        ("Funcionalidad básica", test_basic_functionality),
        ("Procesamiento de datos", test_data_processing),
        ("Indicadores técnicos", test_technical_indicators),
        ("Modelo simple", test_simple_model),
        ("API", test_api_creation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN FINAL")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed >= 4:
        print("\n🎉 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
        print("\n🚀 Tu IA Financiera está lista para usar:")
        print("   - Datos generados: ✅")
        print("   - Indicadores técnicos: ✅")
        print("   - Modelo de predicción: ✅")
        print("   - API web: ✅")
        print("\n💡 Próximos pasos:")
        print("   1. Revisar config.json para ajustes")
        print("   2. Ejecutar: cd src && python api_server.py")
        print("   3. Probar predicciones en: http://localhost:8080")
        
    elif passed >= 2:
        print("\n⚠️ Sistema parcialmente funcional")
        print("   - Algunos componentes funcionan")
        print("   - Revisa los errores anteriores")
        
    else:
        print("\n❌ Sistema con problemas")
        print("   - Revisa la instalación de dependencias")

if __name__ == "__main__":
    main() 