#!/usr/bin/env python3
"""
Script para crear datos de ejemplo pequeños para GitHub
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_sample_data():
    """Crea un archivo CSV de ejemplo pequeño para GitHub"""
    
    print("📊 Creando datos de ejemplo para GitHub...")
    
    # Crear fechas de ejemplo (últimos 100 minutos)
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=100)
    
    dates = pd.date_range(start=start_time, end=end_time, freq='1min')
    
    # Generar datos de precio realistas
    np.random.seed(42)  # Para reproducibilidad
    
    # Precio base
    base_price = 100.0
    prices = []
    
    for i in range(len(dates)):
        # Simular movimiento de precio realista
        if i == 0:
            price = base_price
        else:
            # Cambio de precio basado en volatilidad
            change = np.random.normal(0, 0.1)  # 0.1% de volatilidad
            price = prices[-1] * (1 + change)
        
        prices.append(price)
    
    # Crear DataFrame
    df = pd.DataFrame({
        'timestamp': dates,
        'open': [p * (1 + np.random.normal(0, 0.05)) for p in prices],
        'high': [p * (1 + abs(np.random.normal(0, 0.1))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.1))) for p in prices],
        'close': prices,
        'volume': np.random.randint(1000, 10000, len(dates))
    })
    
    # Asegurar que high >= low
    df['high'] = df[['open', 'close', 'high']].max(axis=1)
    df['low'] = df[['open', 'close', 'low']].min(axis=1)
    
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Guardar archivo de ejemplo
    sample_file = 'data/sample_data.csv'
    df.to_csv(sample_file, index=False)
    
    print(f"✅ Datos de ejemplo creados: {sample_file}")
    print(f"   • Registros: {len(df)}")
    print(f"   • Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"   • Tamaño: {os.path.getsize(sample_file) / 1024:.1f} KB")
    
    return df

def create_sample_config():
    """Crea un archivo de configuración de ejemplo"""
    
    config = {
        "model_settings": {
            "model_type": "random_forest",
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42
        },
        "api_settings": {
            "host": "0.0.0.0",
            "port": 8080,
            "debug": False
        },
        "data_settings": {
            "data_source": "sample",
            "timeframe": "1m",
            "sample_size": 100
        },
        "risk_settings": {
            "max_position_size": 0.02,
            "stop_loss": 0.05,
            "take_profit": 0.10,
            "max_drawdown": 0.20
        }
    }
    
    import json
    with open('config_sample.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuración de ejemplo creada: config_sample.json")

if __name__ == '__main__':
    create_sample_data()
    create_sample_config()
    print("\n🎉 Datos de ejemplo listos para GitHub!")
    print("💡 Estos archivos son seguros para subir al repositorio.") 