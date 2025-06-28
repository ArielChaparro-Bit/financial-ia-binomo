# 📱 Instrucciones para Usar la IA Financiera en Móvil

## 🎯 Configuración Específica para tu Red

### **IP Configurada: 192.168.100.17**

---

## 🚀 Cómo Iniciar la Aplicación

### **Paso 1: Iniciar el Servidor API**
```bash
python start_api.py
```

### **Paso 2: Iniciar la App Móvil**
```bash
python start_mobile_app.py
```

---

## 📱 URLs de Acceso

### **Desde tu PC:**
- **API**: http://192.168.100.17:5000
- **App Móvil**: http://192.168.100.17:8080

### **Desde tu Móvil:**
- **App Principal**: http://192.168.100.17:8080
- **Código QR**: http://192.168.100.17:8080/qr
- **Estado API**: http://192.168.100.17:8080/api/status

---

## 📋 Pasos para Usar en Móvil

### **1. Asegúrate de que esté funcionando:**
- Ejecuta `python start_mobile_app.py` en tu PC
- Verifica que aparezca: "App URL: http://192.168.100.17:8080"

### **2. Accede desde tu móvil:**
- Abre tu navegador en el móvil
- Escribe: `http://192.168.100.17:8080`
- ¡Listo! Ya puedes usar la app

### **3. Instalar como App:**
- **Chrome**: 3 puntos → "Instalar aplicación"
- **Safari**: Botón compartir → "Agregar a pantalla de inicio"
- **Firefox**: 3 líneas → "Instalar aplicación"

---

## 🔧 Solución de Problemas

### **Si no puedes acceder desde el móvil:**

1. **Verifica que estén en la misma red WiFi**
   - Tu PC y móvil deben estar conectados a la misma red

2. **Verifica que el firewall no bloquee**
   - Windows puede bloquear la conexión
   - Permite el acceso cuando te pregunte

3. **Verifica que los puertos estén abiertos**
   - Puerto 5000 (API)
   - Puerto 8080 (App Móvil)

4. **Prueba desde tu PC primero**
   - Abre http://192.168.100.17:8080 en tu PC
   - Si funciona en PC, el problema es de red

### **Si la API no responde:**

1. **Verifica que el servidor API esté ejecutándose**
   - Ejecuta `python start_api.py` en otra terminal

2. **Verifica el estado**
   - Ve a http://192.168.100.17:8080/api/status
   - Debe mostrar "Conectado"

---

## 📊 Funcionalidades Disponibles

### **Dashboard Principal:**
- Estado del sistema
- Conexión con API
- Acceso rápido a funciones

### **Predicciones:**
- Obtener señales de compra/venta
- Nivel de confianza
- Precio actual

### **Backtesting:**
- Resultados de pruebas
- Métricas de rendimiento
- Configuración de parámetros

### **Aprendizaje:**
- Guías de trading
- Explicación de indicadores
- Estrategias básicas

### **Código QR:**
- Acceso rápido desde móvil
- Escanea con la cámara

---

## ⚠️ Importante

- **Esta app es educativa**, no garantiza ganancias
- **El trading tiene riesgos**, nunca inviertas más de lo que puedes perder
- **La IA puede equivocarse**, no confíes 100% en las predicciones
- **Consulta con un asesor financiero** antes de invertir

---

## 📞 Si Tienes Problemas

1. **Verifica que Python esté instalado**
2. **Verifica que estés en la carpeta correcta**
3. **Verifica que tu móvil y PC estén en la misma red WiFi**
4. **Verifica que los puertos 5000 y 8080 estén libres**
5. **Revisa los mensajes de error en la terminal**

---

## 🎯 URLs Importantes

- **App Principal**: http://192.168.100.17:8080
- **API Health**: http://192.168.100.17:5000/health
- **App Status**: http://192.168.100.17:8080/api/status
- **Código QR**: http://192.168.100.17:8080/qr

---

**¡Disfruta usando tu IA Financiera desde tu móvil! 📱✨** 