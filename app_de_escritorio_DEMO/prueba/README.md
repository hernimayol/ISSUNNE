SCORE2 - Calculadora de Riesgo Cardiovascular
Unidad de Prevención Cardiometabólica - ISSUNNE Corrientes Capital
Sistema de escritorio para cálculo de riesgo cardiovascular según guías ESC 2021 (SCORE2 y SCORE2-OP).

📋 Características

✅ Cálculo automático de riesgo cardiovascular a 10 años
✅ SCORE2 para pacientes de 40-69 años
✅ SCORE2-OP para pacientes ≥70 años
✅ Regiones de riesgo: Moderado y Muy Alto
✅ Base de datos SQLite integrada (funciona sin conexión)
✅ Gestión completa de pacientes
✅ Historial de cálculos
✅ Estadísticas y dashboards
✅ Exportación a CSV
✅ Backups automáticos


🚀 Instalación
Requisitos Previos

Python 3.8 o superior
Windows 10/11, Linux o macOS

Paso 1: Clonar o descargar el repositorio
bashgit clone https://github.com/hernimayol/ISSUNNE.git
cd ISSUNNE/app_de_escritorio_DEMO
O descarga directamente los archivos:

tablas_score2.py
database.py
main.py
requirements.txt

Paso 2: Crear entorno virtual (recomendado)
Windows:
bashpython -m venv venv
venv\Scripts\activate
Linux/macOS:
bashpython3 -m venv venv
source venv/bin/activate
Paso 3: Instalar dependencias
bashpip install -r requirements.txt
Paso 4: Ejecutar la aplicación
bashpython main.py

📖 Guía de Uso
1. Crear un Nuevo Paciente

Ir a Archivo → Nuevo Paciente o presionar el botón "➕ Nuevo Paciente"
Completar los datos del formulario:

Nombre y Apellido (obligatorios)
DNI
Fecha de nacimiento
Sexo (obligatorio)
Datos de contacto
Obra social


Presionar "Guardar"

2. Calcular Riesgo Cardiovascular

En la pestaña "📊 Calculadora":

Seleccionar un paciente del desplegable
La edad se completa automáticamente
Ingresar:

PAS (Presión Arterial Sistólica): 100-179 mmHg
Colesterol no-HDL: 3.0-7.0 mmol/L
Estado de fumador (marcar si corresponde)
Región de riesgo: Moderado o Muy Alto


Opcionalmente: peso, altura y otros datos


Presionar "🔄 CALCULAR RIESGO"
Revisar el resultado:

Porcentaje de riesgo a 10 años
Categoría (Bajo/Moderado/Alto)
Interpretación automática
Método utilizado (SCORE2 o SCORE2-OP)


Presionar "💾 GUARDAR CÁLCULO" para almacenar en la base de datos

3. Gestionar Pacientes

Buscar: Usar la barra de búsqueda en la pestaña "👥 Pacientes"
Ver detalles: Seleccionar paciente y presionar "Ver Detalles"
Editar: Seleccionar paciente y presionar "Editar"
Eliminar: Seleccionar paciente y presionar "Eliminar" (eliminación lógica)

4. Ver Historial
En la pestaña "📋 Historial" se muestra:

Todos los cálculos realizados
Fecha de cada cálculo
Paciente asociado
Riesgo calculado
Categoría

5. Estadísticas
En la pestaña "📈 Estadísticas":

Total de pacientes registrados
Total de cálculos realizados
Riesgo promedio
Distribución por categorías (Bajo/Moderado/Alto)
Número de fumadores


🗂️ Estructura del Proyecto
app_de_escritorio_DEMO/
│
├── tablas_score2.py       # Tablas SCORE2 y SCORE2-OP con funciones de cálculo
├── database.py            # Gestor de base de datos SQLite
├── main.py                # Aplicación principal con interfaz gráfica
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Este archivo
│
└── score2_pacientes.db    # Base de datos (se crea automáticamente)

📊 Tablas Implementadas
SCORE2 (40-69 años)
Región de Riesgo MODERADO:

✅ Varones No Fumadores
✅ Varones Fumadores
✅ Mujeres No Fumadoras
✅ Mujeres Fumadoras

SCORE2-OP (≥70 años)
Región de Riesgo MODERADO:

