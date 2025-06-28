import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class RiskManager:
    """
    Sistema avanzado de gestión de riesgo para trading automatizado
    """
    
    def __init__(self, initial_balance: float = 10000):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.max_drawdown_limit = 0.15  # 15% máximo drawdown
        self.max_position_size = 0.05   # 5% máximo por posición
        self.max_daily_loss = 0.05      # 5% máximo pérdida diaria
        self.max_consecutive_losses = 5  # Máximo 5 pérdidas consecutivas
        self.min_confidence = 0.7       # Mínimo 70% confianza
        
        # Estado del sistema
        self.daily_pnl = 0
        self.consecutive_losses = 0
        self.current_drawdown = 0
        self.peak_balance = initial_balance
        self.trading_allowed = True
        self.risk_level = "LOW"  # LOW, MEDIUM, HIGH
        
        # Historial de operaciones
        self.trade_history = []
        self.daily_stats = {}
    
    def calculate_position_size(self, confidence: float, current_price: float, 
                              stop_loss_pct: float = 0.02) -> Dict:
        """
        Calcula el tamaño óptimo de posición basado en gestión de riesgo
        """
        
        # Verificar si el trading está permitido
        if not self.trading_allowed:
            return {
                'position_size': 0,
                'shares': 0,
                'risk_amount': 0,
                'reason': 'Trading suspendido por gestión de riesgo'
            }
        
        # Calcular riesgo por operación (1-2% del balance)
        risk_per_trade = self.current_balance * 0.02  # 2% máximo riesgo por trade
        
        # Ajustar por nivel de confianza
        confidence_multiplier = min(confidence / self.min_confidence, 1.5)
        adjusted_risk = risk_per_trade * confidence_multiplier
        
        # Calcular tamaño de posición basado en stop loss
        stop_loss_amount = current_price * stop_loss_pct
        shares = adjusted_risk / stop_loss_amount
        
        # Limitar por tamaño máximo de posición
        max_position_value = self.current_balance * self.max_position_size
        max_shares = max_position_value / current_price
        shares = min(shares, max_shares)
        
        # Calcular valor de la posición
        position_value = shares * current_price
        
        return {
            'position_size': position_value,
            'shares': shares,
            'risk_amount': adjusted_risk,
            'stop_loss': current_price * (1 - stop_loss_pct),
            'take_profit': current_price * (1 + stop_loss_pct * 2),  # 2:1 ratio
            'confidence_multiplier': confidence_multiplier
        }
    
    def check_risk_limits(self, signal: str, confidence: float, 
                         current_price: float) -> Dict:
        """
        Verifica todos los límites de riesgo antes de ejecutar una operación
        """
        
        risk_checks = {
            'trading_allowed': self.trading_allowed,
            'confidence_sufficient': confidence >= self.min_confidence,
            'drawdown_ok': self.current_drawdown < self.max_drawdown_limit,
            'daily_loss_ok': self.daily_pnl > -self.current_balance * self.max_daily_loss,
            'consecutive_losses_ok': self.consecutive_losses < self.max_consecutive_losses,
            'balance_sufficient': self.current_balance > self.initial_balance * 0.5
        }
        
        # Calcular posición si todos los checks pasan
        if all(risk_checks.values()):
            position_info = self.calculate_position_size(confidence, current_price)
            risk_checks['position_info'] = position_info
            risk_checks['can_trade'] = True
        else:
            risk_checks['can_trade'] = False
            risk_checks['position_info'] = {
                'position_size': 0,
                'shares': 0,
                'risk_amount': 0,
                'reason': 'Límites de riesgo excedidos'
            }
        
        return risk_checks
    
    def update_risk_metrics(self, trade_result: Dict):
        """
        Actualiza métricas de riesgo después de una operación
        """
        
        # Actualizar balance
        if 'profit' in trade_result:
            profit = trade_result['profit']
            self.current_balance += profit
            self.daily_pnl += profit
            
            # Actualizar drawdown
            if self.current_balance > self.peak_balance:
                self.peak_balance = self.current_balance
            
            self.current_drawdown = (self.peak_balance - self.current_balance) / self.peak_balance
            
            # Actualizar pérdidas consecutivas
            if profit < 0:
                self.consecutive_losses += 1
            else:
                self.consecutive_losses = 0
            
            # Verificar límites críticos
            self._check_critical_limits()
        
        # Registrar trade
        trade_result['timestamp'] = datetime.now()
        trade_result['balance_after'] = self.current_balance
        trade_result['drawdown'] = self.current_drawdown
        self.trade_history.append(trade_result)
    
    def _check_critical_limits(self):
        """
        Verifica límites críticos y toma acciones automáticas
        """
        
        # Suspender trading si drawdown excede límite
        if self.current_drawdown > self.max_drawdown_limit:
            self.trading_allowed = False
            self.risk_level = "HIGH"
            print(f"🚨 TRADING SUSPENDIDO: Drawdown {self.current_drawdown*100:.2f}% excede límite")
        
        # Suspender si pérdidas consecutivas exceden límite
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.trading_allowed = False
            self.risk_level = "HIGH"
            print(f"🚨 TRADING SUSPENDIDO: {self.consecutive_losses} pérdidas consecutivas")
        
        # Suspender si pérdida diaria excede límite
        if self.daily_pnl < -self.current_balance * self.max_daily_loss:
            self.trading_allowed = False
            self.risk_level = "HIGH"
            print(f"🚨 TRADING SUSPENDIDO: Pérdida diaria {self.daily_pnl:.2f} excede límite")
        
        # Ajustar nivel de riesgo
        if self.current_drawdown > 0.1:
            self.risk_level = "MEDIUM"
        elif self.current_drawdown > 0.05:
            self.risk_level = "LOW"
    
    def reset_daily_metrics(self):
        """
        Reinicia métricas diarias (llamar al inicio de cada día)
        """
        self.daily_pnl = 0
        self.daily_stats = {
            'date': datetime.now().date(),
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'pnl': 0
        }
    
    def get_risk_status(self) -> Dict:
        """
        Retorna el estado actual del sistema de riesgo
        """
        return {
            'trading_allowed': self.trading_allowed,
            'risk_level': self.risk_level,
            'current_balance': self.current_balance,
            'peak_balance': self.peak_balance,
            'current_drawdown': self.current_drawdown,
            'daily_pnl': self.daily_pnl,
            'consecutive_losses': self.consecutive_losses,
            'max_drawdown_limit': self.max_drawdown_limit,
            'max_daily_loss': self.max_daily_loss,
            'max_consecutive_losses': self.max_consecutive_losses,
            'min_confidence': self.min_confidence
        }
    
    def adjust_risk_parameters(self, market_conditions: str = "NORMAL"):
        """
        Ajusta parámetros de riesgo según condiciones de mercado
        """
        
        if market_conditions == "VOLATILE":
            # Reducir exposición en mercados volátiles
            self.max_position_size = 0.03  # 3% máximo
            self.max_drawdown_limit = 0.10  # 10% máximo
            self.min_confidence = 0.8       # 80% mínimo
            print("⚠️ Parámetros ajustados para mercado volátil")
            
        elif market_conditions == "TRENDING":
            # Aumentar exposición en tendencias claras
            self.max_position_size = 0.07  # 7% máximo
            self.min_confidence = 0.6       # 60% mínimo
            print("✅ Parámetros ajustados para mercado en tendencia")
            
        else:  # NORMAL
            # Parámetros estándar
            self.max_position_size = 0.05
            self.max_drawdown_limit = 0.15
            self.min_confidence = 0.7
            print("📊 Parámetros estándar para mercado normal")
    
    def calculate_kelly_criterion(self, win_rate: float, avg_win: float, avg_loss: float) -> float:
        """
        Calcula el porcentaje óptimo de Kelly Criterion
        """
        if avg_loss == 0:
            return 0
        
        kelly_percentage = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
        
        # Limitar a un máximo del 25% para evitar riesgo excesivo
        return min(max(kelly_percentage, 0), 0.25)
    
    def get_optimal_stop_loss(self, atr: float, volatility: float) -> float:
        """
        Calcula stop loss óptimo basado en ATR y volatilidad
        """
        # Stop loss basado en ATR (2x ATR)
        atr_stop = atr * 2
        
        # Stop loss basado en volatilidad (2x desviación estándar)
        vol_stop = volatility * 2
        
        # Usar el más conservador
        return min(atr_stop, vol_stop)
    
    def get_optimal_take_profit(self, stop_loss: float, risk_reward_ratio: float = 2.0) -> float:
        """
        Calcula take profit óptimo basado en stop loss y ratio riesgo/retorno
        """
        return stop_loss * risk_reward_ratio
    
    def analyze_market_volatility(self, price_data: pd.DataFrame, window: int = 20) -> Dict:
        """
        Analiza la volatilidad del mercado para ajustar parámetros
        """
        
        # Calcular volatilidad
        returns = price_data['close'].pct_change().dropna()
        volatility = returns.rolling(window=window).std()
        current_volatility = volatility.iloc[-1]
        
        # Calcular ATR
        high_low = price_data['high'] - price_data['low']
        high_close = np.abs(price_data['high'] - price_data['close'].shift())
        low_close = np.abs(price_data['low'] - price_data['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=window).mean().iloc[-1]
        
        # Determinar condiciones de mercado
        if current_volatility > 0.03:  # 3% volatilidad
            market_condition = "VOLATILE"
        elif current_volatility < 0.01:  # 1% volatilidad
            market_condition = "LOW_VOL"
        else:
            market_condition = "NORMAL"
        
        return {
            'volatility': current_volatility,
            'atr': atr,
            'market_condition': market_condition,
            'recommended_position_size': self.max_position_size * (1 - current_volatility * 10)
        }
    
    def generate_risk_report(self) -> str:
        """
        Genera un reporte detallado del estado de riesgo
        """
        
        status = self.get_risk_status()
        
        report = f"""
# 🛡️ REPORTE DE GESTIÓN DE RIESGO

## 📊 Estado Actual
- **Trading Permitido**: {'✅ SÍ' if status['trading_allowed'] else '❌ NO'}
- **Nivel de Riesgo**: {status['risk_level']}
- **Balance Actual**: ${status['current_balance']:,.2f}
- **Balance Máximo**: ${status['peak_balance']:,.2f}
- **Drawdown Actual**: {status['current_drawdown']*100:.2f}%

## ⚠️ Límites de Riesgo
- **Drawdown Máximo**: {status['max_drawdown_limit']*100:.1f}%
- **Pérdida Diaria Máxima**: {status['max_daily_loss']*100:.1f}%
- **Pérdidas Consecutivas Máximas**: {status['max_consecutive_losses']}
- **Confianza Mínima**: {status['min_confidence']*100:.0f}%

## 📈 Métricas Actuales
- **P&L Diario**: ${status['daily_pnl']:,.2f}
- **Pérdidas Consecutivas**: {status['consecutive_losses']}
- **Operaciones Totales**: {len(self.trade_history)}

## 💡 Recomendaciones
"""
        
        # Análisis de recomendaciones
        if not status['trading_allowed']:
            report += "- 🚨 **TRADING SUSPENDIDO**: Revisar estrategia y parámetros\n"
        
        if status['current_drawdown'] > 0.1:
            report += "- ⚠️ **Drawdown Alto**: Considerar reducir tamaño de posiciones\n"
        
        if status['consecutive_losses'] > 3:
            report += "- ⚠️ **Pérdidas Consecutivas**: Revisar señales del modelo\n"
        
        if status['daily_pnl'] < 0:
            report += "- ⚠️ **P&L Diario Negativo**: Considerar pausar trading\n"
        
        return report

class PositionSizer:
    """
    Calculador avanzado de tamaño de posiciones
    """
    
    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
    
    def calculate_position(self, signal: str, confidence: float, current_price: float,
                          market_data: pd.DataFrame) -> Dict:
        """
        Calcula el tamaño óptimo de posición considerando múltiples factores
        """
        
        # Verificar límites de riesgo
        risk_check = self.risk_manager.check_risk_limits(signal, confidence, current_price)
        
        if not risk_check['can_trade']:
            return {
                'action': 'HOLD',
                'reason': 'Límites de riesgo excedidos',
                'position_size': 0,
                'stop_loss': 0,
                'take_profit': 0
            }
        
        # Analizar volatilidad del mercado
        volatility_analysis = self.risk_manager.analyze_market_volatility(market_data)
        
        # Calcular stop loss dinámico
        stop_loss_pct = volatility_analysis['atr'] / current_price
        stop_loss_pct = min(max(stop_loss_pct, 0.01), 0.05)  # Entre 1% y 5%
        
        # Calcular posición base
        position_info = self.risk_manager.calculate_position_size(
            confidence, current_price, stop_loss_pct
        )
        
        # Ajustar por condiciones de mercado
        market_multiplier = 1.0
        if volatility_analysis['market_condition'] == "VOLATILE":
            market_multiplier = 0.7  # Reducir 30% en volatilidad alta
        elif volatility_analysis['market_condition'] == "LOW_VOL":
            market_multiplier = 1.2  # Aumentar 20% en volatilidad baja
        
        # Aplicar ajustes
        final_position_size = position_info['position_size'] * market_multiplier
        final_shares = position_info['shares'] * market_multiplier
        
        return {
            'action': signal,
            'position_size': final_position_size,
            'shares': final_shares,
            'stop_loss': current_price * (1 - stop_loss_pct),
            'take_profit': current_price * (1 + stop_loss_pct * 2),
            'confidence': confidence,
            'market_condition': volatility_analysis['market_condition'],
            'risk_level': self.risk_manager.risk_level,
            'reason': 'Posición calculada exitosamente'
        }

def main():
    """Función principal para probar el sistema de gestión de riesgo"""
    print("🛡️ SISTEMA DE GESTIÓN DE RIESGO")
    print("=" * 50)
    
    # Crear gestor de riesgo
    risk_manager = RiskManager(initial_balance=10000)
    
    # Simular algunas operaciones
    print("📊 Simulando operaciones...")
    
    # Operación 1: Ganancia
    trade1 = {'profit': 150, 'confidence': 0.8}
    risk_manager.update_risk_metrics(trade1)
    
    # Operación 2: Pérdida
    trade2 = {'profit': -80, 'confidence': 0.7}
    risk_manager.update_risk_metrics(trade2)
    
    # Operación 3: Pérdida
    trade3 = {'profit': -120, 'confidence': 0.6}
    risk_manager.update_risk_metrics(trade3)
    
    # Mostrar estado
    status = risk_manager.get_risk_status()
    print(f"Balance actual: ${status['current_balance']:,.2f}")
    print(f"Drawdown: {status['current_drawdown']*100:.2f}%")
    print(f"Pérdidas consecutivas: {status['consecutive_losses']}")
    print(f"Trading permitido: {status['trading_allowed']}")
    
    # Generar reporte
    report = risk_manager.generate_risk_report()
    print(report)

if __name__ == "__main__":
    main() 