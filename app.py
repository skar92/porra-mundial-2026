import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import csv

# Configuración de la interfaz de Streamlit
st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra (Modelo No Acumulativo)")

FILE_GANADORES = "ganadores_sopa.csv"

def guardar_ganador(nombre):
    if not nombre.strip():
        return
    file_exists = os.path.exists(FILE_GANADORES)
    with open(FILE_GANADORES, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Nombre", "Fecha y Hora"])
        writer.writerow([nombre.strip(), datetime.now().strftime('%d/%m/%Y %H:%M')])

# --- CONFIGURACIÓN DE LOS JUGADORES Y COMPOSICIÓN DE EQUIPOS ---
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

# --- GOLES DE FUTBOLISTAS ACTUALIZADOS ---
porra_futbolistas = {
    'Sierra': {'Kane': 6, 'Julián Álvarez':1},
    'Joaquín': {'Messi': 8, 'Olise': 0},
    'Ejkar': {'Lautaro': 2, 'Raphinha': 0},
    'Vecina': {'Havertz': 3, 'Lamine Yamal': 1},
    'Telenti': {'Endrick': 0, 'Ramos': 1},
    'Miguel Ángel': {'Haaland': 7, 'Embolo': 2},
    'Mírete': {'Oyarzabal':3, 'El Bicho': 3}, 
    'Juan': {'Mbappé': 8, 'Vinicius': 4}
}

puntos_futbolistas_actuales = {jugador: sum(datos.values()) if isinstance(datos, dict) else 0 
                               for jugador, datos in porra_futbolistas.items()}

# --- PUNTOS GANADOS EN APUESTA MESA ACTUALIZADOS ---
puntos_apuesta = {
    'Sierra': 2, 
    'Joaquín': 2,       
    'Ejkar': -1,         
    'Vecina': -2,       
    'Telenti': 1,       
    'Miguel Ángel': 1, 
    'Mírete': -1,       
    'Juan': -2          
}

traduccion_interna = {
    'Francia': 'Francia', 'España': 'España', 'Inglaterra': 'Inglaterra', 'Portugal': 'Portugal',
    'Argentina': 'Argentina', 'Brasil': 'Brasil', 'Alemania': 'Alemania', 'Holanda': 'Países Bajos',
    'Noruega': 'Noruega', 'Bélgica': 'Bélgica', 'Marruecos': 'Marruecos', 'Colombia': 'Colombia',
    'Japón': 'Japón', 'México': 'México', 'EE.UU.': 'EE. UU.', 'Uruguay': 'Uruguay',
    'Croacia': 'Croacia', 'Suiza': 'Suiza', 'Ecuador': 'Ecuador', 'Austria': 'Austria',
    'Turquía': 'Turquía', 'Senegal': 'Senegal', 'Escocia': 'Escocia', 'Canadá': 'Canadá',
    'Costa de Marfil': 'Costa de Marfil', 'Bosnia and Herzegovina': 'Bosnia y Herzegovina'
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

# --- CUOTAS OCTAVOS ---
cuotas_octavos = {
    'Francia': 1.00, 'Marruecos': 1.00, 'España': 1.00, 'Bélgica': 1.00, 
    'Noruega': 1.00, 'Inglaterra': 1.00, 'Argentina': 1.00, 'Suiza': 1.00, 'Colombia': 1.00,
    'Canadá': 1.00, 'Paraguay': 1.00, 'EE. UU.': 1.00, 'Portugal': 1.00, 
    'Brasil': 1.00, 'México': 1.00, 'Egipto': 1.00, 
    'Alemania': float('inf'), 'Países Bajos': float('inf'), 'Japón': float('inf'), 'Croacia': float('inf'),
    'Turquía': float('inf'), 'Escocia': float('inf'), 'Uruguay': float('inf'), 
    'Senegal': float('inf'), 'Ecuador': float('inf'), 'Costa de Marfil': float('inf'), 
    'Bosnia y Herzegovina': float('inf'), 'Austria': float('inf'), 'Cabo Verde': float('inf')
}

# --- CUOTAS CUARTOS ---
cuotas_cuartos = {
    'Francia': 1.00, 'Argentina': 1.00, 'Marruecos': 1.00, 'España': 1.00, 
    'Inglaterra': 1.00, 'Bélgica': 1.00, 'Noruega': 1.00, 'Suiza': 1.00,          
    'Colombia': float('inf'), 'Canadá': float('inf'), 'Paraguay': float('inf'), 'EE. UU.': float('inf'), 'Portugal': float('inf'), 
    'Brasil': float('inf'), 'México': float('inf'), 'Egipto': float('inf'), 'Croacia': float('inf'),
    'Alemania': float('inf'), 'Países Bajos': float('inf'), 'Japón': float('inf'), 
    'Turquía': float('inf'), 'Escocia': float('inf'), 'Uruguay': float('inf'),
    'Senegal': float('inf'), 'Ecuador': float('inf'), 'Costa de Marfil': float('inf'), 
    'Bosnia y Herzegovina': float('inf'), 'Austria': float('inf'), 'Cabo Verde': float('inf')
}

# --- CUOTAS SEMIFINALES ACTUALIZADAS (11/07) ---
cuotas_semis = {
    'Francia': 1.00,          
    'España': 1.00,           
    'Argentina': 1,      
    'Inglaterra': 1,      
    'Noruega':  float('inf'),        
    'Suiza':  float('inf'),           
    # Eliminados (incluida Bélgica)
    'Bélgica': float('inf'), 'Marruecos': float('inf'), 'Colombia': float('inf'), 'Canadá': float('inf'), 
    'Paraguay': float('inf'), 'EE. UU.': float('inf'), 'Portugal': float('inf'), 'Brasil': float('inf'), 
    'México': float('inf'), 'Egipto': float('inf'), 'Croacia': float('inf'), 'Alemania': float('inf'), 
    'Países Bajos': float('inf'), 'Japón': float('inf'), 'Turquía': float('inf'), 'Escocia': float('inf'), 
    'Uruguay': float('inf'), 'Senegal': float('inf'), 'Ecuador': float('inf'), 'Costa de Marfil': float('inf'), 
    'Bosnia y Herzegovina': float('inf'), 'Austria': float('inf'), 'Cabo Verde': float('inf')
}

# --- CUOTAS FINALISTAS ACTUALIZADAS (11/07) ---
cuotas_final = {
    'Francia':  float('inf'),        
    'España':   1,          
    'Argentina': 1,      
    'Inglaterra': float('inf'),     
    'Noruega':  float('inf'),          
    'Suiza':  float('inf'),           
    # Eliminados (incluida Bélgica)
    'Bélgica': float('inf'), 'Marruecos': float('inf'), 'Colombia': float('inf'), 'Canadá': float('inf'), 
    'Paraguay': float('inf'), 'EE. UU.': float('inf'), 'Portugal': float('inf'), 'Brasil': float('inf'), 
    'México': float('inf'), 'Egipto': float('inf'), 'Croacia': float('inf'), 'Alemania': float('inf'), 
    'Países Bajos': float('inf'), 'Japón': float('inf'), 'Turquía': float('inf'), 'Escocia': float('inf'), 
    'Uruguay': float('inf'), 'Senegal': float('inf'), 'Ecuador': float('inf'), 'Costa de Marfil': float('inf'), 
    'Bosnia y Herzegovina': float('inf'), 'Austria': float('inf'), 'Cabo Verde': float('inf')
}

# --- CUOTAS GANADOR DEL TORNEO ACTUALIZADAS (11/07) ---
cuotas_ganador = {
    'Francia':  float('inf'),        
    'España': (8/13) + 1,         
    'Argentina': (13/10) + 1,       
    'Inglaterra': float('inf'),       
    'Noruega':  float('inf'),         
    'Suiza':  float('inf'),           
    # Eliminados (incluida Bélgica)
    'Bélgica': float('inf'), 'Marruecos': float('inf'), 'Colombia': float('inf'), 'Canadá': float('inf'), 
    'Paraguay': float('inf'), 'EE. UU.': float('inf'), 'Portugal': float('inf'), 'Brasil': float('inf'), 
    'México': float('inf'), 'Egipto': float('inf'), 'Croacia': float('inf'), 'Alemania': float('inf'), 
    'Países Bajos': float('inf'), 'Japón': float('inf'), 'Turquía': float('inf'), 'Escocia': float('inf'), 
    'Uruguay': float('inf'), 'Senegal': float('inf'), 'Ecuador': float('inf'), 'Costa de Marfil': float('inf'), 
    'Bosnia y Herzegovina': float('inf'), 'Austria': float('inf'), 'Cabo Verde': float('inf')
}

# --- CÓMPUTO MATEMÁTICO NO ACUMULATIVO ---
todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades_fase_maxima = {}

for eq in todos_equipos:
    n = traduccion_interna.get(eq, eq)
    
    p_oct = 1 / float(cuotas_octavos.get(n, float('inf'))) if cuotas_octavos.get(n, float('inf')) != float('inf') else 0.0
    p_cua = 1 / float(cuotas_cuartos.get(n, float('inf'))) if cuotas_cuartos.get(n, float('inf')) != float('inf') else 0.0
    p_sem = 1 / float(cuotas_semis.get(n, float('inf'))) if cuotas_semis.get(n, float('inf')) != float('inf') else 0.0
    p_fin = 1 / float(cuotas_final.get(n, float('inf'))) if cuotas_final.get(n, float('inf')) != float('inf') else 0.0
    p_gan = 1 / float(cuotas_ganador.get(n, float('inf'))) if cuotas_ganador.get(n, float('inf')) != float('inf') else 0.0

    p_exacta_oct = max(0.0, p_oct - p_cua)
    p_exacta_cua = max(0.0, p_cua - p_sem)
    p_exacta_sem = max(0.0, p_sem - p_fin)
    p_exacta_fin = max(0.0, p_fin - p_gan)
    p_exacta_gan = p_gan

    puntos_esperados = (10 * p_exacta_oct) + (12 * p_exacta_cua) + (15 * p_exacta_sem) + (18 * p_exacta_fin) + (20 * p_exacta_gan)
    probabilidades_fase_maxima[eq] = puntos_esperados

# Filas para el día de HOY (11/07)
filas_hoy = []
for jugador, equipos in porra.items():
    puntos_selecciones = sum([probabilidades_fase_maxima.get(e, 0.0) for e in equipos])
    puntos_totales = puntos_selecciones + puntos_futbolistas_actuales.get(jugador, 0) + puntos_apuesta.get(jugador, 0)
    filas_hoy.append({
        "Fecha": "16/07",
        "Jugador": jugador,
        "Equipos": ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos]),
        "Futbolistas": ", ".join([f"{f} ({pts})" for f, pts in porra_futbolistas.get(jugador, {}).items()]),
        "Puntos Apuesta": puntos_apuesta.get(jugador, 0),
        "Puntos Esperados": round(puntos_totales, 2)
    })

