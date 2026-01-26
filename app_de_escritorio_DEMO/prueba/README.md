# 🏥 SCORE2 - Calculadora de Riesgo Cardiovascular

**Aplicación de escritorio para evaluación de riesgo cardiovascular basada en las Guías ESC 2021**

Desarrollado para la **Unidad de Prevención Cardiometabólica - ISSUNNE Corrientes Capital**

---

## 📋 Descripción

Sistema completo de gestión y cálculo de riesgo cardiovascular que implementa los algoritmos **SCORE2** (40-69 años) y **SCORE2-OP** (70-89 años) según las guías de la Sociedad Europea de Cardiología (ESC) 2021.

### ✨ Características Principales

- ✅ **Cálculo automático de riesgo cardiovascular** a 10 años
- 📊 **Dos algoritmos integrados**: SCORE2 y SCORE2-OP
- 🌍 **Regiones de riesgo**: Moderado y Muy Alto (Argentina: Moderado)
- 👥 **Gestión completa de pacientes** con base de datos SQLite
- 📈 **Historial de evaluaciones** con seguimiento temporal
- 📄 **Exportación a PDF** con reportes profesionales
- 💾 **Sistema de backup** automático de base de datos
- 🔍 **Búsqueda y filtrado** de pacientes
- 📊 **Dashboard de estadísticas** generales

---

## 🆕 Actualización Importante - Unidades de Colesterol

**VERSIÓN ACTUAL: Solo mg/dl**

La aplicación ahora trabaja exclusivamente con **mg/dl** para todos los valores de colesterol, según requerimientos médicos:

- ✅ Colesterol Total: **mg/dl**
- ✅ HDL-Cholesterol: **mg/dl**
- ✅ LDL-Cholesterol: **mg/dl**
- ✅ Colesterol no-HDL: **mg/dl** (calculado automáticamente)

**Conversión interna:** El sistema convierte automáticamente a mmol/L para los cálculos con las tablas SCORE2, pero toda la interfaz y reportes muestran valores en mg/dl.

**Fórmula de conversión:** `mmol/L = mg/dl / 38.67`

---

## 🖥️ Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo:** Windows 10/11, Linux, macOS
- **Python:** 3.8 o superior
- **RAM:** 2 GB mínimo
- **Espacio en disco:** 50 MB

### Dependencias Python
```
tkinter (incluido con Python)
sqlite3 (incluido con Python)
reportlab (para exportación PDF)
```

---

## 📦 Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/hernimayol/ISSUNNE.git
cd ISSUNNE/app_de_escritorio_DEMO/prueba
```

### 2. Instalar dependencias

```bash
pip install reportlab
```

### 3. Estructura de archivos

Asegúrate de tener estos archivos en la misma carpeta:

```
prueba/
├── main.py                    # Aplicación principal
├── database.py                # Gestor de base de datos
├── tablas_score2.py          # Tablas SCORE2/SCORE2-OP
├── score2_pacientes.db       # Base de datos (se crea automáticamente)
└── README.md                 # Este archivo
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

---

## 📖 Guía de Uso

### 1️⃣ **Agregar un Nuevo Paciente**

1. Haz clic en **"➕ Nuevo Paciente"** o ve a **Archivo → Nuevo Paciente**
2. Completa los datos obligatorios (marcados con *)
3. Haz clic en **"Guardar"**

### 2️⃣ **Calcular Riesgo Cardiovascular**

1. Selecciona un paciente del desplegable
2. Completa los datos requeridos:
   - **Fecha de nacimiento** (mes/año)
   - **Sexo**
   - **Presión Arterial Sistólica** (mmHg)
   - **Colesterol Total** (mg/dl)
   - **HDL-Cholesterol** (mg/dl)
   - **¿Fumador activo?** (Sí/No)
   - **Región de Riesgo** (usar MODERADO para Argentina)

3. Haz clic en **"📊 CALCULAR RIESGO"**
4. Revisa los resultados en el panel derecho
5. Haz clic en **"💾 GUARDAR CÁLCULO"** para almacenar la evaluación

### 3️⃣ **Ver Historial de Paciente**

1. Ve a la pestaña **"👥 Pacientes"**
2. Selecciona un paciente de la lista
3. Haz clic en **"Ver Detalles"** para ver información completa
4. Haz clic en **"📄 Exportar PDF"** para generar un reporte

