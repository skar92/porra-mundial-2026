import streamlit as st
import pandas as pd
import plotly.express as px
import re
import requests
from datetime import datetime

# =================================================================
# ⚙️ AQUÍ SE ESCRIBEN LAS APIS (JUSTO AQUÍ)
# =================================================================

URL_API_GOLES = "https://api.openligadb.de/getmatchdata/wm2026"

ODDS_API_KEY = "bb4e2d54f5e310838ac064bdade169fd"

URL_HISTORICO = "https://docs.google.com/spreadsheets/d/1mmRhevyqOCuJQBcsYNXHGIUbnSJPaSR2zLuSPjvTfQg/export?format=csv&gid=0"

# =================================================================
# (A partir de aquí abajo viene el resto del código de la porra...)
# --- CONFIGURACIÓN DE LA PORRA ---
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
    'Sierra': ['Harry Kane', 'Julián Álvarez'],
    'Joaquín': ['Lionel Messi', 'Michael Olise'],
    'Ejkar': ['Lautaro Martínez', 'Raphinha'],
    'Vecina': ['Kai Havertz', 'Lamine Yamal'],
    'Telenti': ['Endrick', 'Ramos'], 
    'Miguel Ángel': ['Erling Haaland', 'Breel Embolo'],
    'Mírete': ['Mikel Oyarzabal', 'Cristiano Ronaldo'],
    'Juan': ['Kylian Mbappé', 'Vinícius Júnior']
}

banderas = {
    'Francia': '🇫🇷', 'España': '🇪🇸', 'Inglaterra': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Portugal': '🇵🇹', 
    'Argentina': '🇦🇷', 'Brasil': '🇧🇷', 'Alemania': '🇩🇪', 'Holanda': '🇳🇱', 
    'Noruega': '🇳🇴', 'Bélgica': '🇧🇪', 'Marruecos': '🇲🇦', 'Colombia': '🇨🇴', 
    'Japón': '🇯🇵', 'México': '🇲🇽', 'EE.UU.': '🇺🇸', 'Uruguay': '🇺🇾', 
    'Croacia': '🇭🇷', 'Suiza': '🇨🇭', 'Ecuador': '🇪🇨', 'Austria': '🇦🇹', 
    'Turquía': '🇹🇷', 'Senegal': '🇸🇳', 'Escocia': '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 'Canadá': '🇨🇦', 
    'Costa de Marfil': '🇨🇮', 'Bosnia and Herzegovina': '🇧🇦'
}

# Traductores de nombres de países (La API de apuestas devuelve los nombres en inglés)
traductor_paises = {
    'France': 'Francia', 'Spain': 'España', 'England': 'Inglaterra', 'Portugal': 'Portugal',
    'Argentina': 'Argentina', 'Brazil': 'Brasil', 'Germany': 'Alemania', 'Netherlands': 'Holanda',
    'Norway': 'Noruega', 'Belgium': 'Bélgica', 'Morocco': 'Marruecos', 'Colombia': 'Colombia',
    'Japan': 'Japón', 'Mexico': 'México', 'USA': 'EE.UU.', 'United States': 'EE.UU.', 'Uruguay': 'Uruguay',
    'Croatia': 'Croacia', 'Switzerland': 'Suiza', 'Ecuador': 'Ecuador', 'Austria': 'Austria',
    'Turkey': 'Turquía', 'Senegal': 'Senegal', 'Scotland': 'Escocia', 'Canada': 'Canadá',
    'Ivory Coast': 'Costa de Marfil', 'Bosnia and Herzegovina': 'Bosnia and Herzegovina'
}

# --- APIS AUTOMATIZADAS (CON CACHÉ) ---

@st.cache_data(ttl=300)  # Goles en vivo: caché de 5 minutos
def obtener_goles_futbolistas_live():
    """Consulta OpenLigaDB y mapea con inteligencia los nombres de la API"""
    puntos_en_vivo = {}
    try:
        res = requests.get("https://api.openligadb.de/getmatchdata/wm2026", timeout=5)
        partidos = res.json()
        
        mapeo_goles_api = {}
        for partido in partidos:
            for gol in partido.get("goals", []):
                goleador = gol.get("goalGetterName")
                if goleador:
                    goleador_limpio = goleador.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
                    mapeo_goles_api[goleador_limpio] = mapeo_goles_api.get(goleador_limpio, 0) + 1
        
        for participante, lista_futbolistas in porra_futbolistas.items():
            diccionario_jugador = {}
            for nombre_porra in lista_futbolistas:
                goles = 0
                busqueda_completa = nombre_porra.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
                apellido = busqueda_completa.split()[-1] 
                
                for nombre_api, cantidad_goles in mapeo_goles_api.items():
                    if (apellido in nombre_api) or (nombre_api in busqueda_completa) or (busqueda_completa[:4] in nombre_api):
                        goles = cantidad_goles
                        break
                diccionario_jugador[nombre_porra] = goles
            puntos_en_vivo[participante] = diccionario_jugador
    except:
        return {j: {f: 0 for f in de_jug} for j, de_jug in porra_futbolistas.items()}
    return puntos_en_vivo


