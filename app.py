import streamlit as st
import pandas as pd
import plotly.express as px
import re
from datetime import datetime

st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra")
st.write(f"Actualizado al: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ⚠️ PEGA AQUÍ TU URL DE GOOGLE SHEETS EN FORMATO EXPORTACIÓN CSV ⚠️
URL_SHEETS = "https://docs.google.com/spreadsheets/d/1mmRhevyqOCuJQBcsYNXHGIUbnSJPaSR2zLuSPjvTfQg/export?format=csv"

# Participantes oficiales (¡Damos la bienvenida a Juan con sus 5 equipos!)
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

# Diccionario de banderas corregido e indexado
banderas = {
    'Francia': '🇫🇷', 'España': '🇪🇸', 'Inglaterra': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Portugal': '🇵🇹', 
    'Argentina': '🇦🇷', 'Brasil': '🇧🇷', 'Alemania': '🇩🇪', 'Holanda': '🇳🇱', 
    'Noruega': '🇳🇴', 'Bélgica': '🇧🇪', 'Marruecos': '🇲🇦', 'Colombia': '🇨🇴', 
    'Japón': '🇯🇵', 'México': '🇲🇽', 'EE.UU.': '🇺🇸', 'Uruguay': '🇺🇾', 
    'Croacia': '🇭🇷', 'Suiza': '🇨🇭', 'Ecuador': '🇪🇨', 'Austria': '🇦🇹', 
    'Turquía': '🇹🇷', 'Senegal': '🇸🇳', 'Suecia': '🇸🇪', 'Escocia': '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 
    'Canadá': '🇨🇦', 'Egipto': '🇪🇬', 'Costa de Marfil': '🇨🇮', 'Corea del Sur': '🇰🇷', 
    'Australia': '🇦🇺', 'Argelia': '🇩🇿', 'Ghana': '🇬🇭', 'Irán': '🇮🇷', 
    'Bosnia and Herzegovina': '🇧🇦', 'Túnez': '🇹🇳', 'Paraguay': '🇵🇾', 'República Checa': '🇨🇿', 
    'Montenegro': '🇲🇪', 'Arabia Saudí': '🇸🇦', 'Ruanda': '🇷🇼', 'Burkina Faso': '🇧🇫', 
    'El Salvador': '🇸🇻', 'RD Congo': '🇨🇩', 'Panamá': '🇵🇦', 'Puerto Rico': '🇵🇷', 
    'Togo': '🇹🇬', 'Benín': '🇧🇯', 'Qatar': '🇶🇦', 'Cabo Verde': '🇨🇻', 
    'Sudáfrica': '🇿🇦', 'Indonesia': '🇮🇩', 'Uzbekistán': '🇺🇿', 'Gambia': '🇬🇲', 
    'Luxemburgo': '🇱🇺', 'Nueva Zelanda': '🇳🇿', 'Tanzania': '🇹🇿', 'Jordania': '🇯🇴', 
    'Chipre': '🇨🇾', 'Malta': '🇲🇹', 'Iraq': '🇮🇶', 'Curazao': '🇨🇼', 
    'Haití': '🇭🇹', 'Kenia': '🇰🇪', 'Gibraltar': '🇬🇮', 'Islas Vírgenes EE.UU.': '🇻🇮', 
    'Fiyi': '🇫🇯', 'Cook Islands AI': '🇨🇰', 'Tahiti': '🇵🇫'
}

# 🗓️ NUEVAS CUOTAS ACTUALIZADAS (Datos frescos de Oddschecker)
datos_cuotas = {
    'ganador': """Francia 5.75 España 6 Inglaterra 9 Portugal 9 Argentina 11.1 Brasil 12 Alemania 17 Holanda 23 Noruega 35 Bélgica 41 Marruecos 41 Colombia 42 Japón 55 México 60 EE.UU. 60 Uruguay 70 Croacia 100 Suiza 101 Ecuador 101 Austria 151 Turquía 151 Senegal 151 Suecia 151 Escocia 250 Canadá 251 Egipto 301 Costa de Marfil 301 Corea del Sur 400 Australia 500 Argelia 500 Ghana 501 Irán 501 Bosnia and Herzegovina 501 Túnez 501 Paraguay 750 República Checa 751 Montenegro 1001 Arabia Saudí 1001 Ruanda 1001 Burkina Faso 1001 El Salvador 1001 RD Congo 1501 Panamá 1501 Puerto Rico 1501 Togo 1501 Benín 1501 Qatar 2001 Cabo Verde 2001 Sudáfrica 2001 Indonesia 2001 Uzbekistán 2001 Gambia 2001 Luxemburgo 2001 Nueva Zelanda 2501 Tanzania 2501 Jordania 2501 Chipre 2501 Malta 2501 Iraq 3501 Curazao 3501 Haití 4001 Kenia 4501 Gibraltar 4501 Islas Vírgenes EE.UU. 4501 Fiyi 4501 Cook Islands 4501 Tahití 4501""",
    
    'final': """Francia 8 España 8 Inglaterra 9 Portugal 9 Argentina 10 Brasil 11 Alemania 13 Holanda 15 Bélgica 15 Noruega 20 EE.UU. 21 Colombia 23 México 26 Uruguay 26 Marruecos 26 Croacia 34 Suiza 36 Ecuador 36 Japón 36 Austria 41 Senegal 56 Costa de Marfil 67 Suecia 71 Canadá 71 Turquía 81 Argelia 91 Escocia 101 Egipto 101 Corea del Sur 101 Ghana 126 Australia 151 República Checa 176 Irán 176 Paraguay 201 Bosnia and Herzegovina 201 Túnez 426 RD Congo 476 Qatar 501 Panamá 501 Arabia Saudí 501 Sudáfrica 501 Curazao 501 Uzbekistán 501 Cabo Verde 501 Iraq 501 Nueva Zelanda 501 Jordania 501 Haití 501""",
    
    'cuartos': """España 1.75 Francia 1.82 Inglaterra 1.86 Portugal 2 Argentina 2.02 Brasil 2.22 Alemania 2.6 Holanda 2.9 Bélgica 2.92 Noruega 3.35 EE.UU. 3.43 México 3.78 Marruecos 3.78 Colombia 3.78 Suiza 4.9 Uruguay 5.05 Japón 5.1 Croacia 6.05 Ecuador 6.2 Canadá 6.5 Australia 8 Corea del Sur 8 Austria 8.05 Escocia 9 Suecia 9.05 Turquía 9.05 Senegal 9.05 Costa de Marfil 10 Egipto 11 Argelia 11 Bosnia and Herzegovina 11.1 República Checa 13 Ghana 15 Irán 15 Paraguay 17 Túnez 23 RD Congo 23 Arabia Saudí 34 Panamá 41 Uzbekistán 43 Sudáfrica 51 Cabo Verde 61 Nueva Zelanda 67 Qatar 81 Jordania 101 Iraq 110 Curazao 301 Haití 800""",
    
    'octavos': """España 1.25 Francia 1.25 Inglaterra 1.33 Portugal 1.4 Brasil 1.45 Alemania 1.45 Argentina 1.5 Bélgica 1.63 EE.UU. 1.67 México 1.67 Holanda 1.8 Noruega 1.83 Suiza 1.83 Colombia 2 Marruecos 2.2 Corea del Sur 2.25 Canadá 2.25 Uruguay 2.38 Japón 2.6 Ecuador 2.63 Croacia 2.63 Australia 2.88 Costa de Marfil 3.25 Escocia 3.3 Austria 3.5 Egipto 3.5 Senegal 3.75 Turquía 4 República Checa 4 Bosnia and Herzegovina 4 Suecia 4.2 Argelia 4.33 Irán 5 Paraguay 6 Ghana 6 RD Congo 8 Túnez 9.5 Nueva Zelanda 10 Arabia Saudí 11 Sudáfrica 13 Uzbekistán 13 Panamá 13 Cabo Verde 15 Qatar 17 Jordania 26 Iraq 26 Curazao 67 Haití 101"""
}

# --- PROCESAMIENTO MATEMÁTICO ---
todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades = {eq: {'octavos': 0.0, 'cuartos': 0.0, 'final': 0.0, 'ganador': 0.0} for eq in todos_equipos}

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
    # Sumamos las probabilidades multiplicadas por el valor de cada ronda (excluyendo semis al no tener cuotas)
    puntos_totales = sum([
        (10 * probabilidades[e]['octavos'] + 12 * probabilidades[e]['cuartos'] + 
         18 * probabilidades[e]['final'] + 20 * probabilidades[e]['ganador']) for e in equipos
    ])
    
    # Creamos un string visual combinando el nombre del equipo con su emoji de bandera
    string_equipos_banderas = ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos])
    filas_hoy.append({"Fecha": fecha_hoy, "Jugador": jugador, "Equipos": string_equipos_banderas, "Puntos": round(puntos_totales, 2)})

df_hoy = pd.DataFrame(filas_hoy)
total_puntos = df_hoy["Puntos"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos"] / (total_puntos if total_puntos > 0 else 1)) * 100, 2)

# 🔄 INTENTAR LEER EL HISTÓRICO DESDE TU GOOGLE SHEETS
try:
    df_hist_sheets = pd.read_csv(URL_SHEETS)
    df_hist = pd.concat([df_hist_sheets, df_hoy], ignore_index=True)
except:
    df_hist = df_hoy.copy()

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
st.subheader("⏳ Evolución Temporal de la Porra")
fig_lineas = px.line(df_hist, x="Fecha", y="Probabilidad (%)", color="Jugador", markers=True)
fig_lineas.update_xaxes(type='category')
st.plotly_chart(fig_lineas, use_container_width=True)
