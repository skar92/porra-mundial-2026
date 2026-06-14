import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Porra Mundial 2026 - Algoritmo Puro", layout="wide")

st.title("🏆 Porra Mundial 2026: Simulador y Motor Predictivo")
st.markdown("""
Este sistema calcula la **Esperanza Matemática** de la porra en tiempo real. 
1. **Equipos:** Puntos calculados sumando la probabilidad exacta de avanzar ronda a ronda.
2. **Jugadores:** Goles por minuto cruzados con el **Factor Rival (FR) Real**, extraído de los cruces del cuadro FIFA.
""")

# ==========================================
# 1. CONEXIÓN CON GOOGLE SHEETS (Tus Datos)
# ==========================================
URL_SHEETS = "https://docs.google.com/spreadsheets/d/1mmRhevyqOCuJQBcsYNXHGIUbnSJPaSR2zLuSPjvTfQg/export?format=csv"

@st.cache_data(ttl=300)
def cargar_datos_equipos():
    try:
        df = pd.read_csv(SHEET_URL)
        columnas_necesarias = ['Seleccion', 'Cuota_Ganar', 'Prob_1o', 'Prob_2o', 'Prob_Cuartos', 'Prob_Semis', 'Prob_Final', 'Goles_Encajados_S']
        for col in columnas_necesarias:
            if col not in df.columns:
                if col == 'Seleccion': pass
                elif 'Prob' in col: df[col] = 0.25
                elif col == 'Goles_Encajados_S': df[col] = 1.20
                else: df[col] = 15.0
        return df
    except Exception as e:
        st.warning(f"Usando base de datos interna de emergencia: {e}")
        datos_base = {
            'Seleccion': ["México", "Suiza", "Bosnia", "Canadá", "Marruecos", "Brasil", "Escocia", "EE.UU.", "Turquía", "Ecuador", "Alemania", "Costa de Marfil", "Japón", "Países Bajos", "Bélgica", "España", "Uruguay", "Francia", "Noruega", "Senegal", "Argentina", "Austria", "Portugal", "Croacia", "Colombia", "Inglaterra"],
            'Grupo':     ["A",      "B",     "B",      "B",      "C",         "C",      "C",       "D",      "D",       "E",       "E",        "E",               "F",     "F",            "G",       "H",      "H",       "I",       "I",       "I",       "J",         "J",       "K",        "L",       "K",        "L"],
            'Cuota_Ganar': [25.0, 60.0, 150.0, 80.0, 40.0, 8.5, 120.0, 35.0, 70.0, 50.0, 14.0, 200.0, 50.0, 16.0, 28.0, 6.5, 18.0, 6.0, 45.0, 80.0, 9.0, 65.0, 7.5, 35.0, 40.0, 7.0],
            'Prob_1o':   [0.45, 0.25, 0.10, 0.20, 0.30, 0.55, 0.10, 0.40, 0.25, 0.25, 0.45, 0.10, 0.30, 0.45, 0.50, 0.60, 0.30, 0.60, 0.20, 0.15, 0.55, 0.25, 0.55, 0.35, 0.25, 0.50],
            'Prob_2o':   [0.30, 0.30, 0.20, 0.25, 0.30, 0.25, 0.15, 0.30, 0.30, 0.30, 0.30, 0.15, 0.30, 0.30, 0.25, 0.25, 0.35, 0.25, 0.25, 0.20, 0.25, 0.30, 0.25, 0.30, 0.30, 0.30],
            'Prob_Cuartos': [0.15, 0.05, 0.01, 0.03, 0.08, 0.45, 0.01, 0.12, 0.05, 0.05, 0.28, 0.01, 0.06, 0.25, 0.14, 0.50, 0.22, 0.52, 0.08, 0.03, 0.42, 0.06, 0.46, 0.12, 0.10, 0.48],
            'Prob_Semis': [0.05, 0.01, 0.00, 0.01, 0.02, 0.22, 0.00, 0.04, 0.01, 0.01, 0.12, 0.00, 0.01, 0.10, 0.05, 0.26, 0.08, 0.28, 0.02, 0.01, 0.20, 0.01, 0.22, 0.04, 0.03, 0.24],
            'Prob_Final': [0.02, 0.00, 0.00, 0.00, 0.01, 0.10, 0.00, 0.01, 0.00, 0.00, 0.05, 0.00, 0.00, 0.04, 0.02, 0.14, 0.03, 0.15, 0.01, 0.00, 0.09, 0.00, 0.11, 0.01, 0.01, 0.12],
            'Goles_Encajados_S': [1.3, 1.1, 1.5, 1.4, 1.0, 0.8, 1.6, 1.2, 1.3, 1.2, 0.9, 1.7, 1.1, 1.0, 1.1, 0.7, 0.9, 0.7, 1.2, 1.3, 0.8, 1.2, 0.8, 1.0, 1.1, 0.7]
        }
        return pd.DataFrame(datos_base)