df_hoy = pd.DataFrame(filas_hoy)
total_puntos_global = df_hoy["Puntos Esperados"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos Esperados"] / (total_puntos_global if total_puntos_global > 0 else 1)) * 100, 2)

# --- HISTORIAL CRONOLÓGICO CONGELADO (Incluye la captura enviada del 10/07) ---
datos_historicos = [
    {"Fecha": "22/06", "Jugador": "Joaquín", "Probabilidad (%)": 14.34},
    {"Fecha": "22/06", "Jugador": "Miguel Ángel", "Probabilidad (%)": 13.99},
    {"Fecha": "22/06", "Jugador": "Sierra", "Probabilidad (%)": 13.06},
    {"Fecha": "22/06", "Jugador": "Mírete", "Probabilidad (%)": 13.02},
    {"Fecha": "22/06", "Jugador": "Ejkar", "Probabilidad (%)": 12.87},
    {"Fecha": "22/06", "Jugador": "Telenti", "Probabilidad (%)": 12.21},
    {"Fecha": "22/06", "Jugador": "Juan", "Probabilidad (%)": 10.31},
    {"Fecha": "22/06", "Jugador": "Vecina", "Probabilidad (%)": 10.20},
    
    {"Fecha": "02/07", "Jugador": "Joaquín", "Probabilidad (%)": 19.24},
    {"Fecha": "02/07", "Jugador": "Sierra", "Probabilidad (%)": 13.51},
    {"Fecha": "02/07", "Jugador": "Telenti", "Probabilidad (%)": 13.45},
    {"Fecha": "02/07", "Jugador": "Vecina", "Probabilidad (%)": 13.21},
    {"Fecha": "02/07", "Jugador": "Ejkar", "Probabilidad (%)": 11.22},
    {"Fecha": "02/07", "Jugador": "Juan", "Probabilidad (%)": 10.88},
    {"Fecha": "02/07", "Jugador": "Miguel Ángel", "Probabilidad (%)": 9.81},
    {"Fecha": "02/07", "Jugador": "Mírete", "Probabilidad (%)": 8.69},

    # Datos extraídos de la captura (10/07)
    {"Fecha": "10/07", "Jugador": "Joaquín", "Probabilidad (%)": 18.83},
    {"Fecha": "10/07", "Jugador": "Telenti", "Probabilidad (%)": 15.90},
    {"Fecha": "10/07", "Jugador": "Sierra", "Probabilidad (%)": 15.64},
    {"Fecha": "10/07", "Jugador": "Ejkar", "Probabilidad (%)": 12.37},
    {"Fecha": "10/07", "Jugador": "Vecina", "Probabilidad (%)": 11.28},
    {"Fecha": "10/07", "Jugador": "Miguel Ángel", "Probabilidad (%)": 10.73},
    {"Fecha": "10/07", "Jugador": "Juan", "Probabilidad (%)": 8.97},
    {"Fecha": "10/07", "Jugador": "Mírete", "Probabilidad (%)": 6.28},

        # Datos extraídos de la captura (11/07)
    {"Fecha": "11/07", "Jugador": "Joaquín", "Probabilidad (%)": 18.86},
    {"Fecha": "11/07", "Jugador": "Telenti", "Probabilidad (%)": 15.86},
    {"Fecha": "11/07", "Jugador": "Sierra", "Probabilidad (%)": 16.17},
    {"Fecha": "11/07", "Jugador": "Ejkar", "Probabilidad (%)": 12.34},
    {"Fecha": "11/07", "Jugador": "Vecina", "Probabilidad (%)": 10.77},
    {"Fecha": "11/07", "Jugador": "Miguel Ángel", "Probabilidad (%)": 10.74},
    {"Fecha": "11/07", "Jugador": "Juan", "Probabilidad (%)": 8.97},
    {"Fecha": "11/07", "Jugador": "Mírete", "Probabilidad (%)": 6.28},

    {"Fecha": "15/07", "Jugador": "Joaquín", "Probabilidad (%)": 18.73},
    {"Fecha": "15/07", "Jugador": "Telenti", "Probabilidad (%)": 12.93},
    {"Fecha": "15/07", "Jugador": "Sierra", "Probabilidad (%)": 17.92},
    {"Fecha": "15/07", "Jugador": "Ejkar", "Probabilidad (%)": 13.04},
    {"Fecha": "15/07", "Jugador": "Vecina", "Probabilidad (%)": 10.7},
    {"Fecha": "15/07", "Jugador": "Miguel Ángel", "Probabilidad (%)": 11.07},
    {"Fecha": "15/07", "Jugador": "Juan", "Probabilidad (%)": 8.92},
    {"Fecha": "15/07", "Jugador": "Mírete", "Probabilidad (%)": 6.69}
]

df_hist_previo = pd.DataFrame(datos_historicos)
df_hoy_linea = df_hoy[["Fecha", "Jugador", "Probabilidad (%)"]].copy()
df_historial_completo = pd.concat([df_hist_previo, df_hoy_linea], ignore_index=True)

# --- RENDERIZADO INTERFAZ STREAMLIT ---
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.subheader("📊 Tabla de Clasificación de la Porra (16/07)")
    df_mostrar = df_hoy.sort_values(by="Puntos Esperados", ascending=False)[["Jugador", "Equipos", "Futbolistas", "Puntos Apuesta", "Puntos Esperados", "Probabilidad (%)"]]
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🎯 Distribución Actual de Probabilidad (%)")
    fig_barras = px.bar(df_mostrar, x="Jugador", y="Probabilidad (%)", color="Jugador", text_auto=True)
    st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")
st.subheader("⏳ Evolución Temporal de la Porra")

fig_lineas = px.line(
    df_historial_completo, 
    x="Fecha", 
    y="Probabilidad (%)", 
    color="Jugador", 
    markers=True,
    category_orders={"Fecha": ["22/06", "02/07", "10/07", "11/07","15/07", "16/07"]}
)
fig_lineas.update_layout(xaxis_title="Fecha de Actualización", yaxis_title="Probabilidad de Victoria (%)")
st.plotly_chart(fig_lineas, use_container_width=True)


import streamlit as st
import random
import json
import os
import base64
from datetime import datetime

# ==============================================================================
# --- 📊 CONTROL DE JUGADORES POR JUEGO (INDEPENDIENTES) ---
# ==============================================================================
# Se ha añadido "joaquin" a la lista base
JUGADORES_BASE = ["telenti", "juan", "mirete", "carlos", "miguel angel", "sierra", "ejkar", "joaquin"]

# Asumimos que estas funciones existen en tu app principal, si no, darán error.
# Para esta demo, si no existen, creamos un mock vacío.
if 'listar_ganadores' not in globals():
    def listar_ganadores():
        return st.session_state.get('mock_ganadores', st.empty())
if 'guardar_ganador' not in globals():
    def guardar_ganador(nombre):
        if 'mock_ganadores_list' not in st.session_state:
            st.session_state['mock_ganadores_list'] = []
        st.session_state['mock_ganadores_list'].append(nombre)
        # Esto es solo para que el mock funcione en la demo
        import pandas as pd
        st.session_state['mock_ganadores'] = pd.DataFrame(st.session_state['mock_ganadores_list'], columns=['Ganador'])

df_ganadores = listar_ganadores()
registros_reales = []

# Intentamos obtener los valores si es un DataFrame, si no, asumimos lista vacía del mock inicial
try:
    if not df_ganadores.empty:
        registros_reales = [str(val).strip().lower() for val in df_ganadores.values.flatten()]
except:
    registros_reales = []

# 🧩 FILTRO SOPA: Desaparece si el nombre está tal cual
jugadores_sopa = [p for p in JUGADORES_BASE if p.lower() not in registros_reales]

# 🦖 FILTRO DINO: Desaparece si ya tiene una línea que empiece por su nombre + (dino:
jugadores_dino = [p for p in JUGADORES_BASE if not any(r.startswith(f"{p.lower()} (dino:") for r in registros_reales)]


# ==============================================================================
# --- 🧩 SOPA DE LETRAS INTERACTIVA ---
# ==============================================================================
st.markdown("---")
st.subheader("🧩 Sopa de Letras Interactiva: Encuentra los 20 Juanes")
st.write("Usa el **dedo** o el **ratón** para arrastrar sobre las letras en cualquier dirección. Si encuentras un **JUAN**, quedará redondeado en verde.")

@st.cache_data
def generar_sopa_juan_sin_clones():
    tam = 15
    grid = [['' for _ in range(tam)] for _ in range(tam)]
    word = "JUAN"
    direcciones = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
    
    random.seed(101) 
    
    colocados = 0
    intentos = 0
    juanes_coordenadas = []
    registro_coordenadas = set()
    
    while colocados < 20 and intentos < 4000:
        intentos += 1
        d = random.choice(direcciones)
        r = random.randint(0, tam - 1)
        c = random.randint(0, tam - 1)
        
        if (r, c, d) in registro_coordenadas:
            continue
            
        if 0 <= r + d[0]*3 < tam and 0 <= c + d[1]*3 < tam:
            viable = True
            for i in range(4):
                nr, nc = r + d[0]*i, c + d[1]*i
                if grid[nr][nc] != '' and grid[nr][nc] != word[i]:
                    viable = False
                    break
                    
            if viable:
                coords_palabra = []
                for i in range(4):
                    nr, nc = r + d[0]*i, c + d[1]*i
                    grid[nr][nc] = word[i]
                    coords_palabra.append({"r": nr, "c": nc})
                
                juanes_coordenadas.append(coords_palabra)
                registro_coordenadas.add((r, c, d))
                colocados += 1

    letras_relleno = "BCDEFGHIKLMNOPQRSTVXYZ"
    for r in range(tam):
        for c in range(tam):
            if grid[r][c] == '':
                grid[r][c] = random.choice(letras_relleno)
    return grid, juanes_coordenadas

grid_sopa, lista_juanes = generar_sopa_juan_sin_clones()

import streamlit.components.v1 as components

html_game = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0; padding: 5px; background-color: transparent;
        display: flex; flex-direction: column; align-items: center;
        user-select: none; -webkit-user-select: none;
    }}
    .header-box {{
        font-size: 18px; font-weight: bold; margin-bottom: 12px;
        color: #2ecc71; background: rgba(46, 204, 113, 0.15);
        padding: 8px 20px; border-radius: 30px; border: 1px solid rgba(46, 204, 113, 0.3);
    }}
    .grid-container {{
        width: 100%; max-width: 440px; aspect-ratio: 1;
        background: #1e1e24; padding: 8px; border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4); box-sizing: border-box;
    }}
    .grid {{
        display: grid; grid-template-columns: repeat(15, 1fr); grid-gap: 3px;
        width: 100%; height: 100%; touch-action: none;
    }}
    .cell {{
        aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-family: 'Courier New', Courier, monospace; font-size: 4vw;
        color: #ecf0f1; background: #2c3e50; border-radius: 4px;
        cursor: pointer; transition: background 0.1s, transform 0.05s;
    }}
    @media (min-width: 450px) {{
        .cell {{ font-size: 18px; }}
    }}
    .cell.dragging {{
        background: #3498db !important; color: #fff !important;
        border-radius: 50%; transform: scale(1.05);
    }}
    .cell.found {{
        background: #2ecc71 !important; color: #fff !important;
        border-radius: 50% !important;
        box-shadow: 0 0 6px #2ecc71;
    }}
    .win-banner {{
        display: none; margin-top: 15px; padding: 12px 20px;
        background: #27ae60; color: white; font-weight: bold;
        border-radius: 10px; font-size: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4); max-width: 420px;
    }}
