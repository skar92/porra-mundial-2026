import streamlit as st
import pandas as pd
import plotly.express as px
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
    'Sierra': {'Kane': 2, 'Julián Álvarez': 0},
    'Joaquín': {'Messi': 3, 'Olise': 0},
    'Ejkar': {'Lautaro': 0, 'Raphinha': 0},
    'Vecina': {'Havertz': 2, 'Lamine Yamal': 0},
    'Telenti': {'Endrick': 0, 'Ramos': 0},
    'Miguel Ángel': {'Haaland': 2, 'Embolo': 1},
    'Mírete': {'Oyarzabal': 0, 'El Bicho': 0}, 
    'Juan': {'Mbappé': 2, 'Vinicius': 1}
}

puntos_futbolistas_actuales = {jugador: sum(datos.values()) if isinstance(datos, dict) else 0 
                               for jugador, datos in porra_futbolistas.items()}

# Diccionario de traducción directa
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

# --- TABLAS DE CUOTAS MANUALES ACTUALIZADAS (18/06) ---
cuotas_ganador = {
    'Francia': 4.75, 'España': 6.00, 'Inglaterra': 6.50, 'Argentina': 9.00, 'Portugal': 9.00, 'Brasil': 10.00,
    'Alemania': 13.00, 'Países Bajos': 21.00, 'Noruega': 29.00, 'EE. UU.': 34.00, 'Marruecos': 34.00, 'Bélgica': 41.00,
    'Colombia': 41.00, 'Japón': 51.00, 'Uruguay': 67.00, 'México': 67.00, 'Suiza': 67.00, 'Croacia': 101.00,
    'Ecuador': 101.00, 'Austria': 101.00, 'Costa de Marfil': 101.00, 'Senegal': 101.00, 'Turquía': 126.00,
    'Canadá': 151.00, 'Escocia': 151.00, 'Bosnia y Herzegovina': 251.00
}

cuotas_final = {
    'Francia': 3.25, 'España': 3.75, 'Inglaterra': 3.75, 'Argentina': 5.00, 'Portugal': 5.00, 'Brasil': 5.50,
    'Alemania': 6.50, 'Países Bajos': 9.00, 'Noruega': 11.00, 'Colombia': 15.00, 'Bélgica': 17.00, 'EE. UU.': 17.00,
    'México': 17.00, 'Marruecos': 17.00, 'Japón': 23.00, 'Uruguay': 26.00, 'Suiza': 26.00, 'Croacia': 34.00,
    'Austria': 34.00, 'Ecuador': 41.00, 'Canadá': 51.00, 'Senegal': 51.00, 'Turquía': 51.00, 'Escocia': 81.00,
    'Costa de Marfil': 81.00, 'Bosnia y Herzegovina': 101.00
}

cuotas_semis = {
    'Francia': 2.25, 'España': 2.60, 'Inglaterra': 2.60, 'Argentina': 3.00, 'Portugal': 3.40, 'Brasil': 3.50,
    'Alemania': 3.75, 'Países Bajos': 5.00, 'Noruega': 6.00, 'Bélgica': 6.50, 'Colombia': 6.50, 'EE. UU.': 7.00,
    'Marruecos': 7.50, 'México': 8.00, 'Japón': 10.00, 'Uruguay': 12.00, 'Suiza': 13.00, 'Croacia': 15.00,
    'Senegal': 15.00, 'Austria': 15.00, 'Canadá': 17.00, 'Costa de Marfil': 17.00, 'Ecuador': 19.00, 'Turquía': 21.00,
    'Escocia': 23.00, 'Bosnia y Herzegovina': 41.00
}

cuotas_cuartos = {
    'Francia': 1.53, 'Inglaterra': 1.66, 'España': 1.66, 'Argentina': 1.75, 'Portugal': 1.90, 'Brasil': 2.15,
    'Alemania': 2.30, 'Países Bajos': 2.75, 'Noruega': 2.75, 'EE. UU.': 3.00, 'Bélgica': 3.00, 'Colombia': 3.50,
    'México': 3.50, 'Marruecos': 3.75, 'Japón': 4.50, 'Suiza': 4.50, 'Uruguay': 5.00, 'Canadá': 6.00,
    'Austria': 6.00, 'Croacia': 6.50, 'Costa de Marfil': 7.00, 'Ecuador': 7.00, 'Senegal': 8.00, 'Escocia': 9.00, 
    'Turquía': 9.00, 'Bosnia y Herzegovina': 11.00
}

