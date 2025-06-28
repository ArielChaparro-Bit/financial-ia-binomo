import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

class AdvancedBacktester:
    """
    Sistema de backtesting avanzado para evaluar estrategias de trading
    """
    
    def __init__(self, initial_balance: float = 10000, commission: float = 0.001):
        self.initial_balance = initial_balance
        self.commission = commission  # 0.1% por operación
        self.reset()
    
    def reset(self):
        """Reinicia el backtester"""
        self.balance = self.initial_balance
        self.positions = []
        self.trades = []
        self.equity_curve = []
        self.current_position = None
    
    def load_model_and_data(self, model_path: str, data_path: str, scaler_path: str = None):
        """Carga el modelo y los datos"""
        try:
            # Cargar modelo
            from tensorflow.keras.models import load_model
            self.model = load_model(model_path)
            print(f"✅ Modelo cargado desde {model_path}")
            
            # Cargar datos
            self.data = pd.read_csv(data_path)
            self.data['datetime'] = pd.to_datetime(self.data['datetime'])
            print(f"✅ Datos cargados: {len(self.data)} registros")
            
            # Cargar scaler si existe
            if scaler_path and os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print(f"✅ Scaler cargado desde {scaler_path}")
            else:
                self.scaler = None
            
            # Cargar características
            features_path = model_path.replace('lstm_model.h5', 'features.pkl')
            if os.path.exists(features_path):
                self.features = joblib.load(features_path)
                print(f"✅ Características cargadas: {len(self.features)}")
            else:
                self.features = None
            
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo y datos: {e}")
            return False
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara las características para el modelo"""
        from features import add_technical_indicators
        
        # Agregar indicadores técnicos
        df = add_technical_indicators(df.copy())
        
        # Usar características específicas si están definidas
        if self.features:
            available_features = [f for f in self.features if f in df.columns]
            df = df[['datetime'] + available_features]
        else:
            # Usar características por defecto
            default_features = ['close', 'SMA_5', 'SMA_10', 'RSI_14', 'MACD', 'Volume_ratio']
            available_features = [f for f in default_features if f in df.columns]
            df = df[['datetime'] + available_features]
        
        return df
    
    def create_sequences(self, data: np.ndarray, seq_length: int = 30) -> Tuple[np.ndarray, np.ndarray]:
        """Crea secuencias para predicción"""
        X, y = [], []
        
        for i in range(len(data) - seq_length - 1):
            X.append(data[i:i+seq_length])
            # Etiqueta: 1 si el precio sube, 0 si baja
            future_price = data[i+seq_length][0]  # Precio de cierre
            current_price = data[i+seq_length-1][0]
            y.append(1 if future_price > current_price else 0)
        
        return np.array(X), np.array(y)
    
    def predict_signal(self, sequence: np.ndarray, threshold: float = 0.5) -> Dict:
        """Realiza predicción para una secuencia"""
        try:
            # Normalizar si hay scaler
            if self.scaler:
                sequence_normalized = self.scaler.transform(sequence.reshape(-1, sequence.shape[-1]))
                sequence_normalized = sequence_normalized.reshape(sequence.shape)
            else:
                sequence_normalized = sequence
            
            # Predicción
            prediction = self.model.predict(sequence_normalized, verbose=0)[0][0]
            
            # Determinar señal
            signal = "BUY" if prediction > threshold else "SELL"
            confidence = abs(prediction - 0.5) * 2  # Normalizar a 0-1
            
            return {
                'signal': signal,
                'confidence': confidence,
                'prediction': prediction,
                'threshold': threshold
            }
            
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
            return {'signal': 'HOLD', 'confidence': 0, 'prediction': 0.5, 'threshold': threshold}
    
    def execute_trade(self, signal: str, price: float, timestamp: datetime, 
                     confidence: float, position_size: float = 0.1):
        """Ejecuta una operación de trading"""
        
        # Calcular tamaño de la posición
        position_value = self.balance * position_size * confidence
        
        if signal == "BUY" and self.current_position is None:
            # Abrir posición larga
            shares = position_value / price
            cost = position_value + (position_value * self.commission)
            
            if cost <= self.balance:
                self.current_position = {
                    'type': 'LONG',
                    'shares': shares,
                    'entry_price': price,
                    'entry_time': timestamp,
                    'entry_value': position_value
                }
                self.balance -= cost
                
                self.trades.append({
                    'timestamp': timestamp,
                    'action': 'BUY',
                    'price': price,
                    'shares': shares,
                    'value': position_value,
                    'commission': position_value * self.commission,
                    'balance': self.balance,
                    'confidence': confidence
                })
                
        elif signal == "SELL" and self.current_position is not None:
            # Cerrar posición
            exit_value = self.current_position['shares'] * price
            commission = exit_value * self.commission
            net_profit = exit_value - commission - self.current_position['entry_value']
            
            self.balance += exit_value - commission
            
            # Registrar trade
            self.trades.append({
                'timestamp': timestamp,
                'action': 'SELL',
                'price': price,
                'shares': self.current_position['shares'],
                'value': exit_value,
                'commission': commission,
                'profit': net_profit,
                'balance': self.balance,
                'confidence': confidence,
                'hold_time': timestamp - self.current_position['entry_time']
            })
            
            self.current_position = None
    
    def run_backtest(self, data: pd.DataFrame, seq_length: int = 30, 
                    confidence_threshold: float = 0.6, position_size: float = 0.1) -> Dict:
        """Ejecuta el backtest completo"""
        
        print("🔄 Iniciando backtest...")
        
        # Preparar datos
        df = self.prepare_features(data)
        
        # Crear secuencias
        feature_data = df.drop('datetime', axis=1).values
        X, y_true = self.create_sequences(feature_data, seq_length)
        
        print(f"📊 Secuencias creadas: {len(X)}")
        print(f"   Balance inicial: ${self.initial_balance:,.2f}")
        print(f"   Umbral de confianza: {confidence_threshold}")
        print(f"   Tamaño de posición: {position_size*100}%")
        
        # Ejecutar backtest
        predictions = []
        signals_executed = 0
        
        for i in range(seq_length, len(df)):
            current_idx = i - seq_length
            
            # Obtener secuencia actual
            sequence = feature_data[current_idx:i]
            
            # Realizar predicción
            prediction_result = self.predict_signal(sequence.reshape(1, seq_length, -1))
            
            # Solo ejecutar si la confianza es suficiente
            if prediction_result['confidence'] >= confidence_threshold:
                current_price = df.iloc[i]['close']
                current_time = df.iloc[i]['datetime']
                
                # Ejecutar trade
                self.execute_trade(
                    prediction_result['signal'],
                    current_price,
                    current_time,
                    prediction_result['confidence'],
                    position_size
                )
                signals_executed += 1
            
            # Registrar predicción para análisis
            predictions.append({
                'timestamp': df.iloc[i]['datetime'],
                'actual_price': df.iloc[i]['close'],
                'predicted_signal': prediction_result['signal'],
                'confidence': prediction_result['confidence'],
                'prediction': prediction_result['prediction']
            })
            
            # Actualizar curva de equity
            current_equity = self.balance
            if self.current_position:
                current_price = df.iloc[i]['close']
                position_value = self.current_position['shares'] * current_price
                current_equity += position_value
            
            self.equity_curve.append({
                'timestamp': df.iloc[i]['datetime'],
                'equity': current_equity,
                'balance': self.balance
            })
        
        # Cerrar posición abierta al final
        if self.current_position:
            final_price = df.iloc[-1]['close']
            final_time = df.iloc[-1]['datetime']
            self.execute_trade("SELL", final_price, final_time, 1.0, 0)
        
        # Calcular métricas
        results = self.calculate_performance_metrics(predictions, y_true)
        
        print(f"✅ Backtest completado!")
        print(f"   Señales ejecutadas: {signals_executed}")
        print(f"   Balance final: ${self.balance:,.2f}")
        print(f"   Retorno total: {((self.balance/self.initial_balance)-1)*100:.2f}%")
        
        return results
    
    def calculate_performance_metrics(self, predictions: List[Dict], y_true: np.ndarray) -> Dict:
        """Calcula métricas de rendimiento"""
        
        # Convertir predicciones a formato de evaluación
        y_pred = []
        for pred in predictions:
            if pred['predicted_signal'] == 'BUY':
                y_pred.append(1)
            else:
                y_pred.append(0)
        
        # Ajustar longitudes
        min_len = min(len(y_pred), len(y_true))
        y_pred = y_pred[:min_len]
        y_true = y_true[:min_len]
        
        # Métricas de clasificación
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Métricas de trading
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.get('profit', 0) > 0])
        losing_trades = len([t for t in self.trades if t.get('profit', 0) < 0])
        
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        total_profit = sum([t.get('profit', 0) for t in self.trades])
        total_commission = sum([t.get('commission', 0) for t in self.trades])
        
        # Calcular drawdown
        equity_values = [e['equity'] for e in self.equity_curve]
        peak = self.initial_balance
        max_drawdown = 0
        
        for equity in equity_values:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        # Sharpe ratio (simplificado)
        returns = []
        for i in range(1, len(self.equity_curve)):
            prev_equity = self.equity_curve[i-1]['equity']
            curr_equity = self.equity_curve[i]['equity']
            ret = (curr_equity - prev_equity) / prev_equity
            returns.append(ret)
        
        sharpe_ratio = np.mean(returns) / np.std(returns) if len(returns) > 0 and np.std(returns) > 0 else 0
        
        return {
            'initial_balance': self.initial_balance,
            'final_balance': self.balance,
            'total_return': (self.balance / self.initial_balance) - 1,
            'total_return_pct': ((self.balance / self.initial_balance) - 1) * 100,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_commission': total_commission,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'trades': self.trades,
            'equity_curve': self.equity_curve
        }
    
    def plot_results(self, results: Dict, save_path: str = None):
        """Genera gráficos de resultados"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Resultados del Backtest - IA Financiera Binomo', fontsize=16)
        
        # 1. Curva de equity
        equity_df = pd.DataFrame(results['equity_curve'])
        axes[0, 0].plot(equity_df['timestamp'], equity_df['equity'], linewidth=2)
        axes[0, 0].set_title('Curva de Equity')
        axes[0, 0].set_ylabel('Equity ($)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Distribución de ganancias/pérdidas
        profits = [t.get('profit', 0) for t in results['trades'] if 'profit' in t]
        if profits:
            axes[0, 1].hist(profits, bins=20, alpha=0.7, color='green')
            axes[0, 1].axvline(0, color='red', linestyle='--', alpha=0.7)
            axes[0, 1].set_title('Distribución de Ganancias/Pérdidas')
            axes[0, 1].set_xlabel('Profit/Loss ($)')
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Métricas de rendimiento
        metrics_text = f"""
        Retorno Total: {results['total_return_pct']:.2f}%
        Win Rate: {results['win_rate']*100:.1f}%
        Total Trades: {results['total_trades']}
        Max Drawdown: {results['max_drawdown']*100:.2f}%
        Sharpe Ratio: {results['sharpe_ratio']:.3f}
        Precisión: {results['accuracy']*100:.1f}%
        """
        axes[1, 0].text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center')
        axes[1, 0].set_title('Métricas de Rendimiento')
        axes[1, 0].axis('off')
        
        # 4. Balance por operación
        if results['trades']:
            trade_df = pd.DataFrame(results['trades'])
            trade_df['cumulative_balance'] = trade_df['balance'].cumsum()
            axes[1, 1].plot(trade_df['timestamp'], trade_df['cumulative_balance'], marker='o', markersize=3)
            axes[1, 1].set_title('Balance Acumulado por Operación')
            axes[1, 1].set_ylabel('Balance ($)')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Gráficos guardados en: {save_path}")
        
        plt.show()
    
    def generate_report(self, results: Dict, save_path: str = None) -> str:
        """Genera un reporte detallado"""
        
        report = f"""
# 📊 REPORTE DE BACKTEST - IA FINANCIERA BINOMO

## 📈 Resumen Ejecutivo
- **Balance Inicial**: ${results['initial_balance']:,.2f}
- **Balance Final**: ${results['final_balance']:,.2f}
- **Retorno Total**: {results['total_return_pct']:.2f}%
- **Tiempo de Análisis**: {len(results['equity_curve'])} períodos

## 🎯 Métricas de Trading
- **Total de Operaciones**: {results['total_trades']}
- **Operaciones Ganadoras**: {results['winning_trades']}
- **Operaciones Perdedoras**: {results['losing_trades']}
- **Win Rate**: {results['win_rate']*100:.1f}%
- **Profit Total**: ${results['total_profit']:,.2f}
- **Comisiones Total**: ${results['total_commission']:,.2f}

## 📊 Métricas de Riesgo
- **Máximo Drawdown**: {results['max_drawdown']*100:.2f}%
- **Sharpe Ratio**: {results['sharpe_ratio']:.3f}
- **Ratio de Riesgo/Retorno**: {results['total_return_pct']/results['max_drawdown']:.2f}

## 🤖 Métricas del Modelo
- **Precisión**: {results['accuracy']*100:.1f}%
- **Precisión (Precision)**: {results['precision']*100:.1f}%
- **Sensibilidad (Recall)**: {results['recall']*100:.1f}%
- **F1-Score**: {results['f1_score']*100:.1f}%

## 💡 Recomendaciones
"""
        
        # Análisis de recomendaciones
        if results['total_return_pct'] > 20:
            report += "- ✅ **Excelente rendimiento**: El modelo muestra resultados muy positivos\n"
        elif results['total_return_pct'] > 10:
            report += "- ✅ **Buen rendimiento**: El modelo es rentable\n"
        elif results['total_return_pct'] > 0:
            report += "- ⚠️ **Rendimiento moderado**: Considera ajustar parámetros\n"
        else:
            report += "- ❌ **Rendimiento negativo**: Revisa el modelo y datos\n"
        
        if results['win_rate'] > 0.6:
            report += "- ✅ **Win rate alto**: Buena precisión en predicciones\n"
        else:
            report += "- ⚠️ **Win rate bajo**: Considera mejorar la precisión del modelo\n"
        
        if results['max_drawdown'] < 0.1:
            report += "- ✅ **Riesgo controlado**: Drawdown aceptable\n"
        else:
            report += "- ⚠️ **Riesgo alto**: Drawdown excesivo, considera reducir posición\n"
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Reporte guardado en: {save_path}")
        
        return report

def main():
    """Función principal para ejecutar backtest"""
    print("🎯 BACKTESTER AVANZADO - IA FINANCIERA BINOMO")
    print("=" * 60)
    
    # Configurar backtester
    backtester = AdvancedBacktester(
        initial_balance=10000,  # $10,000 inicial
        commission=0.001        # 0.1% comisión
    )
    
    # Cargar modelo y datos
    model_path = "../models/lstm_model.h5"
    data_path = "../data/EURUSD_combined_20231201.csv"  # Ajusta según tus datos
    scaler_path = "../models/scaler.pkl"
    
    if not backtester.load_model_and_data(model_path, data_path, scaler_path):
        print("❌ No se pudo cargar el modelo o datos")
        return
    
    # Ejecutar backtest
    results = backtester.run_backtest(
        data=backtester.data,
        seq_length=30,
        confidence_threshold=0.6,  # Solo operar con 60%+ confianza
        position_size=0.1          # 10% del balance por operación
    )
    
    # Generar reporte
    report = backtester.generate_report(results, "../reports/backtest_report.md")
    print(report)
    
    # Generar gráficos
    backtester.plot_results(results, "../reports/backtest_results.png")
    
    print("✅ Backtest completado exitosamente!")

if __name__ == "__main__":
    import os
    main() 