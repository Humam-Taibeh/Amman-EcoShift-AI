import streamlit as st
import requests
import json
import time
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Eco-Shift AI | Cyber-Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Cyberpunk 2077 CSS Injection ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
    /* Reset & Background */
    html, body, [class*="st-"] {
        font-family: 'Share Tech Mono', monospace;
        color: #00ffc3;
    }
    .main {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0, 255, 195, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 195, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        position: relative;
    }
    
    /* Scanline Effect */
    .main::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 2;
        background-size: 100% 4px, 3px 100%;
        pointer-events: none;
    }

    /* Cyber Card */
    .cyber-card {
        background: rgba(0, 0, 0, 0.85);
        border: 1px solid #00ffc3;
        box-shadow: 0 0 15px rgba(0, 255, 195, 0.2), inset 0 0 5px rgba(0, 255, 195, 0.1);
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .cyber-card::after {
        content: "";
        position: absolute;
        top: 0; right: 0;
        border-style: solid;
        border-width: 0 15px 15px 0;
        border-color: transparent #00ffc3 transparent transparent;
    }
    
    /* Hero Metrics */
    .hero-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 40px 0;
    }
    .hero-metric {
        text-align: center;
        padding: 30px;
        background: rgba(0, 255, 195, 0.05);
        border: 2px solid #00ffc3;
        box-shadow: 0 0 25px rgba(0, 255, 195, 0.3);
        min-width: 250px;
        clip-path: polygon(10% 0, 100% 0, 100% 85%, 90% 100%, 0 100%, 0 15%);
    }
    .hero-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5em;
        font-weight: 900;
        color: #00ffc3;
        text-shadow: 0 0 20px #00ffc3;
    }
    .hero-label {
        font-size: 1em;
        letter-spacing: 3px;
        color: #00ffc3;
        opacity: 0.7;
        margin-top: 10px;
    }
    
    /* Sidebar */
    .css-1d391kg { background-color: #000 !important; border-right: 1px solid #00ffc3 !important; }
    
    /* Buttons */
    .stButton>button {
        background: transparent;
        color: #00ffc3;
        border: 1px solid #00ffc3;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 15px;
        transition: all 0.2s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #00ffc3;
        color: #000;
        box-shadow: 0 0 30px #00ffc3;
    }
    
    /* Headers */
    .cyber-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 2em;
        color: #00ffc3;
        text-shadow: 2px 2px #ff0055; /* Glitch effect */
        margin-bottom: 20px;
    }

    /* Map Override */
    .stMap {
        filter: invert(1) hue-rotate(180deg) brightness(0.8) contrast(1.2);
        border: 1px solid #00ffc3;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: Cyber-Inputs ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffc3; text-shadow: 0 0 10px #00ffc3;'>AMMAN_OS_v4.0</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### [GEO_COORD_INPUT]")
    origin_lat = st.number_input("ORIGIN_LAT", value=31.9515, format="%.4f")
    origin_lng = st.number_input("ORIGIN_LNG", value=35.9394, format="%.4f")
    dest_lat = st.number_input("DEST_LAT", value=31.9527, format="%.4f")
    dest_lng = st.number_input("DEST_LNG", value=35.8548, format="%.4f")
    
    st.markdown("---")
    st.markdown("### [DRIVE_SYSTEM]")
    vehicle_type = st.selectbox("CORE_PROFILE", ["GASOLINE", "HYBRID", "ELECTRIC"], index=2)
    
    st.markdown("---")
    if st.button("RUN_OPTIMIZER_CORE"):
        st.session_state.run = True
    else:
        st.session_state.run = False

# --- Main Interface ---

if not st.session_state.run:
    # --- Landing / Terminal View ---
    st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4em; color:#00ffc3; text-shadow:0 0 30px #00ffc3;'>ECO_SHIFT <span style='color:#ff0055;'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.5em; letter-spacing:5px;'>[ STATUS: WAITING_FOR_INPUT ]</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='cyber-card'>
            <h3 style='color:#00ffc3;'>TERRAIN_SENSORS: ACTIVE</h3>
            <p>Accessing Amman Elevation Grids... Sampling 7 hills topography...</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='cyber-card'>
            <h3 style='color:#00ffc3;'>AI_MODELS: READY</h3>
            <p>Gemini 2.0 Core initialized... Contextual traffic awareness: ON...</p>
        </div>""", unsafe_allow_html=True)

else:
    # --- Execution Sequence ---
    with st.spinner("[ CALCULATING_VECTORS... ]"):
        try:
            payload = {
                "origin": {"lat": origin_lat, "lng": origin_lng},
                "destination": {"lat": dest_lat, "lng": dest_lng},
                "vehicle_type": vehicle_type
            }
            response = requests.post("http://127.0.0.1:8000/optimize", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                route = data["routes"][0]
                terrain = route.get("terrain_metrics", {})

                # --- Huge Glow Metrics ---
                st.markdown(f"""
                <div class="hero-container">
                    <div class="hero-metric">
                        <div class="hero-value">{route['efficiency_score']}%</div>
                        <div class="hero-label">ECO_EFFICIENCY</div>
                    </div>
                    <div class="hero-metric">
                        <div class="hero-value">{route['money_saved_jod']}</div>
                        <div class="hero-label">SAVINGS_JOD</div>
                    </div>
                    <div class="hero-metric">
                        <div class="hero-value">{route['co2_savings_grams']}</div>
                        <div class="hero-label">CO2_OFFSET_G</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --- Cyber Grid Layout ---
                c_left, c_right = st.columns([1.5, 1])

                with c_left:
                    st.markdown("<div class='cyber-header'>[ TRAJECTORY_MAP ]</div>", unsafe_allow_html=True)
                    st.map(data=[{"lat": origin_lat, "lon": origin_lng}, {"lat": dest_lat, "lon": dest_lng}], zoom=13)
                    
                    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div class='cyber-header'>[ AI_ADVISOR_LOG ]</div>", unsafe_allow_html=True)
                    st.markdown(f"""<div class='cyber-card' style='border-left: 5px solid #ff0055;'>
                        <p style='color:#00ffc3; font-size:1.2em;'>>> MASTER_TIP: {route['master_tip']}</p>
                    </div>""", unsafe_allow_html=True)

                with c_right:
                    st.markdown("<div class='cyber-header'>[ TERRAIN_DATA ]</div>", unsafe_allow_html=True)
                    st.markdown(f"""<div class='cyber-card'>
                        <p>ASCENT: {terrain.get('ascent')}M</p>
                        <p>DESCENT: {terrain.get('descent')}M</p>
                        <p>OPTIMAL_V: {route['optimal_speed_kmh']} KM/H</p>
                        <p>ETA: {route['duration']}</p>
                    </div>""", unsafe_allow_html=True)

                    st.markdown("<div class='cyber-header'>[ ECO_ZONES ]</div>", unsafe_allow_html=True)
                    for zone in route.get("eco_zones", []):
                        st.markdown(f"""<div class='cyber-card'>
                            <span style='color:#ff0055; font-weight:bold;'>[ZONE_{zone['zone']}]</span><br/>
                            {zone['advice']}
                        </div>""", unsafe_allow_html=True)
                
                if data.get("cached"):
                    st.toast("⚡ CACHE_HIT: Instant response.", icon="⚡")

            else:
                st.error("CORE_FAILURE: Backend refused response.")
        
        except Exception as e:
            st.error("SYSTEM_OFFLINE: Could not establish uplink.")
            st.write(e)