df_equipos = cargar_datos_equipos()

mapeo_grupos = {
    "México": "A", "Suiza": "B", "Bosnia": "B", "Canadá": "B", "Marruecos": "C", "Brasil": "C", "Escocia": "C",
    "EE.UU.": "D", "Turquía": "D", "Ecuador": "E", "Alemania": "E", "Costa de Marfil": "E", "Japón": "F",
    "Países Bajos": "F", "Bélgica": "G", "España": "H", "Uruguay": "H", "Francia": "I", "Noruega": "I",
    "Senegal": "I", "Argentina": "J", "Austria": "J", "Portugal": "K", "Colombia": "K", "Inglaterra": "L", "Croacia": "L"
}
if 'Grupo' not in df_equipos.columns:
    df_equipos['Grupo'] = df_equipos['Seleccion'].map(mapeo_grupos).fillna("A")

# ==========================================
# 2. ESQUELETO OFICIAL DE CRUCES DE LA FIFA
# ==========================================
cruces_fifa = {
    "A": {"1o": "Mejor_3o", "2o": "B"}, "B": {"1o": "Mejor_3o", "2o": "A"},
    "C": {"1o": "2o_F",      "2o": "1o_F"}, "D": {"1o": "Mejor_3o", "2o": "G"},
    "E": {"1o": "Mejor_3o", "2o": "I"}, "F": {"1o": "2o_C",      "2o": "1o_C"},
    "G": {"1o": "Mejor_3o", "2o": "D"}, "H": {"1o": "2o_J",      "2o": "1o_J"},
    "I": {"1o": "Mejor_3o", "2o": "I"}, "J": {"1o": "2o_H",      "2o": "1o_H"},
    "K": {"1o": "Mejor_3o", "2o": "L"}, "L": {"1o": "Mejor_3o", "2o": "K"}
}

# ==========================================
# 3. CONFIGURACIÓN DE JUGADORES Y PORRA
# ==========================================
stats_jugadores_base = {
    "Kane": {"g_90": 1.08, "mins_por_partido": 75, "pais": "Inglaterra"},
    "Julián Álvarez": {"g_90": 0.65, "mins_por_partido": 65, "pais": "Argentina"},
    "Messi": {"g_90": 0.90, "mins_por_partido": 80, "pais": "Argentina"},
    "Olise": {"g_90": 0.45, "mins_por_partido": 70, "pais": "Francia"},
    "Lautaro": {"g_90": 0.77, "mins_por_partido": 60, "pais": "Argentina"},
    "Raphinha": {"g_90": 0.54, "mins_por_partido": 70, "pais": "Brasil"},
    "Havertz": {"g_90": 0.62, "mins_por_partido": 75, "pais": "Alemania"},
    "Lamine Yamal": {"g_90": 0.38, "mins_por_partido": 75, "pais": "España"},
    "Endrick": {"g_90": 0.72, "mins_por_partido": 30, "pais": "Brasil"},
    "Ramos": {"g_90": 0.73, "mins_por_partido": 45, "pais": "Portugal"},
    "Haaland": {"g_90": 1.10, "mins_por_partido": 90, "pais": "Noruega"},
    "Embolo": {"g_90": 0.54, "mins_por_partido": 65, "pais": "Suiza"},
    "Oyarzabal": {"g_90": 0.55, "mins_por_partido": 55, "pais": "España"},
    "El Bicho": {"g_90": 1.05, "mins_por_partido": 70, "pais": "Portugal"},
    "Mbappé": {"g_90": 0.96, "mins_por_partido": 85, "pais": "Francia"},
    "Vinicius": {"g_90": 0.73, "mins_por_partido": 80, "pais": "Brasil"}
}

