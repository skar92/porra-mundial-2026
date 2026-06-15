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

# Participantes oficiales
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
    'Fiyi': '🇫🇯', 'Cook Islands': '🇨🇰', 'Tahití': '🇵🇫'
}

# 🗓️ NUEVAS CUOTAS ACTUALIZADAS (Datos de las últimas capturas procesadas)
datos_cuotas = {
    'ganador': """Francia 5.50 España 5.50 Inglaterra 8.00 Portugal 8.00 Brasil 10.00 Argentina 10.00 Alemania 15.00 Holanda 19.00 Bélgica 34.00 Noruega 34.00 EE.UU. 34.00 Colombia 41.00 Marruecos 41.00 México 51.00 Japón 51.00 Uruguay 67.00 Suiza 67.00 Croacia 81.00 Senegal 81.00 Suecia 81.00 Ecuador 101.00 Australia 101.00 Costa de Marfil 101.00 Turquía 126.00 Canadá 151.00 Escocia 151.00 Austria 151.00 Corea del Sur 201.00 Bosnia and Herzegovina 251.00 Argelia 251.00 Egipto 251.00 Paraguay 301.00 República Checa 301.00 Ghana 501.00 Irán 501.00 Túnez 751.00 RD Congo 751.00 Panamá 1001.00 Sudáfrica 1001.00 Uzbekistán 1001.00 Arabia Saudí 1001.00 Catar 1001.00 Nueva Zelanda 1001.00 Jordan 1001.00 Cabo Verde 1001.00 Iraq 1001.00 Haití 2501.00 Curazao 2501.00""",
    
    'final': """España 3.25 Francia 3.50 Inglaterra 4.00 Portugal 4.50 Argentina 5.00 Brasil 5.50 Alemania 7.00 Holanda 9.00 Noruega 13.00 Bélgica 15.00 Colombia 17.00 EE.UU. 17.00 México 17.00 Marruecos 17.00 Japón 23.00 Uruguay 26.00 Croacia 26.00 Suiza 26.00 Suecia 26.00 Ecuador 29.00 Australia 34.00 Austria 41.00 Canadá 41.00 Senegal 51.00 Turquía 51.00 Escocia 67.00 Argelia 67.00 Egipto 81.00 Costa de Marfil 81.00 Corea del Sur 101.00 Ghana 101.00 Bosnia and Herzegovina 101.00 Paraguay 126.00 Irán 126.00 República Checa 126.00 RD Congo 201.00 Arabia Saudí 251.00 Catar 251.00 Panamá 301.00 Nueva Zelanda 301.00 Jordan 351.00 Uzbekistán 401.00 Cabo Verde 401.00 Iraq 501.00 Túnez 701.00 Sudáfrica 1001.00 Curazao 1001.00 Haití 1001.00""",
    
    'semis': """España 2.10 Inglaterra 2.50 Francia 2.50 Argentina 3.00 Portugal 3.00 Brasil 3.40 Alemania 4.00 Holanda 5.50 Bélgica 5.50 Noruega 5.75 Colombia 7.00 EE.UU. 7.00 Marruecos 7.50 Uruguay 8.00 México 8.00 Japón 10.00 Croacia 10.50 Suecia 11.50 Suiza 12.00 Senegal 12.00 Austria 13.00 Canadá 15.00 Ecuador 18.00 Escocia 18.00 Bosnia and Herzegovina 19.50 Australia 21.00 Egipto 21.00 Corea del Sur 21.00 Costa de Marfil 21.00 Turquía 26.00 Argelia 29.00 Paraguay 34.00 Irán 34.00 Ghana 34.00 República Checa 36.00 Panamá 51.00 Arabia Saudí 67.00 RD Congo 67.00 Cabo Verde 101.00 Nueva Zelanda 126.00 Jordan 151.00 Catar 151.00 Uzbekistán 151.00 Túnez 301.00 Iraq 351.00 Curazao 1001.00 Haití 1001.00""",
    
    'cuartos': """España 1.62 Francia 1.70 Inglaterra 1.80 Argentina 1.90 Portugal 1.95 Brasil 2.15 Alemania 2.30 Bélgica 2.87 Holanda 3.00 EE.UU. 3.20 Noruega 3.25 México 3.50 Colombia 3.50 Marruecos 3.75 Uruguay 4.00 Japón 4.50 Suiza 4.50 Suecia 5.50 Canadá 6.00 Croacia 6.00 Australia 7.00 Austria 7.00 Costa de Marfil 7.00 Ecuador 7.00 Corea del Sur 8.00 Senegal 8.00 Escocia 8.50 Turquía 9.00 Argelia 11.00 Bosnia and Herzegovina 11.00 Egipto 11.00 Irán 12.00 República Checa 13.00 Ghana 13.00 Paraguay 17.00 RD Congo 21.00 Arabia Saudí 26.00 Cabo Verde 34.00 Uzbekistán 34.00 Iraq 41.00 Nueva Zelanda 41.00 Panamá 41.00 Sudáfrica 41.00 Túnez 41.00 Catar 51.00 Jordan 67.00 Haití 101.00 Curazao 151.00""",
    
    'octavos': """Francia 1.22 España 1.22 Inglaterra 1.25 Argentina 1.40 Brasil 1.40 Alemania 1.40 Portugal 1.40 México 1.50 Bélgica 1.57 EE.UU. 1.61 Suiza 1.80 Colombia 1.83 Noruega 1.83 Holanda 1.90 Uruguay 2.00 Canadá 2.20 Marruecos 2.20 Corea del Sur 2.25 Croacia 2.37 Japón 2.37 Australia 2.50 Suecia 2.50 Costa de Marfil 2.60 Ecuador 3.00 Escocia 3.00 Egipto 3.20 Austria 3.25 Senegal 3.25 Argelia 3.75 República Checa 3.75 Turquía 3.75 Bosnia and Herzegovina 4.00 Irán 4.00 Ghana 6.00 Paraguay 6.00 RD Congo 7.00 Nueva Zelanda 9.00 Arabia Saudí 9.00 Sudáfrica 11.00 Panamá 12.00 Uzbekistán 12.00 Cabo Verde 15.00 Catar 15.00 Iraq 17.00 Jordan 17.00 Túnez 17.00 Haití 41.00 Curazao 51.00"""
}

# --- PROCESAMIENTO MATEMÁTICO ---
todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
# Añadida la ronda 'semis' a la inicialización de probabilidades
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
    # Modificado el sumatorio incluyendo los 15 puntos correspondientes a la ronda de Semis
    puntos_totales = sum([
        (10 * probabilidades[e]['octavos'] + 
         12 * probabilidades[e]['cuartos'] + 
         15 * probabilidades[e]['semis'] + 
         18 * probabilidades[e]['final'] + 
         20 * probabilidades[e]['ganador']) for e in equipos
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
