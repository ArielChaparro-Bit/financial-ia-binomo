#!/usr/bin/env python3
"""
Colector de Datos Simplificado
Extrae datos de Yahoo Finance y genera datos simulados
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

class SimpleDataCollector:
    """Colector de datos simplificado"""
    
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
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
    
    def collect_multiple_symbols(self, symbols=None, period="30d"):
        """Extrae datos de múltiples símbolos"""
        if symbols is None:
            symbols = [
                "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X",
                "BTC-USD", "ETH-USD", "AAPL", "GOOGL"
            ]
        
        print("🌐 Extrayendo datos de múltiples símbolos...")
        
        all_data = {}
        
        for symbol in symbols:
            print(f"\n📈 Procesando {symbol}...")
            
            data = self.collect_yahoo_finance(symbol, period, "1m")
            if data is not None:
                all_data[symbol] = data
            else:
                print(f"⚠️ Saltando {symbol} - datos no disponibles")
        
        return all_data
    
    def generate_realistic_data(self, symbol="EURUSD", days=30, base_price=1.1000):
        """Genera datos realistas simulados"""
        print(f"🎲 Generando datos realistas: {symbol}")
        
        try:
            # Configuración de mercado
            market_hours = {
                'start': 9,
                'end': 18,
                'days_per_week': 5
            }
            
            # Generar fechas de mercado
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
                if (date.weekday() < 5 and  # Lunes a Viernes
                    date.hour >= market_hours['start'] and 
                    date.hour < market_hours['end']):
                    market_dates.append(date)
            
            # Generar datos OHLCV realistas
            data = []
            current_price = base_price
            
            # Parámetros de volatilidad
            volatility = 0.0005
            trend_strength = 0.0001
            noise_level = 0.0002
            
            for i, dt in enumerate(market_dates):
                # Simular tendencia de mercado
                trend = np.sin(i / 1000) * trend_strength
                
                # Simular volatilidad
                price_change = np.random.normal(0, volatility)
                
                # Agregar ruido de mercado
                noise = np.random.normal(0, noise_level)
                
                # Calcular precios
                open_price = current_price
                close_price = open_price + price_change + trend + noise
                
                # Calcular high y low
                price_range = abs(price_change) * 2
                high_price = max(open_price, close_price) + price_range
                low_price = min(open_price, close_price) - price_range
                
                # Simular volumen
                base_volume = 500
                volume_variation = np.random.randint(-200, 300)
                volume = max(100, base_volume + volume_variation)
                
                # Asegurar que los precios sean válidos
                if low_price <= 0:
                    low_price = open_price * 0.999
                
                data.append({
                    'datetime': dt,
                    'open': round(open_price, 5),
                    'high': round(high_price, 5),
                    'low': round(low_price, 5),
                    'close': round(close_price, 5),
                    'volume': volume
                })
                
                current_price = close_price
            
            df = pd.DataFrame(data)
            
            print(f"✅ Datos realistas generados: {len(df):,} registros")
            print(f"   Rango: {df['datetime'].min()} a {df['datetime'].max()}")
            print(f"   Precio inicial: {df['close'].iloc[0]:.5f}")
            print(f"   Precio final: {df['close'].iloc[-1]:.5f}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error generando datos realistas: {e}")
            return None
    
    def combine_data_sources(self, data_dict):
        """Combina datos de múltiples fuentes"""
        print("\n🔧 Combinando datos de múltiples fuentes...")
        
        if not data_dict:
            print("❌ No hay datos para combinar")
            return None
        
        # Combinar todos los datos
        all_data = []
        for symbol, data in data_dict.items():
            data['symbol'] = symbol
            all_data.append(data)
        
        # Concatenar
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Ordenar por fecha
        combined_df = combined_df.sort_values('datetime')
        
        # Eliminar duplicados
        combined_df = combined_df.drop_duplicates(subset=['datetime', 'symbol'])
        
        # Limpiar datos inválidos
        combined_df = combined_df[
            (combined_df['open'] > 0) &
            (combined_df['high'] > 0) &
            (combined_df['low'] > 0) &
            (combined_df['close'] > 0) &
            (combined_df['volume'] > 0)
        ]
        
        print(f"✅ Datos combinados: {len(combined_df):,} registros")
        print(f"   Símbolos: {combined_df['symbol'].unique()}")
        
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
    
    def update_main_dataset(self, new_data_path):
        """Actualiza el dataset principal"""
        main_path = os.path.join(self.data_dir, "price_data.csv")
        
        if os.path.exists(main_path):
            print("📊 Actualizando dataset principal...")
            
            # Cargar datos existentes
            existing_df = pd.read_csv(main_path)
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
            combined_df.to_csv(main_path, index=False)
            
            print(f"✅ Dataset actualizado: {len(combined_df):,} registros totales")
            return main_path
        else:
            # Si no existe, usar los nuevos datos
            new_df = pd.read_csv(new_data_path)
            new_df.to_csv(main_path, index=False)
            print(f"✅ Dataset inicial creado: {len(new_df):,} registros")
            return main_path
    
    def show_data_info(self, filepath):
        """Muestra información sobre los datos"""
        try:
            df = pd.read_csv(filepath)
            df['datetime'] = pd.to_datetime(df['datetime'])
            
            print(f"\n📊 Información del dataset: {filepath}")
            print("=" * 50)
            print(f"Total de registros: {len(df):,}")
            print(f"Rango de fechas: {df['datetime'].min()} a {df['datetime'].max()}")
            print(f"Columnas: {list(df.columns)}")
            
            if 'symbol' in df.columns:
                print(f"Símbolos: {df['symbol'].unique()}")
            
            print(f"\nEstadísticas de precios:")
            print(f"Precio mínimo: ${df['close'].min():.5f}")
            print(f"Precio máximo: ${df['close'].max():.5f}")
            print(f"Precio promedio: ${df['close'].mean():.5f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error mostrando información: {e}")
            return False

def main():
    """Función principal"""
    print("📊 COLECTOR DE DATOS SIMPLIFICADO")
    print("=" * 50)
    
    # Crear colector
    collector = SimpleDataCollector()
    
    # Opción 1: Extraer datos reales de Yahoo Finance
    print("\n1️⃣ Extrayendo datos reales de Yahoo Finance...")
    real_data = collector.collect_multiple_symbols(
        symbols=["EURUSD=X", "GBPUSD=X", "BTC-USD"],
        period="7d"  # Últimos 7 días para evitar límites
    )
    
    # Opción 2: Generar datos realistas
    print("\n2️⃣ Generando datos realistas...")
    realistic_data = {}
    
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD"]
    base_prices = [1.1000, 1.2500, 150.00, 50000.00]
    
    for symbol, base_price in zip(symbols, base_prices):
        data = collector.generate_realistic_data(symbol, days=30, base_price=base_price)
        if data is not None:
            realistic_data[symbol] = data
    
    # Combinar datos
    all_data = {**real_data, **realistic_data}
    
    if not all_data:
        print("❌ No se pudieron obtener datos")
        return
    
    # Combinar y limpiar
    combined_data = collector.combine_data_sources(all_data)
    
    if combined_data is None:
        print("❌ Error combinando datos")
        return
    
    # Guardar datos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extracted_data_{timestamp}.csv"
    saved_path = collector.save_data(combined_data, filename)
    
    if saved_path:
        # Actualizar dataset principal
        updated_path = collector.update_main_dataset(saved_path)
        
        # Mostrar información
        collector.show_data_info(updated_path)
        
        print(f"\n🎉 Extracción completada!")
        print(f"📁 Dataset principal: {updated_path}")
        
        print("\n💡 Próximos pasos:")
        print("   1. Reentrenar IA: python train_ai.py")
        print("   2. Probar predicciones: cd src && python api_server.py")
        print("   3. Revisar datos en: data/price_data.csv")

if __name__ == "__main__":
    main() 