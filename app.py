import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import csv

# Configuración de la interfaz de Streamlit
st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra (Modelo No Acumulativo)")
st.write(f"Última actualización de cuotas reales: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

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

porra_futbolistas = {
    'Sierra': {'Kane': 2, 'Julián Álvarez': 0},
    'Joaquín': {'Messi': 5, 'Olise': 0},
    'Ejkar': {'Lautaro': 0, 'Raphinha': 0},
    'Vecina': {'Havertz': 2, 'Lamine Yamal': 1},
    'Telenti': {'Endrick': 0, 'Ramos': 0},
    'Miguel Ángel': {'Haaland': 4, 'Embolo': 1},
    'Mírete': {'Oyarzabal': 2, 'El Bicho': 2}, 
    'Juan': {'Mbappé': 4, 'Vinicius': 4}
}

puntos_futbolistas_actuales = {jugador: sum(datos.values()) if isinstance(datos, dict) else 0 
                               for jugador, datos in porra_futbolistas.items()}

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

# --- CUOTAS EXTRAÍDAS FIELMENTE DE LAS CAPTURAS DE PANTALLA (Actualizadas al 25/06) ---
cuotas_octavos = {
    'Francia': 1.13, 'Argentina': 1.17, 'Inglaterra': 1.19, 'España': 1.19, 'Alemania': 1.27, 
    'Portugal': 1.33, 'Canadá': 1.34, 'Brasil': 1.40, 'Noruega': 1.44, 'Suiza': 1.50, 
    'Países Bajos': 1.53, 'México': 1.53, 'Colombia': 1.60, 'Bélgica': 1.70, 'Marruecos': 1.95, 
    'Japón': 2.10, 'Croacia': 2.30, 'Egipto': 2.50, 'Costa de Marfil': 2.60, 'Corea del Sur': 2.75, 
    'Australia': 3.00, 'Austria': 3.00, 'Senegal': 3.00, 'Ghana': 3.25, 'Sudáfrica': 3.25, 
    'Paraguay': 3.50, 'Suecia': 3.50, 'Argelia': 4.00, 'Bosnia y Herzegovina': 4.00, 'Uruguay': 4.75, 
    'Irán': 5.00, 'Cabo Verde': 7.00, 'RD Congo': 7.00, 'Ecuador': 7.00, 'Arabia Saudita': 10.00, 
    'Escocia': 11.00, 'Nueva Zelanda': 26.00, 'Uzbekistán': 29.00, 'Curazao': 34.00, 'Irak': 51.00, 
    'EE. UU.': 1.33, 'Turquía': float('inf')
}

cuotas_cuartos = {
    'Argentina': 1.44, 'Francia': 1.47, 'Inglaterra': 1.57, 'España': 1.57, 'Portugal': 1.95, 
    'EE. UU.': 2.10, 'Brasil': 2.20, 'Países Bajos': 2.20, 'Alemania': 2.30, 'Noruega': 2.75, 
    'Colombia': 3.25, 'Marruecos': 3.25, 'México': 3.75, 'Bélgica': 3.75, 'Japón': 3.75, 
    'Suiza': 3.75, 'Canadá': 4.33, 'Croacia': 6.00, 'Egipto': 7.00, 'Corea del Sur': 7.50, 
    'Costa de Marfil': 7.50, 'Senegal': 7.50, 'Australia': 8.00, 'Austria': 8.00, 'Suecia': 9.00, 
    'Uruguay': 10.00, 'Ghana': 11.00, 'Argelia': 13.00, 'Bosnia y Herzegovina': 13.00, 'Sudáfrica': 13.00, 
    'Ecuador': 15.00, 'Paraguay': 15.00, 'Escocia': 21.00, 'Irán': 21.00, 'Cabo Verde': 29.00, 
    'RD Congo': 29.00, 'Arabia Saudita': 41.00, 'Nueva Zelanda': 51.00, 'Irak': 67.00, 
    'Uzbekistán': 81.00, 'Curazao': 101.00, 'Turquía': float('inf')
}

cuotas_semis = {
    'Francia': 2.10, 'Argentina': 2.20, 'España': 2.25, 'Inglaterra': 2.60, 'Portugal': 3.25, 
    'Brasil': 3.50, 'Alemania': 3.75, 'Países Bajos': 4.00, 'EE. UU.': 5.00, 'Noruega': 5.50, 
    'México': 7.00, 'Marruecos': 7.00, 'Bélgica': 8.00, 'Colombia': 8.00, 'Japón': 8.00, 
    'Suiza': 10.00, 'Croacia': 17.00, 'Canadá': 17.00, 'Senegal': 19.00, 'Austria': 21.00, 
    'Costa de Marfil': 21.00, 'Uruguay': 23.00, 'Egipto': 23.00, 'Australia': 26.00, 'Suecia': 26.00, 
    'Ecuador': 34.00, 'Corea del Sur': 34.00, 'Paraguay': 41.00, 'Argelia': 41.00, 'Ghana': 41.00, 
    'Sudáfrica': 51.00, 'Bosnia y Herzegovina': 51.00, 'Escocia': 81.00, 'Irán': 81.00, 'Cabo Verde': 101.00, 
    'RD Congo': 101.00, 'Arabia Saudita': 151.00, 'Nueva Zelanda': 201.00, 'Uzbekistán': 251.00, 
    'Irak': 251.00, 'Curazao': 401.00, 'Turquía': float('inf')
}

cuotas_final = {
    'Francia': 2.87, 'España': 3.50, 'Argentina': 3.75, 'Inglaterra': 4.00, 'Portugal': 5.50, 
    'Brasil': 6.00, 'Alemania': 7.00, 'Países Bajos': 8.00, 'Noruega': 13.00, 'EE. UU.': 15.00, 
    'México': 15.00, 'Marruecos': 15.00, 'Colombia': 17.00, 'Japón': 17.00, 'Bélgica': 21.00, 
    'Suiza': 26.00, 'Croacia': 34.00, 'Canadá': 41.00, 'Austria': 51.00, 'Senegal': 51.00, 
    'Costa de Marfil': 51.00, 'Uruguay': 67.00, 'Australia': 67.00, 'Egipto': 67.00, 'Suecia': 67.00, 
    'Ecuador': 81.00, 'Paraguay': 101.00, 'Ghana': 126.00, 'Argelia': 126.00, 'Corea del Sur': 151.00, 
    'Sudáfrica': 151.00, 'Bosnia y Herzegovina': 151.00, 'Escocia': 201.00, 'Irán': 251.00, 
    'Cabo Verde': 301.00, 'Nueva Zelanda': 301.00, 'RD Congo': 301.00, 'Arabia Saudita': 401.00, 
    'Uzbekistán': 501.00, 'Irak': 751.00, 'Curazao': 1001.00, 'Turquía': float('inf')
}

cuotas_ganador = {
    'Francia': 4.75, 'España': 6.50, 'Argentina': 7.00, 'Inglaterra': 7.50, 'Portugal': 10.00, 
    'Brasil': 11.00, 'Alemania': 13.00, 'Países Bajos': 15.00, 'Noruega': 29.00, 'EE. UU.': 29.00, 
    'Marruecos': 29.00, 'México': 34.00, 'Japón': 34.00, 'Colombia': 41.00, 'Bélgica': 51.00, 
    'Suiza': 67.00, 'Croacia': 101.00, 'Uruguay': 101.00, 'Costa de Marfil': 101.00, 'Suecia': 101.00, 
    'Canadá': 126.00, 'Austria': 126.00, 'Australia': 126.00, 'Senegal': 126.00, 'Paraguay': 201.00, 
    'Egipto': 201.00, 'Ecuador': 251.00, 'Sudáfrica': 251.00, 'Bosnia y Herzegovina': 301.00, 'Corea del Sur': 301.00, 
    'Ghana': 301.00, 'RD Congo': 401.00, 'Argelia': 501.00, 'Irán': 501.00, 'Nueva Zelanda': 501.00, 
    'Cabo Verde': 501.00, 'Escocia': 751.00, 'Arabia Saudita': 751.00, 'Uzbekistán': 1001.00, 
    'Irak': 1001.00, 'Curazao': 2001.00, 'Turquía': float('inf')
}

# --- CÓMPUTO MATEMÁTICO NO ACUMULATIVO ---
todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades_fase_maxima = {}

for eq in todos_equipos:
    n = traduccion_interna.get(eq, eq)
    
    p_oct = 1 / float(cuotas_octavos[n]) if cuotas_octavos[n] != float('inf') else 0.0
    p_cua = 1 / float(cuotas_cuartos[n]) if cuotas_cuartos[n] != float('inf') else 0.0
    p_sem = 1 / float(cuotas_semis[n]) if cuotas_semis[n] != float('inf') else 0.0
    p_fin = 1 / float(cuotas_final[n]) if cuotas_final[n] != float('inf') else 0.0
    p_gan = 1 / float(cuotas_ganador[n]) if cuotas_ganador[n] != float('inf') else 0.0

    # Lógica de exclusión mutua para fases exactas
    p_exacta_oct = max(0.0, p_oct - p_cua)
    p_exacta_cua = max(0.0, p_cua - p_sem)
    p_exacta_sem = max(0.0, p_sem - p_fin)
    p_exacta_fin = max(0.0, p_fin - p_gan)
    p_exacta_gan = p_gan

    puntos_esperados = (10 * p_exacta_oct) + (12 * p_exacta_cua) + (15 * p_exacta_sem) + (18 * p_exacta_fin) + (20 * p_exacta_gan)
    probabilidades_fase_maxima[eq] = puntos_esperados

# Filas calculadas para hoy (25/06)
filas_hoy = []
for jugador, equipos in porra.items():
    puntos_selecciones = sum([probabilidades_fase_maxima.get(e, 0.0) for e in equipos])
    puntos_totales = puntos_selecciones + puntos_futbolistas_actuales.get(jugador, 0)
    filas_hoy.append({
        "Fecha": "25/06",
        "Jugador": jugador,
        "Equipos": ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos]),
        "Futbolistas": ", ".join([f"{f} ({pts})" for f, pts in porra_futbolistas.get(jugador, {}).items()]),
        "Puntos Esperados": round(puntos_totales, 2)
    })

