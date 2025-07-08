import streamlit as st
import pandas as pd
import plotly.express as px

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

def main():
    st.title("🌟 Explorador Interactivo de la Tabla de Nucleidos")
    df = cargar_datos()

    simbolo = st.text_input("Ingresa el símbolo del elemento (Ej: Fe):").capitalize()
    
    if simbolo:
        Z_central = buscar_Z(df, simbolo)
        if Z_central is None:
            st.warning("Elemento no encontrado.")
            return
        
        ventana = df[(df['Z'] >= Z_central - 3) & (df['Z'] <= Z_central + 3)]
        
        fig = px.scatter(
            ventana, x="A", y="Z", 
            text="Simbolo",
            color="Estabilidad",
            color_discrete_map={"Estable": "green", "Inestable": "red"},
            title=f"Nucleidos alrededor de {simbolo}",
            labels={"A": "Número de masa (A)", "Z": "Número atómico (Z)"}
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(height=600)
        st.plotly_chart(fig)

        st.dataframe(ventana[["Z", "A", "Simbolo", "Nombre", "Estabilidad"]])
    else:
        st.info("Ingresa un símbolo para comenzar.")

if __name__ == "__main__":
    main()