</style>
</head>
<body>

<div class="header-box">🕵️‍♂️ Juanes Cazados: <span id="counter">0</span> / 20</div>
<div class="grid-container">
    <div class="grid" id="soup-grid"></div>
</div>
<div class="win-banner" id="win-banner">
    🎉 ¡BRUTAL! HAS CAZADO LOS 20 JUANES.<br>
    🔑 Código de Registro Secreto: <span style="font-family:monospace; background:#1b5e20; padding:2px 6px; border-radius:4px;">JUANETE!!</span>
</div>

<script>
    const gridData = {json.dumps(grid_sopa)};
    const targetWords = {json.dumps(lista_juanes)};
    
    let isDragging = false; let startCell = null; let currentEndCell = null; let foundIndexes = [];
    const gridContainer = document.getElementById('soup-grid');
    
    for(let r=0; r<15; r++) {{
        for(let c=0; c<15; c++) {{
            const cell = document.createElement('div');
            cell.className = 'cell'; cell.innerText = gridData[r][c];
            cell.setAttribute('data-r', r); cell.setAttribute('data-c', c);
            cell.id = `c-${{r}}-${{c}}`; gridContainer.appendChild(cell);
        }}
    }}
    
    gridContainer.addEventListener('mousedown', (e) => {{
        if(e.target.classList.contains('cell')) {{ isDragging = true; startCell = getCoords(e.target); currentEndCell = startCell; highlightCells(startCell, startCell); }}
    }});
    gridContainer.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        let el = document.elementFromPoint(e.clientX, e.clientY);
        if(el && el.classList.contains('cell')) {{ let cellCoords = getCoords(el); currentEndCell = cellCoords; highlightCells(startCell, cellCoords); }}
    }});
    window.addEventListener('mouseup', () => {{
        if (!isDragging) return; isDragging = false; checkWord(startCell, currentEndCell);
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
    }});
    gridContainer.addEventListener('touchstart', (e) => {{
        let touch = e.touches[0]; let el = document.elementFromPoint(touch.clientX, touch.clientY);
        if(el && el.classList.contains('cell')) {{ e.preventDefault(); isDragging = true; startCell = getCoords(el); currentEndCell = startCell; highlightCells(startCell, startCell); }}
    }}, {{passive: false}});
    gridContainer.addEventListener('touchmove', (e) => {{
        if (!isDragging) return; e.preventDefault(); let touch = e.touches[0]; let el = document.elementFromPoint(touch.clientX, touch.clientY);
        if(el && el.classList.contains('cell')) {{ let cellCoords = getCoords(el); currentEndCell = cellCoords; highlightCells(startCell, cellCoords); }}
    }}, {{passive: false}});
    gridContainer.addEventListener('touchend', (e) => {{
        if (!isDragging) return; isDragging = false; checkWord(startCell, currentEndCell);
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
    }}, {{passive: false}});

    function getCoords(el) {{ return {{ r: parseInt(el.getAttribute('data-r')), c: parseInt(el.getAttribute('data-c')) }}; }}
    function getLineCells(start, end) {{
        let dr = end.r - start.r; let dc = end.c - start.c; let steps = Math.max(Math.abs(dr), Math.abs(dc));
        if (steps !== 3) return null; if (dr !== 0 && dc !== 0 && Math.abs(dr) !== Math.abs(dc)) return null;
        let stepR = dr === 0 ? 0 : dr / steps; let stepC = dc === 0 ? 0 : dc / steps;
        let path = []; for(let i=0; i<=steps; i++) {{ path.push({{r: start.r + stepR*i, c: start.c + stepC*i}}); }}
        return path;
    }}
    function highlightCells(start, end) {{
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
        let path = getLineCells(start, end);
        if (path) {{ path.forEach(cell => {{ document.getElementById(`c-${{cell.r}}-${{cell.c}}`).classList.add('dragging'); }}); }}
        else {{ document.getElementById(`c-${{start.r}}-${{start.c}}`).classList.add('dragging'); }}
    }}
    function checkWord(start, end) {{
        if(!start || !end) return; let path = getLineCells(start, end); if (!path) return;
        for(let i=0; i<targetWords.length; i++) {{
            if (foundIndexes.includes(i)) continue;
            let target = targetWords[i]; let matchForward = true, matchBackward = true;
            for(let j=0; j<4; j++) {{
                if(path[j].r !== target[j].r || path[j].c !== target[j].c) matchForward = false;
                if(path[j].r !== target[3-j].r || path[j].c !== target[3-j].c) matchBackward = false;
            }}
            if (matchForward || matchBackward) {{
                foundIndexes.push(i); target.forEach(cell => {{ document.getElementById(`c-${{cell.r}}-${{cell.c}}`).classList.add('found'); }});
                document.getElementById('counter').innerText = foundIndexes.length;
                if (foundIndexes.length === 20) {{ document.getElementById('win-banner').style.display = 'block'; }}
                break;
            }}
        }}
    }}
