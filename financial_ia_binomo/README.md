# 🤖 IA Financiera para Binomo

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/tu-usuario/financial-ia-binomo)
[![Mobile](https://img.shields.io/badge/Mobile-App-blue.svg)](mobile_app/README.md)
[![Deploy](https://img.shields.io/badge/Deploy-Cloud-orange.svg)](#-despliegue-en-la-nube)

Sistema de inteligencia artificial para análisis y predicción de mercados financieros, optimizado para la plataforma Binomo.

## 🚀 Características

- **Modelo de Machine Learning**: Random Forest optimizado para predicciones de mercado
- **API REST**: Servidor Flask con endpoints para predicciones y backtesting
- **📱 Aplicación Móvil**: Interfaz web responsive con PWA (Progressive Web App)
- **🌐 Despliegue Cloud**: Funciona sin IP local - accesible desde cualquier lugar
- **Indicadores Técnicos**: RSI, MACD, Bollinger Bands, Stochastic, ATR, Williams %R
- **Gestión de Riesgo**: Sistema integrado de gestión de riesgo
- **Backtesting**: Herramientas para probar estrategias
- **Código QR**: Acceso rápido desde móvil

## 📱 Aplicación Móvil

### 🎯 Características de la App
- **PWA (Progressive Web App)**: Instálala como app nativa
- **Responsive**: Se adapta a cualquier dispositivo
- **Offline**: Funciona sin conexión (datos básicos)
- **Código QR**: Acceso rápido desde móvil
- **Tema Oscuro**: Interfaz moderna
- **🌐 Cloud Ready**: Funciona sin IP local

### 📱 Cómo usar la App Móvil
```bash
# Local
python start_mobile_app.py

# Cloud (Recomendado)
# Despliega en Render/Heroku y accede desde cualquier lugar
```

### 📱 Instalar como App
- **Chrome/Edge**: "Instalar aplicación"
- **Safari**: "Agregar a pantalla de inicio"
- **Firefox**: "Instalar aplicación"

## 🌐 Despliegue en la Nube

### 🎯 ¿Por qué Cloud?
- ✅ **Sin IP local** - Acceso desde cualquier lugar
- ✅ **Siempre disponible** - 24/7 online
- ✅ **Compartible** - Cualquiera puede usar tu app
- ✅ **Escalable** - Se adapta al tráfico
- ✅ **Seguro** - HTTPS automático

### 🚀 Despliegue Rápido

#### Opción 1: Render (Recomendado - Gratis)
1. **Ve a [Render.com](https://render.com)**
2. **Conecta tu repositorio** de GitHub
3. **Crea Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python mobile_app/app_cloud.py`
4. **¡Listo!** Tu app estará en `https://tu-app.onrender.com`

#### Opción 2: Heroku
```bash
# Instalar Heroku CLI
# Ejecutar despliegue automático
python deploy_to_cloud.py
```

#### Opción 3: Vercel
1. **Ve a [Vercel.com](https://vercel.com)**
2. **Importa tu repositorio**
3. **Configura como Python app**
4. **¡Listo!**

### 📱 Acceso desde Móvil (Cloud)
- **URL directa**: `https://tu-app.onrender.com`
- **Código QR**: Escanea desde `/qr`
- **PWA**: Instala como app nativa
- **Sin configuración**: Funciona inmediatamente

## 📋 Requisitos

- Python 3.8+
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/financial-ia-binomo.git
cd financial-ia-binomo
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Instala dependencias del servidor (opcional):**
```bash
pip install -r requirements_server.txt
```

## 🎯 Uso Rápido

### 1. Entrenar el Modelo
```bash
python train_ai.py
```

### 2. Generar Datos de Ejemplo
```bash
python get_data.py
```

### 3. Ejecutar la API
```bash
python start_api.py
```

### 4. Ejecutar la App Móvil
```bash
# Local
python start_mobile_app.py

# Cloud (Recomendado)
python deploy_to_cloud.py
```

### 5. Probar el Sistema
```bash
python test_api.py
```

## 📊 Endpoints de la API

### Estado del Sistema
```http
GET http://localhost:5000/health
```

### Predicciones
```http
GET http://localhost:5000/predict
```

### Backtesting
```http
GET http://localhost:5000/backtest
```

### Página Principal
```http
GET http://localhost:5000/
```

## 📱 Endpoints de la App Móvil

### Aplicación Móvil
```http
GET http://localhost:8080/
```

### Estado de la App
```http
GET http://localhost:8080/api/status
```

### Predicciones desde App
```http
GET http://localhost:8080/api/predict
```

### Código QR
```http
GET http://localhost:8080/qr
```

### Demo (Sin API)
```http
GET http://localhost:8080/demo
```

## 🏗️ Estructura del Proyecto

```
financial_ia_binomo/
├── src/                    # Código fuente principal
│   ├── api_server.py      # Servidor API principal
│   ├── auto_trader.py     # Trading automático
│   ├── backtester.py      # Sistema de backtesting
│   ├── data_collector.py  # Recolector de datos
│   ├── data_processing.py # Procesamiento de datos
│   ├── features.py        # Generación de features
│   ├── model_train.py     # Entrenamiento de modelos
│   ├── optimizer.py       # Optimización de hiperparámetros
│   ├── risk_manager.py    # Gestión de riesgo
│   └── simple_model.py    # Modelo simple
├── mobile_app/            # 📱 Aplicación móvil
│   ├── app.py            # Servidor de la app móvil (local)
│   ├── app_cloud.py      # Servidor de la app móvil (cloud)
│   ├── templates/        # Plantillas HTML
│   ├── static/           # Archivos estáticos
│   └── README.md         # Documentación de la app
├── data/                  # Datos y archivos CSV
├── models/                # Modelos entrenados
├── logs/                 # Archivos de log
├── reports/              # Reportes generados
├── start_api.py          # Script para iniciar API
├── start_mobile_app.py   # Script para iniciar app móvil (local)
├── deploy_to_cloud.py    # Script para desplegar a la nube
├── train_ai.py           # Script de entrenamiento
├── test_api.py           # Script de pruebas
├── build_android_app.py  # Generador de APK
├── config.json           # Configuración del sistema
├── render.yaml           # Configuración para Render
├── Procfile              # Configuración para Heroku
└── requirements.txt      # Dependencias
```

## 🔧 Configuración

El archivo `config.json` contiene la configuración del sistema:

```json
{
  "model_settings": {
    "model_type": "random_forest",
    "n_estimators": 100,
    "max_depth": 10
  },
  "api_settings": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "mobile_settings": {
    "host": "0.0.0.0",
    "port": 8080,
    "api_url": "http://localhost:5000"
  },
  "cloud_settings": {
    "api_url": "https://ia-financiera-api.onrender.com",
    "auto_deploy": true
  },
  "data_settings": {
    "data_source": "binomo",
    "timeframe": "1m"
  }
}
```

## 📱 Uso de la Aplicación Móvil

### Acceso Local
1. **Misma red WiFi**: `http://[IP-DE-TU-PC]:8080`
2. **Código QR**: Escanea el QR en `/qr`
3. **Local**: `http://localhost:8080`

### Acceso Cloud (Recomendado)
1. **URL directa**: `https://tu-app.onrender.com`
2. **Código QR**: Escanea desde `/qr`
3. **PWA**: Instala como app nativa
4. **Sin configuración**: Funciona desde cualquier lugar

### Funcionalidades Móviles
- **Dashboard**: Estado del sistema en tiempo real
- **Predicciones**: Señales de compra/venta
- **Backtesting**: Resultados de pruebas
- **Aprendizaje**: Guías y tutoriales
- **Configuración**: Ajustes personalizados
- **Demo**: Funciona sin API

## 🧪 Pruebas

### Prueba Completa del Sistema
```bash
python test_system.py
```

### Prueba de la API
```bash
python test_api.py
```

### Prueba de la App Móvil
```bash
# Verificar que la app responde
curl http://localhost:8080/api/status
```

### Prueba de Acceso
```bash
python test_access.py
```

## 📈 Indicadores Técnicos

El sistema incluye los siguientes indicadores:

- **RSI (Relative Strength Index)**
- **MACD (Moving Average Convergence Divergence)**
- **Bollinger Bands**
- **Stochastic Oscillator**
- **ATR (Average True Range)**
- **Williams %R**
- **Medias Móviles (SMA, EMA)**
- **Momentum y Rate of Change**

## 🔒 Gestión de Riesgo

El sistema incluye:

- **Stop Loss automático**
- **Take Profit configurable**
- **Posición sizing basado en volatilidad**
- **Máximo drawdown permitido**

## 🚀 Despliegue

### Despliegue Local
```bash
# API
python start_api.py

# App Móvil
python start_mobile_app.py
```

### Despliegue en la Nube
```bash
# Despliegue automático
python deploy_to_cloud.py

# O manualmente en Render/Heroku/Vercel
```

### Generar APK Android
```bash
python build_android_app.py
```

## 📝 Scripts Útiles

- `recreate_model.py`: Recrea el modelo desde cero
- `reactivate_system.py`: Reactiva todo el sistema
- `run_complete_system.py`: Ejecuta el sistema completo
- `check_accuracy.py`: Verifica la precisión del modelo
- `simple_test.py`: Pruebas simples del sistema
- `start_mobile_app.py`: Inicia la aplicación móvil (local)
- `deploy_to_cloud.py`: Despliega a la nube automáticamente
- `build_android_app.py`: Genera APK para Android

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Descargo de Responsabilidad

Este software es solo para fines educativos y de investigación. No garantizamos ganancias en trading. El trading financiero conlleva riesgos significativos.

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Ejecuta los scripts de prueba
3. Verifica la configuración en `config.json`
4. Revisa los logs en la carpeta `logs/`
5. Consulta la documentación de la app móvil en `mobile_app/README.md`
6. Para problemas de despliegue, consulta `GUIA_DESPLIEGUE.md`

---

**¡Disfruta usando tu IA Financiera desde cualquier dispositivo y lugar! 🚀📱🌐**