df_hoy = pd.DataFrame(filas_hoy)
total_puntos_global = df_hoy["Puntos Esperados"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos Esperados"] / (total_puntos_global if total_puntos_global > 0 else 1)) * 100, 2)

# --- RECONSTRUCCIÓN CRONOLÓGICA DEL HISTORIAL ---
datos_22_junio = [
    {"Fecha": "22/06", "Jugador": "Joaquín", "Probabilidad (%)": 14.34},
    {"Fecha": "22/06", "Jugador": "Miguel Ángel", "Probabilidad (%)": 13.99},
    {"Fecha": "22/06", "Jugador": "Sierra", "Probabilidad (%)": 13.06},
    {"Fecha": "22/06", "Jugador": "Mírete", "Probabilidad (%)": 13.02},
    {"Fecha": "22/06", "Jugador": "Ejkar", "Probabilidad (%)": 12.87},
    {"Fecha": "22/06", "Jugador": "Telenti", "Probabilidad (%)": 12.21},
    {"Fecha": "22/06", "Jugador": "Juan", "Probabilidad (%)": 10.31},
    {"Fecha": "22/06", "Jugador": "Vecina", "Probabilidad (%)": 10.20}
]

datos_23_junio = [
    {"Fecha": "23/06", "Jugador": "Joaquín", "Probabilidad (%)": 15.08},
    {"Fecha": "23/06", "Jugador": "Miguel Ángel", "Probabilidad (%)": 14.77},
    {"Fecha": "23/06", "Jugador": "Sierra", "Probabilidad (%)": 12.64},
    {"Fecha": "23/06", "Jugador": "Ejkar", "Probabilidad (%)": 12.50},
    {"Fecha": "23/06", "Jugador": "Telenti", "Probabilidad (%)": 12.44},
    {"Fecha": "23/06", "Jugador": "Mírete", "Probabilidad (%)": 12.10},
    {"Fecha": "23/06", "Jugador": "Juan", "Probabilidad (%)": 10.74},
    {"Fecha": "23/06", "Jugador": "Vecina", "Probabilidad (%)": 9.73}
]

datos_24_junio = [
    {"Fecha": "24/06", "Jugador": "Joaquín", "Probabilidad (%)": 14.87},
    {"Fecha": "24/06", "Jugador": "Miguel Ángel", "Probabilidad (%)": 14.42},
    {"Fecha": "24/06", "Jugador": "Sierra", "Probabilidad (%)": 12.75},
    {"Fecha": "24/06", "Jugador": "Mírete", "Probabilidad (%)": 12.68},
    {"Fecha": "24/06", "Jugador": "Ejkar", "Probabilidad (%)": 12.35},
    {"Fecha": "24/06", "Jugador": "Telenti", "Probabilidad (%)": 12.11},
    {"Fecha": "24/06", "Jugador": "Juan", "Probabilidad (%)": 11.40},
    {"Fecha": "24/06", "Jugador": "Vecina", "Probabilidad (%)": 9.42}
]

df_22 = pd.DataFrame(datos_22_junio)
df_23 = pd.DataFrame(datos_23_junio)
df_24 = pd.DataFrame(datos_24_junio)
df_25 = df_hoy[["Fecha", "Jugador", "Probabilidad (%)"]].copy()

# Unión de la línea temporal completa
df_historial_completo = pd.concat([df_22, df_23, df_24, df_25], ignore_index=True)

# --- RENDERIZADO INTERFAZ STREAMLIT ---
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.subheader("📊 Tabla de Clasificación de la Porra (Hoy 25/06)")
    df_mostrar = df_hoy.sort_values(by="Puntos Esperados", ascending=False)[["Jugador", "Equipos", "Futbolistas", "Puntos Esperados", "Probabilidad (%)"]]
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
    category_orders={"Fecha": ["22/06", "23/06", "24/06", "25/06"]}
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



# ==============================================================================
# --- 🎣 MINIJUEGO: LA PESCA DE JUAN (EDICIÓN MÓVIL FULLSCREEN & RADAR) ---
# ==============================================================================
st.markdown("---")
st.subheader("🎣 Minijuego: La Pesca de Juan ")
st.write("Pesca **10 Juanes**. En móvil, pulsa el botón para jugar de forma óptima en horizontal.")

img_base64_pesca = img_base64 

html_pesca = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<style>
    body {{ margin: 0; padding: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; user-select: none; touch-action: none; background: #87CEEB; }}
    #game-container {{ position: relative; width: 100%; max-width: 800px; margin: 0 auto; background: #000; }}
    #game-canvas {{ background: linear-gradient(to bottom, #87CEEB 0%, #87CEEB 35%, #1E90FF 35%, #051937 100%); display: block; width: 100%; height: 500px; }}
    #ui {{ position: absolute; top: 10px; left: 10px; color: white; text-shadow: 1px 1px 2px black; pointer-events: none; font-weight: bold; font-size: 13px; z-index: 10; }}
    
    /* Botón Móvil Pantalla Completa / Horizontal */
    #fullscreen-btn {{
        position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7);
        color: #ffeb3b; border: 2px solid #ffeb3b; padding: 6px 12px; border-radius: 20px;
        font-weight: bold; font-size: 11px; cursor: pointer; z-index: 50; display: block;
    }}

    /* Cartel cinematográfico gigante */
    #giant-alert {{ 
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        color: white; font-size: 36px; font-weight: bold; text-align: center; 
        background: rgba(0, 0, 0, 0.95); padding: 40px; border-radius: 20px; 
        box-shadow: 0 0 30px rgba(255,255,255,0.4); display: none; z-index: 40; width: 85%; max-width: 600px;
        box-sizing: border-box; border: 4px solid #ffeb3b; line-height: 1.4;
    }}
    
    #penalty-timer {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ff4444; font-size: 35px; font-weight: bold; display: none; text-align: center; background: rgba(0,0,0,0.85); padding: 20px; border-radius: 15px; z-index: 20; }}
    #win-screen {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 25px; border-radius: 15px; text-align: center; display: none; box-shadow: 0 0 25px rgba(0,0,0,0.5); z-index: 30; }}
    .btn {{ background: #2ecc71; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 12px; }}
</style>
</head>
<body>

<div id="game-container">
    <button id="fullscreen-btn">📱 FULLSCREEN + HORIZONTAL</button>

    <div id="ui">
        <div>👤 Juanes: <span id="score">0</span> / 10</div>
        <div>⏱️ Tiempo: <span id="clock">0.0</span>s</div>
        <div>🐟 Bultos: <span id="pop-count">0</span></div>
        <div id="instruction-text" style="color: #ffeb3b; margin-top: 5px;">Toca para fijar el ÁNGULO</div>
    </div>
    
    <div id="giant-alert"></div>
    <div id="penalty-timer">🟥 PENALIZACIÓN<br><span id="p-seconds">5</span>s</div>

    <div id="win-screen">
        <h2>🏆 ¡PESCA COMPLETADA!</h2>
        <p id="final-time-text"></p>
        <button id="save-pesca-btn" class="btn">💾 Registrar Tiempo</button>
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

    let width = 800; let height = 500;
    
    function resizeGame() {{
        if (document.fullscreenElement) {{
            // Modo Pantalla Completa Móvil
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.style.height = height + "px";
        }} else {{
            // Modo Streamlit estándar
            width = container.offsetWidth || 800;
            height = 500;
            canvas.style.height = "500px";
        }}
        canvas.width = width;
        canvas.height = height;
    }}
    window.addEventListener('resize', resizeGame);
    setTimeout(resizeGame, 150);

    // Activación Fullscreen + Bloqueo de Orientación Horizontal
    fsBtn.addEventListener('click', async (e) => {{
        e.stopPropagation();
        try {{
            if (!document.fullscreenElement) {{
                if (container.requestFullscreen) {{
                    await container.requestFullscreen();
                }} else if (container.webkitRequestFullscreen) {{
                    await container.webkitRequestFullscreen();
                }}
                
                // Intentar forzar rotación a horizontal
                if (screen.orientation && screen.orientation.lock) {{
                    await screen.orientation.lock('landscape').catch(err => {{
                        console.log("Rotación automática no permitida sin gestos rigurosos:", err);
                    }});
                }}
            }} else {{
                document.exitFullscreen();
            }}
        }} catch (err) {{
            console.error("Error al activar Fullscreen:", err);
        }}
    }});

    document.addEventListener('fullscreenchange', () => {{
        if (!document.fullscreenElement) {{
            if(screen.orientation && screen.orientation.unlock) screen.orientation.unlock();
        }}
        setTimeout(resizeGame, 100);
    }});

    const juanImg = new Image(); let imageLoaded = false;
    juanImg.src = "data:image/png;base64,{img_base64_pesca}";
    juanImg.onload = () => imageLoaded = true;

    // Control Interno
    let score = 0; let accumulatedTime = 0; let lastTimeCheck = Date.now(); let isGameOver = false;
    let penaltyTime = 0; let nPenalties = 0;
    let globalPauseUntil = 0;

    // Mecánica Radar
    let inputState = 'angle'; 
    let angleParam = 0; let angleSpeed = 0.03;
    let fixedAngle = 0; let chargeForce = 0;
    
    // Lluvia visual partículas
    let rainDrops = [];
    let isRainingVisual = false;
    let rainVisualEnd = 0;

    function triggerGiantAlert(message, borderColor = '#ffeb3b') {{
        giantAlert.innerHTML = message.replace(/\\n/g, "<br>");
        giantAlert.style.borderColor = borderColor;
        giantAlert.style.display = 'block';
        globalPauseUntil = Date.now() + 2000; 
        
        setTimeout(() => {{
            giantAlert.style.display = 'none';
        }}, 2000);
    }}

    const TYPES = {{ JUAN: 'juan', BALL: 'ball', CARD: 'card' }};
    let objects = [];

    function countType(t) {{ return objects.filter(o => o.type === t).length; }}

    function spawnObject() {{
        if (objects.length >= 60) return;

        let currentJuanesPct = objects.length > 0 ? countType(TYPES.JUAN) / objects.length : 0;
        let currentCardsPct = objects.length > 0 ? countType(TYPES.CARD) / objects.length : 0;

        let allowedTypes = [TYPES.BALL];
        if (currentJuanesPct < 0.20) allowedTypes.push(TYPES.JUAN);
        if (currentCardsPct < 0.20) allowedTypes.push(TYPES.CARD);

        let type = allowedTypes[Math.floor(Math.random() * allowedTypes.length)];

        objects.push({{
            id: Math.random().toString(36),
            x: Math.random() * width,
            baseY: 220 + Math.random() * (height - 260),
            y: 0,
            type: type,
            vx: (Math.random() - 0.5) * (type === TYPES.JUAN ? 3.5 : 1.2),
            ax: 0,
            depthSpeed: 0.01 + Math.random() * 0.02,
            depthAmp: 10 + Math.random() * 25,
            phase: Math.random() * Math.PI * 2,
            size: 28, // Tamaño masivo duplicado para facilitar jugabilidad táctil
            spawnTime: Date.now()
        }});
    }}

    // Mar inicializado
    for(let i=0; i<30; i++) spawnObject();

    let nextSpawnTime = Date.now() + (5000 + Math.random() * 35000);
    let nextToxicRainTime = Date.now() + 15000 + Math.random() * 20000;

    let hook = {{ x: 0, y: 0, targetX: 0, targetY: 0, size: 8 }};

    function update() {{
        const now = Date.now();
        let deltaTime = now - lastTimeCheck;
        lastTimeCheck = now;

        if (isGameOver) return;
        if (now < globalPauseUntil) return; // Pausa absoluta ante eventos dramáticos

        if (penaltyTime > now) {{
            penaltyEl.style.display = 'block';
            pSecondsEl.innerText = Math.ceil((penaltyTime - now)/1000);
            inputState = 'angle';
            return;
        }} else {{
            penaltyEl.style.display = 'none';
        }}
        
        accumulatedTime += deltaTime;
        clockEl.innerText = (accumulatedTime / 1000).toFixed(1);
        popEl.innerText = objects.length;

        if (inputState === 'angle') insText.innerText = "Toca para fijar ÁNGULO";
        if (inputState === 'force') insText.innerText = "¡Mantén para regular FUERZA!";

        if (inputState === 'angle') {{
            angleParam += angleSpeed;
            if (angleParam > Math.PI || angleParam < 0) angleSpeed *= -1;
        }}
        if (inputState === 'force') {{
            chargeForce = Math.min(chargeForce + 1.8, 100);
        }}

        // Spawns dinámicos de bultos
        if (now > nextSpawnTime) {{
            let batch = Math.floor(4 + Math.random() * 8);
            for(let k=0; k<batch; k++) spawnObject();
            nextSpawnTime = now + (5000 + Math.random() * 35000);
        }}

        // Ejecución Lluvia Tóxica
        if (now > nextToxicRainTime) {{
            let killCount = Math.floor(objects.length * 0.20);
            for (let i = 0; i < killCount; i++) {{
                if (objects.length > 5) {{
                    let idx = Math.floor(Math.random() * objects.length);
                    objects.splice(idx, 1);
                }}
            }}
            isRainingVisual = true;
            rainVisualEnd = now + 4000;
            
            triggerGiantAlert("🌧️ ¡LLUVIA TÓXICA!\\nEliminado el 20% de bultos al azar", "#e74c3c");
            nextToxicRainTime = now + 25000 + Math.random() * 25000;
            return; 
        }}

        // Ciclo biológico y mareas de los bultos
        for (let i = objects.length - 1; i >= 0; i--) {{
            let obj = objects[i];

            // Muerte por envejecimiento tras 1 min de vida
            if (obj.type === TYPES.JUAN && (now - obj.spawnTime) > 60000) {{
                objects.splice(i, 1);
                if(objects.length < 5) spawnObject();
                triggerGiantAlert("👴 ¡UN JUAN HA MUERTO DE VIEJO!\\n👴 :(", "#95a5a6");
                return;
            }}

            if (obj.type === TYPES.JUAN) {{
                obj.ax = (Math.random() - 0.5) * 0.3;
            }}
            obj.vx += obj.ax;
            let maxV = obj.type === TYPES.JUAN ? 3.2 : 1.1;
            obj.vx = Math.max(Math.min(obj.vx, maxV), -maxV);
            obj.x += obj.vx;
            if (obj.x < 0 || obj.x > width) obj.vx *= -1;

            obj.phase += obj.depthSpeed;
            obj.y = obj.baseY + Math.sin(obj.phase) * obj.depthAmp;
            if (obj.y < 185) obj.y = 185;
            if (obj.y > height - 25) obj.y = height - 25;
        }}

        // Viaje de la caña / Anzuelo
        if (inputState === 'launching') {{
            let dx = hook.targetX - hook.x;
            let dy = hook.targetY - hook.y;
            let dist = Math.sqrt(dx*dx + dy*dy);

            if (dist > 14) {{
                hook.x += (dx / dist) * 14;
                hook.y += (dy / dist) * 14;
            }} else {{
                let targetHit = null; let hitIndex = -1;
                for(let i=0; i<objects.length; i++) {{
                    let o = objects[i];
                    let odx = hook.x - o.x; let ody = hook.y - o.y;
                    if (Math.sqrt(odx*odx + ody*ody) < o.size) {{
                        targetHit = o; hitIndex = i; break;
                    }}
                }}

                if (targetHit) {{
                    processCatch(targetHit, hitIndex);
                }} else {{
                    inputState = 'returning';
                }}
            }}
        }} else if (inputState === 'returning') {{
            let dx = (width/2) - hook.x; let dy = 135 - hook.y;
            let dist = Math.sqrt(dx*dx + dy*dy);
            if (dist > 18) {{
                hook.x += (dx / dist) * 18; hook.y += (dy / dist) * 18;
            }} else {{
                inputState = 'angle';
            }}
        }}
    }}

    function processCatch(obj, index) {{
        objects.splice(index, 1);
        if(objects.length < 5) {{ while(objects.length < 5) spawnObject(); }}
        inputState = 'returning';

        if (obj.type === TYPES.JUAN) {{
            score++; scoreEl.innerText = score;
            if (score >= 10) {{
                isGameOver = true;
                setTimeout(win, 100);
            }} else {{
                triggerGiantAlert("👤 ¡JUAN CAPTURADO!\\n+1 Al marcador", "#2ecc71");
            }}
        }} else if (obj.type === TYPES.CARD) {{
            nPenalties++;
            penaltyTime = Date.now() + (4 + nPenalties) * 1000;
            triggerGiantAlert("🟥 ¡TARJETA ROJA!\\nPenalización temporal activada", "#ff4444");
        }} else {{
            triggerGiantAlert("⚽ ¡PELOTA DE FÚTBOL!\\nBulto fallido, sigue buscando", "#3498db");
        }}
    }}

    function win() {{
        if (document.fullscreenElement) document.exitFullscreen();
        const finalTime = (accumulatedTime / 1000).toFixed(2);
        winScreen.style.display = 'block';
        document.getElementById('final-time-text').innerText = "¡Has completado el reto en " + finalTime + "s!";
        document.getElementById('save-pesca-btn').onclick = () => {{
            let parentUrl = document.referrer.split('?')[0]; 
            window.open(parentUrl + '?game_pesca_score=' + finalTime, '_blank');
        }};
    }}

    function draw() {{
        update(); 

        ctx.clearRect(0, 0, width, height);

        // Generar gotas si llueve de manera ácida
        if (isRainingVisual) {{
            if (Date.now() > rainVisualEnd) isRainingVisual = false;
            if (rainDrops.length < 50) {{
                rainDrops.push({{ x: Math.random() * width, y: 0, speed: 9 + Math.random() * 5, len: 15 + Math.random() * 12 }});
            }}
        }}

        // Renderizado de la tormenta verde ácida
        for (let r = rainDrops.length - 1; r >= 0; r--) {{
            let drop = rainDrops[r];
            ctx.strokeStyle = '#39ff14'; 
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(drop.x, drop.y);
            ctx.lineTo(drop.x + 1, drop.y + drop.len);
            ctx.stroke();
            
            if (Date.now() >= globalPauseUntil) drop.y += drop.speed;
            if (drop.y > height) rainDrops.splice(r, 1);
        }}

        // Dibujar bultos colosales
        objects.forEach(obj => {{
            ctx.beginPath();
            ctx.arc(obj.x, obj.y, obj.size, 0, Math.PI*2);
            ctx.fillStyle = 'rgba(24, 48, 89, 0.88)';
            ctx.fill();
            ctx.strokeStyle = 'rgba(255,255,255,0.4)';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.fillStyle = '#fff';
            ctx.font = "bold 16px sans-serif";
            ctx.fillText("❓", obj.x - 7, obj.y + 6);
        }});

        // Pescador y muelle
        ctx.fillStyle = '#5c3a21'; ctx.fillRect(width/2 - 35, 135, 70, 15);
        if (imageLoaded) {{
            ctx.drawImage(juanImg, width/2 - 25, 75, 50, 65);
        }} else {{
            ctx.fillStyle = '#3498db'; ctx.fillRect(width/2 - 12, 85, 24, 50);
        }}

        // Radar circular superior
        let radarRadius = 45; let radarX = width/2; let radarY = 65;
        ctx.beginPath();
        ctx.arc(radarX, radarY, radarRadius, 0, Math.PI, true);
        ctx.strokeStyle = 'rgba(255,255,255,0.5)';
        ctx.lineWidth = 2;
        ctx.stroke();

        let ballX = radarX + Math.cos(angleParam - Math.PI) * radarRadius;
        let ballY = radarY + Math.sin(angleParam - Math.PI) * radarRadius;
        ctx.beginPath();
        ctx.arc(ballX, ballY, 7, 0, Math.PI*2);
        ctx.fillStyle = (inputState === 'angle') ? '#ffeb3b' : '#2ecc71';
        ctx.fill();

        if (inputState === 'force') {{
            ctx.fillStyle = '#e74c3c'; ctx.fillRect(width/2 - 50, 15, chargeForce, 8);
            ctx.strokeStyle = '#fff'; ctx.strokeRect(width/2 - 50, 15, 100, 8);
        }}

        // Sedal del anzuelo
        if (inputState === 'launching' || inputState === 'returning') {{
            ctx.beginPath();
            ctx.moveTo(width/2, 110);
            ctx.lineTo(hook.x, hook.y);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(hook.x, hook.y, 6, 0, Math.PI*2);
            ctx.fillStyle = '#e74c3c';
            ctx.fill();
        }}

        requestAnimationFrame(draw);
    }}

    function handleActionStart() {{
        if (isGameOver || Date.now() < penaltyTime || Date.now() < globalPauseUntil) return;

        if (inputState === 'angle') {{
            fixedAngle = angleParam - Math.PI;
            inputState = 'force';
            chargeForce = 0;
        }}
    }}

    function handleActionEnd() {{
        if (inputState === 'force') {{
            inputState = 'launching';
            let maxReach = Math.sqrt( (width/2)*(width/2) + height*height );
            let currentReach = (chargeForce / 100) * maxReach;

            hook.targetX = (width/2) + Math.cos(fixedAngle) * currentReach;
            hook.targetY = 175 + Math.abs(Math.sin(fixedAngle) * currentReach * 0.7);

            if (hook.targetX < 0) hook.targetX = 15;
            if (hook.targetX > width) hook.targetX = width - 15;
            if (hook.targetY > height) hook.targetY = height - 20;

            hook.x = width / 2; hook.y = 135;
        }}
    }}

    // Listeners
    container.addEventListener('mousedown', (e) => {{ if(e.target.id !== 'fullscreen-btn') handleActionStart(); }});
    window.addEventListener('mouseup', handleActionEnd);
    container.addEventListener('touchstart', (e) => {{ if(e.target.id !== 'fullscreen-btn') handleActionStart(); }}, {{passive: true}});
    window.addEventListener('touchend', handleActionEnd);
    window.addEventListener('keydown', (e) => {{ if(e.code === 'Space') {{ e.preventDefault(); handleActionStart(); }} }});
    window.addEventListener('keyup', (e) => {{ if(e.code === 'Space') handleActionEnd(); }});

    draw();
</script>
</body>
</html>
"""

components.html(html_pesca, height=520)
