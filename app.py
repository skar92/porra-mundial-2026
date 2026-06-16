import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import os
from datetime import datetime

# Configuración de la interfaz de Streamlit
st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra")
st.write(f"Actualizado al: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- CONFIGURACIÓN DE LOS DATOS DE LA PORRA ---

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

puntos_futbolistas_actuales = {jugador: sum(datos.values()) if isinstance(datos, dict) else 0 
                               for jugador, datos in porra_futbolistas.items()}

traduccion_api = {
    'Francia': 'France', 'España': 'Spain', 'Inglaterra': 'England', 'Portugal': 'Portugal',
    'Argentina': 'Argentina', 'Brasil': 'Brazil', 'Alemania': 'Germany', 'Holanda': 'Netherlands',
    'Noruega': 'Norway', 'Bélgica': 'Belgium', 'Marruecos': 'Morocco', 'Colombia': 'Colombia',
    'Japón': 'Japan', 'México': 'Mexico', 'EE.UU.': 'USA', 'Uruguay': 'Uruguay',
    'Croacia': 'Croatia', 'Suiza': 'Switzerland', 'Ecuador': 'Ecuador', 'Austria': 'Austria',
    'Turquía': 'Turkey', 'Senegal': 'Senegal', 'Escocia': 'Scotland', 'Canadá': 'Canada',
    'Costa de Marfil': 'Ivory Coast', 'Bosnia and Herzegovina': 'Bosnia and Herzegovina'
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

# Archivo local donde se guardará la memoria física de las cuotas
ARCHIVO_MEMORIA = "ultimas_cuotas.json"

# --- LÓGICA DE PERSISTENCIA Y EXTRACCIÓN (THE ODDS API) ---

def guardar_en_memoria_local(datos):
    """Guarda físicamente las cuotas en un archivo JSON en el servidor."""
    try:
        with open(ARCHIVO_MEMORIA, "w") as f:
            json.dump(datos, f)
    except Exception:
        pass

def leer_de_memoria_local():
    """Recupera el último JSON de cuotas guardado si existe."""
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

@st.cache_data(ttl=3600)
def obtener_cuotas_sistema():
    """Consulta la API, calcula las rondas, actualiza la memoria y gestiona fallos."""
    API_KEY = "bb4e2d54f5e310838ac064bdade169fd"
    SPORT_KEY = "soccer_fifa_world_cup_winner"
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT_KEY}/odds/"
    params = {
        'apiKey': API_KEY,
        'regions': 'eu',
        'markets': 'outrights',
        'oddsFormat': 'decimal'
    }
    
    datos_completos = {'ganador': {}, 'final': {}, 'semis': {}, 'cuartos': {}, 'octavos': {}}
    
    try:
        response = requests.get(url, params=params)
        
        # Si la API responde correctamente (Créditos disponibles)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                outcomes = data[0]['bookmakers'][0]['markets'][0]['outcomes']
                cuotas_ganador = {o['name']: float(o['price']) for o in outcomes}
                
                if cuotas_ganador:
                    datos_completos['ganador'] = cuotas_ganador
                    # Generación de las fases eliminatorias
                    for equipo, cuota in cuotas_ganador.items():
                        datos_completos['final'][equipo] = max(1.01, cuota * 0.6)
                        datos_completos['semis'][equipo] = max(1.01, cuota * 0.4)
                        datos_completos['cuartos'][equipo] = max(1.01, cuota * 0.25)
                        datos_completos['octavos'][equipo] = max(1.01, cuota * 0.15)
                    
                    # 💾 GUARDAR EN MEMORIA: Actualizamos nuestro archivo de respaldo real
                    guardar_en_memoria_local(datos_completos)
                    return datos_completos, True
                    
        # Si llega aquí es porque la API dio error 429 (sin créditos), 401 u otros
        memoria = leer_de_memoria_local()
        if memoria:
            return memoria, False
        return None, False
        
    except Exception:
        memoria = leer_de_memoria_local()
        if memoria:
            return memoria, False
        return None, False

# --- PROCESAMIENTO DE PROBABILIDADES ---

todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades = {eq: {'octavos': 0.0, 'cuartos': 0.0, 'semis': 0.0, 'final': 0.0, 'ganador': 0.0} for eq in todos_equipos}

# Solicitamos los datos al sistema inteligente de cuotas
datos_cuotas, api_activa = obtener_cuotas_sistema()

if datos_cuotas:
    if not api_activa:
        # Mensaje de advertencia si estamos tirando del archivo JSON de memoria
        st.warning("⚠️ Los créditos de la API se han agotado. Se están mostrando las últimas cuotas reales extraídas de la memoria.")
    
    # Rellenamos la matriz de probabilidades
    for ronda in ['octavos', 'cuartos', 'semis', 'final', 'ganador']:
        cuotas_ronda = datos_cuotas.get(ronda, {})
        for eq in todos_equipos:
            nombre_ingles = traduccion_api.get(eq, eq)
            cuota = cuotas_ronda.get(nombre_ingles, 1000.0)
            probabilidades[eq][ronda] = 1 / float(cuota)
else:
    st.error("❌ No hay conexión con la API ni datos guardados en la memoria local para arrancar.")

# --- CÁLCULO DE PUNTOS ESPERADOS HOY ---

filas_hoy = []
fecha_hoy = datetime.now().strftime('%Y-%m-%d')

for jugador, equipos in porra.items():
    puntos_selecciones = sum([
        (10 * probabilidades[e]['octavos'] +
         12 * probabilidades[e]['cuartos'] +
         15 * probabilidades[e]['semis'] +
         18 * probabilidades[e]['final'] +
         20 * probabilidades[e]['ganador']) for e in equipos
    ])
    
    puntos_totales = puntos_selecciones + puntos_futbolistas_actuales.get(jugador, 0)
    
    filas_hoy.append({
        "Fecha": fecha_hoy,
        "Jugador": jugador,
        "Equipos": ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos]),
        "Futbolistas": ", ".join([f"{f} ({pts})" for f, pts in porra_futbolistas.get(jugador, {}).items()]),
        "Puntos Esperados": round(puntos_totales, 2)
    })