cuotas_octavos = {
    'Francia': 1.20, 'Inglaterra': 1.25, 'España': 1.30, 'Argentina': 1.38, 'Portugal': 1.38, 'Alemania': 1.45,
    'Brasil': 1.46, 'Noruega': 1.73, 'Bélgica': 1.73, 'EE. UU.': 1.73, 'México': 1.73, 'Países Bajos': 1.91,
    'Colombia': 1.91, 'Marruecos': 2.02, 'Suiza': 2.10, 'Canadá': 2.30, 'Japón': 2.40, 'Costa de Marfil': 2.63,
    'Croacia': 2.75, 'Uruguay': 2.80, 'Ecuador': 3.03, 'Austria': 3.25, 'Escocia': 3.50, 'Turquía': 3.78,
    'Senegal': 3.78, 'Bosnia y Herzegovina': 4.04
}

# --- PROCESAMIENTO DE PROBABILIDADES REALES ---
todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades = {}

for eq in todos_equipos:
    n = traduccion_interna.get(eq, eq)
    
    probabilidades[eq] = {
        'ganador': 1 / float(cuotas_ganador.get(n, 1000.0)),
        'final': 1 / float(cuotas_final.get(n, 1000.0)),
        'semis': 1 / float(cuotas_semis.get(n, 1000.0)),
        'cuartos': 1 / float(cuotas_cuartos.get(n, 1000.0)),
        'octavos': 1 / float(cuotas_octavos.get(n, 1000.0))
    }

# --- CÁLCULO DE PUNTOS ESPERADOS HOY ---
filas_hoy = []
fecha_hoy = "2026-06-18"

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

# --- HISTÓRICO FIJO (3 PUNTOS TEMPORALES) ---

# Día 1: 15 de Junio
datos_15_junio = [
    {"Fecha": "2026-06-15", "Jugador": "Mírete", "Probabilidad (%)": 14.43},
    {"Fecha": "2026-06-15", "Jugador": "Sierra", "Probabilidad (%)": 13.80},
    {"Fecha": "2026-06-15", "Jugador": "Telenti", "Probabilidad (%)": 13.59},
    {"Fecha": "2026-06-15", "Jugador": "Joaquín", "Probabilidad (%)": 13.49},
    {"Fecha": "2026-06-15", "Jugador": "Ejkar", "Probabilidad (%)": 13.48},
    {"Fecha": "2026-06-15", "Jugador": "Miguel Ángel", "Probabilidad (%)": 12.67},
    {"Fecha": "2026-06-15", "Jugador": "Vecina", "Probabilidad (%)": 10.07},
    {"Fecha": "2026-06-15", "Jugador": "Juan", "Probabilidad (%)": 8.48}
]

# Día 2: 17 de Junio (Pega aquí los valores exactos cuando los tengas)
datos_17_junio = [
    {"Fecha": "2026-06-17", "Jugador": "Telenti", "Probabilidad (%)": 14.41},
    {"Fecha": "2026-06-17", "Jugador": "Joaquín", "Probabilidad (%)": 14.30},
    {"Fecha": "2026-06-17", "Jugador": "Miguel Ángel", "Probabilidad (%)": 13.62},
    {"Fecha": "2026-06-17", "Jugador": "Mírete", "Probabilidad (%)": 13.47},
    {"Fecha": "2026-06-17", "Jugador": "Ejkar", "Probabilidad (%)": 12.90},
    {"Fecha": "2026-06-17", "Jugador": "Sierra", "Probabilidad (%)": 12.88},
    {"Fecha": "2026-06-17", "Jugador": "Vecina", "Probabilidad (%)": 9.47},
    {"Fecha": "2026-06-17", "Jugador": "Juan", "Probabilidad (%)": 8.95}
]

df_15 = pd.DataFrame(datos_15_junio)
df_17 = pd.DataFrame(datos_17_junio)
df_18 = df_hoy[["Fecha", "Jugador", "Probabilidad (%)"]]

# Unión de las 3 fechas
df_hist = pd.concat([df_15, df_17, df_18], ignore_index=True)

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
