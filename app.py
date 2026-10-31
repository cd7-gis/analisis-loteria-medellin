import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from scipy.stats import poisson
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Lotería de Medellín - Análisis EDA & Poisson",
    page_icon="🎲",
    layout="wide",
)

# Estilos visuales personalizados
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado Principal
st.markdown(
    '<div class="main-title">Análisis Estadístico y Probabilístico del Premio Mayor de la Lotería de Medellín (2007–2026)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Trabajo de Campo - Materia: <b>Estadística General</b> | Autor: <b>Cristian David Cañas Ospina</b></div>',
    unsafe_allow_html=True,
)


# Carga optimizada de la base de datos
@st.cache_data
def cargar_datos():
  ruta = "data/RESULTADOS_PREMIO_MAYOR_LOTERIA_DE_MEDELLIN_20261025.csv"
  df = pd.read_csv(ruta)

  # Formateo técnico de variables
  df["NÚMERO"] = df["NÚMERO"].astype(str).str.zfill(4)
  df["SERIE"] = df["SERIE"].astype(str).str.zfill(3)
  df["FECHA DE JUEGO"] = pd.to_datetime(
      df["FECHA DE JUEGO"], dayfirst=True, errors="coerce"
  )
  return df


try:
  df = cargar_datos()
except Exception as e:
  st.error(
      f"Error al cargar la base de datos. Verifica que el archivo CSV esté en la ruta 'data/'. Detalle: {e}"
  )
  st.stop()

# Navegación lateral por pestañas
pestana = st.sidebar.radio(
    "📌 Menú de Navegación",
    [
        "1. Planteamiento & Metodología",
        "2. Exploración & Limpieza (EDA)",
        "3. Estadística Descriptiva",
        "4. Modelo de Probabilidad (Poisson)",
        "5. Simulación & Calculadora",
    ],
)

# ------------------------------------------------------------------------------------------------
# PESTAÑA 1: PLANTEAMIENTO & METODOLOGÍA
# ------------------------------------------------------------------------------------------------
if pestana == "1. Planteamiento & Metodología":
  st.header("📋 Planteamiento del Problema y Objetivos")

  col_a, col_b = st.columns([2, 1])

  with col_a:
    st.markdown("""
        ### Situación Problémica
        Los resultados históricos de los juegos de azar permiten analizar si la distribución de los números ganadores responde a un comportamiento genuinamente aleatorio a lo largo del tiempo. En el caso de la **Lotería de Medellín**, existe la creencia popular de que ciertos números "calientes" tienden a repetirse más de lo normal o que otros "están demorados en salir".
        
        ### Pregunta de Investigación
        > **¿Es compatible la cantidad de números repetidos en el premio mayor de la Lotería de Medellín entre 2007 y 2026 con la que se esperaría si cada sorteo fuera uniforme e independiente?**
        
        ### Objetivos del Proyecto
        * **Objetivo General:** Evaluar si la cantidad de números repetidos en el histórico del premio mayor de la Lotería de Medellín (2007–2026) corresponde a la cantidad esperada en un modelo probabilístico uniforme e independiente.
        * **Objetivos Específicos:**
            1. Identificar la frecuencia histórica de aparición de los números y series ganadoras.
            2. Calcular las frecuencias esperadas mediante la **Distribución de Poisson**.
            3. Comparar estadísticamente las frecuencias observadas en la realidad frente a las esperadas por el modelo.
        """)

  with col_b:
    st.info("""
        **Ficha Técnica del Proyecto**
        * **Fuente de Datos:** Portal Nacional de Datos Abiertos (`datos.gov.co`).
        * **Rango Temporal:** 05 de enero de 2007 – 09 de octubre de 2026.
        * **Total Registros:** 1,024 sorteos analizados.
        * **Espacio Muestral ($N$):** 10,000 combinaciones posibles (`0000` a `9999`).
        * **Herramientas:** Python (`Pandas`, `NumPy`, `Matplotlib`, `Seaborn`, `SciPy`).
        """)

