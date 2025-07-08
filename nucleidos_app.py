import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def cargar_datos():
    archivo = st.file_uploader("Sube el archivo 'tabla_nucleidos.csv'", type="csv")
    if archivo is not None:
        return pd.read_csv(archivo)
    else:
        st.stop()

def buscar_Z(df, simbolo):
    fila = df[df['Simbolo'] == simbolo]
    if not fila.empty:
        return fila['Z'].values[0]
    return None

def graficar_grilla(df_filtrado, simbolo):
    fig = go.Figure()

    colores = {"Estable": "green", "Inestable": "red"}

    for _, row in df_filtrado.iterrows():
        color = colores.get(row["Estabilidad"], "gray")
        label = f"{row['Simbolo']}-{int(row['A'])}"
        fig.add_trace(go.Scatter(
            x=[row["A"]],
            y=[row["Z"]],
            mode="markers+text",
            marker=dict(color=color, size=28, line=dict(color='black', width=1)),
            text=[label],
            textposition="middle center",
            showlegend=False
        ))

    fig.update_layout(
        title=f"Tabla de Nucleidos alrededor de {simbolo}",
        xaxis_title="Número de masa (A)",
        yaxis_title="Número atómico (Z)",
        yaxis=dict(autorange='reversed'),
        height=600,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig)

def main():
    st.title("🌟 Explorador Interactivo de la Tabla de Nucleidos")
    df = cargar_datos()

    simbolo = st.text_input("Ingresa el símbolo del elemento (Ej: Fe):").capitalize()
    
    if simbolo:
        Z_central = buscar_Z(df, simbolo)
        if Z_central is None:
            st.warning("Elemento no encontrado.")
            return
        
        # Filtrar ventana de elementos cercanos
        ventana = df[(df['Z'] >= Z_central - 3) & (df['Z'] <= Z_central + 3)]
        
        # Mostrar tabla interactiva (scatter)
        st.subheader("📊 Diagrama Z vs A")
        fig = px.scatter(
            ventana, x="A", y="Z", 
            text="Simbolo",
            color="Estabilidad",
            color_discrete_map={"Estable": "green", "Inestable": "red"},
            labels={"A": "Número de masa (A)", "Z": "Número atómico (Z)"}
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(height=500)
        st.plotly_chart(fig)

        # Mostrar grilla tipo tabla de nucleidos
        st.subheader("🧩 Grilla de nucleidos tipo tabla")
        graficar_grilla(ventana, simbolo)

        # Mostrar tabla
        st.subheader("📋 Datos de nucleidos")
        st.dataframe(ventana[["Z", "A", "Simbolo", "Nombre", "Estabilidad"]])
    else:
        st.info("Ingresa un símbolo para comenzar.")

if __name__ == "__main__":
    main()