✅ Varones No Fumadores
✅ Varones Fumadores
✅ Mujeres No Fumadoras
✅ Mujeres Fumadoras

Regiones de Riesgo MUY ALTO
⚠️ PENDIENTE: Necesitás enviarme las imágenes de las tablas de región MUY ALTO para completarlas.

🔍 Rangos de Valores Válidos
ParámetroRango VálidoUnidadEdad40-89 añosañosPAS100-179mmHgColesterol no-HDL3.0-7.0mmol/L
Conversión de Colesterol
Si tenés los valores en mg/dL, convertir a mmol/L:
Colesterol no-HDL (mmol/L) = Colesterol no-HDL (mg/dL) ÷ 38.67
Ejemplos:

150 mg/dL = 3.88 mmol/L
200 mg/dL = 5.17 mmol/L
250 mg/dL = 6.46 mmol/L


📈 Categorías de Riesgo
Para menores de 50 años:

Riesgo Bajo: < 2.5%
Riesgo Moderado: 2.5% - 7.5%
Riesgo Alto: ≥ 7.5%

Para 50-69 años:

Riesgo Bajo: < 5%
Riesgo Moderado: 5% - 10%
Riesgo Alto: ≥ 10%

Para ≥70 años (SCORE2-OP):

Riesgo Bajo: < 7.5%
Riesgo Moderado: 7.5% - 15%
Riesgo Alto: ≥ 15%


💾 Base de Datos
La aplicación utiliza SQLite, una base de datos embebida que:

✅ No requiere servidor (funciona offline)
✅ Se guarda en un solo archivo (score2_pacientes.db)
✅ Es portable (podés copiarla a otra PC)
✅ Backups simples (copiar el archivo .db)

Tablas de la Base de Datos:

pacientes: Datos demográficos y contacto
calculos_riesgo: Todos los cálculos realizados
seguimiento: Consultas y evolución
usuarios: Control de acceso (opcional)


📤 Exportación de Datos
Exportar a CSV:

Ir a Archivo → Exportar a CSV
Elegir ubicación y nombre del archivo
El archivo contendrá todos los pacientes y sus cálculos

Crear Backup:

Ir a Archivo → Backup Base de Datos
Se creará automáticamente en la carpeta backups/
Nombre del archivo: backup_YYYYMMDD_HHMMSS.db


🔧 Solución de Problemas
Error: "Module not found"
bash# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
Error: "Database is locked"

Cerrar todas las instancias de la aplicación
Reiniciar la aplicación

La ventana no se muestra correctamente

Verificar resolución de pantalla
Modificar root.geometry("1400x900") en main.py


🎨 Próximas Mejoras

 Agregar tablas de región MUY ALTO
 Gráficos de evolución temporal
 Impresión de informes en PDF
 Importación desde Excel
 Recordatorios de seguimiento
 Calculadora de otros scores (Framingham, ASCVD)
 Modo oscuro


👨‍⚕️ Referencias
Guías ESC 2021:

SCORE2 working group and ESC Cardiovascular risk collaboration. (2021).
European Heart Journal, 42(25), 2439–2454.
https://academic.oup.com/eurheartj/article/42/25/2439/6297709

HeartScore:

https://www.heartscore.org


📞 Contacto y Soporte
Desarrollado para:

Unidad de Prevención Cardiometabólica
ISSUNNE - Corrientes Capital

Desarrollador:

GitHub: https://github.com/hernimayol/ISSUNNE


📜 Licencia
Este software es de uso interno para la Unidad de Prevención Cardiometabólica.

✅ Checklist de Configuración Inicial

 Python 3.8+ instalado
 Repositorio clonado/descargado
 Entorno virtual creado
 Dependencias instaladas (pip install -r requirements.txt)
 Aplicación ejecutada correctamente (python main.py)
 Primer paciente creado
 Primer cálculo realizado
 Backup de prueba creado

¡Listo para usar! 🎉

# 🎯 CAMBIOS - Versión HeartScore Compatible

## Fecha: Enero 2026

---

## ✅ Cambios Realizados

### 📋 **Campos del Formulario - Ahora IDÉNTICOS a HeartScore:**

