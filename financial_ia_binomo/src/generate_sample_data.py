import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(start_date='2023-01-01', days=30, interval_minutes=1):
    """
    Genera datos de ejemplo más realistas para entrenamiento
    """
    print(f"📊 Generando datos de ejemplo desde {start_date} por {days} días...")
    
    # Configurar parámetros
    start = datetime.strptime(start_date, '%Y-%m-%d')
    base_price = 27000  # Precio base
    volatility = 0.02   # Volatilidad del 2%
    
    # Generar timestamps
    timestamps = []
    current_time = start
    
    while current_time < start + timedelta(days=days):
        # Generar datos para cada minuto del día (9:00-17:00)
        for hour in range(9, 18):  # 9 AM a 6 PM
            for minute in range(0, 60, interval_minutes):
                current_time = current_time.replace(hour=hour, minute=minute)
                timestamps.append(current_time)
        current_time += timedelta(days=1)
    
    # Generar datos OHLCV
    data = []
    current_price = base_price
    
    for i, timestamp in enumerate(timestamps):
        # Simular movimiento de precio
        price_change = np.random.normal(0, volatility * current_price)
        current_price += price_change
        
        # Generar OHLC
        high = current_price * (1 + abs(np.random.normal(0, 0.005)))
        low = current_price * (1 - abs(np.random.normal(0, 0.005)))
        open_price = current_price * (1 + np.random.normal(0, 0.002))
        close_price = current_price
        
        # Asegurar que high >= max(open, close) y low <= min(open, close)
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)
        
        # Generar volumen
        volume = int(np.random.normal(500, 200))
        volume = max(100, volume)  # Volumen mínimo
        
        data.append({
            'datetime': timestamp,
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
        
        # Actualizar precio para siguiente iteración
        current_price = close_price
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Agregar tendencias y patrones más realistas
    df = add_market_patterns(df)
    
    print(f"✅ Datos generados: {len(df)} registros")
    print(f"   Rango de fechas: {df['datetime'].min()} a {df['datetime'].max()}")
    print(f"   Rango de precios: ${df['low'].min():.2f} - ${df['high'].max():.2f}")
    
    return df

def add_market_patterns(df):
    """
    Agrega patrones de mercado más realistas
    """
    # Agregar tendencias de mercado
    df['trend'] = np.sin(np.arange(len(df)) * 0.01) * 1000
    
    # Aplicar tendencia a los precios
    for i in range(1, len(df)):
        trend_factor = df.loc[i, 'trend'] / 10000
        df.loc[i, 'close'] += trend_factor
        df.loc[i, 'high'] += trend_factor
        df.loc[i, 'low'] += trend_factor
        df.loc[i, 'open'] += trend_factor
    
    # Agregar volatilidad variable
    volatility_cycles = np.sin(np.arange(len(df)) * 0.005) * 0.5 + 1
    for i in range(len(df)):
        vol_factor = volatility_cycles[i]
        df.loc[i, 'high'] *= (1 + vol_factor * 0.01)
        df.loc[i, 'low'] *= (1 - vol_factor * 0.01)
    
    # Limpiar datos
    df = df.drop('trend', axis=1)
    df = df.round(2)
    
    return df

def main():
    """Función principal para generar datos"""
    print("🎲 Generador de Datos de Ejemplo para IA Financiera")
    print("=" * 50)
    
    # Generar datos
    df = generate_sample_data(start_date='2023-01-01', days=60, interval_minutes=1)
    
    # Guardar datos
    output_path = '../data/price_data.csv'
    df.to_csv(output_path, index=False)
    print(f"💾 Datos guardados en: {output_path}")
    
    # Mostrar estadísticas
    print("\n📈 Estadísticas de los datos:")
    print(f"   Total de registros: {len(df):,}")
    print(f"   Días cubiertos: {(df['datetime'].max() - df['datetime'].min()).days}")
    print(f"   Precio promedio: ${df['close'].mean():.2f}")
    print(f"   Volatilidad: {df['close'].std():.2f}")
    print(f"   Volumen promedio: {df['volume'].mean():.0f}")
    
    # Mostrar muestra de datos
    print("\n📋 Muestra de datos:")
    print(df.head(10).to_string(index=False))
    
    print("\n✅ Datos de ejemplo generados exitosamente!")
    print("   Ahora puedes ejecutar model_train.py para entrenar el modelo")

if __name__ == "__main__":
    main() 