### 4️⃣ **Exportar Reporte PDF**

El reporte incluye:
- ✅ Datos personales del paciente
- ✅ Historial completo de evaluaciones
- ✅ Interpretación del último cálculo
- ✅ Recomendaciones personalizadas
- ✅ Formato profesional con tablas y gráficos

---

## 🔬 Metodología SCORE2/SCORE2-OP

### Algoritmo SCORE2 (40-69 años)

Calcula el riesgo de eventos cardiovasculares mortales y no mortales a 10 años basándose en:
- Edad
- Sexo
- Hábito tabáquico
- Presión arterial sistólica
- Colesterol no-HDL

### Algoritmo SCORE2-OP (70-89 años)

Versión optimizada para personas mayores con los mismos parámetros.

### Categorías de Riesgo

| Edad      | Bajo      | Moderado   | Alto       |
|-----------|-----------|------------|------------|
| < 50 años | < 2.5%    | 2.5-7.5%   | ≥ 7.5%     |
| 50-69 años| < 5%      | 5-10%      | ≥ 10%      |
| ≥ 70 años | < 7.5%    | 7.5-15%    | ≥ 15%      |

### Regiones de Riesgo

- **MODERADO**: Argentina, Uruguay, Chile (usado por defecto)
- **MUY ALTO**: Europa del Este, Asia Central

---

## 📊 Cálculo del Colesterol no-HDL

El colesterol no-HDL se calcula automáticamente:

```
no-HDL = Colesterol Total - HDL-Cholesterol
```

**Ejemplo:**
- Colesterol Total: 160 mg/dl
- HDL: 45 mg/dl
- **no-HDL = 115 mg/dl**

**Rango estándar:** 116-271 mg/dl (3.0-7.0 mmol/L)

**Nota:** La aplicación permite valores fuera de rango usando extrapolación, similar a HeartScore.

---

## 💾 Base de Datos

### Tablas Principales

1. **pacientes**: Información demográfica y contacto
2. **calculos_riesgo**: Evaluaciones de riesgo con todos los parámetros
3. **seguimiento**: Consultas y evolución del paciente
4. **usuarios**: Control de acceso (futuro)

### Backup Automático

- Los backups se guardan en la carpeta `backups/`
- Formato: `backup_YYYYMMDD_HHMMSS.db`
- Se recomienda hacer backup antes de actualizaciones importantes

---

## 🔒 Seguridad y Privacidad

- ✅ **Datos locales**: Toda la información se almacena localmente
- ✅ **Sin conexión a internet**: No se envían datos a servidores externos
- ✅ **Eliminación lógica**: Los pacientes se pueden ocultar sin borrar historial
- ✅ **Backup completo**: Sistema de respaldo de base de datos

---

## 🐛 Solución de Problemas

### La aplicación no inicia

**Solución:**
```bash
# Verificar versión de Python
python --version

# Reinstalar dependencias
pip install --upgrade reportlab
```

### Error: "No se puede calcular el riesgo"

**Posibles causas:**
1. **Edad fuera de rango**: Debe estar entre 40-89 años
2. **Campos vacíos**: Todos los campos obligatorios (*) deben completarse
3. **Valores no numéricos**: Verifica que los números sean válidos

### Error: "Colesterol no-HDL fuera de rango"

**Solución:** Este es solo un warning. El cálculo se realizará usando extrapolación. Los valores muy bajos o muy altos pueden no ser precisos.

### No se genera el PDF

**Solución:**
```bash
# Instalar o reinstalar reportlab
pip install reportlab

# Si persiste el error
pip uninstall reportlab
pip install reportlab
```

---

## 📚 Referencias

### Guías y Publicaciones