@st.cache_data(ttl=3600)  # Cuotas: caché de 1 hora para ahorrar cuota de la API gratuita
def obtener_probabilidades_apuestas_live():
    """Obtiene las cuotas de 'Ganador del Mundial' vía The Odds API y calcula probabilidades"""
    todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
    # Inicializamos todas las rondas basadas en la probabilidad matemática de ganar el torneo
    probabilidades = {eq: {'octavos': 0.5, 'cuartos': 0.25, 'semis': 0.12, 'final': 0.06, 'ganador': 0.02} for eq in todos_equipos}
    
    if ODDS_API_KEY == "TU_CLAVE_DE_PRUEBA_SI_NO_HAY_SECRETS":
        return probabilidades # Devuelve modelo base matemático si no hay clave armada

    try:
        # Petición al mercado de "Ganador Final" (Outrights) de la Copa del Mundo
        url = f"https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=outrights"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                outcomes = data[0].get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [])
                
                for outcome in outcomes:
                    nombre_ingles = outcome.get('name')
                    cuota = float(outcome.get('price', 100))
                    
                    # Traducimos el equipo al nombre en español de tu porra
                    nombre_espanol = traductor_paises.get(nombre_ingles, nombre_ingles)
                    
                    if nombre_espanol in probabilidades:
                        prob_ganar = 1 / cuota
                        # Escalamiento dinámico proporcional para simular las rondas previas de forma matemática limpia
                        probabilidades[nombre_espanol] = {
                            'octavos': min(prob_ganar * 5.5, 0.95),
                            'cuartos': min(prob_ganar * 3.5, 0.75),
                            'semis': min(prob_ganar * 2.2, 0.50),
                            'final': min(prob_ganar * 1.5, 0.25),
                            'ganador': prob_ganar
                        }
    except:
        pass # Si falla la API de cuotas, se usan los pesos proporcionales por defecto de la porra
    return probabilidades

# --- PROCESAMIENTO GENERAL ---
with st.spinner("⚽ Actualizando goles y cuotas del Mundial en vivo..."):
    goles_actualizados = obtener_goles_futbolistas_live()
    probabilidades_live = obtener_probabilidades_apuestas_live()

filas_hoy = []
fecha_hoy = datetime.now().strftime('%Y-%m-%d')

for jugador, equipos in porra.items():
    # Cálculo automático de puntos esperados según las cuotas en vivo de la API
    puntos_selecciones = sum([
        (10 * probabilidades_live[e]['octavos'] + 
         12 * probabilidades_live[e]['cuartos'] + 
         15 * probabilidades_live[e]['semis'] + 
         18 * probabilidades_live[e]['final'] + 
         20 * probabilidades_live[e]['ganador']) for e in equipos
    ])
    
    # Suma de goles de la API de OpenLigaDB
    datos_f = goles_actualizados.get(jugador, {})
    puntos_bonus_futbolistas = sum(datos_f.values())
    
    puntos_totales = puntos_selecciones + puntos_bonus_futbolistas
    
    string_equipos_banderas = ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos])
    string_futbolistas = ", ".join([f"{f} ({gols} ⚽)" for f, gols in datos_f.items()])
        
    filas_hoy.append({
        "Fecha": fecha_hoy, 
        "Jugador": jugador, 
        "Equipos": string_equipos_banderas, 
        "Futbolistas": string_futbolistas,
        "Puntos Esperados": round(puntos_totales, 2)
    })

df_hoy = pd.DataFrame(filas_hoy)
total_puntos = df_hoy["Puntos Esperados"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos Esperados"] / (total_puntos if total_puntos > 0 else 1)) * 100, 2)

# --- SINCRONIZACIÓN DEL HISTÓRICO EN GOOGLE SHEETS ---
try:
    df_hist_sheets = pd.read_csv(URL_HISTORICO)
    if "Puntos" in df_hist_sheets.columns:
        df_hist_sheets = df_hist_sheets.rename(columns={"Puntos": "Puntos Esperados"})
    df_hist = pd.concat([df_hist_sheets, df_hoy], ignore_index=True)
except:
    df_hist = df_hoy.copy()

df_hist = df_hist.drop_duplicates(subset=['Fecha', 'Jugador'], keep='last')
df_hist = df_hist.sort_values(by="Fecha")

# --- INTERFAZ GRÁFICA DE STREAMLIT ---
col1, col2 = st.columns([1.2, 0.8])
with col1:
    st.subheader("📊 Clasificación General de la Porra")
    df_mostrar = df_hoy.sort_values(by="Puntos Esperados", ascending=False)[["Jugador", "Equipos", "Futbolistas", "Puntos Esperados", "Probabilidad (%)"]]
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📈 Proyección de Puntos")
    fig_barras = px.bar(df_mostrar, x="Jugador", y="Puntos Esperados", color="Jugador", text_auto=True)
    st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")
st.subheader("⏳ Evolución Temporal y Tendencia")
fig_lineas = px.line(df_hist, x="Fecha", y="Probabilidad (%)", color="Jugador", markers=True)
fig_lineas.update_xaxes(type='category')
st.plotly_chart(fig_lineas, use_container_width=True)
