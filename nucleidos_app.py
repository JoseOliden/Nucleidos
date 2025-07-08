import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_data():
    archivo = st.file_uploader("📂 Sube el archivo CSV con datos nucleares", type="csv")
    if archivo is not None:
        df = pd.read_csv(archivo)
        return df
    else:
        st.info("Por favor, sube un archivo CSV para continuar.")
        st.stop()

def color_map(dec):
    if isinstance(dec, str):
        dec = dec.lower()
    return {
        'stable': 'black',
        'beta-': 'red',
        'beta+': 'blue',
        'alpha': 'purple',
        'isomer': 'orange',
    }.get(dec, 'lightgray')

def main():
    st.title("🔬 Visualizador de la Tabla de Nucleidos (tipo IAEA)")

    df = load_data()

    simbolo = st.text_input("🔎 Ingresa el símbolo del elemento (Ej: Fe):").capitalize()
    if simbolo:
        fila = df[df["Simbolo"] == simbolo]
        if fila.empty:
            st.warning("Elemento no encontrado.")
            st.stop()

        Z_central = fila["Z"].values[0]

        # Filtrar nucleidos vecinos
        vecinos = df[(df["Z"] >= Z_central - 5) & (df["Z"] <= Z_central + 5)]

        # Agregar color a cada nucleido
        vecinos["Color"] = vecinos["Decaimiento"].apply(color_map)

        # Gráfico tipo grilla
        fig = go.Figure()

        for _, r in vecinos.iterrows():
            texto = f"{r['Simbolo']}-{int(r['A'])}<br>{r['Tiempo_decaimiento']}"
            fig.add_trace(go.Scatter(
                x=[r["A"]],
                y=[r["Z"]],
                mode="markers+text",
                marker=dict(symbol="square", size=30, color=r["Color"], line=dict(width=1)),
                text=[texto],
                textposition="middle center",
                textfont=dict(color="white", size=10),
                hovertext=f"{r['Nombre']} ({r['Simbolo']}-{r['A']})\nDecaimiento: {r['Decaimiento']}\nT½: {r['Tiempo_decaimiento']}",
                hoverinfo="text",
                showlegend=False
            ))

        fig.update_layout(
            title=f"🧩 Nucleidos alrededor de {simbolo}",
            xaxis_title="Número de masa (A)",
            yaxis_title="Número atómico (Z)",
            yaxis=dict(autorange='reversed', dtick=1),
            xaxis=dict(dtick=1),
            height=700,
            plot_bgcolor="white",
        )
        st.plotly_chart(fig)

        # Mostrar la tabla
        st.subheader("📋 Tabla de nucleidos cercanos")
        st.dataframe(vecinos[["Z", "A", "Simbolo", "Nombre", "Estabilidad", "Decaimiento", "Tiempo_decaimiento"]])

    else:
        st.info("Ingresa el símbolo de un elemento para comenzar.")

if __name__ == "__main__":
    main()
