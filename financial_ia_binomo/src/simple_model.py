import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
from data_processing import load_data
from features import add_technical_indicators, get_feature_columns

class SimpleTradingModel:
    """
    Modelo simple de trading usando Random Forest
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = MinMaxScaler()
        self.features = None
        self.is_trained = False
    
    def prepare_data(self, data_path):
        """Prepara los datos para entrenamiento"""
        print("📊 Preparando datos...")
        
        # Cargar datos
        df = load_data(data_path)
        if df is None:
            return None
        
        # Agregar indicadores técnicos
        df = add_technical_indicators(df)
        
        # Obtener características
        self.features = get_feature_columns()
        available_features = [f for f in self.features if f in df.columns]
        
        if len(available_features) < 5:
            print("⚠️ Pocas características disponibles")
            return None
        
        # Preparar datos
        X = df[available_features].values
        y = []
        
        # Crear etiquetas: 1 si el precio sube, 0 si baja
        for i in range(len(X) - 1):
            if df['close'].iloc[i+1] > df['close'].iloc[i]:
                y.append(1)
            else:
                y.append(0)
        
        # Ajustar X para que coincida con y
        X = X[:-1]
        y = np.array(y)
        
        # Eliminar filas con valores NaN
        mask = ~np.isnan(X).any(axis=1)
        X = X[mask]
        y = y[mask]
        
        print(f"✅ Datos preparados: {len(X)} muestras, {len(available_features)} características")
        
        return X, y, available_features
    
    def train(self, data_path):
        """Entrena el modelo"""
        print("🤖 Entrenando modelo Random Forest...")
        
        # Preparar datos
        result = self.prepare_data(data_path)
        if result is None:
            return False
        
        X, y, features = result
        
        # Normalizar datos
        X_scaled = self.scaler.fit_transform(X)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        print(f"   Datos de entrenamiento: {len(X_train)} muestras")
        print(f"   Datos de validación: {len(X_test)} muestras")
        
        # Entrenar modelo
        self.model.fit(X_train, y_train)
        
        # Evaluar modelo
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        print(f"📊 Resultados del modelo:")
        print(f"   Precisión: {accuracy:.3f}")
        print(f"   Precision: {precision:.3f}")
        print(f"   Recall: {recall:.3f}")
        print(f"   F1-Score: {f1:.3f}")
        
        self.is_trained = True
        self.features = features
        
        return True
    
    def predict(self, data):
        """Realiza predicción"""
        if not self.is_trained:
            return None
        
        # Normalizar datos
        data_scaled = self.scaler.transform(data)
        
        # Predicción
        prediction = self.model.predict_proba(data_scaled)[0]
        
        return {
            'probability_up': prediction[1],
            'probability_down': prediction[0],
            'signal': 'BUY' if prediction[1] > 0.5 else 'SELL',
            'confidence': abs(prediction[1] - 0.5) * 2
        }
    
    def save_model(self, model_path):
        """Guarda el modelo"""
        if not self.is_trained:
            print("❌ Modelo no entrenado")
            return False
        
        try:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Guardar modelo
            joblib.dump(self.model, model_path)
            
            # Guardar scaler
            scaler_path = model_path.replace('.pkl', '_scaler.pkl')
            joblib.dump(self.scaler, scaler_path)
            
            # Guardar características
            features_path = model_path.replace('.pkl', '_features.pkl')
            joblib.dump(self.features, features_path)
            
            print(f"💾 Modelo guardado en: {model_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando modelo: {e}")
            return False
    
    def load_model(self, model_path):
        """Carga el modelo"""
        try:
            # Cargar modelo
            self.model = joblib.load(model_path)
            
            # Cargar scaler
            scaler_path = model_path.replace('.pkl', '_scaler.pkl')
            self.scaler = joblib.load(scaler_path)
            
            # Cargar características
            features_path = model_path.replace('.pkl', '_features.pkl')
            self.features = joblib.load(features_path)
            
            self.is_trained = True
            print(f"✅ Modelo cargado desde: {model_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False

def main():
    """Función principal"""
    print("🤖 MODELO SIMPLE DE TRADING")
    print("=" * 40)
    
    # Crear modelo
    model = SimpleTradingModel()
    
    # Entrenar modelo
    data_path = "../data/price_data.csv"
    if model.train(data_path):
        # Guardar modelo
        model_path = "../models/simple_model.pkl"
        model.save_model(model_path)
        
        print("🎉 Modelo entrenado y guardado exitosamente!")
    else:
        print("❌ Error entrenando modelo")

if __name__ == "__main__":
    main() 