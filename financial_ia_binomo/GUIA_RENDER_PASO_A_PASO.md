# 🚀 Guía Visual: Desplegar en Render (Paso a Paso)

## 📋 Preparación (5 minutos)

### Paso 1: Crear cuenta en GitHub
1. Ve a [github.com](https://github.com)
2. Click "Sign up"
3. Completa el registro
4. Verifica tu email

### Paso 2: Subir código a GitHub
**Opción A: GitHub Desktop (Más fácil)**
1. Descarga [GitHub Desktop](https://desktop.github.com/)
2. Instala y abre
3. Click "Sign in to GitHub.com"
4. Click "Clone a repository from the Internet"
5. Click "Create a New Repository"
6. Nombre: `ia-financiera-mobile`
7. Click "Create Repository"
8. Arrastra tu carpeta `financial_ia_binomo` a GitHub Desktop
9. Escribe mensaje: "Primera versión de IA Financiera"
10. Click "Commit to main"
11. Click "Push origin"

**Opción B: Manual (Si no tienes GitHub Desktop)**
1. Ve a [github.com](https://github.com)
2. Click "New repository"
3. Nombre: `ia-financiera-mobile`
4. Marca "Public"
5. Click "Create repository"
6. Sube manualmente los archivos usando la interfaz web

---

## 🎯 Desplegar en Render (5 minutos)

### Paso 3: Crear cuenta en Render
1. Ve a [render.com](https://render.com)
2. Click "Get Started for Free"
3. Click "Continue with GitHub"
4. Autoriza Render a acceder a GitHub

### Paso 4: Crear Web Service
1. En Render Dashboard, click "New +"
2. Selecciona "Web Service"
3. Click "Connect" en tu repositorio `ia-financiera-mobile`

### Paso 5: Configurar
1. **Name**: `ia-financiera-mobile`
2. **Environment**: `Python 3`
3. **Build Command**: `pip install -r requirements_server.txt`
4. **Start Command**: `cd mobile_app && gunicorn server_app:app`
5. **Plan**: `Free`

### Paso 6: Crear
1. Click "Create Web Service"
2. Espera 2-3 minutos mientras se construye
3. ¡Listo! Tu URL aparecerá automáticamente

---

## 🌐 Tu URL Global

Una vez completado, tendrás una URL como:
```
https://ia-financiera-mobile.onrender.com
```

**Esta URL funciona:**
- ✅ Desde cualquier dispositivo
- ✅ Desde cualquier lugar del mundo
- ✅ No necesitas estar en la misma red WiFi
- ✅ Con SSL seguro (https://)

---

## 📱 Probar tu App

### Desde PC:
1. Abre tu navegador
2. Ve a tu URL de Render
3. La app se cargará automáticamente

### Desde Móvil:
1. Abre navegador en tu móvil
2. Ve a tu URL de Render
3. La app se adaptará automáticamente
4. Puedes agregarla a pantalla de inicio

---

## 🔍 Verificar que Funciona

### Endpoints de prueba:
- **Página principal**: `https://tu-app.onrender.com/`
- **Estado del servidor**: `https://tu-app.onrender.com/health`
- **Estadísticas**: `https://tu-app.onrender.com/stats`

### Respuesta esperada en `/health`:
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

### Error: "Build failed"
- Verifica que `requirements_server.txt` esté en la raíz
- Asegúrate de que `server_app.py` esté en `mobile_app/`

### Error: "Module not found"
- Todas las dependencias deben estar en `requirements_server.txt`
- Verifica que no haya errores de sintaxis

### App no carga
- Revisa los logs en Render Dashboard
- Verifica que todos los archivos estén en GitHub

---

## 📊 Monitoreo

### En Render Dashboard:
1. Ve a tu servicio
2. Click "Logs" para ver errores
3. Click "Metrics" para ver uso de recursos
4. Click "Events" para ver actividad

---

## 🔄 Actualizaciones

### Para actualizar tu app:
1. Haz cambios en tu código local
2. Sube a GitHub (GitHub Desktop o manual)
3. Render se actualizará automáticamente

### Para forzar redeploy:
1. Ve a tu servicio en Render
2. Click "Manual Deploy"
3. Selecciona "Clear build cache & deploy"

---

## 💡 Consejos

1. **Prueba localmente** antes de subir a GitHub
2. **Verifica los logs** si algo no funciona
3. **Usa HTTPS** siempre (incluido automáticamente)
4. **Monitorea el uso** en la pestaña Metrics

---

## 🎉 ¡Listo!

**Tu IA Financiera ahora está disponible globalmente:**
- 🌍 Acceso desde cualquier lugar
- 📱 Funciona en móviles y PCs
- 🔒 Seguro con HTTPS
- 🚀 Rápido y confiable

**¡Comparte tu URL con amigos y familia para que colaboren en el aprendizaje de la IA!**

---

**¿Necesitas ayuda con algún paso específico? ¡Pregunta sin miedo!** 😊 