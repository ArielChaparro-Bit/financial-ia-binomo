# 🚀 Guía de Despliegue - IA Financiera Móvil

## 📋 Opciones de Servidor Externo (Gratuitas)

### 1. **Render (Recomendado - Gratuito)**
- ✅ Fácil de configurar
- ✅ Dominio automático
- ✅ SSL gratuito
- ✅ Base de datos incluida

### 2. **Railway**
- ✅ Muy rápido
- ✅ Dominio automático
- ✅ SSL gratuito

### 3. **Heroku**
- ⚠️ Ya no es gratuito
- ✅ Muy estable
- ✅ Muchos add-ons

### 4. **Vercel**
- ✅ Excelente para frontend
- ⚠️ Limitado para Python

---

## 🎯 Despliegue en Render (Paso a Paso)

### **Paso 1: Preparar el Código**

1. **Asegúrate de tener estos archivos:**
   ```
   financial_ia_binomo/
   ├── requirements_server.txt
   ├── render.yaml
   ├── mobile_app/
   │   ├── server_app.py
   │   ├── templates/
   │   │   ├── index.html
   │   │   └── learn.html
   │   └── static/
   ```

2. **Verifica que `server_app.py` esté en `mobile_app/`**

### **Paso 2: Crear Cuenta en Render**

1. Ve a [render.com](https://render.com)
2. Regístrate con GitHub
3. Conecta tu repositorio

### **Paso 3: Desplegar**

1. **En Render Dashboard:**
   - Click "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub

2. **Configuración:**
   ```
   Name: ia-financiera-mobile
   Environment: Python 3
   Build Command: pip install -r requirements_server.txt
   Start Command: cd mobile_app && gunicorn server_app:app
   ```

3. **Variables de Entorno:**
   ```
   PYTHON_VERSION=3.9.16
   ```

4. **Click "Create Web Service"**

### **Paso 4: Obtener URL**

- Render te dará una URL como: `https://ia-financiera-mobile.onrender.com`
- Esta URL funcionará desde cualquier dispositivo con internet

---

## 🔧 Despliegue en Railway

### **Paso 1: Preparar**
1. Ve a [railway.app](https://railway.app)
2. Regístrate con GitHub

### **Paso 2: Desplegar**
1. Click "New Project"
2. Selecciona tu repositorio
3. Railway detectará automáticamente que es Python
4. Configura:
   ```
   Build Command: pip install -r requirements_server.txt
   Start Command: cd mobile_app && gunicorn server_app:app
   ```

### **Paso 3: Obtener URL**
- Railway te dará una URL automáticamente
- Ejemplo: `https://ia-financiera-mobile-production.up.railway.app`

---

## 🌐 Dominio Personalizado (Opcional)

### **Con Render:**
1. Ve a tu servicio en Render
2. Click "Settings"
3. En "Custom Domains" agrega tu dominio
4. Configura DNS en tu proveedor de dominio

### **Ejemplo de DNS:**
```
Type: CNAME
Name: ia
Value: ia-financiera-mobile.onrender.com
```

---

## 📱 Acceso desde Móvil

### **Una vez desplegado:**
- **URL global:** `https://tu-app.onrender.com`
- **Funciona desde cualquier dispositivo**
- **No necesitas estar en la misma red WiFi**
- **Acceso desde cualquier lugar del mundo**

### **Agregar a Pantalla de Inicio:**
1. Abre la URL en tu móvil
2. En Chrome/Safari, toca "Compartir"
3. Selecciona "Agregar a Pantalla de Inicio"
4. La app aparecerá como una app nativa

---

## 🔍 Verificar que Funciona

### **Endpoints de Prueba:**
- **Página principal:** `https://tu-app.onrender.com/`
- **Estado del servidor:** `https://tu-app.onrender.com/health`
- **Estadísticas:** `https://tu-app.onrender.com/stats`

### **Respuesta esperada en `/health`:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-25T21:45:42",
  "server": "IA Financiera Móvil",
  "version": "1.0.0"
}
```

---

## 🛠️ Solución de Problemas

### **Error: "Module not found"**
- Verifica que `requirements_server.txt` esté en la raíz
- Asegúrate de que todas las dependencias estén listadas

### **Error: "No such file or directory"**
- Verifica que `server_app.py` esté en `mobile_app/`
- Revisa la ruta en `startCommand`

### **Error: "Port already in use"**
- Render/Railway maneja los puertos automáticamente
- Usa `os.environ.get('PORT', 5000)` en el código

### **App no carga**
- Verifica los logs en el dashboard del servidor
- Revisa que todos los archivos estén en el repositorio

---

## 📊 Monitoreo

### **En Render:**
- Ve a tu servicio
- Click "Logs" para ver errores
- Click "Metrics" para ver uso de recursos

### **En Railway:**
- Ve a tu proyecto
- Click "Deployments" para ver logs
- Click "Variables" para configurar

---

## 🔄 Actualizaciones

### **Para actualizar la app:**
1. Haz cambios en tu código local
2. Sube a GitHub (`git push`)
3. El servidor se actualizará automáticamente

### **Para forzar redeploy:**
- En Render: Click "Manual Deploy"
- En Railway: Click "Deploy" en la pestaña Deployments

---

## 💡 Consejos

1. **Prueba localmente** antes de desplegar
2. **Usa variables de entorno** para configuraciones sensibles
3. **Monitorea los logs** para detectar errores
4. **Haz backups** de la base de datos si es importante
5. **Usa HTTPS** siempre (incluido automáticamente)

---

**¡Con esto tendrás tu IA Financiera accesible desde cualquier lugar del mundo!** 🌍📱 