porra_config = {
    "Sierra": {"equipos": ["España", "Suiza", "Croacia"], "jugadores": ["Kane", "Julián Álvarez"]},
    "Joaquín": {"equipos": ["Portugal", "Marruecos", "EE.UU."], "jugadores": ["Messi", "Olise"]},
    "Ejkar": {"equipos": ["Inglaterra", "Colombia", "Japón"], "jugadores": ["Lautaro", "Raphinha"]},
    "Vecina": {"equipos": ["Ecuador", "Bélgica", "México"], "jugadores": ["Havertz", "Lamine Yamal"]},
    "Telenti": {"equipos": ["Francia", "Noruega", "Senegal"], "jugadores": ["Endrick", "Ramos"]},
    "Miguel": {"equipos": ["Argentina", "Países Bajos", "Costa de Marfil"], "jugadores": ["Haaland", "Embolo"]},
    "Mírete": {"equipos": ["Brasil", "Alemania", "Uruguay"], "jugadores": ["Oyarzabal", "El Bicho"]},
    "Juan": {"equipos": ["Canadá", "Turquía", "Austria", "Escocia", "Bosnia"], "jugadores": ["Mbappé", "Vinicius"]}
}

# ==========================================
# 4. MOTOR MATEMÁTICO UNIFICADO
# ==========================================

# A. LÓGICA DE EQUIPOS POR RONDAS
def calcular_puntos_equipo_por_rondas(nombre_seleccion, df):
    """
    Asigna puntos base al equipo dependiendo de su probabilidad de llegar a cada ronda.
    Modifica los multiplicadores (2.0, 3.0...) según los puntos reales que dé vuestra porra por fase.
    """
    try:
        fila = df[df['Seleccion'] == nombre_seleccion].iloc[0]
        p_1o = fila['Prob_1o']
        p_2o = fila['Prob_2o']
        p_cuartos = fila['Prob_Cuartos']
        p_semis = fila['Prob_Semis']
        p_final = fila['Prob_Final']
        
        # Ponderación de Puntos:
        # Clasificar de grupos (1º o 2º) -> 2 pts
        # Llegar a Cuartos -> +3 pts
        # Llegar a Semis -> +4 pts
        # Final / Ganar -> +5 pts
        puntos_esperados = ((p_1o + p_2o) * 2.0) + (p_cuartos * 3.0) + (p_semis * 4.0) + (p_final * 5.0)
        return round(puntos_esperados, 2)
    except:
        return 1.5

# B. LÓGICA DE JUGADORES (ÁRBOL DE CRUCES)
def obtener_goles_encajados_medios_grupo(grupo, posicion, df):
    equipos_grupo = df[df['Grupo'] == grupo]
    if equipos_grupo.empty:
        return 1.20
    
    if posicion == "1o":
        return equipos_grupo.sort_values('Cuota_Ganar').iloc[0]['Goles_Encajados_S']
    elif posicion == "2o":
        if len(equipos_grupo) > 1:
            return equipos_grupo.sort_values('Cuota_Ganar').iloc[1]['Goles_Encajados_S']
        return equipos_grupo.iloc[0]['Goles_Encajados_S']
    else:
        return equipos_grupo['Goles_Encajados_S'].mean()