df_hoy = pd.DataFrame(filas_hoy)
total_puntos = df_hoy["Puntos Esperados"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos Esperados"] / (total_puntos if total_puntos > 0 else 1)) * 100, 2)

# --- HISTÓRICO FIJO ---
datos_ayer = [
    {"Fecha": "2026-06-15", "Jugador": "Mírete", "Probabilidad (%)": 14.43},
    {"Fecha": "2026-06-15", "Jugador": "Sierra", "Probabilidad (%)": 13.80},
    {"Fecha": "2026-06-15", "Jugador": "Telenti", "Probabilidad (%)": 13.59},
    {"Fecha": "2026-06-15", "Jugador": "Joaquín", "Probabilidad (%)": 13.49},
    {"Fecha": "2026-06-15", "Jugador": "Ejkar", "Probabilidad (%)": 13.48},
    {"Fecha": "2026-06-15", "Jugador": "Miguel Ángel", "Probabilidad (%)": 12.67},
    {"Fecha": "2026-06-15", "Jugador": "Vecina", "Probabilidad (%)": 10.07},
    {"Fecha": "2026-06-15", "Jugador": "Juan", "Probabilidad (%)": 8.48}
]
df_ayer = pd.DataFrame(datos_ayer)
df_hist = pd.concat([df_ayer, df_hoy[["Fecha", "Jugador", "Probabilidad (%)"]]], ignore_index=True)

# --- INTERFAZ GRÁFICA ---

col1, col2 = st.columns([1.2, 0.8])
with col1:
    st.subheader("📊 Clasificación General de Probabilidad")
    df_mostrar = df_hoy.sort_values(by="Probabilidad (%)", ascending=False)[["Jugador", "Equipos", "Futbolistas", "Puntos Esperados", "Probabilidad (%)"]]
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📈 Cuota de Mercado (%)")
    fig_barras = px.bar(df_mostrar, x="Jugador", y="Probabilidad (%)", color="Jugador", text_auto=True)
    st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")
st.subheader("⏳ Evolución Temporal de las Opciones al Título (%)")
fig_lineas = px.line(df_hist, x="Fecha", y="Probabilidad (%)", color="Jugador", markers=True)
fig_lineas.update_xaxes(type='category')
st.plotly_chart(fig_lineas, use_container_width=True)
