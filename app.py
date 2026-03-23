import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Nuvix Picks AI", page_icon="⚡", layout="centered")

# --- ESTILOS CSS (Mantenemos la estética Dark/Neon) ---
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Contenedores Estilo Card */
    .card {
        background-color: #1E293B; border-radius: 12px; padding: 20px;
        border: 1px solid #334155; margin-bottom: 20px;
    }
    .odds-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
        background: #0F172A; padding: 15px; border-radius: 8px; margin: 15px 0;
    }
    .odd-item { text-align: center; }
    .odd-label { font-size: 10px; color: #94A3B8; text-transform: uppercase; }
    .odd-val { font-size: 14px; font-weight: bold; color: #F8FAFC; }
    
    /* Alertas */
    .alert-box {
        display: flex; align-items: center; gap: 10px;
        background: #0F172A; padding: 10px; border-radius: 8px;
        margin-top: 10px; font-size: 12px; border-left: 4px solid #38BDF8;
    }
    
    /* Sección de Predicción */
    .prediction-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 15px;
    }
    .confidence-circle {
        border: 4px solid #22C55E; border-radius: 50%; width: 70px; height: 70px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .analysis-text { line-height: 1.6; color: #CBD5E1; font-size: 14px; }
    
    /* Botón Volver */
    .stButton>button { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS MOCK (Datos del repositorio) ---
GAMES = {
    "1": {
        "id": "1", "sport": "NFL • Week 14", "game_date": "2026-12-08 16:25",
        "away_team": "Eagles", "home_team": "Cowboys",
        "spread": "PHI -3.5", "total": "O/U 47.5", "moneyline_away": "-175", "moneyline_home": "+150",
        "weather_alert": "Rain expected • Favors UNDER",
        "injury_update": "Starting QB Questionable",
        "prediction": {
            "pick_team": "Eagles", "pick_type": "Spread -3.5", "confidence_score": 78,
            "ai_analysis": "The Eagles defensive line matches up exceptionally well against a depleted Cowboys O-line. Expect heavy pressure on the QB.",
            "spanish_analysis": "La línea defensiva de los Eagles tiene una ventaja clara contra la línea ofensiva de los Cowboys, que tiene bajas. Se espera mucha presión al mariscal."
        }
    },
    "2": {
        "id": "2", "sport": "NBA", "game_date": "2026-12-08 20:00",
        "away_team": "Lakers", "home_team": "Celtics",
        "spread": "BOS -5.5", "total": "224.5", "moneyline_away": "+110", "moneyline_home": "-130",
        "prediction": None
    }
}

# --- LÓGICA DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_game_id' not in st.session_state:
    st.session_state.selected_game_id = None

def go_to_detail(game_id):
    st.session_state.page = 'detail'
    st.session_state.selected_game_id = game_id

def go_back():
    st.session_state.page = 'home'

# --- RENDERIZADO DE PÁGINAS ---

# PÁGINA: LISTA DE PICKS
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white;">Today\'s <span style="color:#38BDF8;">Picks</span></h2>', unsafe_allow_html=True)
    
    for gid, game in GAMES.items():
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#94A3B8;">
                    <span>{game['sport']}</span>
                    <span>{game['game_date']}</span>
                </div>
                <h3 style="margin:10px 0;">{game['away_team']} @ {game['home_team']}</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ver Análisis: {game['away_team']} vs {game['home_team']}", key=gid):
                go_to_detail(gid)
                st.rerun()

# PÁGINA: DETALLE DEL PICK
elif st.session_state.page == 'detail':
    game = GAMES[st.session_state.selected_game_id]
    
    if st.button("⬅️ Volver"):
        go_back()
        st.rerun()

    st.markdown(f"""
    <div class="card">
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#94A3B8;">
            <span>{game['sport']}</span>
            <span>{game['game_date']}</span>
        </div>
        <div style="display:flex; justify-content:space-around; align-items:center; margin:20px 0;">
            <h2 style="margin:0;">{game['away_team']}</h2>
            <span style="color:#64748B;">@</span>
            <h2 style="margin:0;">{game['home_team']}</h2>
        </div>
        
        <div class="odds-grid">
            <div class="odd-item"><p class="odd-label">Spread</p><p class="odd-val">{game['spread']}</p></div>
            <div class="odd-item"><p class="odd-label">Total</p><p class="odd-val">{game['total']}</p></div>
            <div class="odd-item"><p class="odd-label">ML ({game['away_team']})</p><p class="odd-val">{game['moneyline_away']}</p></div>
            <div class="odd-item"><p class="odd-label">ML ({game['home_team']})</p><p class="odd-val">{game['moneyline_home']}</p></div>
        </div>
    """, unsafe_allow_html=True)
    
    if game.get('weather_alert'):
        st.markdown(f'<div class="alert-box">☁️ {game["weather_alert"]}</div>', unsafe_allow_html=True)
    if game.get('injury_update'):
        st.markdown(f'<div class="alert-box">🏥 {game["injury_update"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # SECCIÓN DE PREDICCIÓN
    if game['prediction']:
        pred = game['prediction']
        st.markdown(f"""
        <h4 style="color:white; margin-left:5px;">AI Prediction</h4>
        <div class="card" style="border-color:#3B82F6; border-width:2px;">
            <div class="prediction-header">
                <div>
                    <p style="color:#60A5FA; font-size:10px; font-weight:bold; margin:0;">RECOMMENDED PICK</p>
                    <p style="font-size:18px; font-weight:bold; margin:0;">{pred['pick_team']} ({pred['pick_type']})</p>
                </div>
                <div class="confidence-circle">
                    <span style="color:#22C55E; font-size:18px; font-weight:bold;">{pred['confidence_score']}%</span>
                    <span style="font-size:7px; color:#94A3B8;">CONFIDENCE</span>
                </div>
            </div>
            <p style="font-size:10px; color:#94A3B8; letter-spacing:1px;">ANALYSIS</p>
            <p class="analysis-text">{pred['ai_analysis']}</p>
            <hr style="border-color:#334155;">
            <p style="font-size:10px; color:#94A3B8; letter-spacing:1px;">ANÁLISIS EN ESPAÑOL</p>
            <p class="analysis-text">{pred['spanish_analysis']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("La IA todavía está analizando este encuentro. Vuelve más tarde.")
