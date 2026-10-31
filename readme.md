
# Análisis Estadístico y Probabilístico del Premio Mayor de la Lotería de Medellín (2007–2026)

<p align="center">
  <img src="imagenes/Dise%C3%B1o%20sin%20t%C3%ADtulo.png" alt="Banner del Proyecto" width="700"/>
</p>
<sub>Imagen generada con Ai</sub>


**Materia:** Estadística General  
**Autor:** Cristian David Cañas Ospina  
**Perfil de GitHub:** [cd7-gis](https://github.com/cd7-gis)  

---
## 📌 Descripción del Proyecto
Este proyecto consiste en un Análisis Exploratorio de Datos (EDA) y un estudio de modelado probabilístico aplicado a los registros históricos del premio mayor de la **Lotería de Medellín**[cite: 1], abarcando un periodo de casi 20 años (desde el 5 de enero de 2007 hasta el 9 de octubre de 2026). El objetivo principal es evaluar si la repetición de números ganadores a lo largo del tiempo responde a un comportamiento compatible con un sistema de sorteos completamente aleatorio, uniforme e independiente.

## 📌 1. Planteamiento del Problema
En los juegos de azar independientes, existe la inquietud de evaluar si la repetición histórica de ciertas combinaciones ganadoras se debe a sesgos en el sistema o al comportamiento normal de la aleatoriedad. 

### Pregunta de Investigación
¿Es compatible la cantidad de números repetidos en el premio mayor de la Lotería de Medellín entre 2007 y 2026 con la frecuencia esperada bajo un modelo probabilístico uniforme e independiente?

---

## 🎯 2. Objetivos

### Objetivo General
Evaluar la compatibilidad estadística de las repeticiones observadas en los números ganadores del premio mayor de la Lotería de Medellín (2007–2026) frente a un modelo probabilístico de Poisson.

### Objetivos Específicos
1. Procesar y explorar la base de datos histórica mediante **Python** y **Pandas**.
2. Identificar la frecuencia de aparición de números y series ganadoras durante el periodo 2007–2026.
3. Modelar las frecuencias esperadas utilizando la **Distribución de Poisson** ($\lambda = n \cdot p$).
4. Comparar las frecuencias observadas frente a las teóricas para contrastar la hipótesis de independencia y aleatoriedad.

---

## 🛠️ 3. Metodología y Estructura de Datos

* **Población / Espacio Muestral:** $10,000$ números posibles (`0000` al `9999`).
* **Muestra:** $1,024$ sorteos históricos analizados entre el 05/01/2007 y el 09/10/2026.
* **Fuente de datos:** [Portal Nacional de Datos Abiertos (datos.gov.co)](https://www.datos.gov.co/Comercio-Industria-y-Turismo/RESULTADOS-PREMIO-MAYOR-LOTERIA-DE-MEDELLIN/4w3i-wxax/about_data).
* **Herramientas:** Python (Pandas, NumPy, Matplotlib, Seaborn, SciPy).

### Estructura del Repositorio
```text
analisis-loteria-medellin/
│
├── data/
│   └── RESULTADOS_PREMIO_MAYOR_LOTERIA_DE_MEDELLIN_20261025.csv
│
├── imagenes/
│   └── Diseño sin título.png
│
├── analisis_loteria_medellin.ipynb
├── requirements.txt
├── .gitignore
└── readme.md

Autor: Cristian David Cañas Ospina

[GitHub](https://github.com/cd7-gis)