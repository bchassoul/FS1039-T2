# 🌌 Simulaciones de Física Espacial - Tarea Programada II

Este proyecto contiene el análisis computacional de una simulación 2D de un disco de acreción y jet protoestelar, implementado usando datos de simulaciones numéricas.

## 📁 Estructura del Proyecto

```
FS1039-T2/
├── src/                    # Código fuente
│   ├── config.py           # Constantes físicas y configuraciones
│   └── utils.py            # Funciones utilitarias para análisis
├── notebooks/              # Jupyter Notebooks para análisis
│   └── analysis.ipynb      # Análisis completo de la simulación
├── data/                   # Datos de entrada
│   ├── v_r.npy             # Velocidad radial [cm/s]
│   ├── rho.npy             # Densidad [g/cm³]
│   ├── Pgrad_r.npy         # Gradiente de presión térmica [dyn/cm³]
│   ├── PBgrad_r.npy        # Gradiente de presión magnética [dyn/cm³]
│   ├── x.npy               # Posiciones en x [au]
│   ├── z.npy               # Posiciones en z [au]
│   └── table.txt           # Tabla temporal con evolución del sistema
├── results/                # Resultados generados
│   └── analysis.html       # Notebook exportado a HTML
├── requirements.txt        # Dependencias
└── README.md
```

## 🚀 Instalación y Uso

### 📋 Prerrequisitos (Ejecutar una vez)
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 🎯 Opciones de Ejecución

#### Opción 1: Análisis interactivo con Jupyter Notebooks (Recomendado)
```bash
# Abrir notebook interactivo
cd notebooks
jupyter notebook analysis.ipynb

# O usar JupyterLab
jupyter lab
```

#### Opción 2: Exportar notebook a HTML
```bash
# Exportar a HTML (recomendado para visualización)
jupyter nbconvert --to html notebooks/analysis.ipynb --output-dir results/

# El archivo HTML se generará en results/analysis.html
```

## 📊 Análisis Realizado

El notebook `analysis.ipynb` contiene el análisis completo de la simulación, dividido en cuatro problemas principales:

### 🔵 Problema 1: Velocidad radial
- 1.1: Visualización de la velocidad radial en km/s usando `pcolormesh` con colormap `seismic_r`
- 1.2: Identificación de tres regiones principales:
  - Jet
  - Disco de acreción
  - Infall
- Estadísticas: Cálculo de área porcentual y estadísticas de velocidad para cada región

### 🟢 Problema 2: Densidad
- 2.1: Visualización del logaritmo en base 10 de la densidad
- 2.2: Identificación de densidades típicas del jet y disco de acreción

### 🟠 Problema 3: Gradiente de presión vs gravedad
- 3.1: Cálculo de la fuerza gravitacional por unidad de volumen (F_g = GM*ρ/r²)
- 3.2: Visualización de razones presión/gravedad:
  - Razón térmica: (∂P/∂r) / F_g
  - Razón magnética: (∂P_B/∂r) / F_g

### 🟣 Problema 4: Evolución temporal
- Análisis: Evolución de masa, tasa de acreción y luminosidades

## 👀 Resultados

Los resultados se generan automáticamente en la carpeta `results/`:

- 📓 Notebook HTML: `results/analysis.html` - Análisis completo exportado para fácil visualización
- 📊 Gráficas: Visualizaciones interactivas dentro del notebook:
  - Mapas de velocidad radial con identificación de regiones
  - Mapas de densidad logarítmica
  - Mapas de razones presión/gravedad (térmica y magnética)
  - Evolución temporal de masa, tasas y luminosidades

## 📝 Notas Técnicas

- El código está organizado en módulos reutilizables en `src/`:
  - `config.py`: Constantes físicas (G, M_STAR, conversiones de unidades)
  - `utils.py`: Funciones utilitarias (carga de datos, cálculo de estadísticas, etc.)


---

Autor: Barbara Chassoul  
Curso: UCR, FS1039 - Introducción a la Física Espacial - Tarea Programada II  
Git: [FS1039-T2](https://github.com/bchassoul/FS1039-T2)