def calcular_puntos_jugador_cuadro_real(nombre_jugador, df):
    if nombre_jugador not in stats_jugadores_base:
        return 0.0
        
    stats = stats_jugadores_base[nombre_jugador]
    g_90 = stats["g_90"]
    mins_partido = stats["mins_por_partido"]
    seleccion_jugador = stats["pais"]
    
    try:
        fila_sel = df[df['Seleccion'] == seleccion_jugador].iloc[0]
        grupo_sel = fila_sel['Grupo']
        p_1o = fila_sel['Prob_1o']
        p_2o = fila_sel['Prob_2o']
        p_cuartos = fila_sel['Prob_Cuartos']
        p_semis = fila_sel['Prob_Semis']
        p_final = fila_sel['Prob_Final']
    except:
        return round(4 * ((mins_partido / 90.0) * g_90), 2)

    puntos_totales = 0.0
    
    # 1. Fase de Grupos
    puntos_totales += 3 * ((mins_partido / 90.0) * g_90 * 1.0)
    
    # 2. Partido 4 (Dieciseisavos de Final con Árbol FIFA)
    prob_llegar_p4 = p_1o + p_2o
    if prob_llegar_p4 > 0:
        reglas_grupo = cruces_fifa.get(grupo_sel, {"1o": "Mejor_3o", "2o": "Mejor_3o"})
        
        cruce_si_1o = reglas_grupo["1o"]
        if "2o_" in cruce_si_1o:
            gc_camino_1 = obtener_goles_encajados_medios_grupo(cruce_si_1o.split("_")[1], "2o", df)
        elif cruce_si_1o == "Mejor_3o":
            gc_camino_1 = 1.35 
        else:
            gc_camino_1 = obtener_goles_encajados_medios_grupo(cruce_si_1o, "1o", df)
            
        cruce_si_2o = reglas_grupo["2o"]
        if "1o_" in cruce_si_2o:
            gc_camino_2 = obtener_goles_encajados_medios_grupo(cruce_si_2o.split("_")[1], "1o", df)
        elif cruce_si_2o == "Mejor_3o":
            gc_camino_2 = 1.35
        else:
            gc_camino_2 = obtener_goles_encajados_medios_grupo(cruce_si_2o, "2o", df)
        
        fr_ponderado_real = ((p_1o / prob_llegar_p4) * gc_camino_1) + ((p_2o / prob_llegar_p4) * gc_camino_2)
        puntos_totales += prob_llegar_p4 * ((mins_partido / 90.0) * g_90 * fr_ponderado_real)

    # 3. Rondas Avanzadas
    puntos_totales += p_cuartos * ((mins_partido / 90.0) * g_90 * 0.90)
    puntos_totales += p_semis * ((mins_partido / 90.0) * g_90 * 0.80)
    puntos_totales += p_final * (((mins_partido + 15) / 90.0) * g_90 * 0.70)
    
    return round(puntos_totales, 2)

# ==========================================
# 5. PROCESAMIENTO Y RANKING FINAL
# ==========================================
filas_ranking = []

for participante, elecciones in porra_config.items():
    # Usamos la nueva función basada en las rondas probabilísticas
    pts_equipos = sum(calcular_puntos_equipo_por_rondas(eq, df_equipos) for eq in elecciones["equipos"])
    desglose_eq_lista = [f"{eq} ({calcular_puntos_equipo_por_rondas(eq, df_equipos)} pts)" for eq in elecciones["equipos"]]
    
    pts_jugadores = 0.0
    desglose_jug_lista = []
    for jug in elecciones["jugadores"]:
        pts_j = calcular_puntos_jugador_cuadro_real(jug, df_equipos)
        pts_jugadores += pts_j
        desglose_jug_lista.append(f"{jug} ({pts_j} pts)")
        
    total_esperado = pts_equipos + pts_jugadores
    
    filas_ranking.append({
        "Participante": participante,
        "Total Puntos Esperados": round(total_esperado, 2),
        "Ptos. Equipos": round(pts_equipos, 2),
        "Ptos. Jugadores": round(pts_jugadores, 2),
        "Elección de Equipos (Detalle)": " // ".join(desglose_eq_lista),
        "Elección de Jugadores (Detalle)": " + ".join(desglose_jug_lista)
    })

df_ranking = pd.DataFrame(filas_ranking).sort_values("Total Puntos Esperados", ascending=False).reset_index(drop=True)
df_ranking.index = df_ranking.index + 1

# ==========================================
# 6. INTERFAZ GRÁFICA
# ==========================================
st.subheader("📊 Clasificación General de la Porra (Matriz Combinada)")

st.dataframe(
    df_ranking.style.background_gradient(cmap='YlGn', subset=['Total Puntos Esperados'])
    .format({
        "Total Puntos Esperados": "{:.2f}",
        "Ptos. Equipos": "{:.2f}",
        "Ptos. Jugadores": "{:.2f}"
    }),
    use_container_width=True,
    height=340
)

st.divider()
st.info("💡 **Integración Total Activada:** Los equipos y los jugadores ahora comparten el mismo motor. Los puntos de las selecciones se calculan sumando las probabilidades exactas que tienen de pasar de grupos, llegar a cuartos, semis y final. ¡El equilibrio matemático es perfecto!")

