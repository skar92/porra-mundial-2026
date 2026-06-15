import streamlit as st
import pandas as pd
import plotly.express as px
import re
from datetime import datetime

# --- CHUNK 1: CONFIGURACIÓN Y DATOS ---
st.set_page_config(page_title="Porra Mundial 2026", layout="wide")

porra = {
    'Sierra': ['España', 'Suiza', 'Croacia'],
    'Joaquín': ['Portugal', 'Marruecos', 'EE.UU.'],
    'Ejkar': ['Inglaterra', 'Colombia', 'Japón'],
    'Vecina': ['Ecuador', 'Bélgica', 'México'],
    'Telenti': ['Francia', 'Noruega', 'Senegal'],
    'Miguel Ángel': ['Argentina', 'Holanda', 'Costa de Marfil'],
    'Mírete': ['Brasil', 'Alemania', 'Uruguay'],
    'Juan': ['Canadá', 'Turquía', 'Austria', 'Escocia', 'Bosnia and Herzegovina']
}

porra_futbolistas = {
    'Sierra': {'Kane': 0, 'Julián Álvarez': 0},
    'Joaquín': {'Messi': 0, 'Olise': 0},
    'Ejkar': {'Lautaro': 0, 'Raphinha': 0},
    'Vecina': {'Havertz': 2, 'Lamine Yamal': 0},
    'Telenti': {'Endrick': 0, 'Ramos': 0},
    'Miguel Ángel': {'Haaland': 0, 'Embolo': 1},
    'Mírete': {'Oyarzabal': 0, 'El Bicho': 0},
    'Juan': {'Mbappé': 0, 'Vinicius': 1}
}

banderas = {'Francia': '🇫🇷', 'España': '🇪🇸', 'Inglaterra': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Portugal': '🇵🇹', 'Argentina': '🇦🇷', 'Brasil': '🇧🇷', 'Alemania': '🇩🇪', 'Holanda': '🇳🇱', 'Noruega': '🇳🇴', 'Bélgica': '🇧🇪', 'Marruecos': '🇲🇦', 'Colombia': '🇨🇴', 'Japón': '🇯🇵', 'México': '🇲🇽', 'EE.UU.': '🇺🇸', 'Uruguay': '🇺🇾', 'Croacia': '🇭🇷', 'Suiza': '🇨🇭', 'Ecuador': '🇪🇨', 'Austria': '🇦🇹', 'Turquía': '🇹🇷', 'Senegal': '🇸🇳', 'Suecia': '🇸🇪', 'Escocia': '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 'Canadá': '🇨🇦', 'Costa de Marfil': '🇨🇮', 'Bosnia and Herzegovina': '🇧🇦'}

datos_cuotas = {
    'ganador': "Francia 5.50 España 5.50 Inglaterra 8.00 Portugal 8.00 Brasil 10.00 Argentina 10.00 Alemania 15.00 Holanda 19.00 Bélgica 34.00 Noruega 34.00 EE.UU. 34.00 Colombia 41.00 Marruecos 41.00 México 51.00 Japón 51.00 Uruguay 67.00 Suiza 67.00 Croacia 81.00 Senegal 81.00",
    'final': "España 3.25 Francia 3.50 Inglaterra 4.00 Portugal 4.50 Argentina 5.00 Brasil 5.50 Alemania 7.00 Holanda 9.00 Noruega 13.00 Bélgica 15.00 Colombia 17.00 EE.UU. 17.00 México 17.00 Marruecos 17.00 Japón 23.00 Uruguay 26.00 Croacia 26.00 Suiza 26.00",
    'semis': "España 2.10 Inglaterra 2.50 Francia 2.50 Argentina 3.00 Portugal 3.00 Brasil 3.40 Alemania 4.00 Holanda 5.50 Bélgica 5.50 Noruega 5.75 Colombia 7.00 EE.UU. 7.00 Marruecos 7.50 Uruguay 8.00 México 8.00 Japón 10.00 Croacia 10.50",
    'cuartos': "España 1.62 Francia 1.70 Inglaterra 1.80 Argentina 1.90 Portugal 1.95 Brasil 2.15 Alemania 2.30 Bélgica 2.87 Holanda 3.00 EE.UU. 3.20 Noruega 3.25 México 3.50 Colombia 3.50 Marruecos 3.75 Uruguay 4.00 Japón 4.50 Suiza 4.50",
    'octavos': "Francia 1.22 España 1.22 Inglaterra 1.25 Argentina 1.40 Brasil 1.40 Alemania 1.40 Portugal 1.40 México 1.50 Bélgica 1.57 EE.UU. 1.61 Suiza 1.80 Colombia 1.83 Noruega 1.83 Holanda 1.90 Uruguay 2.00"
}

# --- CHUNK 2: PROCESAMIENTO MATEMÁTICO ---
def calcular_probabilidades(datos, equipos):
    probs = {eq: {'octavos': 0.0, 'cuartos': 0.0, 'semis': 0.0, 'final': 0.0, 'ganador': 0.0} for eq in equipos}
    for ronda, texto in datos.items():
        for eq in equipos:
            match = re.search(re.escape(eq) + r'\s*([\d\.]+)', texto, re.IGNORECASE)
            if match:
                probs[eq][ronda] = 1 / float(match.group(1))
    return probs

todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades = calcular_probabilidades(datos_cuotas, todos_equipos)

# --- CHUNK 3: GENERACIÓN DE DATOS DE USUARIO ---
filas = []
for jugador, equipos in porra.items():
    puntos_selecciones = sum([(10 * probabilidades[e]['octavos'] + 12 * probabilidades[e]['cuartos'] + 15 * probabilidades[e]['semis'] + 18 * probabilidades[e]['final'] + 20 * probabilidades[e]['ganador']) for e in equipos])
    puntos_totales = puntos_selecciones + sum(porra_futbolistas[jugador].values())
    
    filas.append({
        "Jugador": jugador,
        "Equipos": ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos]),
        "Futbolistas": ", ".join([f"{f} ({pts})" for f, pts in porra_futbolistas[jugador].items()]),
        "Puntos Esperados": round(puntos_totales, 2)
    })

df = pd.DataFrame(filas).sort_values(by="Puntos Esperados", ascending=False)

# --- CHUNK 4: INTERFAZ VISUAL ---
st.title("🏆 Seguimiento y Evolución de la Porra")
st.write(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

col1, col2 = st.columns([1.2, 0.8])
with col1:
    st.subheader("📊 Clasificación Actual")
    st.dataframe(df, use_container_width=True, hide_index=True)
with col2:
    st.subheader("📈 Gráfico de Rendimiento")
    st.plotly_chart(px.bar(df, x="Jugador", y="Puntos Esperados", color="Jugador", text_auto=True), use_container_width=True)