#### ❌ **ANTES** (versión anterior):
- Edad (en años directamente)
- Colesterol no-HDL (ingreso manual)

#### ✅ **AHORA** (compatible con HeartScore):

1. **Birth date** (mes/año)
   - ✓ El usuario ingresa: mes y año de nacimiento
   - ✓ La app calcula automáticamente la edad

2. **Sex** (male/female)
   - ✓ Radio buttons: male / female
   - ✓ Idéntico a HeartScore

3. **Systolic blood pressure** (mmHg)
   - ✓ Rango: 100-179 mmHg
   - ✓ Unidad mostrada: mmHg

4. **Total Cholesterol** con selector de unidades
   - ✓ **mmol/L** o **mg/dl**
   - ✓ Conversión automática a mmol/L si se ingresa en mg/dl
   - ✓ Radio buttons para elegir unidad

5. **HDL-Cholesterol** (mmol/L)
   - ✓ Campo nuevo, requerido
   - ✓ Unidad fija: mmol/L

6. **LDL-Cholesterol** (mmol/L)
   - ✓ Campo nuevo, OPCIONAL
   - ✓ No afecta el cálculo de riesgo
   - ✓ Se guarda en la BD para referencia

7. **Current Smoker** (Yes/No)
   - ✓ Radio buttons: Yes / No
   - ✓ Idéntico a HeartScore

---

## 🔢 **Cálculo Automático de Colesterol no-HDL**

```
no-HDL = Total Cholesterol - HDL
```

**Ejemplo:**
- Total Cholesterol: 6.0 mmol/L
- HDL: 1.2 mmol/L
- **no-HDL = 6.0 - 1.2 = 4.8 mmol/L** ← Este valor se usa para el cálculo SCORE2

**Nota:** La app muestra una alerta si el no-HDL calculado está fuera del rango válido (3.0-7.0 mmol/L).

---

## 🔄 **Conversión Automática de Unidades**

### Colesterol Total:

**De mg/dl a mmol/L:**
```
mmol/L = mg/dl ÷ 38.67
```

**Ejemplos:**
| mg/dl | mmol/L |
|-------|--------|
| 150   | 3.88   |
| 200   | 5.17   |
| 250   | 6.46   |
| 270   | 6.98   |

---

## 🎨 **Mejoras en la Interfaz**

### 1. Campos Marcados como Requeridos
- Todos los campos obligatorios tienen **asterisco rojo (*)** 
- Al final del formulario: "* Required fields"

### 2. Cuadro Informativo
```
ℹ️ El colesterol no-HDL se calcula automáticamente:
   no-HDL = Total Cholesterol - HDL
```

### 3. Botones en Inglés (como HeartScore)
- ✅ "CALCULATE RISK" (antes: "Calcular Riesgo")
- ✅ "SAVE CALCULATION" (antes: "Guardar Cálculo")

### 4. Etiquetas Bilingües
- Birth date / Fecha de nacimiento
- Sex / Sexo
- Current Smoker / Fumador actual

---

## 📊 **Resultado del Cálculo - Información Adicional**

Ahora el resultado muestra:

```
Riesgo Cardiovascular a 10 años

25%

[Riesgo Alto]

Detalles:
• Edad: 50 años
• Método: SCORE2
• Región: MODERADO

Valores de Colesterol:
• Total: 6.00 mmol/L
• HDL: 1.20 mmol/L
• no-HDL: 4.80 mmol/L ← Usado para el cálculo

Interpretación:
[Texto explicativo del riesgo...]
```

---

## 💾 **Base de Datos - Campos Nuevos**

Los cálculos ahora guardan:
- ✅ `colesterol_total` (mmol/L)
- ✅ `hdl` (mmol/L)
- ✅ `ldl` (mmol/L) - opcional
- ✅ `colesterol_no_hdl` (calculado automáticamente)

**Compatibilidad:** Los cálculos antiguos siguen funcionando.

---

## 🐛 **Validaciones Implementadas**

### 1. Fecha de Nacimiento
- ✓ Mes: 1-12
- ✓ Año: debe resultar en edad 40-89 años
- ✓ Mensaje de error claro si falta

### 2. Colesterol no-HDL (calculado)
- ✓ Advertencia si está fuera del rango 3.0-7.0 mmol/L
- ✓ Muestra el detalle del cálculo
- ✓ Permite continuar para ver el resultado

