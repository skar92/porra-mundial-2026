import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import os
import csv

# Configuración de la interfaz de Streamlit
st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra")
st.write(f"Actualizado al: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- INICIALIZACIÓN DEL ESTADO DEL JUEGO ---
if 'juanes_encontrados' not in st.session_state:
    st.session_state.juanes_encontrados = set()
if 'celdas_resaltadas' not in st.session_state:
    st.session_state.celdas_resaltadas = set()

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

def listar_ganadores():
    if not os.path.exists(FILE_GANADORES):
        return pd.DataFrame(columns=["Nombre", "Fecha y Hora"])
    try:
        return pd.read_csv(FILE_GANADORES)
    except:
        return pd.DataFrame(columns=["Nombre", "Fecha y Hora"])

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

# --- CUOTAS ACTUALIZADAS ---
cuotas_ganador = {'Francia': 4.75, 'España': 6.00, 'Inglaterra': 6.50, 'Argentina': 9.00, 'Portugal': 9.00, 'Brasil': 10.00, 'Alemania': 13.00, 'Países Bajos': 21.00, 'Noruega': 29.00, 'EE. UU.': 34.00, 'Marruecos': 34.00, 'Bélgica': 41.00, 'Colombia': 41.00, 'Japón': 51.00, 'Uruguay': 67.00, 'México': 67.00, 'Suiza': 67.00, 'Croacia': 101.00, 'Ecuador': 101.00, 'Austria': 101.00, 'Costa de Marfil': 101.00, 'Senegal': 101.00, 'Turquía': 126.00, 'Canadá': 151.00, 'Escocia': 151.00, 'Bosnia y Herzegovina': 251.00}
cuotas_final = {'Francia': 3.25, 'España': 3.75, 'Inglaterra': 3.75, 'Argentina': 5.00, 'Portugal': 5.00, 'Brasil': 5.50, 'Alemania': 6.50, 'Países Bajos': 9.00, 'Noruega': 11.00, 'Colombia': 15.00, 'Bélgica': 17.00, 'EE. UU.': 17.00, 'México': 17.00, 'Marruecos': 17.00, 'Japón': 23.00, 'Uruguay': 26.00, 'Suiza': 26.00, 'Croacia': 34.00, 'Austria': 34.00, 'Ecuador': 41.00, 'Canadá': 51.00, 'Senegal': 51.00, 'Turquía': 51.00, 'Escocia': 81.00, 'Costa de Marfil': 81.00, 'Bosnia y Herzegovina': 101.00}
cuotas_semis = {'Francia': 2.25, 'España': 2.60, 'Inglaterra': 2.60, 'Argentina': 3.00, 'Portugal': 3.40, 'Brasil': 3.50, 'Alemania': 3.75, 'Países Bajos': 5.00, 'Noruega': 6.00, 'Bélgica': 6.50, 'Colombia': 6.50, 'EE. UU.': 7.00, 'Marruecos': 7.50, 'México': 8.00, 'Japón': 10.00, 'Uruguay': 12.00, 'Suiza': 13.00, 'Croacia': 15.00, 'Senegal': 15.00, 'Austria': 15.00, 'Canadá': 17.00, 'Costa de Marfil': 17.00, 'Ecuador': 19.00, 'Turquía': 21.00, 'Escocia': 23.00, 'Bosnia y Herzegovina': 41.00}
cuotas_cuartos = {'Francia': 1.53, 'Inglaterra': 1.66, 'España': 1.66, 'Argentina': 1.75, 'Portugal': 1.90, 'Brasil': 2.15, 'Alemania': 2.30, 'Países Bajos': 2.75, 'Noruega': 2.75, 'EE. UU.': 3.00, 'Bélgica': 3.00, 'Colombia': 3.50, 'México': 3.50, 'Marruecos': 3.75, 'Japón': 4.50, 'Suiza': 4.50, 'Uruguay': 5.00, 'Canadá': 6.00, 'Austria': 6.00, 'Croacia': 6.50, 'Costa de Marfil': 7.00, 'Ecuador': 7.00, 'Senegal': 8.00, 'Escocia': 9.00, 'Turquía': 9.00, 'Bosnia y Herzegovina': 11.00}
cuotas_octavos = {'Francia': 1.20, 'Inglaterra': 1.25, 'España': 1.30, 'Argentina': 1.38, 'Portugal': 1.38, 'Alemania': 1.45, 'Brasil': 1.46, 'Noruega': 1.73, 'Bélgica': 1.73, 'EE. UU.': 1.73, 'México': 1.73, 'Países Bajos': 1.91, 'Colombia': 1.91, 'Marruecos': 2.02, 'Suiza': 2.10, 'Canadá': 2.30, 'Japón': 2.40, 'Costa de Marfil': 2.63, 'Croacia': 2.75, 'Uruguay': 2.80, 'Ecuador': 3.03, 'Austria': 3.25, 'Escocia': 3.50, 'Turquía': 3.78, 'Senegal': 3.78, 'Bosnia y Herzegovina': 4.04}

todos_equipos = set([eq for eqs in porra.values() for eq in eqs])
probabilidades = {}
for eq in todos_equipos:
    n = traduccion_interna.get(eq, eq)
    probabilidades[eq] = {
        'ganador': 1 / float(cuotas_ganador.get(n, 1000.0)), 'final': 1 / float(cuotas_final.get(n, 1000.0)),
        'semis': 1 / float(cuotas_semis.get(n, 1000.0)), 'cuartos': 1 / float(cuotas_cuartos.get(n, 1000.0)),
        'octavos': 1 / float(cuotas_octavos.get(n, 1000.0))
    }

filas_hoy = []
fecha_hoy = "2026-06-18"
for jugador, equipos in porra.items():
    puntos_selecciones = sum([(10 * probabilidades[e]['octavos'] + 12 * probabilidades[e]['cuartos'] + 15 * probabilidades[e]['semis'] + 18 * probabilidades[e]['final'] + 20 * probabilidades[e]['ganador']) for e in equipos])
    puntos_totales = puntos_selecciones + puntos_futbolistas_actuales.get(jugador, 0)
    filas_hoy.append({"Fecha": fecha_hoy, "Jugador": jugador, "Equipos": ", ".join([f"{banderas.get(e, '🏳️')} {e}" for e in equipos]), "Futbolistas": ", ".join([f"{f} ({pts})" for f, pts in porra_futbolistas.get(jugador, {}).items()]), "Puntos Esperados": round(puntos_totales, 2)})

df_hoy = pd.DataFrame(filas_hoy)
total_puntos = df_hoy["Puntos Esperados"].sum()
df_hoy["Probabilidad (%)"] = round((df_hoy["Puntos Esperados"] / (total_puntos if total_puntos > 0 else 1)) * 100, 2)

datos_15_junio = [{"Fecha": "2026-06-15", "Jugador": "Mírete", "Probabilidad (%)": 14.43}, {"Fecha": "2026-06-15", "Jugador": "Sierra", "Probabilidad (%)": 13.80}, {"Fecha": "2026-06-15", "Jugador": "Telenti", "Probabilidad (%)": 13.59}, {"Fecha": "2026-06-15", "Jugador": "Joaquín", "Probabilidad (%)": 13.49}, {"Fecha": "2026-06-15", "Jugador": "Ejkar", "Probabilidad (%)": 13.48}, {"Fecha": "2026-06-15", "Jugador": "Miguel Ángel", "Probabilidad (%)": 12.67}, {"Fecha": "2026-06-15", "Jugador": "Vecina", "Probabilidad (%)": 10.07}, {"Fecha": "2026-06-15", "Jugador": "Juan", "Probabilidad (%)": 8.48}]
datos_17_junio = [{"Fecha": "2026-06-17", "Jugador": "Telenti", "Probabilidad (%)": 14.41}, {"Fecha": "2026-06-17", "Jugador": "Joaquín", "Probabilidad (%)": 14.30}, {"Fecha": "2026-06-17", "Jugador": "Miguel Ángel", "Probabilidad (%)": 13.62}, {"Fecha": "2026-06-17", "Jugador": "Mírete", "Probabilidad (%)": 13.47}, {"Fecha": "2026-06-17", "Jugador": "Ejkar", "Probabilidad (%)": 12.90}, {"Fecha": "2026-06-17", "Jugador": "Sierra", "Probabilidad (%)": 12.88}, {"Fecha": "2026-06-17", "Jugador": "Vecina", "Probabilidad (%)": 9.47}, {"Fecha": "2026-06-17", "Jugador": "Juan", "Probabilidad (%)": 8.95}]
df_15 = pd.DataFrame(datos_15_junio)
df_17 = pd.DataFrame(datos_17_junio)
df_18 = df_hoy[["Fecha", "Jugador", "Probabilidad (%)"]]
df_hist = pd.concat([df_15, df_17, df_18], ignore_index=True)

# INTERFAZ DE GRÁFICOS
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


# ==============================================================================
# --- 🧩 SOPA DE LETRAS INTERACTIVA: BUSCANDO A LOS 20 JUANES ---
# ==============================================================================
st.markdown("---")
st.subheader("🧩 Sopa de Letras Interactiva: Encuentra los 20 Juanes")
st.write("Indica la coordenada de inicio y fin para capturar un **JUAN** (ej. de `A1` a `A4`). ¡Completa los 20 para registrarte en el Salón de la Fama!")

@st.cache_data
def generar_sopa_juan_v2():
    tam = 15
    grid = [['' for _ in range(tam)] for _ in range(tam)]
    sol_mask = [[False for _ in range(tam)] for _ in range(tam)]
    word = "JUAN"
    direcciones = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
    random.seed(42)
    
    colocados = 0
    intentos = 0
    juanes_coordenadas = []
    
    while colocados < 20 and intentos < 3000:
        intentos += 1
        d = random.choice(direcciones)
        r = random.randint(0, tam - 1)
        c = random.randint(0, tam - 1)
        
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
                    sol_mask[nr][nc] = True
                    coords_palabra.append((nr, nc))
                juanes_coordenadas.append(coords_palabra)
                colocados += 1

    letras_relleno = "BCDEFGHIKLMNOPQRSTVXYZ"
    for r in range(tam):
        for c in range(tam):
            if grid[r][c] == '':
                grid[r][c] = random.choice(letras_relleno)
    return grid, sol_mask, juanes_coordenadas

grid_sopa, mascara_solucion, lista_juanes = generar_sopa_juan_v2()

def parse_coordenada(texto):
    texto = texto.strip().upper()
    if len(texto) < 2 or not texto[0].isalpha() or not texto[1:].isdigit():
        return None
    fila = ord(texto[0]) - ord('A')
    columna = int(texto[1:]) - 1
    if 0 <= fila < 15 and 0 <= columna < 15:
        return (fila, columna)
    return None

# Panel de juego y controles
col_game1, col_game2 = st.columns([0.4, 0.6])

with col_game1:
    progreso_actual = len(st.session_state.juanes_encontrados)
    st.metric(label="Juanes descubiertos", value=f"{progreso_actual} / 20")
    st.progress(progreso_actual / 20)
    
    # Formulario para mandar coordenadas
    if progreso_actual < 20:
        with st.form("verificar_palabra", clear_on_submit=True):
            st.write("**Introduce Coordenadas:**")
            c_inicio = st.text_input("Casilla Inicial (Ej: A1 o F10):").upper()
            c_fin = st.text_input("Casilla Final (Ej: A4 o C12):").upper()
            boton_enviar = st.form_submit_button("👉 Validar Selección")
            
            if boton_enviar:
                coord_i = parse_coordenada(c_inicio)
                coord_f = parse_coordenada(c_fin)
                
                if coord_i and coord_f:
                    encontrado = False
                    for idx, palabra in enumerate(lista_juanes):
                        # Comprobamos si coincide de principio a fin o viceversa
                        if (coord_i == palabra[0] and coord_f == palabra[3]) or (coord_i == palabra[3] and coord_f == palabra[0]):
                            if idx in st.session_state.juanes_encontrados:
                                st.warning("¡Ya habías encontrado este JUAN específicamente!")
                            else:
                                st.session_state.juanes_encontrados.add(idx)
                                for (r, c) in palabra:
                                    st.session_state.celdas_resaltadas.add((r, c))
                                st.success("¡BRUTAL! Has cazado un JUAN.")
                                st.rerun()
                            encontrado = True
                            break
                    if not encontrado:
                        st.error("No hay ningún JUAN válido entre esas dos casillas. ¡Sigue buscando!")
                else:
                    st.error("Coordenadas no válidas. Las filas van de A a O y las columnas de 1 a 15.")
    else:
        st.balloons()
        st.success("🎉 ¡Felicidades! Has completado el juego.")
        
        # Formulario de registro para el Salón de la Fama
        with st.form("registro_salon_fama", clear_on_submit=True):
            st.write("🌟 **¡Inmortaliza tu victoria en la base de datos!**")
            nombre_campeon = st.text_input("Tu Nombre / Alias:")
            boton_guardar = st.form_submit_button("🏆 Registrar mi Nombre")
            if boton_guardar and nombre_campeon:
                guardar_ganador(nombre_campeon)
                st.success(f"¡{nombre_campeon} se ha añadido al Salón de la Fama!")
                st.rerun()

    mostrar_solucion = st.checkbox("💡 Revelar Solución (Modo Dios)")
    
    # Visualización de ganadores históricos
    st.markdown("### 🏆 Salón de la Fama")
    df_ganadores = listar_ganadores()
    if not df_ganadores.empty:
        st.dataframe(df_ganadores.sort_index(ascending=False), use_container_width=True, hide_index=True)
    else:
        st.caption("Nadie ha completado el desafío todavía. ¿Quién será el primero?")

with col_game2:
    # Construcción de la matriz HTML interactiva con índices visuales
    html_sopa = "<table style='margin: auto; border-collapse: separate; border-spacing: 3px; font-family: monospace; font-size: 17px; text-align: center;'><tr>"
    # Fila superior de números (columnas)
    html_sopa += "<td style='width: 34px; height: 34px; font-weight: bold; color: #888;'></td>"
    for c in range(15):
        html_sopa += f"<td style='width: 34px; height: 34px; font-weight: bold; color: #888;'>{c+1}</td>"
    html_sopa += "</tr>"
    
    for r in range(15):
        letra_fila = chr(ord('A') + r)
        html_sopa += "<tr>"
        # Columna izquierda de letras (filas)
        html_sopa += f"<td style='width: 34px; height: 34px; font-weight: bold; color: #888;'>{letra_fila}</td>"
        
        for c in range(15):
            letra = grid_sopa[r][c]
            # Determinar si la casilla está coloreada
            es_exito = mascara_solucion[r][c] if mostrar_solucion else ((r, c) in st.session_state.celdas_resaltadas)
            
            if es_exito:
                bg_color = "#FFD700" if mostrar_solucion else "#2ecc71"  # Oro para trampa, verde esmeralda para juego real
                text_color = "#000000"
                border_style = "2px solid #FF8C00" if mostrar_solucion else "2px solid #27ae60"
            else:
                bg_color = "rgba(128, 128, 128, 0.08)"
                text_color = "inherit"
                border_style = "1px solid rgba(128, 128, 128, 0.2)"
                
            html_sopa += f"<td style='width: 34px; height: 34px; border: {border_style}; background-color: {bg_color}; color: {text_color}; font-weight: bold; border-radius: 4px;'>{letra}</td>"
        html_sopa += "</tr>"
    html_sopa += "</table>"
    
    st.markdown(html_sopa, unsafe_allow_html=True)
