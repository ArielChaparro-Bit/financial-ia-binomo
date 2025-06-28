# 📱 IA Financiera Móvil

## 🎯 Descripción

Aplicación móvil web progresiva (PWA) que permite a usuarios con conocimientos básicos usar y mejorar una IA financiera. La aplicación aprende por sí misma con cada predicción y feedback del usuario.

## ✨ Características Principales

### 🤖 **IA Autodidacta**
- **Aprendizaje automático**: La IA mejora con cada predicción
- **Feedback del usuario**: Sistema de calificación con estrellas
- **Base de datos local**: Almacena todas las predicciones y resultados
- **Reentrenamiento automático**: Se actualiza cada 10 predicciones

### 📊 **Interfaz Simple**
- **Diseño móvil**: Optimizada para smartphones
- **3 pestañas principales**: Predecir, Estadísticas, Aprender
- **Símbolos populares**: EUR/USD, GBP/USD, USD/JPY, BTC/USD
- **Feedback visual**: Colores y iconos intuitivos

### 📈 **Sistema de Estadísticas**
- **Precisión en tiempo real**: Muestra el porcentaje de aciertos
- **Historial de predicciones**: Últimas 10 predicciones
- **Nivel de IA**: Sistema de niveles basado en precisión
- **Logros**: Sistema de gamificación

## 🚀 Cómo Usar

### 1. **Iniciar la Aplicación**
```bash
cd mobile_app
python app.py
```

### 2. **Acceder desde el Móvil**
- Abre tu navegador móvil
- Ve a: `http://TU_IP:5000`
- Ejemplo: `http://192.168.1.100:5000`

### 3. **Hacer una Predicción**
1. Selecciona el símbolo (EUR/USD, etc.)
2. Toca "Obtener Predicción"
3. La IA te dará una señal (COMPRAR/VENDER)
4. Observa el resultado real
5. Da feedback sobre si fue correcta

### 4. **Mejorar la IA**
- **Califica cada predicción** con 1-5 estrellas
- **Indica si subió o bajó** el precio
- **Usa la app regularmente** para que aprenda
- **Revisa las estadísticas** para ver el progreso

## 🧠 Cómo Aprende la IA

### **Sistema de Aprendizaje**
1. **Predicción inicial**: La IA analiza datos de mercado
2. **Feedback del usuario**: El usuario indica si fue correcta
3. **Almacenamiento**: Se guarda en base de datos SQLite
4. **Reentrenamiento**: Cada 10 predicciones, la IA se actualiza
5. **Mejora continua**: La precisión aumenta con el tiempo

### **Características que Aprende**
- **Patrones de precio**: Movimientos históricos
- **Indicadores técnicos**: RSI, MACD, medias móviles
- **Comportamiento del usuario**: Preferencias y horarios
- **Mercados específicos**: Diferencias entre símbolos

## 📱 Características Móviles

### **Diseño Responsivo**
- **Adaptable**: Se ajusta a cualquier pantalla
- **Touch-friendly**: Botones grandes para dedos
- **Navegación simple**: 3 pestañas principales
- **Carga rápida**: Optimizada para conexiones lentas

### **Funcionalidades Offline**
- **Datos locales**: Base de datos SQLite
- **Predicciones guardadas**: Historial completo
- **Estadísticas offline**: Funciona sin internet
- **Sincronización**: Se actualiza cuando hay conexión

## 🔧 Configuración

### **Requisitos**
- Python 3.7+
- Flask
- scikit-learn
- pandas
- numpy

### **Instalación**
```bash
pip install flask scikit-learn pandas numpy
```

### **Configuración de Red**
Para acceder desde móviles en la misma red:
1. Encuentra tu IP local: `ipconfig` (Windows) o `ifconfig` (Mac/Linux)
2. Modifica `app.py` línea final: `app.run(host='0.0.0.0', port=5000)`
3. Accede desde móvil: `http://TU_IP:5000`

## 📊 Estructura de Datos

### **Base de Datos SQLite**
```sql
-- Predicciones
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    prediction TEXT,
    confidence REAL,
    actual_result TEXT,
    timestamp DATETIME,
    is_correct BOOLEAN
);

-- Feedback de usuarios
CREATE TABLE user_feedback (
    id INTEGER PRIMARY KEY,
    prediction_id INTEGER,
    user_rating INTEGER,
    user_comment TEXT,
    timestamp DATETIME
);

-- Datos de mercado
CREATE TABLE market_data (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    timestamp DATETIME
);
```

## 🎮 Sistema de Gamificación

### **Niveles de IA**
- **Nivel 1-3**: IA Básica (0-30% precisión)
- **Nivel 4-6**: IA Intermedia (30-60% precisión)
- **Nivel 7-9**: IA Avanzada (60-90% precisión)
- **Nivel 10**: IA Experta (90%+ precisión)

### **Logros Desbloqueables**
- ✅ Primera Predicción
- ✅ 10 Predicciones
- ✅ 50% Precisión
- 🔒 100 Predicciones
- 🔒 80% Precisión
- 🔒 7 días consecutivos

## 🔮 Futuras Mejoras

### **Funcionalidades Planificadas**
- **Notificaciones push**: Alertas de predicciones
- **Modo oscuro**: Interfaz nocturna
- **Gráficos interactivos**: Visualización de datos
- **Comunidad**: Compartir predicciones
- **API de datos reales**: Conexión con Binomo
- **Trading automático**: Ejecución automática

### **Mejoras de IA**
- **Deep Learning**: Redes neuronales
- **Análisis de sentimiento**: Noticias y redes sociales
- **Predicciones múltiples**: Varios timeframes
- **Gestión de riesgo**: Stop loss automático

## 🛠️ Desarrollo

### **Estructura del Proyecto**
```
mobile_app/
├── app.py              # Servidor Flask
├── templates/          # Plantillas HTML
│   ├── index.html     # Página principal
│   └── learn.html     # Página de aprendizaje
├── static/            # Archivos estáticos
├── user_data.db       # Base de datos SQLite
├── mobile_model.pkl   # Modelo de IA
└── mobile_scaler.pkl  # Normalizador de datos
```

### **Personalización**
- **Colores**: Modifica el CSS en las plantillas
- **Símbolos**: Agrega nuevos en `app.py`
- **Algoritmos**: Cambia el modelo en `MobileIA`
- **Interfaz**: Edita las plantillas HTML

## 📞 Soporte

### **Problemas Comunes**
1. **No se conecta desde móvil**: Verifica la IP y firewall
2. **Predicciones incorrectas**: Da más feedback para mejorar
3. **App lenta**: Reinicia el servidor
4. **Datos perdidos**: Los datos se guardan automáticamente

### **Contacto**
- **Issues**: Crear issue en GitHub
- **Mejoras**: Pull requests bienvenidos
- **Documentación**: Actualizar este README

---

**¡Disfruta usando tu IA Financiera personal! 🚀💰** 