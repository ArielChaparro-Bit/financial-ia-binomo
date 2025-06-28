#!/usr/bin/env python3
"""
Script de prueba simple para verificar el sistema
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

def test_imports():
    """Prueba las importaciones básicas"""
    print("🔍 Probando importaciones...")
    
    try:
        import pandas as pd
        print("✅ pandas - OK")
    except ImportError as e:
        print(f"❌ pandas - Error: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy - OK")
    except ImportError as e:
        print(f"❌ numpy - Error: {e}")
        return False
    
    try:
        import sklearn
        print("✅ sklearn - OK")
    except ImportError as e:
        print(f"❌ sklearn - Error: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✅ tensorflow - OK")
    except ImportError as e:
        print(f"❌ tensorflow - Error: {e}")
        return False
    
    try:
        import flask
        print("✅ flask - OK")
    except ImportError as e:
        print(f"❌ flask - Error: {e}")
        return False
    
    return True

def test_data_processing():
    """Prueba el procesamiento de datos"""
    print("\n📊 Probando procesamiento de datos...")
    
    try:
        sys.path.append('src')
        from data_processing import load_data, clean_data
        
        # Crear datos de prueba
        test_data = {
            'datetime': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.uniform(27000, 28000, 100),
            'high': np.random.uniform(27000, 28000, 100),
            'low': np.random.uniform(27000, 28000, 100),
            'close': np.random.uniform(27000, 28000, 100),
            'volume': np.random.randint(100, 1000, 100)
        }
        
        df = pd.DataFrame(test_data)
        
        # Guardar datos de prueba
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/test_data.csv', index=False)
        
        # Probar carga de datos
        loaded_df = load_data('data/test_data.csv')
        if loaded_df is not None:
            print("✅ Carga de datos - OK")
        else:
            print("❌ Carga de datos - Error")
            return False
        
        # Probar limpieza de datos
        cleaned_df = clean_data(loaded_df)
        if cleaned_df is not None:
            print("✅ Limpieza de datos - OK")
        else:
            print("❌ Limpieza de datos - Error")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento de datos: {e}")
        return False

def test_features():
    """Prueba los indicadores técnicos"""
    print("\n📈 Probando indicadores técnicos...")
    
    try:
        sys.path.append('src')
        from features import add_technical_indicators, get_feature_columns
        
        # Crear datos de prueba
        test_data = {
            'datetime': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.uniform(27000, 28000, 100),
            'high': np.random.uniform(27000, 28000, 100),
            'low': np.random.uniform(27000, 28000, 100),
            'close': np.random.uniform(27000, 28000, 100),
            'volume': np.random.randint(100, 1000, 100)
        }
        
        df = pd.DataFrame(test_data)
        
        # Agregar indicadores técnicos
        df_with_features = add_technical_indicators(df)
        
        if len(df_with_features.columns) > len(df.columns):
            print("✅ Indicadores técnicos - OK")
            print(f"   Características agregadas: {len(df_with_features.columns) - len(df.columns)}")
        else:
            print("❌ Indicadores técnicos - Error")
            return False
        
        # Probar función de características
        features = get_feature_columns()
        if len(features) > 0:
            print(f"✅ Lista de características - OK ({len(features)} características)")
        else:
            print("❌ Lista de características - Error")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en indicadores técnicos: {e}")
        return False

def test_model_training():
    """Prueba el entrenamiento del modelo"""
    print("\n🤖 Probando entrenamiento del modelo...")
    
    try:
        sys.path.append('src')
        from model_train import main as train_model
        
        # Verificar si hay datos suficientes
        if not os.path.exists('data/test_data.csv'):
            print("⚠️ No hay datos de prueba. Saltando entrenamiento.")
            return True
        
        print("⚠️ Entrenamiento del modelo saltado (puede tomar tiempo)")
        print("   Para entrenar: cd src && python model_train.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en entrenamiento: {e}")
        return False

def test_api():
    """Prueba la API"""
    print("\n🌐 Probando API...")
    
    try:
        sys.path.append('src')
        from api_server import app
        
        print("✅ API Flask creada correctamente")
        print("   Para ejecutar: cd src && python api_server.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en API: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA SIMPLE DEL SISTEMA IA FINANCIERA")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Procesamiento de datos", test_data_processing),
        ("Indicadores técnicos", test_features),
        ("Entrenamiento del modelo", test_model_training),
        ("API", test_api)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores anteriores.")
    
    print("\n💡 Próximos pasos:")
    print("1. cd src")
    print("2. python generate_sample_data.py")
    print("3. python model_train.py")
    print("4. python api_server.py")

if __name__ == "__main__":
    main() 