# ------------------------------------------------------------------------------------------------
# PESTAÑA 2: EXPLORACIÓN & LIMPIEZA
# ------------------------------------------------------------------------------------------------
elif pestana == "2. Exploración & Limpieza (EDA)":
  st.header("🧹 Inspección y Limpieza de Datos")

  # Métricas rápidas
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Filas y Columnas", f"{df.shape[0]} × {df.shape[1]}")
  col2.metric("Fechas Inválidas / Nulos", f"{df['FECHA DE JUEGO'].isna().sum()}")
  col3.metric("Fecha Inicial", df["FECHA DE JUEGO"].min().strftime("%Y-%m-%d"))
  col4.metric("Fecha Final", df["FECHA DE JUEGO"].max().strftime("%Y-%m-%d"))

  st.markdown("---")

  col_c, col_d = st.columns([1, 1])

  with col_c:
    st.subheader("Verificación de Formatos y Zfill")
    st.write(
        "Se aplicó `.str.zfill(4)` a los números y `.str.zfill(3)` a las series"
        " para garantizar la longitud correcta:"
    )
    st.dataframe(df[["FECHA DE JUEGO", "SORTEO", "NÚMERO", "SERIE"]].head(10))

  with col_d:
    st.subheader("Sorteos registrados por año")
    registro_year = (
        df["FECHA DE JUEGO"].dt.year.value_counts().sort_index().reset_index()
    )
    registro_year.columns = ["Año", "Cantidad de Sorteos"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.barplot(
        data=registro_year, x="Año", y="Cantidad de Sorteos", palette="Blues_r", ax=ax
    )
    plt.xticks(rotation=45)
    plt.title("Distribución Anual de Sorteos (2007 - 2026)")
    plt.tight_layout()
    st.pyplot(fig)

    st.caption(
        "Nota: Se observan diferencias notables en años como 2020 (45"
        " registros por contingencia sanitaria) y 2026 (41 registros por ser"
        " corte parcial)."
    )

# ------------------------------------------------------------------------------------------------
# # ------------------------------------------------------------------------------------------------
# PESTAÑA 3: ESTADÍSTICA DESCRIPTIVA
# ------------------------------------------------------------------------------------------------
elif pestana == "3. Estadística Descriptiva":
  st.header("📊 Estadística Descriptiva y Frecuencias Observadas")

  frecuencia_numeros = df["NÚMERO"].value_counts()
  frecuencia_serie = df["SERIE"].value_counts()

  col_m1, col_m2, col_m3, col_m4 = st.columns(4)
  col_m1.metric("Total de Sorteos", len(df))
  col_m2.metric("Números Distintos", df["NÚMERO"].nunique())
  col_m3.metric("Series Distintas", df["SERIE"].nunique())
  col_m4.metric("Máxima Frecuencia (Número)", f"{frecuencia_numeros.max()} veces")

  st.markdown("---")

  col_top1, col_top2 = st.columns(2)

  with col_top1:
    st.subheader("Top 10 Números Más Frecuentes")
    top_10_num = frecuencia_numeros.head(10).reset_index()
    top_10_num.columns = ["Número", "Frecuencia"]

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=top_10_num, x="Número", y="Frecuencia", palette="viridis", ax=ax1
    )
    for p in ax1.patches:
      ax1.annotate(
          f"{int(p.get_height())}",
          (p.get_x() + p.get_width() / 2.0, p.get_height()),
          ha="center",
          va="center",
          xytext=(0, 5),
          textcoords="offset points",
      )
    plt.title("10 Números Ganadores más Frecuentes")
    st.pyplot(fig1)
    st.write(
        "**Números con 3 apariciones:** `0539`, `0169` y `2570`."
    )

  with col_top2:
    st.subheader("Top 10 Series Más Frecuentes")
    top_10_ser = frecuencia_serie.head(10).reset_index()
    top_10_ser.columns = ["Serie", "Frecuencia"]

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=top_10_ser, x="Serie", y="Frecuencia", palette="magma", ax=ax2
    )
    for p in ax2.patches:
      ax2.annotate(
          f"{int(p.get_height())}",
          (p.get_x() + p.get_width() / 2.0, p.get_height()),
          ha="center",
          va="center",
          xytext=(0, 5),
          textcoords="offset points",
      )
    plt.title("10 Series Ganadoras más Frecuentes")
    st.pyplot(fig2)
    st.write("**Serie más frecuente:** `053` con 10 apariciones.")

  st.markdown("---")

  st.subheader("Distribución de Frecuencia de Repetición de Números")

  # Corrección aplicada aquí con name= y renombrado de columnas
  distribucion = (
      frecuencia_numeros.value_counts()
      .sort_index()
      .reset_index(name="Cantidad de números")
  )
  distribucion.columns = [
      "Veces que apareció el número",
      "Cantidad de números distintos",
  ]

  col_t, col_g = st.columns([1, 2])

  with col_t:
    st.dataframe(distribucion, use_container_width=True)
    st.markdown("""
        * **903 números** aparecieron **1 sola vez**.
        * **56 números** aparecieron **2 veces**.
        * **3 números** aparecieron **3 veces**.
        """)

  with col_g:
    fig3, ax3 = plt.subplots(figsize=(8, 3.5))
    sns.barplot(
        data=distribucion,
        x="Veces que apareció el número",
        y="Cantidad de números distintos",
        palette="crest",
        ax=ax3,
    )
    plt.title("Distribución de la Frecuencia Histórica de Números")
    st.pyplot(fig3)

