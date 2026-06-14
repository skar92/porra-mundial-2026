import streamlit as st
import pandas as pd
import plotly.express as px
import re
from datetime import datetime

st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra")
st.write(f"Actualizado al: {datetime.now().strftime('%d/%m/%Y')}")

# ⚠️ PEGA AQUÍ TU URL DE GOOGLE SHEETS EN FORMATO EXPORTACIÓN CSV ⚠️
URL_SHEETS = "https://docs.google.com/spreadsheets/d/1mmRhevyqOCuJQBcsYNXHGIUbnSJPaSR2zLuSPjvTfQg/export?format=csv"

# Participantes oficiales
porra = {
    'Sierra': ['España', 'Suiza', 'Croacia'],
    'Joaquín': ['Portugal', 'Marruecos', 'EE.UU.'],
    'Ejkar': ['Inglaterra', 'Colombia', 'Japón'],
    'Vecina': ['Ecuador', 'Bélgica', 'México'],
    'Telenti': ['Francia', 'Noruega', 'Senegal'],
    'Miguel Ángel': ['Argentina', 'Holanda', 'Costa de Marfil'],
    'Mírete': ['Brasil', 'Alemania', 'Uruguay']
}

banderas = {
    'España': '🇪🇸', 'Suiza': '🇨🇭', 'Croacia': '🇭🇷',
    'Portugal': '🇵🇹', 'Marruecos': '🇲🇦', 'EE.UU.': '🇺🇸',
    'Inglaterra': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Colombia': '🇨🇴', 'Japón': '🇯🇵',
    'Ecuador': '🇪🇨', 'Bélgica': '🇧🇪', 'México': '🇲🇽',
    'Francia': '🇫🇷', 'Noruega': '🇳🇴', 'Senegal': '🇸🇳',
    'Argentina': '🇦🇷', 'Holanda': '🇳🇱', 'Costa de Marfil': '🇨🇮',
    'Brasil': '🇧🇷', 'Alemania': '🇩🇪', 'Uruguay': '🇺🇾'
}

# 🗓️ CUOTAS ACTUALES (Aquí es donde entrarás tú a pegar el bloque nuevo cada día)
datos_cuotas = {
    'ganador': """España 5.75Francia 6Inglaterra 8 Portugal 9Brasil 10.1Argentina 11 Alemania 17Holanda 21Noruega 34 """,
    'final': """Francia 8España 8Inglaterra 9.5 Portugal 9.5Brasil 10Argentina 10 Alemania 12""",
    'semis': """España 2.25Francia 2.4Inglaterra 2.88 Argentina 3.25Portugal 3.25""",
    'cuartos': """España 1.67Francia 1.75Inglaterra 1.8 Argentina 2Portugal 2""",
    'octavos': """España 1.25Francia 1.25Inglaterra 1.3 Portugal 1.4Brasil 1.4"""
}

# --- PROCESAMIENTO MATEMÁTICO ---
todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades = {eq: {'octavos': 0.0, 'cuartos': 0.0, 'semis': 0.0, 'final': 0.0, 'ganador': 0.0} for eq in todos_equipos}

for ronda, texto in datos_cuotas.items():
    for eq in todos_equipos:
        patron = re.escape(eq) + r'\s*([\d\.]+)'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            probabilidades[eq][ronda] = 1 / float(match.group(1))

# Cálculo del día de hoy
filas_hoy = []
fecha_hoy = datetime.now().strftime('%Y-%m-%d')

for jugador, equipos in porra.items():
    puntos_totales = sum([
        (10 * probabilidades[e]['octavos'] + 12 * probabilidades[e]['cuartos'] + 
         15 * probabilidades[e]['semis'] + 18 * probabilidades[e]['final'] + 
         20 * probabilidades[e]['ganador']) for e in equipos
    ])
    string_banderas = " ".join([banderas.get(e, '🏳️') for e in equipos])
    filas_hoy.append({"Fecha": fecha_hoy, "Jugador": jugador, "Equipos": string_banderas, "Puntos": round(puntos_totales, 2)})

df_hoy = pd.DataFrame(filas_hoy)
total_puntos = df_hoy["Puntos"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos"] / (total_puntos if total_puntos > 0 else 1)) * 100, 2)

# 🔄 INTENTAR LEER EL HISTÓRICO DESDE TU GOOGLE SHEETS
try:
    df_hist_sheets = pd.read_csv(URL_SHEETS)
    # Combinamos lo viejo del Excel con lo fresco de hoy
    df_hist = pd.concat([df_hist_sheets, df_hoy], ignore_index=True)
except:
    # Si el Excel falla o está vacío (Día 1), el histórico es solo lo de hoy
    df_hist = df_hoy.copy()

# Limpiar duplicados por si acaso refrescan mucho la web el mismo día
df_hist = df_hist.drop_duplicates(subset=['Fecha', 'Jugador'], keep='last')
df_hist = df_hist.sort_values(by="Fecha")

# --- DISEÑO DE LA WEB (INTERFAZ) ---
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("📊 Clasificación Actual")
    df_mostrar = df_hoy.sort_values(by="Puntos", ascending=False)[["Jugador", "Equipos", "Puntos", "Probabilidad (%)"]]
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📈 Gráfico de Puntos Hoy")
    fig_barras = px.bar(df_mostrar, x="Jugador", y="Puntos", color="Jugador", text_auto=True)
    st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")
st.subheader("⏳ Evolución Temporal de la Porra (Miedo de Vecina)")
fig_lineas = px.line(df_hist, x="Fecha", y="Probabilidad (%)", color="Jugador", markers=True)
fig_lineas.update_xaxes(type='category')
st.plotly_chart(fig_lineas, use_container_width=True)
