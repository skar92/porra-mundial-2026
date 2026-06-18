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
# --- 🧩 SOPA DE LETRAS SIN DUPLICADOS (NUEVA CORRECCIÓN) ---
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
    
    # Cambiamos la semilla aleatoria para generar una distribución nueva y limpia
    random.seed(101) 
    
    colocados = 0
    intentos = 0
    juanes_coordenadas = []
    
    # Conjunto para registrar estrictamente el pack único de (Fila Inicial, Columna Inicial, Dirección)
    registro_coordenadas = set()
    
    while colocados < 20 and intentos < 4000:
        intentos += 1
        d = random.choice(direcciones)
        r = random.randint(0, tam - 1)
        c = random.randint(0, tam - 1)
        
        # Filtro estricto: Si la posición y dirección ya han sido usadas, se ignora por completo
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
        margin: 0; padding: 5px;
        background-color: transparent;
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
    🔑 Código de Registro Secreto: <span style="font-family:monospace; background:#1b5e20; padding:2px 6px; border-radius:4px;">ALABADOSEAJUAN!!</span>
</div>

<script>
    const gridData = {json.dumps(grid_sopa)};
    const targetWords = {json.dumps(lista_juanes)};
    
    let isDragging = false;
    let startCell = null;
    let currentEndCell = null;
    let foundIndexes = [];
    
    const gridContainer = document.getElementById('soup-grid');
    
    // Crear celdas
    for(let r=0; r<15; r++) {{
        for(let c=0; c<15; c++) {{
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.innerText = gridData[r][c];
            cell.setAttribute('data-r', r);
            cell.setAttribute('data-c', c);
            cell.id = `c-${{r}}-${{c}}`;
            gridContainer.appendChild(cell);
        }}
    }}
    
    // CONTROL DE MOUSE (ESCRITORIO)
    gridContainer.addEventListener('mousedown', (e) => {{
        if(e.target.classList.contains('cell')) {{
            isDragging = true;
            startCell = getCoords(e.target);
            currentEndCell = startCell;
            highlightCells(startCell, startCell);
        }}
    }});
    
    gridContainer.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        let el = document.elementFromPoint(e.clientX, e.clientY);
        if(el && el.classList.contains('cell')) {{
            let cellCoords = getCoords(el);
            currentEndCell = cellCoords;
            highlightCells(startCell, cellCoords);
        }}
    }});
    
    window.addEventListener('mouseup', () => {{
        if (!isDragging) return;
        isDragging = false;
        checkWord(startCell, currentEndCell);
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
    }});

    // CONTROL TÁCTIL (MÓVILES - EVITA EL SCROLL)
    gridContainer.addEventListener('touchstart', (e) => {{
        let touch = e.touches[0];
        let el = document.elementFromPoint(touch.clientX, touch.clientY);
        if(el && el.classList.contains('cell')) {{
            e.preventDefault(); 
            isDragging = true;
            startCell = getCoords(el);
            currentEndCell = startCell;
            highlightCells(startCell, startCell);
        }}
    }}, {{passive: false}});
    
    gridContainer.addEventListener('touchmove', (e) => {{
        if (!isDragging) return;
        e.preventDefault(); 
        let touch = e.touches[0];
        let el = document.elementFromPoint(touch.clientX, touch.clientY);
        if(el && el.classList.contains('cell')) {{
            let cellCoords = getCoords(el);
            currentEndCell = cellCoords;
            highlightCells(startCell, cellCoords);
        }}
    }}, {{passive: false}});
    
    gridContainer.addEventListener('touchend', (e) => {{
        if (!isDragging) return;
        isDragging = false;
        checkWord(startCell, currentEndCell);
        document.querySelectorAll('.cell.dragging').forEach(el => el.classList.remove('dragging'));
    }}, {{passive: false}});

    function getCoords(el) {{
        return {{
            r: parseInt(el.getAttribute('data-r')),
            c: parseInt(el.getAttribute('data-c'))
        }};
    }}
    
    function getLineCells(start, end) {{
        let dr = end.r - start.r;
        let dc = end.c - start.c;
        let steps = Math.max(Math.abs(dr), Math.abs(dc));
        
        if (steps !== 3) return null; 
        if (dr !== 0 && dc !== 0 && Math.abs(dr) !== Math.abs(dc)) return null; 
        
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
    
    function checkWord(start, end) {{
        if(!start || !end) return;
        let path = getLineCells(start, end);
        if (!path) return;
        
        for(let i=0; i<targetWords.length; i++) {{
            if (foundIndexes.includes(i)) continue;
            let target = targetWords[i];
            
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
    components.html(html_game, height=560)

with col_registro:
    st.markdown("### 🏆 Canjear Código de Victoria")
    st.write("Cuando la sopa interactiva te dé el código secreto al hallar los 20 Juanes, pégalo aquí abajo:")
    
    codigo_verificador = st.text_input("Introduce el código de la sopa:", type="password")
    
    if codigo_verificador.strip() == "ALABADOSEAJUAN!!":
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
        st.caption("Aún nadie ha completado la sopa. ¿Quién se llevará la pole?")
