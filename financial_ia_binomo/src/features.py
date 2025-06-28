import pandas as pd
import numpy as np

def add_technical_indicators(df):
    """
    Agrega indicadores técnicos útiles para trading en Binomo
    """
    # Medias móviles simples
    df['SMA_5'] = df['close'].rolling(window=5).mean()
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    
    # Medias móviles exponenciales
    df['EMA_12'] = df['close'].ewm(span=12).mean()
    df['EMA_26'] = df['close'].ewm(span=26).mean()
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_histogram'] = df['MACD'] - df['MACD_signal']
    
    # RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = (-delta.clip(upper=0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # Bandas de Bollinger
    df['BB_middle'] = df['close'].rolling(window=20).mean()
    bb_std = df['close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
    df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
    df['BB_width'] = (df['BB_upper'] - df['BB_lower']) / df['BB_middle']
    
    # Estocástico
    low_min = df['low'].rolling(window=14).min()
    high_max = df['high'].rolling(window=14).max()
    df['Stoch_K'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
    df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()
    
    # Volumen promedio
    df['Volume_SMA'] = df['volume'].rolling(window=20).mean()
    df['Volume_ratio'] = df['volume'] / df['Volume_SMA']
    
    # Momentum y volatilidad
    df['Price_change'] = df['close'].pct_change()
    df['Price_change_5'] = df['close'].pct_change(periods=5)
    df['Volatility'] = df['Price_change'].rolling(window=20).std()
    
    # ATR (Average True Range)
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    df['ATR'] = true_range.rolling(window=14).mean()
    
    # Williams %R
    highest_high = df['high'].rolling(window=14).max()
    lowest_low = df['low'].rolling(window=14).min()
    df['Williams_R'] = -100 * ((highest_high - df['close']) / (highest_high - lowest_low))
    
    # CCI (Commodity Channel Index)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    sma_tp = typical_price.rolling(window=20).mean()
    mad = typical_price.rolling(window=20).apply(lambda x: np.mean(np.abs(x - x.mean())))
    df['CCI'] = (typical_price - sma_tp) / (0.015 * mad)
    
    # Rellenar valores NaN (arreglado para evitar deprecación)
    df = df.bfill().ffill()
    
    return df

def get_feature_columns():
    """
    Retorna la lista de características principales para el modelo
    """
    return [
        'close', 'SMA_5', 'SMA_10', 'SMA_20', 
        'EMA_12', 'EMA_26', 'MACD', 'MACD_signal', 'MACD_histogram',
        'RSI_14', 'BB_width', 'Stoch_K', 'Stoch_D',
        'Volume_ratio', 'Price_change', 'Volatility', 'ATR',
        'Williams_R', 'CCI'
    ]