</script>
</body>
</html>
"""

col_sopa, col_registro = st.columns([1.1, 0.9])
with col_sopa:
    components.html(html_game, height=560)

with col_registro:
    st.markdown("### 🏆 Canjear Código de Victoria")
    st.write("Introduce el código de la sopa para desbloquear el registro:")
    codigo_verificador = st.text_input("Código secreto:", type="password")
    
    if codigo_verificador.strip() == "JUANETE!!":
        st.success("🔓 ¡CÓDIGO VERIFICADO!")
        if jugadores_sopa:
            with st.form("salon_fama_form", clear_on_submit=True):
                # Desplegable de la sopa (incluye a Joaquin si no ha ganado)
                jugador_seleccionado = st.selectbox("¿Quién eres?", jugadores_sopa, key="sopa_user")
                enviar_nombre = st.form_submit_button("🥇 Inmortalizar mi Nombre")
                if enviar_nombre and jugador_seleccionado:
                    guardar_ganador(jugador_seleccionado)
                    st.success(f"¡Registrado {jugador_seleccionado}!")
                    st.rerun()
        else:
            st.warning("⚠️ Todos registrados en la sopa.")
    elif codigo_verificador:
        st.error("Código incorrecto.")

    st.markdown("---")
    st.markdown("### 🌟 Historial de Ganadores")
    try:
        if not df_ganadores.empty:
            st.dataframe(df_ganadores.sort_index(ascending=False), use_container_width=True, hide_index=True)
    except:
        pass


# ==============================================================================
# --- 🦖 MINIJUEGO: EL SALTO DEL MUNDIAL ---
# ==============================================================================
st.markdown("---")
st.subheader("🎮 Minijuego: El Salto del Mundial")
st.write("Esquiva las **tarjetas rojas (🟥)** y junta **copas (🏆)**. Salta con **ESPACIO**, **FLECHA ARRIBA** o **TOCANDO LA PANTALLA**.")

carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
# Asegúrate de tener una imagen 'jugador.png' o se usará el fallback de pelota
ruta_foto_jugador = os.path.join(carpeta_del_script, "jugador.png")

img_base64 = ""
if os.path.exists(ruta_foto_jugador):
    try:
        with open(ruta_foto_jugador, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8").replace("\n", "").replace("\r", "")
    except Exception as e:
        st.error(f"⚠️ Error de imagen: {e}")

html_dino = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{ margin: 0; padding: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; background-color: transparent; font-family: sans-serif; user-select: none; -webkit-user-select: none; touch-action: none; }}
    #game-container {{ width: 100%; max-width: 800px; height: 250px; background-color: #f7f7f7; border-bottom: 2px solid #535353; border-radius: 8px; position: relative; overflow: hidden; cursor: pointer; }}
    #player {{ width: 80px; height: 70px; position: absolute; bottom: 0; left: 50px; z-index: 10; }}
    #player-canvas {{ width: 100%; height: 100%; display: block; }}
    .obstacle {{ position: absolute; bottom: 0; z-index: 5; }}
    .cactus {{ width: 25px; height: 45px; background-color: #e74c3c; border-radius: 4px; }}
    .cactus::after {{ content: '🟥'; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 18px; }}
    .copa {{ width: 35px; height: 35px; bottom: 50px; }}
    .copa::after {{ content: '🏆'; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; }}
    #score-board {{ position: absolute; top: 10px; right: 20px; font-size: 20px; font-weight: bold; color: #535353; font-family: monospace; z-index: 15; }}
    
    #restart-message {{ 
        display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        text-align: center; background-color: rgba(0,0,0,0.9); color: white; padding: 15px 25px; border-radius: 12px; z-index: 20; 
    }}
    .save-btn {{
        background-color: #2ecc71; color: white; border: none; padding: 8px 16px; 
        border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: background 0.2s;
    }}
    .save-btn:hover {{ background-color: #27ae60; }}
    .jump {{ animation: jump 0.45s linear; }}
    @keyframes jump {{ 0% {{ bottom: 0; }} 30% {{ bottom: 130px; }} 70% {{ bottom: 130px; }} 100% {{ bottom: 0; }} }}
</style>
</head>
<body>

<div id="game-container">
    <div id="score-board">00000</div>
    <div id="player"><canvas id="player-canvas" width="100" height="100"></canvas></div>
    <div id="restart-message">
        <h2 style="margin:0 0 5px 0; color:#e74c3c;">GAME OVER</h2>
        <div id="final-score-text" style="font-weight:bold; margin-bottom:5px;">Puntos: 0</div>
        <button id="save-score-action" class="save-btn">💾 Enviar Puntos abajo</button>
        <p style="margin:8px 0 0 0; font-size:11px; color:#aaa;">O pulsa Espacio/Toca para reiniciar partida</p>
    </div>
</div>

<script>
    const player = document.getElementById("player");
    const canvas = document.getElementById("player-canvas");
    const ctx = canvas.getContext("2d");
    const container = document.getElementById("game-container");
    const scoreBoard = document.getElementById("score-board");
    const restartMessage = document.getElementById("restart-message");
    const finalScoreText = document.getElementById("final-score-text");
    const saveScoreAction = document.getElementById("save-score-action");
    
    let isJumping = false; let isGameOver = false; let score = 0; let gameSpeed = 6; let obstacleTimer; let scoreInterval;
    const b64Data = "{img_base64}"; const playerImg = new Image();
    if (b64Data && b64Data.length > 0) {{ playerImg.src = "data:image/png;base64," + b64Data; }}
    playerImg.onload = function() {{ dibujarAvatar(); }};
    playerImg.onerror = function() {{ dibujarFallback(); }};

    function dibujarAvatar() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(playerImg, 0, 0, canvas.width, canvas.height); }}
    function dibujarFallback() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = "#3498db"; ctx.beginPath(); ctx.arc(50, 50, 45, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = "#ffffff"; ctx.font = "bold 30px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("⚽", 50, 50); }}

    function jump(e) {{
        if (isGameOver) {{
            if(e.target && e.target.id === 'save-score-action') return;
            if (e.code === 'Space' || e.type === 'touchstart' || e.code === 'ArrowUp') {{ resetGame(); }}
            return;
        }}
        if (e.type === 'keydown' && e.code !== 'Space' && e.code !== 'ArrowUp') return;
        if (!isJumping) {{
            isJumping = true; player.classList.add("jump");
            setTimeout(() => {{ player.classList.remove("jump"); isJumping = false; }}, 450);
        }}
    }}

    document.addEventListener('keydown', jump);
    container.addEventListener('touchstart', jump);

    function createObstacle() {{
        if (isGameOver) return;
        const obstacle = document.createElement('div');
        const isCopa = Math.random() > 0.65;
        obstacle.classList.add('obstacle', isCopa ? 'copa' : 'cactus');
        let obstaclePos = container.offsetWidth;
        obstacle.style.left = obstaclePos + 'px';
        container.appendChild(obstacle);

        let moveInterval = setInterval(() => {{
            if (isGameOver) {{ clearInterval(moveInterval); return; }}
            obstaclePos -= gameSpeed; obstacle.style.left = obstaclePos + 'px';
            if (obstaclePos < -40) {{ clearInterval(moveInterval); obstacle.remove(); }}
            
            if (obstaclePos > 45 && obstaclePos < 95) {{
                let playerBottom = parseInt(window.getComputedStyle(player).getPropertyValue("bottom"));
                if (isCopa) {{
                    if (playerBottom + 50 >= 50 && playerBottom <= 85) {{
                        score += 50; scoreBoard.innerText = score.toString().padStart(5, '0');
                        clearInterval(moveInterval); obstacle.remove(); gameSpeed += 0.2;
                    }}
                }} else {{
                    if (playerBottom < 45) {{ gameOver(); }}
                }}
            }}
        }}, 10);

        let minTiempo = Math.max(600, 1000 - (gameSpeed * 40));
        let maxTiempo = Math.max(1200, 2000 - (gameSpeed * 60));
        obstacleTimer = setTimeout(createObstacle, Math.random() * (maxTiempo - minTiempo) + minTiempo);
    }}

    function startGame() {{
        isGameOver = false; score = 0; gameSpeed = 6; restartMessage.style.display = "none"; player.style.bottom = "0px"; scoreBoard.innerText = "00000";
        if (playerImg.complete && playerImg.naturalWidth !== 0) {{ dibujarAvatar(); }} else {{ dibujarFallback(); }}
        document.querySelectorAll('.obstacle').forEach(el => el.remove());
        scoreInterval = setInterval(() => {{ score += 1; scoreBoard.innerText = score.toString().padStart(5, '0'); if (score % 150 === 0) {{ gameSpeed += 0.5; }} }}, 100);
        createObstacle();
    }}

    function gameOver() {{
        isGameOver = true;
        player.classList.remove("jump");
        clearTimeout(obstacleTimer);
        clearInterval(scoreInterval);
        
        finalScoreText.innerText = "Has conseguido: " + score + " pts";
        restartMessage.style.display = "block";
        
        saveScoreAction.onclick = function(e) {{
            e.stopPropagation();
            let parentUrl = document.referrer.split('?')[0]; 
            window.open(parentUrl + '?game_score=' + score, '_blank');
        }};
    }}

    function resetGame() {{ startGame(); }}
    if (!b64Data || b64Data.length === 0) {{ dibujarFallback(); }}
    startGame();
</script>
</body>
</html>
"""