# ------------------------------------------------------------------------------------------------
## ------------------------------------------------------------------------------------------------
# PESTAÑA 4: MODELO DE POISSON
# ------------------------------------------------------------------------------------------------
elif pestana == "4. Modelo de Probabilidad (Poisson)":
  st.header("🎲 Modelado Probabilístico con Distribución de Poisson")

  st.markdown("""
    Al ser cada sorteo un evento independiente con una probabilidad de éxito muy pequeña ($p = 1/10000 = 0.0001$) y un gran número de experimentos ($n = 1024$), la distribución adecuada para modelar la frecuencia de apariciones de cada número es la **Distribución de Poisson**:
    
    $$P(X = k) = \\frac{e^{-\\lambda} \\cdot \\lambda^k}{k!}$$
    
    donde el parámetro $\\lambda$ (tasa media esperada) se calcula como $\\lambda = n \\cdot p = 1024 \\times 0.0001 = 0.1024$.
    """)

  n_sorteos = len(df)
  n_opcion = 10000
  lambd = n_sorteos * (1 / n_opcion)

  frecuencia_numeros = df["NÚMERO"].value_counts()

  # Construcción de la Tabla Comparativa
  resultados = []
  for k in range(4):
    if k == 0:
      observados = n_opcion - len(frecuencia_numeros)
    else:
      observados = frecuencia_numeros.value_counts().get(k, 0)

    prob_k = poisson.pmf(k, mu=lambd)
    esperados = prob_k * n_opcion

    resultados.append({
        "Apariciones (k)": k,
        "Observados (Realidad)": observados,
        "Probabilidad Poisson": round(prob_k, 4),
        "Esperados (Teórico)": round(esperados, 4),
        "Diferencia": round(observados - esperados, 4),
    })

  tabla_comparativa = pd.DataFrame(resultados)

  st.subheader("Tabla Comparativa: Valores Observados vs. Esperados por Poisson")
  st.table(tabla_comparativa)

  # Gráfico comparativo de barras
  tabla_grafica = tabla_comparativa.melt(
      id_vars="Apariciones (k)",
      value_vars=["Observados (Realidad)", "Esperados (Teórico)"],
      var_name="Tipo de Dato",
      value_name="Cantidad de Combinaciones",
  )

  fig4, ax4 = plt.subplots(figsize=(9, 4.5))
  sns.barplot(
      data=tabla_grafica,
      x="Apariciones (k)",
      y="Cantidad de Combinaciones",
      hue="Tipo de Dato",
      palette=["#2563EB", "#F59E0B"],
      ax=ax4,
  )
  plt.title("Comparativa: Distribución Observada vs. Modelo de Poisson")
  plt.xlabel("Número de Apariciones (k)")
  plt.ylabel("Cantidad de Combinaciones de 4 Dígitos")
  st.pyplot(fig4)

  st.success(
      "Conclusión: Los resultados históricos de la Lotería de Medellín se"
      " ajustan de manera notable al modelo teórico de Poisson. Esto demuestra"
      " estadísticamente que el sistema de sorteos opera bajo un comportamiento"
      " completamente aleatorio e independiente."
  )

# ------------------------------------------------------------------------------------------------
# PESTAÑA 5: SIMULACIÓN & CALCULADORA
# ------------------------------------------------------------------------------------------------
elif pestana == "5. Simulación & Calculadora":
  st.header("🔍 Buscador y Calculadora de Probabilidad de Números")

  st.write(
      "Ingresa cualquier número de 4 dígitos para consultar sus estadísticas"
      " históricas y teóricas:"
  )

  num_buscar = st.text_input(
      "Ingresa el número (ejemplo: 0539, 1234, 0000):", value="0539"
  )
  num_formatted = num_buscar.zfill(4)

  if len(num_formatted) == 4 and num_formatted.isdigit():
    conteo = df[df["NÚMERO"] == num_formatted]
    veces = len(conteo)

    col_res1, col_res2 = st.columns(2)

    with col_res1:
      st.metric("Apariciones Históricas en 1,024 sorteos", f"{veces} veces")
      if veces > 0:
        st.write("**Fechas en las que salió ganador:**")
        st.dataframe(conteo[["FECHA DE JUEGO", "SORTEO", "SERIE"]])
      else:
        st.info("Este número **nunca** ha salido ganador del premio mayor.")

    with col_res2:
      prob_1_sorteo = (1 / 10000) * 100
      prob_poisson_k = poisson.pmf(veces, mu=0.1024) * 100
      st.markdown(f"""
            **Estadísticas de Probabilidad:**
            * Probabilidad de ganar en 1 sorteo individual: **{prob_1_sorteo:.4f}%**
            * Probabilidad de salir exactamente **{veces} veces** en 1,024 sorteos (Poisson): **{prob_poisson_k:.4f}%**
            * Probabilidad de que salga en el **próximo sorteo**: **0.01%** (¡El azar no tiene memoria!).
            """)
  else:
    st.error("Por favor ingresa un número válido de hasta 4 dígitos.")