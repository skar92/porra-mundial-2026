import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import os
import csv
import json

# Configuración de la interfaz de Streamlit
st.set_page_config(page_title="Porra Mundial 2026", layout="wide")
st.title("🏆 Seguimiento y Evolución de la Porra")
st.write(f"Actualizado al: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

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
# --- 🧩 SOPA DE LETRAS CON SELECCIÓN DE RATÓN (DRAG AND DROP) ---
# ==============================================================================
st.markdown("---")
st.subheader("🧩 Sopa de Letras Interactiva: Encuentra los 20 Juanes")
st.write("Usa el **ratón** para hacer clic y arrastrar sobre las letras en cualquier dirección. Si encuentras un **JUAN** válido, quedará marcado en verde. ¡Completa los 20!")

@st.cache_data
def generar_sopa_juan_v3():
    tam = 15
    grid = [['' for _ in range(tam)] for _ in range(tam)]
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
                    coords_palabra.append({"r": nr, "c": nc})
                juanes_coordenadas.append(coords_palabra)
                colocados += 1

    letras_relleno = "BCDEFGHIKLMNOPQRSTVXYZ"
    for r in range(tam):
        for c in range(tam):
            if grid[r][c] == '':
                grid[r][c] = random.choice(letras_relleno)
    return grid, juanes_coordenadas

grid_sopa, lista_juanes = generar_sopa_juan_v3()

# Inyección de la Sopa Interactiva mediante HTML5 + JS Avanzado
import streamlit.components.v1 as components

html_game = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0; padding: 10px;
        background-color: transparent;
        display: flex; flex-direction: column; align-items: center;
        user-select: none; -webkit-user-select: none;
    }}
    .header-box {{
        font-size: 20px; font-weight: bold; margin-bottom: 15px;
        color: #2ecc71; background: rgba(46, 204, 113, 0.15);
        padding: 10px 25px; border-radius: 30px; border: 1px solid rgba(46, 204, 113, 0.3);
    }}
    .grid {{
        display: grid; grid-template-columns: repeat(15, 36px); grid-gap: 5px;
        background: #1e1e24; padding: 12px; border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4); touch-action: none;
    }}
    .cell {{
        width: 36px; height: 36px; line-height: 36px; text-align: center;
        font-weight: bold; font-family: 'Courier New', Courier, monospace; font-size: 19px;
        color: #ecf0f1; background: #2c3e50; border-radius: 6px;
        cursor: pointer; transition: background 0.15s, transform 0.1s;
    }}
    .cell.dragging {{
        background: #3498db !important; color: #fff !important;
        transform: scale(1.08); border-radius: 50%;
    }}
    .cell.found {{
        background: #2ecc71 !important; color: #fff !important;
        border-radius: 50% !important; font-size: 20px;
        box-shadow: 0 0 8px #2ecc71; animation: pop 0.3s ease;
    }}
    .win-banner {{
        display: none; margin-top: 20px; padding: 15px 30px;
        background: #27ae60; color: white; font-weight: bold;
        border-radius: 10px; font-size: 18px; text-align: center;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
    }}
    @keyframes pop {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); }}
    }}
</style>
</head>
<body>

<div class="header-box">🕵️‍♂️ Juanes Cazados: <span id="counter">0</span> / 20</div>
<div class="grid" id="soup-grid"></div>
<div class="win-banner" id="win-banner">
    🎉 ¡BRUTAL! HAS CAZADO LOS 20 JUANES.<br>
    🔑 Código de Registro Secreto: <span style="font-family:monospace; background:#1b5e20; padding:3px 8px; border-radius:4px;">JUAN_MOUSE_MASTER_2026</span>
</div>