components.html(html_dino, height=280)


# ==============================================================================
# --- 🛠️ RECEPCIÓN DE MARCADORES AUTOMÁTICOS ---
# ==============================================================================
st.markdown("### 💾 Guardar Récord del Dino")

puntos_detectados = None
if "game_score" in st.query_params:
    try:
        puntos_detectados = int(st.query_params["game_score"])
    except ValueError:
        puntos_detectados = None

if puntos_detectados is not None:
    st.info(f"🎯 **¡Puntuación cargada con éxito!** Vas a registrar: **{puntos_detectados} puntos**")
    
    if jugadores_dino:
        with st.form("guardar_record_dino_auto", clear_on_submit=True):
            # Desplegable del dino (incluye a Joaquin si no tiene récord)
            jugador_seleccionado = st.selectbox("Selecciona tu nombre para inmortalizar la marca:", jugadores_dino, key="dino_user_final")
            submit_record = st.form_submit_button("🥇 Inmortalizar Récord y Hora")
            
            if submit_record and jugador_seleccionado:
                hora_actual = datetime.now().strftime("%H:%M:%S")
                nombre_registro = f"{jugador_seleccionado} (Dino: {puntos_detectados} pts a las {hora_actual})"
                
                guardar_ganador(nombre_registro)
                st.success(f"¡Récord guardado para {jugador_seleccionado}!")
                
                # Limpiar query params de forma compatible con Streamlit moderno
                st.query_params.clear()
                st.rerun()
                
        if st.button("❌ Descartar y limpiar"):
            st.query_params.clear()
            st.rerun()
    else:
        st.warning("⚠️ Todos los jugadores ya tienen un récord guardado.")
        if st.button("🔄 Limpiar URL"):
            st.query_params.clear()
            st.rerun()
else:
    st.caption("🏃‍♂️ Juega una partida. Al perder, pulsa el botón verde dentro del juego y este panel se activará solo con tus puntos.")



import streamlit as st
import streamlit.components.v1 as components

import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# --- 🎣 MINIJUEGO: LA PESCA DE JUAN (JUANPRONA REPLEGADO 60S + 50% VISIBLES) --
# ==============================================================================
st.markdown("---")
st.subheader("🎣 Minijuego: La Pesca de Juan")

img_base64_pesca = img_base64  # Asegúrate de tener definida esta variable previamente

