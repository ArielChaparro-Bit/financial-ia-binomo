# 🎯 INSTRUCCIONES FINALES - SISTEMA IA FINANCIERA

## ✅ SISTEMA COMPLETAMENTE LISTO

El sistema está configurado y optimizado para funcionar sin errores en tu laptop y móvil.

---

## 🚀 CÓMO EJECUTAR EL SISTEMA

### **PASO 1: Abrir PowerShell**
1. Presiona `Windows + R`
2. Escribe `powershell` y presiona Enter
3. Se abrirá una ventana nueva

### **PASO 2: Navegar a la carpeta**
Copia y pega exactamente:
```powershell
cd "C:\Users\Evelia\OneDrive\Escritorio\Proyecto IA FINANCIERA\financial_ia_binomo"
```

### **PASO 3: Recrear modelo**
Copia y pega:
```powershell
python recreate_model.py
```
**Espera** hasta que diga "MODELO RECREADO EXITOSAMENTE"

### **PASO 4: Iniciar servidor**
Copia y pega:
```powershell
python start_api.py
```
**NO cierres esta ventana** - déjala abierta

### **PASO 5: Probar (opcional)**
Abre otra ventana de PowerShell y ejecuta:
```powershell
cd "C:\Users\Evelia\OneDrive\Escritorio\Proyecto IA FINANCIERA\financial_ia_binomo"
python test_api.py
```

---

## 📱 CÓMO USAR DESDE MÓVIL

### **Requisitos:**
- Tu móvil debe estar en la misma red WiFi que tu laptop
- El servidor debe estar corriendo en la laptop

### **Acceso:**
1. Abre el navegador de tu móvil
2. Ve a: `http://192.168.100.17:8080`
3. ¡Listo! La app funcionará perfectamente

---

## 🔗 URLs DISPONIBLES

- **Laptop**: `http://localhost:8080`
- **Móvil**: `http://192.168.100.17:8080`

---

## 📊 ENDPOINTS DISPONIBLES

- `GET /` - Página principal
- `GET /health` - Estado del sistema
- `GET /predict` - Predicciones
- `GET /backtest` - Backtest

---

## ⚠️ IMPORTANTE

1. **NO cierres la ventana de PowerShell** donde corre el servidor
2. **Para detener**: presiona `Ctrl + C` en la ventana del servidor
3. **Si hay errores**: cierra todas las ventanas y empieza de nuevo desde el PASO 1

---

## 🎉 ¡LISTO!

Una vez que sigas estos pasos:
- ✅ El sistema funcionará sin errores
- ✅ Podrás acceder desde tu laptop
- ✅ Podrás acceder desde tu móvil
- ✅ Todas las funciones estarán disponibles

---

## 📞 SOLUCIÓN DE PROBLEMAS

### **Error "No such file or directory"**
- Asegúrate de estar en la carpeta correcta
- Verifica que el archivo existe con `dir`

### **Error de conexión**
- Verifica que el servidor esté corriendo
- Asegúrate de usar la URL correcta

### **Error de modelo**
- Ejecuta `python recreate_model.py` primero
- Luego reinicia el servidor

---

**¡El sistema está guardado y listo para usar! 🚀** 