1. **SCORE2 working group and ESC Cardiovascular risk collaboration**
   - *SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe*
   - European Heart Journal (2021) 42, 2439–2454
   - DOI: [10.1093/eurheartj/ehab309](https://doi.org/10.1093/eurheartj/ehab309)

2. **SCORE2-OP working group and ESC Cardiovascular risk collaboration**
   - *SCORE2-OP risk prediction algorithms: estimating incident cardiovascular event risk in older persons in four geographical risk regions*
   - European Heart Journal (2021) 42, 2455–2467
   - DOI: [10.1093/eurheartj/ehab312](https://doi.org/10.1093/eurheartj/ehab312)

3. **ESC Guidelines on cardiovascular disease prevention in clinical practice (2021)**
   - European Heart Journal (2021) 42, 3227–3337
   - DOI: [10.1093/eurheartj/ehab484](https://doi.org/10.1093/eurheartj/ehab484)

### Herramientas Online

- **HeartScore®**: [https://www.heartscore.org](https://www.heartscore.org)
- **ESC Guidelines**: [https://www.escardio.org/Guidelines](https://www.escardio.org/Guidelines)

---

## 🔄 Historial de Versiones

### Versión 1.1 (Enero 2026)
- ✅ **Cambio a mg/dl exclusivamente** para colesterol
- ✅ Conversión automática interna a mmol/L
- ✅ Permitir valores fuera de rango con extrapolación
- ✅ Corrección de deprecation warnings (trace_add)
- ✅ Mejoras en mensajes de advertencia

### Versión 1.0 (Enero 2026)
- ✅ Implementación completa de SCORE2 y SCORE2-OP
- ✅ Gestión de pacientes con base de datos SQLite
- ✅ Exportación a PDF con reportes profesionales
- ✅ Sistema de historial y seguimiento
- ✅ Dashboard de estadísticas
- ✅ Interfaz gráfica con Tkinter

---

## 📞 Soporte y Contacto

### Desarrollador
- **Nombre**: José Hernán Mayol Toledo
- **Institución**: ISSUNNE - Corrientes Capital
- **GitHub**: [hernimayol/ISSUNNE](https://github.com/hernimayol/ISSUNNE)

### Reportar Errores

Si encuentras algún error o tienes sugerencias:
1. Abre un **Issue** en GitHub
2. Incluye:
   - Descripción del problema
   - Pasos para reproducirlo
   - Mensaje de error (si aplica)
   - Versión de Python y sistema operativo

---

## 📄 Licencia

Este software fue desarrollado para uso exclusivo de la **Unidad de Prevención Cardiometabólica - ISSUNNE Corrientes Capital**.

**Uso educativo y de investigación permitido con atribución.**

---

## ⚠️ Disclaimer Médico

**IMPORTANTE:** Esta aplicación es una herramienta de apoyo para profesionales de la salud. 

- ❌ **NO reemplaza el juicio clínico profesional**
- ❌ **NO es para autodiagnóstico**
- ✅ Debe ser usada por personal médico capacitado
- ✅ Los resultados deben interpretarse en contexto clínico completo
- ✅ Basado en guías ESC 2021, pero puede requerir adaptación local

**Las decisiones terapéuticas deben tomarse considerando:**
- Historia clínica completa
- Examen físico
- Factores de riesgo adicionales
- Preferencias del paciente
- Recursos disponibles

---

## 🎯 Roadmap Futuro

### Próximas Características
- [ ] Gráficos de evolución temporal
- [ ] Integración con sistemas HIS/EMR
- [ ] Exportación a otros formatos (Excel, Word)
- [ ] Cálculo de objetivos terapéuticos
- [ ] Sistema de alertas y recordatorios
- [ ] Módulo de seguimiento farmacológico
- [ ] Interfaz multi-idioma (Inglés/Portugués)

---

## 🙏 Agradecimientos

- **Dr. Andrés Duarte** - Supervisión médica y validación clínica
- **ISSUNNE Corrientes** - Soporte institucional
- **ESC (European Society of Cardiology)** - Desarrollo de algoritmos SCORE2
- **Comunidad Python Argentina** - Soporte técnico

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~1,600
- **Archivos principales**: 3 (main.py, database.py, tablas_score2.py)
- **Tablas de datos**: 1,536 valores de riesgo (SCORE2 + SCORE2-OP)
- **Regiones implementadas**: 2 (Moderado y Muy Alto)
- **Rangos de edad**: 40-89 años (50 años de cobertura)

---

## 🔐 Cumplimiento Normativo

Esta aplicación cumple con:
- ✅ **Guías ESC 2021** para prevención cardiovascular
- ✅ **Ley de Protección de Datos Personales** (Argentina)
- ✅ Estándares de **buenas prácticas en desarrollo de software médico**

---

**Última actualización:** Enero 26, 2026

**Versión del documento:** 1.1