html_pesca_template = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<style>
    body { margin: 0; padding: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; user-select: none; touch-action: none; background: #87CEEB; }
    #game-container { position: relative; width: 100%; max-width: 800px; margin: 0 auto; background: #000; }
    #game-canvas { background: linear-gradient(to bottom, #87CEEB 0%, #87CEEB 35%, #1E90FF 35%, #051937 100%); display: block; width: 100%; height: 500px; }
    #ui { position: absolute; top: 10px; left: 10px; color: white; text-shadow: 1px 1px 2px black; pointer-events: none; font-weight: bold; font-size: 13px; z-index: 10; }
    
    #fullscreen-btn {
        position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7);
        color: #ffeb3b; border: 2px solid #ffeb3b; padding: 6px 12px; border-radius: 20px;
        font-weight: bold; font-size: 11px; cursor: pointer; z-index: 50; display: block;
    }

    #giant-alert { 
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        color: white; font-size: 30px; font-weight: bold; text-align: center; 
        background: rgba(0, 0, 0, 0.95); padding: 35px; border-radius: 20px; 
        box-shadow: 0 0 30px rgba(255,255,255,0.4); display: none; z-index: 40; width: 85%; max-width: 600px;
        box-sizing: border-box; border: 4px solid #ffeb3b; line-height: 1.4;
    }
    
    #penalty-timer { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ff4444; font-size: 35px; font-weight: bold; display: none; text-align: center; background: rgba(0,0,0,0.85); padding: 20px; border-radius: 15px; z-index: 20; }
    #win-screen { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 25px; border-radius: 15px; text-align: center; display: none; box-shadow: 0 0 25px rgba(0,0,0,0.5); z-index: 30; }
    .btn { background: #2ecc71; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 12px; }
</style>
</head>
<body>

<div id="game-container">
    <button id="fullscreen-btn">📱 FULLSCREEN</button>

    <div id="ui">
        <div style="color: #ffeb3b; font-size: 12px; margin-bottom: 4px; background: rgba(0,0,0,0.4); padding: 4px 8px; border-radius: 4px;">
            🎮 <b>Muelle de Juan:</b> Pesca 10 Juanes. Evita tarjetas rojas. Usa las olas para frenar la patera. Ojo al radar del Juanprona.
        </div>
        <div>👤 Puntos Juan: <span id="score">0</span> / 10 <span id="acid-indicator" style="color:#2ecc71; font-weight:bold; display:none;">⚠️ LLUVIA ÁCIDA</span></div>
        <div>⏱️ Tiempo: <span id="clock">0.0</span>s</div>
        <div>🐟 Bultos: <span id="pop-count">0</span> / 20</div>
        <div id="instruction-text" style="color: #ffeb3b; margin-top: 2px;">Toca para fijar el ÁNGULO</div>
    </div>
    
    <div id="giant-alert"></div>
    <div id="penalty-timer">🟥 PENALIZACIÓN<br><span id="p-seconds">5</span>s</div>

    <div id="win-screen">
        <h2>🏆 ¡DESAFÍO COMPLETADO!</h2>
        <p id="final-time-text"></p>
        <button id="save-pesca-btn" class="btn">💾 Registrar Récord</button>
    </div>

    <canvas id="game-canvas"></canvas>
</div>

<script>
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('score');
    const clockEl = document.getElementById('clock');
    const popEl = document.getElementById('pop-count');
    const winScreen = document.getElementById('win-screen');
    const penaltyEl = document.getElementById('penalty-timer');
    const pSecondsEl = document.getElementById('p-seconds');
    const insText = document.getElementById('instruction-text');
    const giantAlert = document.getElementById('giant-alert');
    const fsBtn = document.getElementById('fullscreen-btn');
    const container = document.getElementById('game-container');
    const acidIndicator = document.getElementById('acid-indicator');

    let width = 800; let height = 500;
    
    function resizeGame() {
        if (document.fullscreenElement) {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.style.height = height + "px";
        } else {
            width = container.offsetWidth || 800;
            height = 500;
            canvas.style.height = "500px";
        }
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resizeGame);
    setTimeout(resizeGame, 150);

    fsBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        try {
            if (!document.fullscreenElement) {
                if (container.requestFullscreen) await container.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        } catch (err) { console.error(err); }
    });

    const juanImg = new Image(); let imageLoaded = false;
    juanImg.src = "data:image/png;base64,{{JUAN_IMAGE_BASE64}}";
    juanImg.onload = () => imageLoaded = true;

    let score = 0; let accumulatedTime = 0; let lastTimeCheck = Date.now(); let isGameOver = false;
    let penaltyTime = 0; let nPenalties = 0;
    let globalPauseUntil = 0;

    let inputState = 'angle'; 
    let angleParam = 0.5; 
    let angleSpeed = 0.035; 
    let fixedAngle = 0; let chargeForce = 0;
    
    // El JUANPRONA tiene un temporizador para volver a activarse
    let heli = { x: 100, y: 35, vx: 3, nextChange: 0, radarWidth: 90, active: true, reactiveTime: 0 };
    
    let patera = { 
        active: false, x: 0, y: 0, startX: 0, baseVx: 0, maxVx: 1.2,
        spawnTimer: Date.now() + 15000, direction: 'right',
        hitFlash: 0 
    };
    let waves = []; 
    let nextWaveSpawn = 0;

    let acidRainActive = false;
    let nextAcidEvent = Date.now() + 25000; 
    let acidEndTime = 0;
    let acidDrops = [];

    function triggerGiantAlert(message, borderColor = '#ffeb3b') {
        giantAlert.innerHTML = message.replace(/\\n/g, "<br>");
        giantAlert.style.borderColor = borderColor;
        giantAlert.style.display = 'block';
        globalPauseUntil = Date.now() + 2500; 
        setTimeout(() => { giantAlert.style.display = 'none'; }, 2500);
    }

    const TYPES = { JUAN: 'juan', BALL: 'ball', CARD: 'card' };
    let objects = [];

    function countType(t) { return objects.filter(o => o.type === t).length; }
    function countJuanines() { return objects.filter(o => o.type === TYPES.JUAN && o.isJuanin).length; }

    function spawnObject() {
        if (objects.length >= 20) return;
        
        let totalJuanesTarget = Math.round(objects.length * 0.30);
        let currentJuanes = countType(TYPES.JUAN);
        
        let type;
        if (currentJuanes < totalJuanesTarget || (objects.length === 0 && Math.random() < 0.30)) {
            type = TYPES.JUAN;
        } else {
            type = Math.random() < 0.5 ? TYPES.BALL : TYPES.CARD;
        }

        let assignJuanin = false;
        if (type === TYPES.JUAN) {
            let currentJuanines = countJuanines();
            if (currentJuanines < Math.round((currentJuanes + 1) * 0.70)) {
                assignJuanin = true;
            }
        }

        // Por defecto nacen con probabilidad 50%
        let isDiscovered = Math.random() >= 0.50; 
        let maxLifeTime = 25000 + Math.random() * 15000;
        let randomDepthPct = 0.45 + Math.random() * 0.45;

        objects.push({
            id: Math.random().toString(36),
            x: Math.random() * width,
            depthPercent: randomDepthPct,
            y: 0, type: type, isJuanin: assignJuanin,
            vx: (Math.random() - 0.5) * (type === TYPES.JUAN ? 8.0 : 4.5), ax: 0,
            depthSpeed: 0.02 + Math.random() * 0.03, depthAmp: 8 + Math.random() * 18, phase: Math.random() * Math.PI * 2,
            spawnTime: Date.now(), discovered: isDiscovered,
            lastDirectionChange: Date.now(), changeInterval: 300 + Math.random() * 600,
            deathTime: Date.now() + maxLifeTime
        });
    }

    for(let i=12; i>0; i--) spawnObject();
    let nextSpawnTime = Date.now() + 4000;

    let hook = { x: 0, y: 0, vx: 0, vy: 0, mode: 'straight', targetX: 0, targetY: 0 };

    function triggerAcidRainStrike() {
        acidRainActive = true;
        acidEndTime = Date.now() + 6000; 
        acidIndicator.style.display = 'inline';
        
        if (objects.length > 0) {
            let countToKill = Math.floor(objects.length * 0.5);
            objects.sort(() => Math.random() - 0.5);
            objects.splice(0, countToKill);
        }
        
        triggerGiantAlert("🌧️ ¡LLUVIA ÁCIDA COLOSAL!\\nEl 50% de los bultos marinos han sido disueltos.", "#2ecc71");
    }

    function update() {
        const now = Date.now();
        let deltaTime = now - lastTimeCheck;
        lastTimeCheck = now;

        if (isGameOver) return;

        let seaTopBoundary = height * 0.35; if(seaTopBoundary < 180) seaTopBoundary = 180;

        if (!acidRainActive && now > nextAcidEvent) {
            triggerAcidRainStrike();
        }
        if (acidRainActive && now > acidEndTime) {
            acidRainActive = false;
            acidIndicator.style.display = 'none';
            nextAcidEvent = now + 25000 + Math.random() * 15000;
        }
        if (acidRainActive && Math.random() < 0.5) {
            acidDrops.push({ x: Math.random() * width, y: 0, speed: 7 + Math.random() * 5 });
        }
        for (let d = acidDrops.length - 1; d >= 0; d--) {
            acidDrops[d].y += acidDrops[d].speed;
            if (acidDrops[d].y > height) acidDrops.splice(d, 1);
        }

        // CONTROL DEL JUANPRONA: Si está inactivo y pasó su tregua de 60s, vuelve
        if (!heli.active && now > heli.reactiveTime) {
            heli.active = true;
            heli.x = 100;
        }

        if (heli.active) {
            if (now > heli.nextChange) {
                heli.vx = (Math.random() > 0.5 ? 1 : -1) * (2 + Math.random() * 5);
                heli.nextChange = now + 600 + Math.random() * 1200;
            }
            heli.x += heli.vx;
            if (heli.x < 40) { heli.x = 40; heli.vx *= -1; }
            if (heli.x > width - 40) { heli.x = width - 40; heli.vx *= -1; }
        }

        if (!patera.active && now > patera.spawnTimer) {
            patera.active = true;
            patera.y = seaTopBoundary - 8;
            waves = []; 
            nextWaveSpawn = now + 1000; 
            
            if (Math.random() > 0.5) {
                patera.x = -45; patera.startX = -45; patera.baseVx = 0.55; 
                patera.direction = 'left'; 
                angleParam = Math.PI * 1.2; 
            } else {
                patera.x = width + 45; patera.startX = width + 45; patera.baseVx = -0.55; 
                patera.direction = 'right'; 
                angleParam = Math.PI * 1.7; 
            }
            triggerGiantAlert("⛵ ¡PATERA DETECTADA!\\nVelocidad progresiva suave hacia el centro. ¡Frénala!", "#f1c40f");
        }

        if (patera.active && now >= globalPauseUntil) {
            let center = width / 2;

            if (now > nextWaveSpawn) {
                waves.push({ x: center, y: seaTopBoundary, vx: patera.direction === 'left' ? -1.4 : 1.4, size: 7 });
                nextWaveSpawn = now + 5800; 
            }

            for (let w = waves.length - 1; w >= 0; w--) {
                let wave = waves[w]; wave.x += wave.vx; wave.size += 0.04; 
                let distanceToPatera = Math.abs(wave.x - patera.x);
                if (distanceToPatera < 15) {
                    let fixedPush = 25; 
                    if (patera.direction === 'left') patera.x = Math.max(patera.startX, patera.x - fixedPush);
                    else patera.x = Math.min(patera.startX, patera.x + fixedPush);
                    patera.hitFlash = now + 250; waves.splice(w, 1); continue;
                }
                if (wave.x < -60 || wave.x > width + 60) waves.splice(w, 1);
            }

            let distanceToCenter = Math.abs(center - patera.x);
            let maxDistance = Math.abs(center - patera.startX);
            let progress = 1 - (distanceToCenter / maxDistance); 
            
            let currentSpeed = patera.baseVx + (patera.maxVx * progress * Math.sign(patera.baseVx));
            patera.x += currentSpeed;
            
            if ((patera.baseVx > 0 && patera.x >= center) || (patera.baseVx < 0 && patera.x <= center)) {
                patera.active = false; waves = []; patera.spawnTimer = now + 45000; score = 0; scoreEl.innerText = score; 
                triggerGiantAlert("☠️ ¡LA PATERA ASALTÓ EL MUELLE!\\nHas perdido todos tus JUANES acumulados", "#e74c3c");
            }
        } else { waves = []; }

        if (now < globalPauseUntil) return; 

        if (penaltyTime > now) {
            penaltyEl.style.display = 'block'; pSecondsEl.innerText = Math.ceil((penaltyTime - now)/1000);
            inputState = 'angle'; return;
        } else { penaltyEl.style.display = 'none'; }
        
        accumulatedTime += deltaTime;
        clockEl.innerText = (accumulatedTime / 1000).toFixed(1);
        popEl.innerText = objects.length;

        if (inputState === 'angle') {
            angleParam += angleSpeed;
            if (patera.active) {
                if (patera.direction === 'left') {
                    let minLimit = Math.PI; let maxLimit = Math.PI * 1.5;
                    if (angleParam > maxLimit) { angleParam = maxLimit; angleSpeed *= -1; }
                    if (angleParam < minLimit) { angleParam = minLimit; angleSpeed *= -1; }
                } else {
                    let minLimit = Math.PI * 1.5; let maxLimit = Math.PI * 2;
                    if (angleParam > maxLimit) { angleParam = maxLimit; angleSpeed *= -1; }
                    if (angleParam < minLimit) { angleParam = minLimit; angleSpeed *= -1; }
                }
            } else {
                if (angleParam > Math.PI) { angleParam = Math.PI; angleSpeed *= -1; }
                if (angleParam < 0) { angleParam = 0; angleSpeed *= -1; }
            }
        }
        
        if (inputState === 'force') chargeForce = Math.min(chargeForce + 2.8, 100);

        if (now > nextSpawnTime) {
            if(objects.length < 20) spawnObject();
            nextSpawnTime = now + 3500;
        }

        // --- REGLAS ESTRICTAS DE PROPORCIONES ---
        let totalJuanesTarget = Math.round(objects.length * 0.30);
        let currentJuanes = countType(TYPES.JUAN);
        
        if (currentJuanes < totalJuanesTarget && objects.length > 0) {
            for (let o of objects) {
                if (o.type !== TYPES.JUAN) {
                    o.type = TYPES.JUAN;
                    currentJuanes++;
                    if (currentJuanes >= totalJuanesTarget) break;
                }
            }
        }
        
        let currentJuanesList = objects.filter(o => o.type === TYPES.JUAN);
        let expectedJuanines = Math.round(currentJuanesList.length * 0.70);
        let actualJuanines = countJuanines();

        if (actualJuanines < expectedJuanines) {
            for (let j of currentJuanesList) {
                if (!j.isJuanin) {
                    j.isJuanin = true;
                    actualJuanines++;
                    if (actualJuanines >= expectedJuanines) break;
                }
            }
        } else if (actualJuanines > expectedJuanines) {
            for (let j of currentJuanesList) {
                if (j.isJuanin) {
                    j.isJuanin = false;
                    actualJuanines--;
                    if (actualJuanines <= expectedJuanines) break;
                }
            }
        }

        // CORRECCIÓN: Como mínimo el 50% de bultos descubiertos siempre
        let totalDiscovered = objects.filter(o => o.discovered).length;
        let minimumRequired = Math.ceil(objects.length * 0.50);

        if (totalDiscovered < minimumRequired) {
            for (let o of objects) {
                if (!o.discovered) {
                    o.discovered = true;
                    totalDiscovered++;
                    if (totalDiscovered >= minimumRequired) break;
                }
            }
        }

        for (let i = objects.length - 1; i >= 0; i--) {
            let obj = objects[i];
            obj.x += obj.vx;
            if (obj.x < 0 || obj.x > width) obj.vx *= -1;
            
            let calculatedBaseY = height * obj.depthPercent;
            obj.phase += obj.depthSpeed; 
            obj.y = calculatedBaseY + Math.sin(obj.phase) * obj.depthAmp;

            if (now > obj.deathTime) {
                objects.splice(i, 1);
                spawnObject();
            }
        }

        if (inputState === 'launching') {
            if (hook.mode === 'parabolic') {
                hook.x += hook.vx; hook.vy += 0.42; hook.y += hook.vy;
                if (patera.active && Math.abs(hook.x - patera.x) < 28 && Math.abs(hook.y - patera.y) < 22) {
                    processPateraCatch(); return;
                }
                if (hook.y >= seaTopBoundary) {
                    hook.mode = 'straight'; hook.targetX = hook.x + hook.vx * 5; hook.targetY = height - 30;
                }
                if (hook.x < 0 || hook.x > width || hook.y > height) inputState = 'returning';
            } else {
                let dx = hook.targetX - hook.x; let dy = hook.targetY - hook.y; let dist = Math.sqrt(dx*dx + dy*dy);
                if (dist > 18) {
                    hook.x += (dx / dist) * 18; hook.y += (dy / dist) * 18;
                } else {
                    let targetHit = null; let hitIndex = -1;
                    for(let i=0; i<objects.length; i++) {
                        let o = objects[i]; let activeSize = o.discovered ? (o.isJuanin ? 15 : 28) : 28;
                        if (Math.sqrt((hook.x - o.x)**2 + (hook.y - o.y)**2) < activeSize) {
                            targetHit = o; hitIndex = i; break;
                        }
                    }
                    if (targetHit) processCatch(targetHit, hitIndex);
                    else inputState = 'returning';
                }
            }
        } else if (inputState === 'returning') {
            let dx = (width/2) - hook.x; let dy = (seaTopBoundary - 15) - hook.y; let dist = Math.sqrt(dx*dx + dy*dy);
            if (dist > 25) { hook.x += (dx / dist) * 25; hook.y += (dy / dist) * 25; } 
            else { inputState = 'angle'; if (angleParam > Math.PI) angleParam = (patera.direction === 'left') ? Math.PI * 1.2 : Math.PI * 1.7; }
        }
    }

    // CORRECCIÓN: El JUANPRONA se retira de la pantalla durante los 60s de la tramitación
    function processPateraCatch() {
        patera.active = false; 
        waves = []; 
        patera.spawnTimer = Date.now() + 60000; 
        
        heli.active = false; 
        heli.reactiveTime = Date.now() + 60000; 
        
        inputState = 'returning';
        
        // MODIFICACIÓNaquí: Ahora solo se suman 2 puntos fijos
        score += 2; 
        scoreEl.innerText = score;
        
        triggerGiantAlert("🚔 ¡EL JUANPRONA SE LLEVA LA PATERA!\\nTramitando la detención en comisaría. ¡Suman +2 PUNTOS fijos! 60s de tregua.", "#3498db");
        if (score >= 10) { isGameOver = true; setTimeout(win, 100); }
    }

    function processCatch(obj, index) {
        objects.splice(index, 1); spawnObject(); inputState = 'returning';
        if (obj.type === TYPES.JUAN) {
            if (obj.isJuanin) {
                let xMinRadar = heli.x - heli.radarWidth; let xMaxRadar = heli.x + heli.radarWidth;
                if (heli.active && width/2 >= xMinRadar && width/2 <= xMaxRadar) {
                    let perdidos = Math.floor(score * 0.75); score -= perdidos; if (score < 0) score = 0;
                    scoreEl.innerText = score;
                    triggerGiantAlert("🚨 ¡MULTAZO DEL JUANPRONA!\\nTe multan por un Juanín bajo el foco radar. -75%", "#e74c3c");
                } else {
                    score += 2; scoreEl.innerText = score;
                    triggerGiantAlert("👶 ¡JUANÍN EXTRAÍDO!\\nFurtivo absoluto, +2 Puntos", "#f39c12");
                }
            } else {
                score++; scoreEl.innerText = score;
                triggerGiantAlert("👤 ¡JUAN ADULTO CAPTURADO!\\n+1 Punto", "#2ecc71");
            }
            if (score >= 10) { isGameOver = true; setTimeout(win, 100); }
        } else if (obj.type === TYPES.CARD) {
            nPenalties++; let extraSeconds = 4 + nPenalties; accumulatedTime += (extraSeconds * 1000); 
            penaltyTime = Date.now() + (extraSeconds * 1000);
            triggerGiantAlert("🟥 ¡TARJETA ROJA!\\n+" + extraSeconds + "s de penalización", "#ff4444");
        } else { triggerGiantAlert("⚽ ¡PELOTA DE FÚTBOL!\\nLimpieza marina", "#3498db"); }
    }

    function win() {
        if (document.fullscreenElement) document.exitFullscreen();
        winScreen.style.display = 'block';
        document.getElementById('final-time-text').innerText = "¡Completado en " + (accumulatedTime/1000).toFixed(2) + "s!";
    }

    function draw() {
        update(); ctx.clearRect(0, 0, width, height);
        let seaLine = height * 0.35; if(seaLine < 180) seaLine = 180;

        ctx.fillStyle = acidRainActive ? '#4d603a' : '#70b5d3'; 
        ctx.fillRect(0, 0, width, seaLine);
        
        let seaGrad = ctx.createLinearGradient(0, seaLine, 0, height);
        seaGrad.addColorStop(0, acidRainActive ? '#0e2b14' : '#1E90FF');
        seaGrad.addColorStop(1, '#051937');
        ctx.fillStyle = seaGrad; ctx.fillRect(0, seaLine, width, height - seaLine);

        if (acidRainActive) {
            ctx.strokeStyle = 'rgba(150, 240, 50, 0.4)'; ctx.lineWidth = 1.5;
            acidDrops.forEach(d => {
                ctx.beginPath(); ctx.moveTo(d.x, d.y); ctx.lineTo(d.x - 1, d.y + 9); ctx.stroke();
            });
        }

        waves.forEach(wave => {
            ctx.strokeStyle = acidRainActive ? 'rgba(150, 240, 50, 0.5)' : 'rgba(255, 255, 255, 0.75)';
            ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(wave.x, wave.y + 4, wave.size, Math.PI, 0, false); ctx.stroke();
        });

        // Solo dibuja el helicóptero si está activo en pantalla
        if (heli.active) {
            ctx.fillStyle = 'rgba(255, 235, 59, 0.14)'; ctx.beginPath(); ctx.moveTo(heli.x, heli.y + 10);
            ctx.lineTo(heli.x - heli.radarWidth, seaLine); ctx.lineTo(heli.x + heli.radarWidth, seaLine); ctx.closePath(); ctx.fill();
            ctx.fillStyle = '#1e3f20'; ctx.fillRect(heli.x - 22, heli.y - 10, 44, 20);
            ctx.fillStyle = '#000'; ctx.fillRect(heli.x - 32, heli.y - 12, 64, 3);
            ctx.font = "10px sans-serif"; ctx.fillStyle = '#fff'; ctx.fillText("🚁 JUANPRONA", heli.x - 35, heli.y - 18);
        }

        if (patera.active) {
            ctx.fillStyle = (Date.now() < patera.hitFlash) ? '#00e5ff' : '#7e5129'; 
            ctx.beginPath(); ctx.moveTo(patera.x - 22, patera.y); ctx.lineTo(patera.x + 22, patera.y);
            ctx.lineTo(patera.x + 14, patera.y + 14); ctx.lineTo(patera.x - 14, patera.y + 14); ctx.closePath(); ctx.fill();
        }

        objects.forEach(obj => {
            let renderSize = obj.discovered ? (obj.isJuanin ? 15 : 28) : 28;
            let lifeLeft = obj.deathTime - Date.now();
            ctx.beginPath(); ctx.arc(obj.x, obj.y, renderSize, 0, Math.PI*2);
            
            if (lifeLeft < 5000 && Math.floor(Date.now() / 250) % 2 === 0) {
                ctx.fillStyle = 'rgba(110, 110, 110, 0.6)';
            } else {
                ctx.fillStyle = obj.discovered ? 'rgba(30, 85, 145, 0.9)' : 'rgba(24, 48, 89, 0.95)';
            }
            ctx.fill();
            ctx.strokeStyle = (obj.discovered && obj.isJuanin) ? '#ffeb3b' : 'rgba(255,255,255,0.4)';
            ctx.lineWidth = 1.5; ctx.stroke();
            
            if (obj.discovered && imageLoaded && obj.type === TYPES.JUAN) {
                ctx.save(); ctx.beginPath(); ctx.arc(obj.x, obj.y, renderSize - 2, 0, Math.PI*2); ctx.clip();
                let dim = obj.isJuanin ? 30 : 54; ctx.drawImage(juanImg, obj.x - dim/2, obj.y - dim/2, dim, dim); ctx.restore();
            } else if (obj.discovered) {
                ctx.fillStyle = '#fff'; ctx.font = "bold 16px sans-serif";
                ctx.fillText(obj.type === TYPES.CARD ? '🟥' : '⚽', obj.x - 8, obj.y + 6);
            } else {
                ctx.fillStyle = '#fff'; ctx.font = "bold 15px sans-serif"; ctx.fillText("❓", obj.x - 6, obj.y + 5);
            }
        });

        ctx.fillStyle = '#5c3a21'; ctx.fillRect(width/2 - 35, seaLine - 15, 70, 15);
        if (imageLoaded) ctx.drawImage(juanImg, width/2 - 22, seaLine - 72, 44, 60);

        let radarRadius = 55; let radarX = width/2; let radarY = seaLine - 15;
        ctx.beginPath();
        if (patera.active) {
            if (patera.direction === 'left') ctx.arc(radarX, radarY, radarRadius, Math.PI, Math.PI * 1.5, false);
            else ctx.arc(radarX, radarY, radarRadius, Math.PI * 1.5, Math.PI * 2, false);
        } else {
            ctx.arc(radarX, radarY, radarRadius, 0, Math.PI, false);
        }
        ctx.strokeStyle = 'rgba(255,235,59,0.6)'; ctx.lineWidth = 2.5; ctx.stroke();

        let ballX = radarX + Math.cos(angleParam) * radarRadius;
        let ballY = radarY + Math.sin(angleParam) * radarRadius;
        ctx.beginPath(); ctx.moveTo(radarX, radarY); ctx.lineTo(ballX, ballY);
        ctx.strokeStyle = '#ffeb3b'; ctx.lineWidth = 2.5; ctx.stroke();
        ctx.beginPath(); ctx.arc(ballX, ballY, 6, 0, Math.PI*2);
        ctx.fillStyle = (inputState === 'angle') ? '#ffeb3b' : '#2ecc71'; ctx.fill();

        if (inputState === 'force') {
            ctx.fillStyle = '#e74c3c'; ctx.fillRect(width/2 - 50, seaLine - 110, chargeForce, 10);
            ctx.strokeStyle = '#fff'; ctx.strokeRect(width/2 - 50, seaLine - 110, 100, 10);
        }

        if (inputState === 'launching' || inputState === 'returning') {
            ctx.beginPath(); ctx.moveTo(width/2, seaLine - 15); ctx.lineTo(hook.x, hook.y);
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.stroke();
            ctx.beginPath(); ctx.arc(hook.x, hook.y, 6, 0, Math.PI*2); ctx.fillStyle = '#e74c3c'; ctx.fill();
        }

        requestAnimationFrame(draw);
    }

    function handleActionStart() {
        if (isGameOver || Date.now() < penaltyTime || Date.now() < globalPauseUntil) return;
        if (inputState === 'angle') { fixedAngle = angleParam; inputState = 'force'; chargeForce = 0; }
    }

    function handleActionEnd() {
        if (inputState === 'force') {
            inputState = 'launching';
            let seaLineBound = height * 0.35; if(seaLineBound < 180) seaLineBound = 180;
            
            if (fixedAngle >= Math.PI && patera.active) {
                hook.mode = 'parabolic';
                let initialVelocity = 4 + (chargeForce / 100) * 14; 
                hook.vx = Math.cos(fixedAngle) * initialVelocity; hook.vy = Math.sin(fixedAngle) * initialVelocity; 
            } else {
                hook.mode = 'straight';
                let maxReach = Math.sqrt((width/2)**2 + height**2) * 0.95;
                let currentReach = (chargeForce / 100) * maxReach;
                hook.targetX = (width/2) + Math.cos(fixedAngle) * currentReach;
                hook.targetY = seaLineBound + Math.abs(Math.sin(fixedAngle) * currentReach);
                if (hook.targetX < 0) hook.targetX = 15; if (hook.targetX > width) hook.targetX = width - 15;
                if (hook.targetY > height) hook.targetY = height - 20;
            }
            hook.x = width / 2; hook.y = seaLineBound - 15;
        }
    }

    container.addEventListener('mousedown', (e) => { if(e.target.id !== 'fullscreen-btn') handleActionStart(); });
    window.addEventListener('mouseup', handleActionEnd);
    container.addEventListener('touchstart', (e) => { if(e.target.id !== 'fullscreen-btn') handleActionStart(); }, {passive: true});
    window.addEventListener('touchend', handleActionEnd);

    draw();
</script>
</body>
</html>
"""

html_pesca = html_pesca_template.replace("{{JUAN_IMAGE_BASE64}}", img_base64_pesca)
components.html(html_pesca, height=520)