<script>
    const gridData = {json.dumps(grid_sopa)};
    const targetWords = {json.dumps(lista_juanes)};
    
    let isDragging = false;
    let startCell = null;
    let foundIndexes = [];
    
    const gridContainer = document.getElementById('soup-grid');
    
    // Crear el tablero visualmente
    for(let r=0; r<15; r++) {{
        for(let c=0; c<15; c++) {{
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.innerText = gridData[r][c];
            cell.setAttribute('data-r', r);
            cell.setAttribute('data-c', c);
            cell.id = `c-${{r}}-${{c}}`;
            
            // Eventos de ratón y táctiles
            cell.addEventListener('mousedown', (e) => startSelect(r, c));
            cell.addEventListener('mouseenter', (e) => updateSelect(r, c));
            gridContainer.appendChild(cell);
        }}
    }}
    
    window.addEventListener('mouseup', endSelect);
    
    function startSelect(r, c) {{
        isDragging = true;
        startCell = {{r, c}};
        highlightCells(startCell, startCell);
    }}
    
    function updateSelect(r, c) {{
        if (!isDragging) return;
        highlightCells(startCell, {{r, c}});
    }}
    
    function getLineCells(start, end) {{
        let dr = end.r - start.r;
        let dc = end.c - start.c;
        let steps = Math.max(Math.abs(dr), Math.abs(dc));
        
        if (steps !== 3) return null; // Un "JUAN" mide exactamente 4 letras (3 pasos de distancia)
        if (dr !== 0 && dc !== 0 && Math.abs(dr) !== Math.abs(dc)) return null; // No es recta ni diagonal perfecta
        
        let stepR = dr === 0 ? 0 : dr / steps;
        let stepC = dc === 0 ? 0 : dc / steps;
        
        let path = [];
        for(let i=0; i<=steps; i++) {{
            path.push({{r: start.r + stepR*i, c: start.c + stepC*i}});
        }}
        return path;
    }}
    
    function highlightCells(start, end) {{
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
        let path = getLineCells(start, end);
        if (path) {{
            path.forEach(cell => {{
                document.getElementById(`c-${{cell.r}}-${{cell.c}}`).classList.add('dragging');
            }});
        }} else {{
            document.getElementById(`c-${{start.r}}-${{start.c}}`).classList.add('dragging');
        }}
    }}
    
    function endSelect() {{
        if (!isDragging) return;
        isDragging = false;
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
    }}
    
    // Captura el mouseup final para validar la palabra elegida
    gridContainer.addEventListener('mouseup', (e) => {{
        if(!isDragging) return;
        let endEl = e.target;
        if(endEl.classList.contains('cell')) {{
            let er = parseInt(endEl.getAttribute('data-r'));
            let ec = parseInt(endEl.getAttribute('data-c'));
            checkWord(startCell, {{r: er, c: ec}});
        }}
    }});

    function checkWord(start, end) {{
        let path = getLineCells(start, end);
        if (!path) return;
        
        for(let i=0; i<targetWords.length; i++) {{
            if (foundIndexes.includes(i)) continue;
            let target = targetWords[i];
            
            // Comprobación en ambos sentidos (al derecho y al revés)
            let matchForward = true, matchBackward = true;
            for(let j=0; j<4; j++) {{
                if(path[j].r !== target[j].r || path[j].c !== target[j].c) matchForward = false;
                if(path[j].r !== target[3-j].r || path[j].c !== target[3-j].c) matchBackward = false;
            }}
            
            if (matchForward || matchBackward) {{
                foundIndexes.push(i);
                target.forEach(cell => {{
                    document.getElementById(`c-${{cell.r}}-${{cell.c}}`).classList.add('found');
                }});
                document.getElementById('counter').innerText = foundIndexes.length;
                
                if (foundIndexes.length === 20) {{
                    document.getElementById('win-banner').style.display = 'block';
                }}
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
    components.html(html_game, height=660)

with col_registro:
    st.markdown("### 🏆 Canjea tu Código de Victoria para registrar tu nombre en la lista. ¡BUEN JUAN A TODOS!")
    st.write("Cuando se te dé el código secreto al hallar los 20 JUANES, pégalo aquí abajo:")
    
    codigo_verificador = st.text_input("Introduce el código de la sopa:", type="password")
    
    if codigo_verificador.strip() == "JUAN_MOUSE_MASTER_2026":
        st.success("🔓 ¡CÓDIGO VERIFICADO! Has desbloqueado el acceso al Salón de la Fama.")
        with st.form("salon_fama_form", clear_on_submit=True):
            nombre_jugador = st.text_input("Tu Nombre / Alias:")
            enviar_nombre = st.form_submit_button("🥇 Inmortalizar mi Nombre")
            
            if enviar_nombre and nombre_jugador:
                guardar_ganador(nombre_jugador)
                st.success(f"¡Brutal! {nombre_jugador} ha sido registrado oficialmente.")
                st.rerun()
    else:
        if codigo_verificador:
            st.error("Código incorrecto. Asegúrate de cazar los 20 Juanes completos.")

    st.markdown("---")
    st.markdown("### 🌟 Historial de Ganadores")
    df_ganadores = listar_ganadores()
    if not df_ganadores.empty:
        st.dataframe(df_ganadores.sort_index(ascending=False), use_container_width=True, hide_index=True)
    else:
        st.caption("Aún nadie ha completado la sopa con el ratón. ¿Quién se llevará la pole?")
