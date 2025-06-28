#!/usr/bin/env python3
"""
Sistema de Extracción de Datos Financieros
Extrae datos de múltiples fuentes para entrenar la IA
"""

import pandas as pd
import numpy as np
import requests
import time
import json
import os
from datetime import datetime, timedelta
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import warnings
warnings.filterwarnings('ignore')

class DataCollector:
    """Sistema de recolección de datos financieros"""
    
    def __init__(self):
        self.data_dir = "data"
        self.config = self.load_config()
        os.makedirs(self.data_dir, exist_ok=True)
        
    def load_config(self):
        """Carga configuración"""
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except:
            return {
                "alpha_vantage_key": "TU_API_KEY_AQUI",
                "symbols": ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD"],
                "timeframes": ["1min", "5min", "15min"],
                "max_days": 30
            }
    
    def collect_yahoo_finance(self, symbol="EURUSD=X", period="30d", interval="1m"):
        """Extrae datos de Yahoo Finance"""
        print(f"📊 Extrayendo datos de Yahoo Finance: {symbol}")
        
        try:
            # Descargar datos
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                print(f"❌ No se encontraron datos para {symbol}")
                return None
            
            # Limpiar datos
            data = data.reset_index()
            data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            data['datetime'] = pd.to_datetime(data['datetime'])
            
            # Filtrar datos válidos
            data = data.dropna()
            
            print(f"✅ Datos extraídos: {len(data):,} registros")
            print(f"   Rango: {data['datetime'].min()} a {data['datetime'].max()}")
            
            return data
            
        except Exception as e:
            print(f"❌ Error extrayendo datos de Yahoo Finance: {e}")
            return None
    
    def collect_alpha_vantage(self, symbol="EURUSD", interval="1min", outputsize="full"):
        """Extrae datos de Alpha Vantage (requiere API key)"""
        print(f"📊 Extrayendo datos de Alpha Vantage: {symbol}")
        
        api_key = self.config.get("alpha_vantage_key")
        if api_key == "TU_API_KEY_AQUI":
            print("⚠️ Configura tu API key de Alpha Vantage en config.json")
            return None
        
        try:
            ts = TimeSeries(key=api_key, output_format='pandas')
            
            if interval == "1min":
                data, meta = ts.get_intraday(symbol=symbol, interval='1min', outputsize=outputsize)
            elif interval == "5min":
                data, meta = ts.get_intraday(symbol=symbol, interval='5min', outputsize=outputsize)
            elif interval == "15min":
                data, meta = ts.get_intraday(symbol=symbol, interval='15min', outputsize=outputsize)
            else:
                data, meta = ts.get_daily(symbol=symbol, outputsize=outputsize)
            
            # Limpiar datos
            data = data.reset_index()
            data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            data['datetime'] = pd.to_datetime(data['datetime'])
            
            # Filtrar datos válidos
            data = data.dropna()
            
            print(f"✅ Datos extraídos: {len(data):,} registros")
            print(f"   Rango: {data['datetime'].min()} a {data['datetime'].max()}")
            
            return data
            
        except Exception as e:
            print(f"❌ Error extrayendo datos de Alpha Vantage: {e}")
            return None
    
    def collect_binomo_simulated(self, symbol="EURUSD", days=30):
        """Genera datos simulados de Binomo"""
        print(f"🎲 Generando datos simulados de Binomo: {symbol}")
        
        try:
            # Configuración de mercado
            market_hours = {
                'start': '09:00',
                'end': '18:00',
                'timezone': 'UTC'
            }
            
            # Generar fechas
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Crear rango de fechas
            date_range = pd.date_range(
                start=start_date,
                end=end_date,
                freq='1min'
            )
            
            # Filtrar horas de mercado
            market_dates = []
            for date in date_range:
                if date.hour >= 9 and date.hour < 18:
                    market_dates.append(date)
            
            # Generar datos OHLCV
            data = []
            base_price = 1.1000  # Precio base EUR/USD
            
            for i, dt in enumerate(market_dates):
                # Simular movimiento de precio
                volatility = 0.0005
                trend = np.sin(i / 100) * 0.0001
                
                open_price = base_price + np.random.normal(0, volatility) + trend
                high_price = open_price + abs(np.random.normal(0, volatility * 2))
                low_price = open_price - abs(np.random.normal(0, volatility * 2))
                close_price = open_price + np.random.normal(0, volatility) + trend
                volume = np.random.randint(100, 1000)
                
                data.append({
                    'datetime': dt,
                    'open': round(open_price, 5),
                    'high': round(high_price, 5),
                    'low': round(low_price, 5),
                    'close': round(close_price, 5),
                    'volume': volume
                })
                
                base_price = close_price
            
            df = pd.DataFrame(data)
            
            print(f"✅ Datos simulados generados: {len(df):,} registros")
            print(f"   Rango: {df['datetime'].min()} a {df['datetime'].max()}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error generando datos simulados: {e}")
            return None
    
    def collect_multiple_sources(self, symbols=None, days=30):
        """Extrae datos de múltiples fuentes"""
        if symbols is None:
            symbols = self.config.get("symbols", ["EURUSD"])
        
        print("🌐 Extrayendo datos de múltiples fuentes...")
        
        all_data = {}
        
        for symbol in symbols:
            print(f"\n📈 Procesando {symbol}...")
            
            # Intentar Yahoo Finance
            data = self.collect_yahoo_finance(f"{symbol}=X", f"{days}d", "1m")
            if data is not None:
                all_data[f"{symbol}_yahoo"] = data
                continue
            
            # Intentar Alpha Vantage
            data = self.collect_alpha_vantage(symbol, "1min", "full")
            if data is not None:
                all_data[f"{symbol}_alphavantage"] = data
                continue
            
            # Usar datos simulados como fallback
            data = self.collect_binomo_simulated(symbol, days)
            if data is not None:
                all_data[f"{symbol}_simulated"] = data
        
        return all_data
    
    def merge_and_clean_data(self, data_dict):
        """Combina y limpia datos de múltiples fuentes"""
        print("\n🔧 Combinando y limpiando datos...")
        
        if not data_dict:
            print("❌ No hay datos para combinar")
            return None
        
        # Combinar todos los datos
        all_data = []
        for source, data in data_dict.items():
            data['source'] = source
            all_data.append(data)
        
        # Concatenar
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Ordenar por fecha
        combined_df = combined_df.sort_values('datetime')
        
        # Eliminar duplicados
        combined_df = combined_df.drop_duplicates(subset=['datetime', 'source'])
        
        # Limpiar datos inválidos
        combined_df = combined_df[
            (combined_df['open'] > 0) &
            (combined_df['high'] > 0) &
            (combined_df['low'] > 0) &
            (combined_df['close'] > 0) &
            (combined_df['volume'] > 0)
        ]
        
        print(f"✅ Datos combinados: {len(combined_df):,} registros")
        print(f"   Fuentes: {combined_df['source'].unique()}")
        
        return combined_df
    
    def save_data(self, df, filename=None):
        """Guarda los datos extraídos"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"extracted_data_{timestamp}.csv"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            df.to_csv(filepath, index=False)
            print(f"💾 Datos guardados en: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
            return None
    
    def update_existing_data(self, new_data_path):
        """Actualiza datos existentes con nuevos datos"""
        existing_path = os.path.join(self.data_dir, "price_data.csv")
        
        if os.path.exists(existing_path):
            print("📊 Actualizando datos existentes...")
            
            # Cargar datos existentes
            existing_df = pd.read_csv(existing_path)
            existing_df['datetime'] = pd.to_datetime(existing_df['datetime'])
            
            # Cargar nuevos datos
            new_df = pd.read_csv(new_data_path)
            new_df['datetime'] = pd.to_datetime(new_df['datetime'])
            
            # Combinar datos
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Eliminar duplicados
            combined_df = combined_df.drop_duplicates(subset=['datetime'])
            
            # Ordenar por fecha
            combined_df = combined_df.sort_values('datetime')
            
            # Guardar datos actualizados
            combined_df.to_csv(existing_path, index=False)
            
            print(f"✅ Datos actualizados: {len(combined_df):,} registros totales")
            return existing_path
        else:
            # Si no existen datos, usar los nuevos
            new_df = pd.read_csv(new_data_path)
            new_df.to_csv(existing_path, index=False)
            print(f"✅ Datos iniciales guardados: {len(new_df):,} registros")
            return existing_path

def main():
    """Función principal"""
    print("📊 SISTEMA DE EXTRACCIÓN DE DATOS FINANCIEROS")
    print("=" * 50)
    
    # Crear colector
    collector = DataCollector()
    
    # Extraer datos de múltiples fuentes
    data_dict = collector.collect_multiple_sources(
        symbols=["EURUSD", "GBPUSD", "BTCUSD"],
        days=30
    )
    
    if not data_dict:
        print("❌ No se pudieron extraer datos")
        return
    
    # Combinar y limpiar datos
    combined_data = collector.merge_and_clean_data(data_dict)
    
    if combined_data is None:
        print("❌ Error combinando datos")
        return
    
    # Guardar datos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extracted_data_{timestamp}.csv"
    saved_path = collector.save_data(combined_data, filename)
    
    if saved_path:
        # Actualizar datos principales
        updated_path = collector.update_existing_data(saved_path)
        
        print(f"\n🎉 Extracción completada!")
        print(f"📁 Datos guardados en: {updated_path}")
        print(f"📊 Total de registros: {len(combined_data):,}")
        
        print("\n💡 Próximos pasos:")
        print("   1. Revisar datos en: data/price_data.csv")
        print("   2. Reentrenar IA: python train_ai.py")
        print("   3. Probar predicciones: cd src && python api_server.py")

if __name__ == "__main__":
    main() 