import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os

print("📊 EXTRACCIÓN DE DATOS FINANCIEROS")
print("=" * 40)

# Crear directorio de datos
os.makedirs("data", exist_ok=True)

# 1. Extraer datos de Yahoo Finance
print("\n1️⃣ Extrayendo datos de Yahoo Finance...")

symbols = ["EURUSD=X", "GBPUSD=X", "BTC-USD"]
all_data = []

for symbol in symbols:
    try:
        print(f"   Procesando {symbol}...")
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="7d", interval="1m")
        
        if not data.empty:
            data = data.reset_index()
            data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            data['symbol'] = symbol
            data = data.dropna()
            
            all_data.append(data)
            print(f"   ✅ {len(data)} registros extraídos")
        else:
            print(f"   ❌ No hay datos para {symbol}")
            
    except Exception as e:
        print(f"   ❌ Error con {symbol}: {e}")

# 2. Generar datos simulados
print("\n2️⃣ Generando datos simulados...")

for i, symbol in enumerate(["EURUSD", "GBPUSD", "USDJPY"]):
    try:
        print(f"   Generando {symbol}...")
        
        # Configuración
        base_price = [1.1000, 1.2500, 150.00][i]
        days = 30
        
        # Generar fechas
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='1min')
        
        # Filtrar horas de mercado (9-18)
        market_dates = [d for d in dates if 9 <= d.hour < 18 and d.weekday() < 5]
        
        # Generar datos
        data = []
        current_price = base_price
        
        for j, dt in enumerate(market_dates):
            # Simular movimiento de precio
            change = np.random.normal(0, 0.0005)
            trend = np.sin(j / 1000) * 0.0001
            
            open_price = current_price
            close_price = open_price + change + trend
            
            high_price = max(open_price, close_price) + abs(change) * 2
            low_price = min(open_price, close_price) - abs(change) * 2
            volume = np.random.randint(100, 1000)
            
            data.append({
                'datetime': dt,
                'open': round(open_price, 5),
                'high': round(high_price, 5),
                'low': round(low_price, 5),
                'close': round(close_price, 5),
                'volume': volume,
                'symbol': symbol
            })
            
            current_price = close_price
        
        df = pd.DataFrame(data)
        all_data.append(df)
        print(f"   ✅ {len(df)} registros generados")
        
    except Exception as e:
        print(f"   ❌ Error generando {symbol}: {e}")

# 3. Combinar todos los datos
print("\n3️⃣ Combinando datos...")

if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('datetime')
    combined_df = combined_df.drop_duplicates(subset=['datetime', 'symbol'])
    
    # Limpiar datos inválidos
    combined_df = combined_df[
        (combined_df['open'] > 0) &
        (combined_df['high'] > 0) &
        (combined_df['low'] > 0) &
        (combined_df['close'] > 0) &
        (combined_df['volume'] > 0)
    ]
    
    print(f"✅ Total combinado: {len(combined_df):,} registros")
    print(f"   Símbolos: {combined_df['symbol'].unique()}")
    
    # 4. Guardar datos
    print("\n4️⃣ Guardando datos...")
    
    # Guardar datos completos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/extracted_data_{timestamp}.csv"
    combined_df.to_csv(filename, index=False)
    print(f"✅ Datos guardados en: {filename}")
    
    # Actualizar dataset principal
    main_file = "data/price_data.csv"
    if os.path.exists(main_file):
        existing_df = pd.read_csv(main_file)
        existing_df['datetime'] = pd.to_datetime(existing_df['datetime'])
        
        # Combinar con datos existentes
        combined_df['datetime'] = pd.to_datetime(combined_df['datetime'])
        final_df = pd.concat([existing_df, combined_df], ignore_index=True)
        final_df = final_df.drop_duplicates(subset=['datetime'])
        final_df = final_df.sort_values('datetime')
        
        final_df.to_csv(main_file, index=False)
        print(f"✅ Dataset principal actualizado: {len(final_df):,} registros")
    else:
        combined_df.to_csv(main_file, index=False)
        print(f"✅ Dataset principal creado: {len(combined_df):,} registros")
    
    # 5. Mostrar estadísticas
    print("\n5️⃣ Estadísticas finales:")
    print("=" * 40)
    print(f"Total de registros: {len(combined_df):,}")
    print(f"Rango de fechas: {combined_df['datetime'].min()} a {combined_df['datetime'].max()}")
    print(f"Símbolos disponibles: {list(combined_df['symbol'].unique())}")
    
    print(f"\nPrecios por símbolo:")
    for symbol in combined_df['symbol'].unique():
        symbol_data = combined_df[combined_df['symbol'] == symbol]
        print(f"   {symbol}: ${symbol_data['close'].min():.5f} - ${symbol_data['close'].max():.5f}")
    
    print(f"\n🎉 ¡Extracción completada!")
    print(f"💡 Próximos pasos:")
    print(f"   1. Reentrenar IA: python train_ai.py")
    print(f"   2. Probar predicciones: cd src && python api_server.py")
    
else:
    print("❌ No se pudieron extraer datos") 