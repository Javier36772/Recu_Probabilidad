import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import trim_mean, gmean

# Configuración inicial de la app
st.title("Calculadora Estadística y Gráfica")

# Cargar archivo Excel
archivo = st.file_uploader("Sube un archivo Excel", type=["xlsx"])

if archivo:
    # Leer el archivo
    try:
        datos_excel = pd.read_excel(archivo)
        st.write("Vista previa de los datos cargados:")
        st.dataframe(datos_excel)

        # Seleccionar columna de datos
        columna = st.selectbox("Selecciona la columna que contiene los datos:", datos_excel.columns)
        datos = datos_excel[columna].dropna().tolist()

        # Detección automática del tipo de datos
        if all(isinstance(d, str) for d in datos):  # Verificar si son cadenas de texto
            tipo_datos = "Datos Cualitativos"
        elif all(isinstance(d, (int, float)) for d in datos):  # Verificar si son números
            tipo_datos = "Datos Cuantitativos No Agrupados"
        else:
            tipo_datos = "Datos Mixtos o No Identificados"

        st.write(f"Tipo de datos detectado: {tipo_datos}")

        # Análisis según el tipo de datos
        if tipo_datos == "Datos Cualitativos":
            st.header("Análisis de Datos Cualitativos")
            frecuencias = pd.Series(datos).value_counts()
            categorias = frecuencias.index.tolist()
            valores = frecuencias.values.tolist()

            # Calcular moda
            moda_cualitativa = categorias[np.argmax(valores)]
            st.write(f"Moda: {moda_cualitativa}")

            # Tabla de frecuencias
            tabla_cualitativa = pd.DataFrame({"Categorías": categorias, "Frecuencias": valores})
            st.write("Tabla de Datos:")
            st.dataframe(tabla_cualitativa)

            # Gráficos
            st.write("Gráfico Circular:")
            fig1, ax1 = plt.subplots()
            ax1.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90)
            ax1.axis("equal")
            st.pyplot(fig1)

            st.write("Histograma:")
            fig2, ax2 = plt.subplots()
            ax2.bar(categorias, valores)
            ax2.set_xlabel("Categorías")
            ax2.set_ylabel("Frecuencias")
            st.pyplot(fig2)

        elif tipo_datos == "Datos Cuantitativos No Agrupados":
            st.header("Análisis de Datos Cuantitativos No Agrupados")
            datos = list(map(float, datos))  # Asegurar que son números

            # Calcular estadísticas
            estadisticas = {
                "Cantidad de datos": len(datos),
                "Media aritmética": np.mean(datos),
                "Media geométrica": gmean(datos),
                "Media recortada (10%)": trim_mean(datos, 0.1),
                "Mediana": np.median(datos),
                "Moda": max(set(datos), key=datos.count),
                "Mínimo": np.min(datos),
                "Máximo": np.max(datos),
                "Rango": np.max(datos) - np.min(datos),
                "Varianza poblacional": np.var(datos),
                "Varianza muestral": np.var(datos, ddof=1),
            }
            st.write("Estadísticas Calculadas:")
            st.json(estadisticas)

            # Tabla de frecuencias
            tabla_frecuencias = pd.Series(datos).value_counts().sort_index()
            st.write("Tabla de Frecuencias:")
            st.dataframe(tabla_frecuencias)

            # Gráficos
            st.write("Histograma:")
            fig1, ax1 = plt.subplots()
            ax1.hist(datos, bins="auto", alpha=0.7, rwidth=0.85)
            ax1.set_xlabel("Datos")
            ax1.set_ylabel("Frecuencias")
            st.pyplot(fig1)

            st.write("Ojiva (Frecuencias Acumuladas):")
            frecuencias_acumuladas = np.cumsum(tabla_frecuencias.values)
            fig2, ax2 = plt.subplots()
            ax2.plot(tabla_frecuencias.index, frecuencias_acumuladas, marker="o", linestyle="-")
            ax2.set_xlabel("Datos")
            ax2.set_ylabel("Frecuencias Acumuladas")
            st.pyplot(fig2)

            st.write("Gráfico Circular:")
            fig3, ax3 = plt.subplots()
            ax3.pie(tabla_frecuencias.values, labels=tabla_frecuencias.index, autopct="%1.1f%%", startangle=90)
            ax3.axis("equal")
            st.pyplot(fig3)

        else:
            st.write("Actualmente no soportamos datos mixtos o no identificados.")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

else:
    st.info("Sube un archivo Excel para comenzar.")