import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_data(filepath):
    """
    Carga datos desde un archivo CSV
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(filepath):
            print(f"❌ Archivo no encontrado: {filepath}")
            return None
        
        # Cargar datos
        df = pd.read_csv(filepath, parse_dates=['datetime'])
        
        # Ordenar por fecha
        df.sort_values('datetime', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # Verificar columnas requeridas
        required_columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"⚠️ Columnas faltantes: {missing_columns}")
            return None
        
        print(f"✅ Datos cargados: {len(df)} registros")
        print(f"   Rango: {df['datetime'].min()} a {df['datetime'].max()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None

def clean_data(df):
    """
    Limpia y valida los datos
    """
    if df is None:
        return None
    
    # Eliminar filas con valores nulos
    initial_rows = len(df)
    df = df.dropna()
    
    if len(df) < initial_rows:
        print(f"⚠️ Se eliminaron {initial_rows - len(df)} filas con valores nulos")
    
    # Verificar valores negativos en precios
    price_columns = ['open', 'high', 'low', 'close']
    for col in price_columns:
        negative_count = (df[col] <= 0).sum()
        if negative_count > 0:
            print(f"⚠️ {negative_count} valores negativos en {col}")
            df = df[df[col] > 0]
    
    # Verificar que high >= max(open, close) y low <= min(open, close)
    invalid_high = (df['high'] < df[['open', 'close']].max(axis=1)).sum()
    invalid_low = (df['low'] > df[['open', 'close']].min(axis=1)).sum()
    
    if invalid_high > 0 or invalid_low > 0:
        print(f"⚠️ {invalid_high + invalid_low} registros con OHLC inválido")
        df = df[
            (df['high'] >= df[['open', 'close']].max(axis=1)) &
            (df['low'] <= df[['open', 'close']].min(axis=1))
        ]
    
    # Verificar volumen
    zero_volume = (df['volume'] <= 0).sum()
    if zero_volume > 0:
        print(f"⚠️ {zero_volume} registros con volumen cero")
        df = df[df['volume'] > 0]
    
    print(f"✅ Datos limpios: {len(df)} registros válidos")
    return df

def resample_data(df, timeframe='1min'):
    """
    Re-muestrea los datos a un timeframe específico
    """
    if df is None:
        return None
    
    try:
        # Configurar datetime como índice
        df_resampled = df.set_index('datetime')
        
        # Re-muestrear
        resampled = df_resampled.resample(timeframe).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        # Eliminar filas con valores nulos
        resampled = resampled.dropna()
        
        # Resetear índice
        resampled = resampled.reset_index()
        
        print(f"✅ Datos re-muestreados a {timeframe}: {len(resampled)} registros")
        return resampled
        
    except Exception as e:
        print(f"❌ Error re-muestreando datos: {e}")
        return df

def add_time_features(df):
    """
    Agrega características de tiempo útiles para el modelo
    """
    if df is None:
        return None
    
    try:
        df = df.copy()
        
        # Extraer características de tiempo
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['day_of_month'] = df['datetime'].dt.day
        df['month'] = df['datetime'].dt.month
        df['quarter'] = df['datetime'].dt.quarter
        
        # Indicadores de sesión de trading
        df['is_market_open'] = ((df['hour'] >= 9) & (df['hour'] <= 17)).astype(int)
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Ciclos de tiempo
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        print("✅ Características de tiempo agregadas")
        return df
        
    except Exception as e:
        print(f"❌ Error agregando características de tiempo: {e}")
        return df

def prepare_data_for_model(df, target_column='close', sequence_length=30):
    """
    Prepara los datos para el modelo de machine learning
    """
    if df is None:
        return None
    
    try:
        # Agregar características de tiempo
        df = add_time_features(df)
        
        # Calcular retornos
        df['returns'] = df[target_column].pct_change()
        df['log_returns'] = np.log(df[target_column] / df[target_column].shift(1))
        
        # Calcular volatilidad móvil
        df['volatility'] = df['returns'].rolling(window=20).std()
        
        # Calcular momentum
        df['momentum_5'] = df[target_column] / df[target_column].shift(5) - 1
        df['momentum_10'] = df[target_column] / df[target_column].shift(10) - 1
        df['momentum_20'] = df[target_column] / df[target_column].shift(20) - 1
        
        # Eliminar filas con valores nulos
        df = df.dropna()
        
        print(f"✅ Datos preparados para modelo: {len(df)} registros")
        print(f"   Características: {len(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error preparando datos: {e}")
        return None

def save_data(df, filepath):
    """
    Guarda los datos en un archivo CSV
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Guardar datos
        df.to_csv(filepath, index=False)
        print(f"💾 Datos guardados en: {filepath}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error guardando datos: {e}")
        return False

def get_data_info(df):
    """
    Retorna información detallada sobre los datos
    """
    if df is None:
        return None
    
    info = {
        'total_records': len(df),
        'date_range': {
            'start': df['datetime'].min().strftime('%Y-%m-%d %H:%M:%S'),
            'end': df['datetime'].max().strftime('%Y-%m-%d %H:%M:%S')
        },
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'price_stats': {
            'min': df['close'].min(),
            'max': df['close'].max(),
            'mean': df['close'].mean(),
            'std': df['close'].std()
        },
        'volume_stats': {
            'min': df['volume'].min(),
            'max': df['volume'].max(),
            'mean': df['volume'].mean(),
            'std': df['volume'].std()
        }
    }
    
    return info