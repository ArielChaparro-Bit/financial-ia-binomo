import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import requests
import json
import os
from typing import List, Dict, Optional

class MarketDataCollector:
    """
    Recolector de datos reales del mercado para múltiples fuentes
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_binomo_data(self, symbol: str = "EURUSD", timeframe: str = "1m", days: int = 30):
        """
        Obtiene datos de Binomo usando su API (simulado - necesitas API key real)
        """
        print(f"📊 Obteniendo datos de Binomo para {symbol}...")
        
        # Simulación de datos de Binomo (reemplazar con API real)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Generar datos más realistas basados en patrones de mercado real
        data = self._generate_realistic_market_data(symbol, start_date, end_date, timeframe)
        
        return data
    
    def get_yahoo_finance_data(self, symbol: str, period: str = "1mo", interval: str = "1m"):
        """
        Obtiene datos de Yahoo Finance
        """
        print(f"📈 Obteniendo datos de Yahoo Finance para {symbol}...")
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                print(f"⚠️ No se encontraron datos para {symbol}")
                return None
            
            # Renombrar columnas para consistencia
            data = data.reset_index()
            data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            
            # Filtrar solo datos de trading (9:30-16:00 para mercados US)
            data['hour'] = data['datetime'].dt.hour
            data = data[(data['hour'] >= 9) & (data['hour'] <= 16)]
            data = data.drop('hour', axis=1)
            
            print(f"✅ Datos obtenidos: {len(data)} registros")
            return data
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de Yahoo Finance: {e}")
            return None
    
    def get_alpha_vantage_data(self, symbol: str, api_key: str, interval: str = "1min"):
        """
        Obtiene datos de Alpha Vantage (necesitas API key gratuita)
        """
        print(f"📊 Obteniendo datos de Alpha Vantage para {symbol}...")
        
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": interval,
                "apikey": api_key,
                "outputsize": "full"
            }
            
            response = self.session.get(url, params=params)
            data = response.json()
            
            if "Error Message" in data:
                print(f"❌ Error en Alpha Vantage: {data['Error Message']}")
                return None
            
            # Procesar datos
            time_series = data.get(f"Time Series ({interval})", {})
            records = []
            
            for timestamp, values in time_series.items():
                records.append({
                    'datetime': datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
                    'open': float(values['1. open']),
                    'high': float(values['2. high']),
                    'low': float(values['3. low']),
                    'close': float(values['4. close']),
                    'volume': int(values['5. volume'])
                })
            
            df = pd.DataFrame(records)
            df = df.sort_values('datetime').reset_index(drop=True)
            
            print(f"✅ Datos obtenidos: {len(df)} registros")
            return df
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de Alpha Vantage: {e}")
            return None
    
    def _generate_realistic_market_data(self, symbol: str, start_date: datetime, 
                                      end_date: datetime, timeframe: str):
        """
        Genera datos más realistas basados en patrones de mercado real
        """
        # Parámetros específicos por símbolo
        symbol_params = {
            "EURUSD": {"base_price": 1.0850, "volatility": 0.0008, "trend": 0.0001},
            "GBPUSD": {"base_price": 1.2650, "volatility": 0.0012, "trend": -0.0002},
            "USDJPY": {"base_price": 148.50, "volatility": 0.15, "trend": 0.05},
            "BTCUSD": {"base_price": 45000, "volatility": 0.03, "trend": 0.002},
            "ETHUSD": {"base_price": 2800, "volatility": 0.04, "trend": 0.001},
        }
        
        params = symbol_params.get(symbol, {"base_price": 100, "volatility": 0.02, "trend": 0})
        
        # Generar timestamps
        if timeframe == "1m":
            freq = "1min"
        elif timeframe == "5m":
            freq = "5min"
        else:
            freq = "1min"
        
        timestamps = pd.date_range(start=start_date, end=end_date, freq=freq)
        
        # Filtrar solo horario de trading (varía por mercado)
        if "USD" in symbol or "JPY" in symbol:
            # Forex: 24/5
            timestamps = timestamps[timestamps.weekday < 5]
        else:
            # Stocks: 9:30-16:00
            timestamps = timestamps[
                (timestamps.hour >= 9) & (timestamps.hour <= 16) & (timestamps.weekday < 5)
            ]
        
        # Generar datos OHLCV
        data = []
        current_price = params["base_price"]
        
        for i, timestamp in enumerate(timestamps):
            # Simular patrones de mercado reales
            time_factor = i / len(timestamps)
            
            # Tendencia de mercado
            trend_component = params["trend"] * i
            
            # Volatilidad variable (mayor en apertura y cierre)
            hour = timestamp.hour
            if hour in [9, 10, 15, 16]:  # Horas de mayor actividad
                volatility_multiplier = 1.5
            else:
                volatility_multiplier = 1.0
            
            # Ciclos de mercado (semanales, mensuales)
            weekly_cycle = np.sin(2 * np.pi * timestamp.weekday / 5) * 0.3
            monthly_cycle = np.sin(2 * np.pi * timestamp.day / 30) * 0.2
            
            # Movimiento de precio
            base_change = np.random.normal(0, params["volatility"] * volatility_multiplier)
            cyclical_change = weekly_cycle + monthly_cycle
            trend_change = trend_component
            
            price_change = base_change + cyclical_change + trend_change
            current_price += price_change
            
            # Generar OHLC
            spread = current_price * 0.0001  # Spread típico de forex
            
            open_price = current_price + np.random.normal(0, spread)
            close_price = current_price + np.random.normal(0, spread)
            
            # High y Low basados en volatilidad
            volatility_range = current_price * params["volatility"] * volatility_multiplier
            high = max(open_price, close_price) + abs(np.random.normal(0, volatility_range * 0.5))
            low = min(open_price, close_price) - abs(np.random.normal(0, volatility_range * 0.5))
            
            # Volumen variable
            base_volume = 1000000 if "USD" in symbol else 1000
            volume_multiplier = 1 + abs(price_change) / params["volatility"]  # Más volumen en movimientos grandes
            volume = int(base_volume * volume_multiplier * np.random.uniform(0.5, 1.5))
            
            data.append({
                'datetime': timestamp,
                'open': round(open_price, 5) if "USD" in symbol else round(open_price, 2),
                'high': round(high, 5) if "USD" in symbol else round(high, 2),
                'low': round(low, 5) if "USD" in symbol else round(low, 2),
                'close': round(close_price, 5) if "USD" in symbol else round(close_price, 2),
                'volume': volume
            })
            
            # Actualizar precio para siguiente iteración
            current_price = close_price
        
        df = pd.DataFrame(data)
        print(f"✅ Datos generados: {len(df)} registros para {symbol}")
        return df
    
    def get_multiple_sources_data(self, symbol: str, days: int = 30):
        """
        Obtiene datos de múltiples fuentes y los combina
        """
        print(f"🔄 Obteniendo datos de múltiples fuentes para {symbol}...")
        
        data_sources = []
        
        # 1. Yahoo Finance (para stocks)
        if not any(forex in symbol for forex in ["USD", "EUR", "GBP", "JPY"]):
            yahoo_data = self.get_yahoo_finance_data(symbol, period=f"{days}d")
            if yahoo_data is not None:
                data_sources.append(("Yahoo Finance", yahoo_data))
        
        # 2. Alpha Vantage (necesitas API key)
        # alpha_data = self.get_alpha_vantage_data(symbol, "TU_API_KEY")
        # if alpha_data is not None:
        #     data_sources.append(("Alpha Vantage", alpha_data))
        
        # 3. Binomo (simulado)
        binomo_data = self.get_binomo_data(symbol, "1m", days)
        data_sources.append(("Binomo", binomo_data))
        
        if not data_sources:
            print("❌ No se pudieron obtener datos de ninguna fuente")
            return None
        
        # Combinar datos (priorizar fuentes más confiables)
        combined_data = data_sources[0][1]  # Usar la primera fuente disponible
        
        print(f"✅ Datos combinados de {len(data_sources)} fuentes")
        return combined_data
    
    def save_data(self, data: pd.DataFrame, symbol: str, source: str = "combined"):
        """
        Guarda los datos en archivo CSV
        """
        filename = f"../data/{symbol}_{source}_{datetime.now().strftime('%Y%m%d')}.csv"
        data.to_csv(filename, index=False)
        print(f"💾 Datos guardados en: {filename}")
        return filename

def main():
    """Función principal para recolectar datos"""
    print("📊 RECOLECTOR DE DATOS DE MERCADO")
    print("=" * 50)
    
    collector = MarketDataCollector()
    
    # Símbolos populares en Binomo
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD"]
    
    for symbol in symbols:
        print(f"\n🎯 Procesando {symbol}...")
        
        # Obtener datos
        data = collector.get_multiple_sources_data(symbol, days=60)
        
        if data is not None:
            # Guardar datos
            filename = collector.save_data(data, symbol)
            
            # Mostrar estadísticas
            print(f"📈 Estadísticas de {symbol}:")
            print(f"   Registros: {len(data):,}")
            print(f"   Rango: {data['datetime'].min()} a {data['datetime'].max()}")
            print(f"   Precio promedio: {data['close'].mean():.5f}")
            print(f"   Volatilidad: {data['close'].std():.5f}")
        
        time.sleep(1)  # Pausa entre símbolos
    
    print("\n✅ Recolección de datos completada!")

if __name__ == "__main__":
    main() 