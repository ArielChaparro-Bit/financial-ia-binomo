# 📱 IA Financiera Móvil

Aplicación móvil responsive para el sistema de IA Financiera Binomo.

## 🚀 Características

- **Interfaz Responsive**: Se adapta a cualquier dispositivo
- **PWA (Progressive Web App)**: Instálala como app nativa
- **Acceso Offline**: Funciona sin conexión (datos básicos)
- **Código QR**: Acceso rápido desde móvil
- **API Integration**: Conecta con el servidor de IA
- **Tema Oscuro**: Interfaz moderna y elegante

## 📱 Cómo usar

### 1. Iniciar la aplicación
```bash
# Desde la carpeta principal
python start_mobile_app.py

# O directamente
cd mobile_app
python app.py
```

### 2. Acceder desde móvil
- **Misma red WiFi**: `http://[IP-DE-TU-PC]:8080`
- **Código QR**: Escanea el QR en `/qr`
- **Local**: `http://localhost:8080`

### 3. Instalar como app
- **Chrome/Edge**: "Instalar aplicación"
- **Safari**: "Agregar a pantalla de inicio"
- **Firefox**: "Instalar aplicación"

## 🎯 Funcionalidades

### 📊 Dashboard Principal
- Estado del sistema
- Últimas predicciones
- Indicadores en tiempo real
- Acceso rápido a funciones

### 🔮 Predicciones
- Señales de compra/venta
- Nivel de confianza
- Indicadores técnicos
- Historial de predicciones

### 📈 Backtesting
- Resultados de pruebas
- Métricas de rendimiento
- Gráficos de resultados
- Configuración de parámetros

### 📚 Aprendizaje
- Guías de trading
- Explicación de indicadores
- Estrategias básicas
- Consejos de gestión de riesgo

## 🔧 Configuración

### Variables de entorno
```bash
# Puerto de la aplicación móvil
MOBILE_PORT=8080

# URL del servidor API
API_BASE_URL=http://localhost:5000

# Modo de desarrollo
DEBUG=False
```

### Personalización
- **Colores**: Edita `static/css/style.css`
- **Iconos**: Reemplaza en `static/icons/`
- **Temas**: Modifica `templates/`

## 📱 Compatibilidad

### Navegadores
- ✅ Chrome 80+
- ✅ Safari 13+
- ✅ Firefox 75+
- ✅ Edge 80+

### Dispositivos
- ✅ iPhone/iPad (iOS 13+)
- ✅ Android (Chrome 80+)
- ✅ Windows (Edge/Chrome)
- ✅ macOS (Safari/Chrome)

## 🚀 Despliegue

### Local
```bash
python start_mobile_app.py
```

### Render/Heroku
```bash
# Configurar variables de entorno
MOBILE_PORT=8080
API_BASE_URL=https://tu-api.herokuapp.com

# Desplegar
git push heroku main
```

### Vercel/Netlify
```bash
# Configurar build command
python -m http.server 8080

# Desplegar automáticamente
```

## 🔒 Seguridad

- **HTTPS**: Recomendado para producción
- **CORS**: Configurado para API local
- **Validación**: Input sanitization
- **Rate Limiting**: Protección contra spam

## 📊 Monitoreo

### Endpoints de estado
- `/api/status` - Estado de la aplicación
- `/api/health` - Salud del sistema
- `/api/predict` - Predicciones
- `/api/backtest` - Resultados de backtesting

### Logs
- Errores de conexión
- Predicciones realizadas
- Usuarios conectados
- Rendimiento del sistema

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Haz tus cambios
4. Prueba en diferentes dispositivos
5. Envía un Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE en el directorio principal.

---

**¡Disfruta usando tu IA Financiera desde cualquier dispositivo! 📱🚀** 