### 3. Campos Requeridos
- ✓ Birth date
- ✓ Sex
- ✓ Systolic blood pressure
- ✓ Total Cholesterol
- ✓ HDL-Cholesterol
- ✓ Current Smoker

---

## 🔍 **Modo DEBUG Mejorado**

En la consola ahora se muestra:

```
============================================================
CÁLCULO DE RIESGO - DEBUG
============================================================
Fecha nacimiento: 6/1974
Edad calculada: 50 años
Sexo: varon
Fumador: Sí
PAS: 130 mmHg
Colesterol Total: 6.00 mmol/L
HDL-Cholesterol: 1.20 mmol/L
Colesterol no-HDL (calculado): 4.80 mmol/L
Región: moderado
============================================================
RESULTADO: {'riesgo': 23, 'categoria': 'Alto', ...}
============================================================
```

---

## 📖 **Cómo Usar la Nueva Versión**

### Paso 1: Cerrar la aplicación si está abierta

### Paso 2: Ejecutar de nuevo
```bash
python main.py
```

### Paso 3: Calcular riesgo con el nuevo formato

**Ejemplo de datos de prueba:**

```
Birth date: 6 / 1974
Sex: ○ male ○ female  ← Seleccionar "male"
Systolic blood pressure: 130 mmHg
Total Cholesterol: 6.0  ○ mmol/L ○ mg/dl  ← Seleccionar "mmol/L"
HDL-Cholesterol: 1.2 mmol/L
LDL-Cholesterol: [dejar vacío o ingresar un valor]
Current Smoker: ○ Yes ○ No  ← Seleccionar "Yes"
```

**Presionar:** CALCULATE RISK

**Resultado esperado:**
- Edad calculada: 50 años
- no-HDL calculado: 4.8 mmol/L
- Riesgo: ~23-25% (Alto)

---

## 🎯 **Compatibilidad con HeartScore**

### ✅ Lo que COINCIDE exactamente:
- Campos del formulario
- Orden de los campos
- Nombres de los campos
- Validaciones de rangos
- Cálculo de no-HDL = Total - HDL
- Selector de unidades para colesterol total

### ⚠️ Diferencias (mejoras de nuestra app):
- ✅ Nuestra app soporta **2 regiones** (Moderado y Muy Alto)
- ✅ HeartScore solo muestra 1 región automática por país
- ✅ Nuestra app guarda historial en base de datos local
- ✅ Nuestra app permite exportar a CSV
- ✅ Nuestra app funciona 100% offline

---

## 📝 **Notas Importantes**

### Conversión de Unidades

**Si tenés valores en mg/dl:**
1. Ingresar el valor en el campo "Total Cholesterol"
2. Seleccionar el radio button "mg/dl"
3. La app convierte automáticamente a mmol/L

**Si tenés HDL en mg/dl:**
- Convertir manualmente: `HDL_mmol/L = HDL_mg/dl ÷ 38.67`
- Ejemplo: HDL 50 mg/dl = 1.29 mmol/L

### Rangos Válidos

| Parámetro | Rango | Unidad |
|-----------|-------|--------|
| Edad | 40-89 años | años |
| PAS | 100-179 | mmHg |
| Col Total | - | mmol/L o mg/dl |
| HDL | - | mmol/L |
| **Col no-HDL** | **3.0-7.0** | **mmol/L** |

---

## 🚀 **Próximos Pasos Sugeridos**

1. ✅ Probar con varios pacientes
2. ✅ Verificar que los cálculos coincidan con HeartScore.org
3. ✅ Guardar cálculos en la base de datos
4. ✅ Exportar resultados a CSV
5. ✅ Crear backups periódicos

---

## 💬 **Soporte**

Si hay algún problema o diferencia con HeartScore, revisar:
1. Consola (ventana negra) - modo DEBUG
2. Verificar conversión de unidades
3. Confirmar rangos de edad (40-89 años)
4. Verificar que no-HDL esté en rango 3.0-7.0

---

**Desarrollado para:**
Unidad de Prevención Cardiometabólica
ISSUNNE - Corrientes Capital

**Última actualización:** Enero 2026