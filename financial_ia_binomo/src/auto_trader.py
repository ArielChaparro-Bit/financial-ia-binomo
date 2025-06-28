import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class AutoTrader:
    """
    Sistema de trading automático integrado para Binomo
    """
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.is_running = False
        self.current_positions = {}
        self.trade_history = []
        self.daily_stats = {}
        
        # Inicializar componentes
        self.initialize_components()
    
    def load_config(self, config_path: str) -> Dict:
        """Carga configuración del sistema"""
        
        default_config = {
            "trading": {
                "enabled": False,
                "initial_balance": 10000,
                "max_position_size": 0.05,
                "min_confidence": 0.7,
                "max_daily_trades": 20,
                "max_daily_loss": 0.05
            },
            "model": {
                "path": "../models/lstm_model.h5",
                "scaler_path": "../models/scaler.pkl",
                "features_path": "../models/features.pkl",
                "sequence_length": 30
            },
            "risk_management": {
                "max_drawdown": 0.15,
                "stop_loss_pct": 0.02,
                "take_profit_ratio": 2.0,
                "max_consecutive_losses": 5
            },
            "data": {
                "symbols": ["EURUSD", "GBPUSD", "USDJPY"],
                "timeframe": "1m",
                "update_interval": 60
            },
            "api": {
                "base_url": "http://localhost:8080",
                "timeout": 10
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Combinar con configuración por defecto
                for section in default_config:
                    if section in user_config:
                        default_config[section].update(user_config[section])
        
        return default_config
    
    def initialize_components(self):
        """Inicializa todos los componentes del sistema"""
        
        print("🔧 Inicializando componentes del sistema...")
        
        # Cargar modelo
        self.load_model()
        
        # Inicializar gestor de riesgo
        from risk_manager import RiskManager
        self.risk_manager = RiskManager(
            initial_balance=self.config['trading']['initial_balance']
        )
        
        # Inicializar recolector de datos
        from data_collector import MarketDataCollector
        self.data_collector = MarketDataCollector()
        
        # Inicializar backtester
        from backtester import AdvancedBacktester
        self.backtester = AdvancedBacktester(
            initial_balance=self.config['trading']['initial_balance']
        )
        
        print("✅ Componentes inicializados")
    
    def load_model(self):
        """Carga el modelo entrenado"""
        
        try:
            from tensorflow.keras.models import load_model
            import joblib
            
            model_path = self.config['model']['path']
            scaler_path = self.config['model']['scaler_path']
            features_path = self.config['model']['features_path']
            
            if os.path.exists(model_path):
                self.model = load_model(model_path)
                print(f"✅ Modelo cargado desde {model_path}")
            else:
                print(f"⚠️ Modelo no encontrado en {model_path}")
                self.model = None
            
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print(f"✅ Scaler cargado desde {scaler_path}")
            else:
                self.scaler = None
            
            if os.path.exists(features_path):
                self.features = joblib.load(features_path)
                print(f"✅ Características cargadas: {len(self.features)}")
            else:
                self.features = None
                
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            self.model = None
    
    def get_market_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Obtiene datos actuales del mercado"""
        
        try:
            # Obtener datos de múltiples fuentes
            data = self.data_collector.get_multiple_sources_data(symbol, days=7)
            
            if data is not None and len(data) > 0:
                return data
            else:
                print(f"⚠️ No se pudieron obtener datos para {symbol}")
                return None
                
        except Exception as e:
            print(f"❌ Error obteniendo datos de {symbol}: {e}")
            return None
    
    def prepare_features(self, data: pd.DataFrame) -> Optional[np.ndarray]:
        """Prepara características para predicción"""
        
        try:
            from features import add_technical_indicators
            
            # Agregar indicadores técnicos
            df = add_technical_indicators(data.copy())
            
            # Usar características específicas
            if self.features:
                available_features = [f for f in self.features if f in df.columns]
                if len(available_features) < 5:
                    print(f"⚠️ Pocas características disponibles: {available_features}")
                    return None
                feature_data = df[available_features].values
            else:
                # Características por defecto
                default_features = ['close', 'SMA_5', 'SMA_10', 'RSI_14', 'MACD']
                available_features = [f for f in default_features if f in df.columns]
                feature_data = df[available_features].values
            
            # Normalizar datos
            if self.scaler:
                feature_data = self.scaler.transform(feature_data)
            
            return feature_data
            
        except Exception as e:
            print(f"❌ Error preparando características: {e}")
            return None
    
    def predict_signal(self, feature_data: np.ndarray, symbol: str) -> Dict:
        """Realiza predicción para un símbolo"""
        
        if self.model is None:
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'reason': 'Modelo no disponible'
            }
        
        try:
            seq_length = self.config['model']['sequence_length']
            
            if len(feature_data) < seq_length:
                return {
                    'signal': 'HOLD',
                    'confidence': 0,
                    'reason': 'Datos insuficientes'
                }
            
            # Crear secuencia
            sequence = feature_data[-seq_length:].reshape(1, seq_length, -1)
            
            # Predicción
            prediction = self.model.predict(sequence, verbose=0)[0][0]
            
            # Determinar señal
            threshold = 0.5
            signal = "BUY" if prediction > threshold else "SELL"
            confidence = abs(prediction - 0.5) * 2  # Normalizar a 0-1
            
            return {
                'signal': signal,
                'confidence': confidence,
                'prediction': prediction,
                'symbol': symbol,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"❌ Error en predicción para {symbol}: {e}")
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'reason': f'Error: {str(e)}'
            }
    
    def execute_trade(self, signal: Dict, current_price: float) -> Dict:
        """Ejecuta una operación de trading"""
        
        if not self.config['trading']['enabled']:
            return {
                'executed': False,
                'reason': 'Trading deshabilitado en configuración'
            }
        
        # Verificar límites de riesgo
        risk_check = self.risk_manager.check_risk_limits(
            signal['signal'], 
            signal['confidence'], 
            current_price
        )
        
        if not risk_check['can_trade']:
            return {
                'executed': False,
                'reason': 'Límites de riesgo excedidos'
            }
        
        # Calcular tamaño de posición
        position_info = risk_check['position_info']
        
        # Simular ejecución (reemplazar con API real de Binomo)
        trade_result = {
            'symbol': signal['symbol'],
            'signal': signal['signal'],
            'entry_price': current_price,
            'position_size': position_info['position_size'],
            'shares': position_info['shares'],
            'confidence': signal['confidence'],
            'timestamp': datetime.now(),
            'status': 'OPEN'
        }
        
        # Registrar trade
        self.current_positions[signal['symbol']] = trade_result
        self.trade_history.append(trade_result)
        
        print(f"✅ Trade ejecutado: {signal['symbol']} {signal['signal']} @ {current_price:.5f}")
        
        return {
            'executed': True,
            'trade': trade_result
        }
    
    def monitor_positions(self):
        """Monitorea posiciones abiertas"""
        
        for symbol, position in list(self.current_positions.items()):
            if position['status'] != 'OPEN':
                continue
            
            # Obtener precio actual
            current_data = self.get_market_data(symbol)
            if current_data is None:
                continue
            
            current_price = current_data['close'].iloc[-1]
            entry_price = position['entry_price']
            
            # Calcular P&L
            if position['signal'] == 'BUY':
                pnl_pct = (current_price - entry_price) / entry_price
            else:  # SELL
                pnl_pct = (entry_price - current_price) / entry_price
            
            # Verificar stop loss y take profit
            stop_loss_pct = self.config['risk_management']['stop_loss_pct']
            take_profit_ratio = self.config['risk_management']['take_profit_ratio']
            
            should_close = False
            close_reason = ""
            
            if pnl_pct <= -stop_loss_pct:
                should_close = True
                close_reason = "Stop Loss"
            elif pnl_pct >= stop_loss_pct * take_profit_ratio:
                should_close = True
                close_reason = "Take Profit"
            
            if should_close:
                # Cerrar posición
                position['exit_price'] = current_price
                position['pnl_pct'] = pnl_pct
                position['pnl_amount'] = position['position_size'] * pnl_pct
                position['exit_time'] = datetime.now()
                position['status'] = 'CLOSED'
                position['close_reason'] = close_reason
                
                # Actualizar métricas de riesgo
                self.risk_manager.update_risk_metrics({
                    'profit': position['pnl_amount']
                })
                
                print(f"🔒 Posición cerrada: {symbol} {close_reason} P&L: {pnl_pct*100:.2f}%")
    
    def run_trading_cycle(self):
        """Ejecuta un ciclo completo de trading"""
        
        print(f"\n🔄 Ciclo de trading iniciado: {datetime.now()}")
        
        # Obtener símbolos a operar
        symbols = self.config['data']['symbols']
        
        for symbol in symbols:
            try:
                # Obtener datos del mercado
                market_data = self.get_market_data(symbol)
                if market_data is None:
                    continue
                
                # Preparar características
                feature_data = self.prepare_features(market_data)
                if feature_data is None:
                    continue
                
                # Realizar predicción
                signal = self.predict_signal(feature_data, symbol)
                
                # Verificar si ya hay posición abierta
                if symbol in self.current_positions:
                    continue
                
                # Verificar confianza mínima
                if signal['confidence'] < self.config['trading']['min_confidence']:
                    continue
                
                # Ejecutar trade
                current_price = market_data['close'].iloc[-1]
                trade_result = self.execute_trade(signal, current_price)
                
                if trade_result['executed']:
                    print(f"📊 {symbol}: {signal['signal']} (conf: {signal['confidence']:.2f})")
                
            except Exception as e:
                print(f"❌ Error procesando {symbol}: {e}")
        
        # Monitorear posiciones existentes
        self.monitor_positions()
        
        # Mostrar estado
        self.print_status()
    
    def print_status(self):
        """Imprime estado actual del sistema"""
        
        print(f"\n📊 Estado del Sistema:")
        print(f"   Posiciones abiertas: {len([p for p in self.current_positions.values() if p['status'] == 'OPEN'])}")
        print(f"   Trades totales: {len(self.trade_history)}")
        print(f"   Balance: ${self.risk_manager.current_balance:,.2f}")
        print(f"   Drawdown: {self.risk_manager.current_drawdown*100:.2f}%")
        print(f"   Trading permitido: {self.risk_manager.trading_allowed}")
    
    def start_trading(self):
        """Inicia el trading automático"""
        
        if not self.config['trading']['enabled']:
            print("❌ Trading deshabilitado en configuración")
            return
        
        if self.model is None:
            print("❌ Modelo no disponible")
            return
        
        print("🚀 Iniciando trading automático...")
        self.is_running = True
        
        try:
            while self.is_running:
                # Ejecutar ciclo de trading
                self.run_trading_cycle()
                
                # Esperar intervalo configurado
                interval = self.config['data']['update_interval']
                print(f"⏰ Esperando {interval} segundos...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️ Trading detenido por usuario")
        except Exception as e:
            print(f"❌ Error en trading: {e}")
        finally:
            self.stop_trading()
    
    def stop_trading(self):
        """Detiene el trading automático"""
        
        print("🛑 Deteniendo trading automático...")
        self.is_running = False
        
        # Cerrar posiciones abiertas
        for symbol, position in self.current_positions.items():
            if position['status'] == 'OPEN':
                print(f"⚠️ Posición abierta en {symbol} - cerrar manualmente")
        
        # Generar reporte final
        self.generate_final_report()
    
    def generate_final_report(self):
        """Genera reporte final de trading"""
        
        print("\n📄 Generando reporte final...")
        
        # Estadísticas básicas
        total_trades = len(self.trade_history)
        closed_trades = [t for t in self.trade_history if t.get('status') == 'CLOSED']
        winning_trades = [t for t in closed_trades if t.get('pnl_amount', 0) > 0]
        
        if len(closed_trades) > 0:
            win_rate = len(winning_trades) / len(closed_trades)
            total_pnl = sum([t.get('pnl_amount', 0) for t in closed_trades])
        else:
            win_rate = 0
            total_pnl = 0
        
        report = f"""
# 📊 REPORTE FINAL DE TRADING AUTOMÁTICO

## 📈 Resumen
- **Trades Totales**: {total_trades}
- **Trades Cerrados**: {len(closed_trades)}
- **Trades Ganadores**: {len(winning_trades)}
- **Win Rate**: {win_rate*100:.1f}%
- **P&L Total**: ${total_pnl:,.2f}
- **Balance Final**: ${self.risk_manager.current_balance:,.2f}

## 🛡️ Gestión de Riesgo
- **Drawdown Máximo**: {self.risk_manager.current_drawdown*100:.2f}%
- **Pérdidas Consecutivas**: {self.risk_manager.consecutive_losses}
- **Trading Permitido**: {self.risk_manager.trading_allowed}

## 💡 Recomendaciones
"""
        
        if win_rate > 0.6:
            report += "- ✅ **Excelente win rate**: El sistema está funcionando bien\n"
        elif win_rate > 0.5:
            report += "- ✅ **Win rate positivo**: El sistema es rentable\n"
        else:
            report += "- ⚠️ **Win rate bajo**: Considerar ajustes en el modelo\n"
        
        if total_pnl > 0:
            report += "- ✅ **P&L positivo**: El sistema generó ganancias\n"
        else:
            report += "- ❌ **P&L negativo**: Revisar estrategia\n"
        
        print(report)
        
        # Guardar reporte
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"../reports/trading_report_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"💾 Reporte guardado en: {report_path}")

def main():
    """Función principal"""
    print("🤖 SISTEMA DE TRADING AUTOMÁTICO")
    print("=" * 60)
    
    # Crear trader
    trader = AutoTrader()
    
    # Mostrar configuración
    print("📋 Configuración actual:")
    print(f"   Trading habilitado: {trader.config['trading']['enabled']}")
    print(f"   Símbolos: {trader.config['data']['symbols']}")
    print(f"   Balance inicial: ${trader.config['trading']['initial_balance']:,.2f}")
    
    # Preguntar si iniciar trading
    if trader.config['trading']['enabled']:
        response = input("\n¿Iniciar trading automático? (y/n): ")
        if response.lower() == 'y':
            trader.start_trading()
        else:
            print("Trading cancelado")
    else:
        print("⚠️ Trading deshabilitado en configuración")
        print("   Edita config.json para habilitar")

if __name__ == "__main__":
    main() 