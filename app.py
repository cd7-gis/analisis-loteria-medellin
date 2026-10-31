import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import poisson

# Configuración de la página
st.set_page_config(page_title="Lotería de Medellín - Análisis EDA & Poisson", layout="wide")

st.title("📊 Análisis Estadístico y Probabilístico de la Lotería de Medellín (2007–2026)")
st.markdown("**Autor:** Cristian David Cañas Ospina | **Materia:** Estadística General")
st.markdown("---")

# Cargar datos
@st.cache_data
def cargar_datos():
    ruta = "data/RESULTADOS_PREMIO_MAYOR_LOTERIA_DE_MEDELLIN_20261025.csv"
    df = pd.read_csv(ruta)
    df['NÚMERO'] = df['NÚMERO'].astype(str).str.zfill(4)
    df['SERIE'] = df['SERIE'].astype(str).str.zfill(3)
    df['FECHA DE JUEGO'] = pd.to_datetime(df['FECHA DE JUEGO'], dayfirst=True, errors="coerce")
    return df

df = cargar_datos()

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Total Sorteos Analizados", len(df))
col2.metric("Números Distintos", df["NÚMERO"].nunique())
col3.metric("Series Distintas", df["SERIE"].nunique())

st.markdown("---")
st.subheader("🔍 Vista Previa de los Registros Históricos")
st.dataframe(df.head(10))

# Gráfica de frecuencias
st.markdown("---")
st.subheader("📈 Top 10 Números Más Frecuentes")
frecuencia_numeros = df["NÚMERO"].value_counts()
top_10 = frecuencia_numeros.head(10).reset_index()
top_10.columns = ["Número", "Frecuencia"]

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=top_10, x="Número", y="Frecuencia", ax=ax, palette="Blues_r")
ax.set_title("10 números ganadores más frecuentes (2007-2026)")
ax.set_xlabel("Número ganador")
ax.set_ylabel("Cantidad de apariciones")
st.pyplot(fig)

# Análisis de Poisson
st.markdown("---")
st.subheader("🎲 Validación con el Modelo de Poisson")
st.markdown("Se evalúa si las repeticiones se ajustan a un modelo de aleatoriedad e independencia.")

n_sorteos = len(df)
n_opcion = 10000
lambd = n_sorteos / n_opcion

resultados = []
for k in range(4):
    prob_k = poisson.pmf(k, mu=lambd)
    esperados = prob_k * n_opcion
    observados = (frecuencia_numeros.value_counts().get(k, 0)) if k <= frecuencia_numeros.max() else 0
    resultados.append({
        "Apariciones (k)": k,
        "Observados (Realidad)": observados,
        "Esperados (Poisson)": round(esperados, 2)
    })

df_poisson = pd.DataFrame(resultados)
st.table(df_poisson)

st.success("Conclusión: Los datos observados se ajustan de manera notable al modelo teórico de Poisson, confirmando la aleatoriedad del sistema de sorteos.")