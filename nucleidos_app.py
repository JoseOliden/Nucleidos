import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_csv("iaea_chart.csv")

def main():
    st.title("🎯 Chart of Nuclides (IAEA style)")

    df = load_data()
    df['DecayType'] = df['decay']  # ajustar según columna
    elemento = st.text_input("Elemento (símbolo, ej. Fe)").capitalize()
    if not elemento:
        st.info("Ingresa un símbolo para iniciar.")
        st.stop()

    # obtener Z del elemento
    Z0 = df[df['symbol']==elemento]['Z'].unique()
    if len(Z0)==0:
        st.warning("Elemento no encontrado.")
        st.stop()
    Z0 = int(Z0[0])

    # ventana de Z ±5
    ventana = df[(df['Z']>=Z0-5)&(df['Z']<=Z0+5)]

    # mapeo de color según estabilidad/decay
    def color_map(dec):
        return {
            'stable': 'black',
            'beta-': 'red',
            'beta+': 'blue',
            'alpha': 'purple',
        }.get(dec, 'lightgray')

    ventana['color'] = ventana['DecayType'].apply(color_map)

    fig = go.Figure()
    for _, r in ventana.iterrows():
        fig.add_trace(go.Scatter(
            x=[r['A']], y=[r['Z']],
            text=r['symbol'],
            mode='markers+text',
            marker=dict(symbol='square', size=20, color=r['color'], line=dict(width=1)),
            textfont=dict(color="white", size=12),
            showlegend=False
        ))
    fig.update_layout(
        xaxis_title="A (número de masa)",
        yaxis_title="Z (número atómico)",
        yaxis=dict(autorange="reversed", dtick=1),
        xaxis=dict(dtick=1),
        height=700, width=900,
        plot_bgcolor="white",
    )
    st.plotly_chart(fig)

if __name__=="__main__":
    main()
