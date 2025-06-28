import pandas as pd
import numpy as np
from datetime import datetime
import itertools
from typing import Dict, List, Tuple, Any
import joblib
from sklearn.model_selection import TimeSeriesSplit
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import warnings
warnings.filterwarnings('ignore')

class HyperparameterOptimizer:
    """
    Optimizador de hiperparámetros para el modelo LSTM
    """
    
    def __init__(self, data_path: str, max_trials: int = 50):
        self.data_path = data_path
        self.max_trials = max_trials
        self.best_params = None
        self.best_score = -np.inf
        self.results = []
        
        # Cargar datos
        self.load_data()
    
    def load_data(self):
        """Carga y prepara los datos"""
        from data_processing import load_data
        from features import add_technical_indicators
        
        print("📊 Cargando datos para optimización...")
        
        # Cargar datos
        self.df = load_data(self.data_path)
        self.df = add_technical_indicators(self.df)
        
        # Preparar características
        feature_columns = [
            'close', 'SMA_5', 'SMA_10', 'SMA_20', 'EMA_12', 'EMA_26',
            'MACD', 'MACD_signal', 'MACD_histogram', 'RSI_14', 'BB_width',
            'Stoch_K', 'Stoch_D', 'Volume_ratio', 'Price_change', 'Volatility',
            'ATR', 'Williams_R', 'CCI'
        ]
        
        # Usar solo características disponibles
        self.features = [f for f in feature_columns if f in self.df.columns]
        print(f"✅ Características disponibles: {len(self.features)}")
        
        # Normalizar datos
        from sklearn.preprocessing import MinMaxScaler
        self.scaler = MinMaxScaler()
        self.data = self.scaler.fit_transform(self.df[self.features])
        
        # Crear secuencias
        self.X, self.y = self.create_sequences(self.data)
        print(f"✅ Secuencias creadas: {len(self.X)}")
    
    def create_sequences(self, data: np.ndarray, seq_length: int = 30) -> Tuple[np.ndarray, np.ndarray]:
        """Crea secuencias para entrenamiento"""
        X, y = [], []
        
        for i in range(len(data) - seq_length - 1):
            X.append(data[i:i+seq_length])
            # Etiqueta: 1 si el precio sube, 0 si baja
            future_price = data[i+seq_length][0]
            current_price = data[i+seq_length-1][0]
            y.append(1 if future_price > current_price else 0)
        
        return np.array(X), np.array(y)
    
    def build_model(self, params: Dict) -> Sequential:
        """Construye modelo con parámetros dados"""
        
        model = Sequential()
        
        # Primera capa LSTM
        model.add(LSTM(
            units=params['lstm_units_1'],
            return_sequences=True,
            input_shape=(self.X.shape[1], self.X.shape[2])
        ))
        model.add(Dropout(params['dropout_1']))
        
        # Segunda capa LSTM (si se especifica)
        if params['lstm_units_2'] > 0:
            model.add(LSTM(
                units=params['lstm_units_2'],
                return_sequences=params['lstm_units_3'] > 0
            ))
            model.add(Dropout(params['dropout_2']))
        
        # Tercera capa LSTM (si se especifica)
        if params['lstm_units_3'] > 0:
            model.add(LSTM(units=params['lstm_units_3']))
            model.add(Dropout(params['dropout_3']))
        
        # Capas densas
        if params['dense_units_1'] > 0:
            model.add(Dense(units=params['dense_units_1'], activation='relu'))
            model.add(Dropout(params['dropout_4']))
        
        # Capa de salida
        model.add(Dense(1, activation='sigmoid'))
        
        # Compilar modelo
        model.compile(
            optimizer=Adam(learning_rate=params['learning_rate']),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def evaluate_model(self, params: Dict) -> Dict:
        """Evalúa un modelo con parámetros dados"""
        
        try:
            # Configurar validación cruzada temporal
            tscv = TimeSeriesSplit(n_splits=3)
            scores = []
            
            for train_idx, val_idx in tscv.split(self.X):
                X_train, X_val = self.X[train_idx], self.X[val_idx]
                y_train, y_val = self.y[train_idx], self.y[val_idx]
                
                # Construir modelo
                model = self.build_model(params)
                
                # Callbacks
                early_stopping = EarlyStopping(
                    monitor='val_loss',
                    patience=params['patience'],
                    restore_best_weights=True,
                    verbose=0
                )
                
                # Entrenar modelo
                history = model.fit(
                    X_train, y_train,
                    validation_data=(X_val, y_val),
                    epochs=params['epochs'],
                    batch_size=params['batch_size'],
                    callbacks=[early_stopping],
                    verbose=0
                )
                
                # Evaluar
                val_loss, val_acc, val_precision, val_recall = model.evaluate(
                    X_val, y_val, verbose=0
                )
                
                # Calcular F1-Score
                f1_score = 2 * (val_precision * val_recall) / (val_precision + val_recall) if (val_precision + val_recall) > 0 else 0
                
                scores.append({
                    'accuracy': val_acc,
                    'precision': val_precision,
                    'recall': val_recall,
                    'f1_score': f1_score,
                    'loss': val_loss
                })
            
            # Calcular métricas promedio
            avg_scores = {
                'accuracy': np.mean([s['accuracy'] for s in scores]),
                'precision': np.mean([s['precision'] for s in scores]),
                'recall': np.mean([s['recall'] for s in scores]),
                'f1_score': np.mean([s['f1_score'] for s in scores]),
                'loss': np.mean([s['loss'] for s in scores])
            }
            
            return avg_scores
            
        except Exception as e:
            print(f"❌ Error evaluando modelo: {e}")
            return {
                'accuracy': 0,
                'precision': 0,
                'recall': 0,
                'f1_score': 0,
                'loss': float('inf')
            }
    
    def generate_parameter_combinations(self) -> List[Dict]:
        """Genera combinaciones de hiperparámetros para probar"""
        
        # Definir rangos de parámetros
        param_ranges = {
            'lstm_units_1': [32, 64, 128, 256],
            'lstm_units_2': [0, 32, 64, 128],
            'lstm_units_3': [0, 16, 32, 64],
            'dropout_1': [0.1, 0.2, 0.3, 0.4],
            'dropout_2': [0.1, 0.2, 0.3],
            'dropout_3': [0.1, 0.2, 0.3],
            'dense_units_1': [0, 16, 32, 64],
            'dropout_4': [0.1, 0.2, 0.3],
            'learning_rate': [0.001, 0.01, 0.1],
            'batch_size': [16, 32, 64],
            'epochs': [50, 100],
            'patience': [5, 10, 15]
        }
        
        # Generar combinaciones
        param_names = list(param_ranges.keys())
        param_values = list(param_ranges.values())
        
        combinations = []
        for values in itertools.product(*param_values):
            params = dict(zip(param_names, values))
            
            # Filtrar combinaciones inválidas
            if params['lstm_units_2'] == 0 and params['lstm_units_3'] > 0:
                continue  # No puede tener tercera capa sin segunda
            
            combinations.append(params)
        
        # Limitar número de combinaciones
        if len(combinations) > self.max_trials:
            # Seleccionar aleatoriamente
            np.random.shuffle(combinations)
            combinations = combinations[:self.max_trials]
        
        return combinations
    
    def optimize(self, metric: str = 'f1_score') -> Dict:
        """
        Ejecuta la optimización de hiperparámetros
        """
        
        print(f"🎯 Iniciando optimización de hiperparámetros...")
        print(f"   Métrica objetivo: {metric}")
        print(f"   Máximo de pruebas: {self.max_trials}")
        
        # Generar combinaciones de parámetros
        param_combinations = self.generate_parameter_combinations()
        print(f"   Combinaciones a probar: {len(param_combinations)}")
        
        # Probar cada combinación
        for i, params in enumerate(param_combinations):
            print(f"\n🔄 Prueba {i+1}/{len(param_combinations)}")
            print(f"   Parámetros: {params}")
            
            # Evaluar modelo
            scores = self.evaluate_model(params)
            
            # Guardar resultados
            result = {
                'trial': i + 1,
                'params': params,
                'scores': scores,
                'metric_value': scores[metric]
            }
            self.results.append(result)
            
            # Actualizar mejor resultado
            if scores[metric] > self.best_score:
                self.best_score = scores[metric]
                self.best_params = params
                print(f"   ✅ Nuevo mejor resultado: {scores[metric]:.4f}")
            
            print(f"   Resultado: {scores[metric]:.4f}")
        
        # Mostrar resultados finales
        self.print_optimization_results(metric)
        
        return {
            'best_params': self.best_params,
            'best_score': self.best_score,
            'all_results': self.results
        }
    
    def print_optimization_results(self, metric: str):
        """Imprime resultados de la optimización"""
        
        print(f"\n{'='*60}")
        print(f"🎉 OPTIMIZACIÓN COMPLETADA")
        print(f"{'='*60}")
        
        print(f"📊 Mejor resultado:")
        print(f"   Métrica ({metric}): {self.best_score:.4f}")
        print(f"   Parámetros:")
        for key, value in self.best_params.items():
            print(f"     {key}: {value}")
        
        # Top 5 resultados
        sorted_results = sorted(self.results, key=lambda x: x['metric_value'], reverse=True)
        
        print(f"\n🏆 Top 5 resultados:")
        for i, result in enumerate(sorted_results[:5]):
            print(f"   {i+1}. {result['metric_value']:.4f} - {result['params']}")
        
        # Análisis de parámetros
        self.analyze_parameter_importance(metric)
    
    def analyze_parameter_importance(self, metric: str):
        """Analiza la importancia de los parámetros"""
        
        print(f"\n📈 Análisis de importancia de parámetros:")
        
        # Agrupar por parámetro y calcular promedio
        param_importance = {}
        
        for result in self.results:
            for param_name, param_value in result['params'].items():
                if param_name not in param_importance:
                    param_importance[param_name] = {}
                
                if param_value not in param_importance[param_name]:
                    param_importance[param_name][param_value] = []
                
                param_importance[param_name][param_value].append(result['metric_value'])
        
        # Calcular promedios
        for param_name, values in param_importance.items():
            print(f"\n   {param_name}:")
            for value, scores in values.items():
                avg_score = np.mean(scores)
                print(f"     {value}: {avg_score:.4f} (n={len(scores)})")
    
    def save_results(self, filename: str = None):
        """Guarda los resultados de la optimización"""
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"../reports/optimization_results_{timestamp}.pkl"
        
        results_data = {
            'best_params': self.best_params,
            'best_score': self.best_score,
            'all_results': self.results,
            'timestamp': datetime.now(),
            'data_path': self.data_path
        }
        
        joblib.dump(results_data, filename)
        print(f"💾 Resultados guardados en: {filename}")
    
    def train_best_model(self, save_path: str = "../models/optimized_model.h5"):
        """Entrena el modelo con los mejores parámetros encontrados"""
        
        if self.best_params is None:
            print("❌ No hay parámetros optimizados disponibles")
            return None
        
        print("🏗️ Entrenando modelo con parámetros optimizados...")
        
        # Dividir datos finales
        split_idx = int(len(self.X) * 0.8)
        X_train, X_test = self.X[:split_idx], self.X[split_idx:]
        y_train, y_test = self.y[:split_idx], self.y[split_idx:]
        
        # Construir modelo
        model = self.build_model(self.best_params)
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=self.best_params['patience'],
            restore_best_weights=True,
            verbose=1
        )
        
        # Entrenar modelo
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=self.best_params['epochs'],
            batch_size=self.best_params['batch_size'],
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Evaluar modelo final
        test_loss, test_acc, test_precision, test_recall = model.evaluate(
            X_test, y_test, verbose=0
        )
        
        f1_score = 2 * (test_precision * test_recall) / (test_precision + test_recall) if (test_precision + test_recall) > 0 else 0
        
        print(f"✅ Modelo optimizado entrenado:")
        print(f"   Precisión: {test_acc:.4f}")
        print(f"   F1-Score: {f1_score:.4f}")
        
        # Guardar modelo
        model.save(save_path)
        print(f"💾 Modelo guardado en: {save_path}")
        
        # Guardar scaler
        scaler_path = save_path.replace('.h5', '_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        # Guardar características
        features_path = save_path.replace('.h5', '_features.pkl')
        joblib.dump(self.features, features_path)
        
        return model

def main():
    """Función principal para optimización"""
    print("🎯 OPTIMIZADOR DE HIPERPARÁMETROS")
    print("=" * 60)
    
    # Configurar optimizador
    optimizer = HyperparameterOptimizer(
        data_path="../data/EURUSD_combined_20231201.csv",  # Ajusta según tus datos
        max_trials=20  # Reducir para pruebas rápidas
    )
    
    # Ejecutar optimización
    results = optimizer.optimize(metric='f1_score')
    
    # Guardar resultados
    optimizer.save_results()
    
    # Entrenar modelo optimizado
    model = optimizer.train_best_model()
    
    print("✅ Optimización completada!")

if __name__ == "__main__":
    import os
    main() 