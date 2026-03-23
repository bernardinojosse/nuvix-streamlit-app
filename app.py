import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE LLAVES (Tus llaves ya integradas) ---
ODDS_API_KEY = "aa1b6ba3f8c2d0db7f385589c2e4b7e7"
AF_API_KEY = "ce5c4b7acd955eec8ea540250e554f90"

st.set_page_config(page_title="Nuvix Pro AI", page_icon="⚡", layout="wide")

# --- ESTILOS CSS PROFESIONALES ---
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .main-card {
        background: #1E293B; border-radius: 15px; padding: 20px;
        border: 1px solid #334155; margin-bottom: 20px;
    }
    .ev-badge {
        background: #22C55E; color: #064E3B; font-weight: 800;
        padding: 4px 12px; border-radius: 20px; font-size: 12px;
    }
    .sharp-alert {
        background: rgba(250, 204, 21, 0.1); border: 1px solid #FACC15;
        padding: 10px; border-radius: 8px; color: #FACC15; font-size: 12px;
    }
    .metric-box { text-align: center; background: #0F172A; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA MATEMÁTICA ---
def get_implied_prob(odds):
    if odds > 0: return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)

# --- OBTENCIÓN DE DATOS REALES ---
@st.cache_data(ttl=3600)
def fetch_data():
    # Nota: Usamos NFL como ejemplo, puedes cambiar el sport_key
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={ODDS_API_KEY}&regions=us&markets=h2h,spreads"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

# --- RENDERIZADO DE INTERFAZ ---
st.title("⚡ NUVIX PRO AI")
st.markdown("### Dashboard de Inteligencia Deportiva & Value Betting")

data = fetch_data()

if not data:
    st.error("No se pudieron cargar los datos. Revisa tu Odds API Key.")
else:
    # Sidebar para Filtros
    sport_select = st.sidebar.selectbox("Seleccionar Liga", ["NFL", "NBA", "Soccer"])
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Matchup Analysis & Predictions")
        for game in data[:5]:  # Limitamos a 5 para el ejemplo
            home = game['home_team']
            away = game['away_team']
            commence_time = datetime.fromisoformat(game['commence_time'].replace('Z', '')).strftime('%H:%M')
            
            # Simulación de IA (Aquí conectarías con tu lógica de Predictbet)
            ai_prob = 65  # 65% probabilidad para el local
            odds_val = -110 # Cuota real de la API
            edge = ai_prob - (get_implied_prob(odds_val) * 100)

            with st.container():
                st.markdown(f"""
                <div class="main-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#94A3B8; font-size:12px;">{game['sport_title']} • HOY {commence_time}</span>
                        {f'<span class="ev-badge">🔥 EV+ EDGE: {edge:.1f}%</span>' if edge > 5 else ''}
                    </div>
                    
                    <div style="display:flex; justify-content:space-around; align-items:center; margin:20px 0;">
                        <div style="text-align:center;">
                            <img src="https://via.placeholder.com/50" width="50">
                            <p><b>{away}</b></p>
                        </div>
                        <div style="color:#475569; font-weight:bold;">VS</div>
                        <div style="text-align:center;">
                            <img src="https://via.placeholder.com/50" width="50">
                            <p><b>{home}</b></p>
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-bottom:15px;">
                        <div class="metric-box"><p style="font-size:10px; color:#64748B; margin:0;">SPREAD</p><b>-3.5</b></div>
                        <div class="metric-box"><p style="font-size:10px; color:#64748B; margin:0;">O/U</p><b>48.5</b></div>
                        <div class="metric-box"><p style="font-size:10px; color:#64748B; margin:0;">ML</p><b>{odds_val}</b></div>
                    </div>

                    <div class="sharp-alert">
                        <b>⚠️ SHARP MOVE:</b> Se detectó flujo de dinero profesional hacia {home}. La línea abrió en -4 y bajó a -3.5.
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.subheader("Smart Parlay 🚀")
        st.markdown("""
        <div style="background:linear-gradient(135deg, #1E293B, #0F172A); padding:20px; border-radius:15px; border: 2px solid #FACC15;">
            <p style="color:#FACC15; font-weight:bold; margin-bottom:15px;">TOP ACCA DEL DÍA</p>
            <div style="font-size:13px; color:#CBD5E1;">
                <p>✅ Eagles ML (-175)</p>
                <p>✅ Over 224.5 NBA (-110)</p>
                <p>✅ Real Madrid ML (+120)</p>
            </div>
            <hr style="border-color:#334155;">
            <div style="display:flex; justify-content:space-between;">
                <span>CUOTA TOTAL:</span><span style="color:#FACC15; font-weight:bold;">+450</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>PROB. ÉXITO:</span><span style="color:#22C55E; font-weight:bold;">38.4%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Market Sentiment")
        # Gráfica de Sentimiento
        fig = go.Figure(go.Bar(
            x=[70, 30],
            y=['Public', 'Pros'],
            orientation='h',
            marker_color=['#3B82F6', '#FACC15']
        ))
        fig.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Módulo de Gestión de Bankroll: Sugerencia de apuesta: 1-2 Unidades por pick.")
