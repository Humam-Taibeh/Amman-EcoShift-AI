"""
Eco-Shift AI Masterpiece UI.
"""
import time
import requests
import textwrap
import pandas as pd
import folium
import polyline
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

# Mock locations for geocoding fallback
LOCATIONS = {
    "Amman Citadel": (31.9544, 35.9354),
    "Abdali Boulevard": (31.9633, 35.9056),
    "Default": (31.95, 35.93)
}

def get_coords(location_name: str) -> tuple[float, float]:
    return LOCATIONS.get(location_name, LOCATIONS["Default"])

def inject_global_css():
    css = textwrap.dedent("""
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Syne:wght@600;800&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        /* Base Resets */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        [data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
        
        .stApp {
            background-color: #020617 !important;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
            overflow-y: hidden; /* Prevent scrolling if possible */
        }

        /* Topography Background */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: 
                radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.05) 0%, transparent 60%),
                repeating-radial-gradient(circle at 50% 50%, transparent 0, transparent 40px, rgba(0, 255, 255, 0.03) 41px, transparent 42px);
            z-index: -1;
            pointer-events: none;
            animation: radarPulse 15s infinite linear;
        }
        
        @keyframes radarPulse {
            0% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.05); opacity: 0.8; }
            100% { transform: scale(1); opacity: 0.5; }
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 { font-family: 'Syne', sans-serif !important; }
        .mono-text { font-family: 'IBM Plex Mono', monospace !important; }
        
        .heading-dynamic {
            font-family: 'Syne', sans-serif !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #00ffff 0%, #ccff00 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.4));
            margin-bottom: 0.2rem;
            line-height: 1.1;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.8) !important;
            backdrop-filter: blur(24px) !important;
            border-right: 1px solid rgba(0, 255, 255, 0.15) !important;
        }

        /* Inputs */
        .stTextInput input, .stSelectbox > div > div {
            background-color: rgba(0, 255, 255, 0.02) !important;
            border: 1px solid rgba(0, 255, 255, 0.2) !important;
            border-radius: 4px !important;
            color: #00ffff !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 0.85rem !important;
            padding: 8px 12px !important;
            transition: all 0.3s ease !important;
            min-height: 40px !important;
            height: 40px !important;
        }
        
        .stTextInput input:focus, .stSelectbox > div > div:focus {
            background-color: rgba(0, 255, 255, 0.08) !important;
            border-color: #00ffff !important;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
            transform: scaleX(1.02);
        }

        .stTextInput label p, .stSelectbox label p {
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 0.7rem !important;
            color: #00ffff !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.3rem !important;
        }

        /* Buttons */
        button[data-testid="baseButton-primary"] {
            background: transparent !important;
            color: #ccff00 !important;
            border: 1px solid #ccff00 !important;
            border-radius: 4px !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            height: 45px !important;
            min-height: 45px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 10px rgba(204, 255, 0, 0.2), inset 0 0 10px rgba(204, 255, 0, 0.1) !important;
        }

        button[data-testid="baseButton-primary"]:hover {
            background: rgba(204, 255, 0, 0.15) !important;
            box-shadow: 0 0 20px rgba(204, 255, 0, 0.5), inset 0 0 15px rgba(204, 255, 0, 0.3) !important;
            text-shadow: 0 0 8px #ccff00;
        }

        button[data-testid="baseButton-secondary"] {
            background: rgba(0, 255, 255, 0.05) !important;
            color: #00ffff !important;
            border: 1px solid rgba(0, 255, 255, 0.3) !important;
            border-radius: 4px !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-weight: 600 !important;
            height: 45px !important;
            min-height: 45px !important;
            transition: all 0.3s ease !important;
        }
        
        button[data-testid="baseButton-secondary"]:hover {
            background: rgba(0, 255, 255, 0.15) !important;
            border-color: #00ffff !important;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.4) !important;
        }

        /* Glass Cards */
        .glass-card {
            background: rgba(2, 6, 23, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7), inset 0 0 0 1px rgba(0, 255, 255, 0.1);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        
        .glass-card:hover {
            border-color: rgba(204, 255, 0, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7), inset 0 0 0 1px rgba(204, 255, 0, 0.2);
        }

        /* Boot-up */
        .system-boot {
            animation: bootUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
        }
        @keyframes bootUp {
            0% { opacity: 0; filter: blur(10px) brightness(2); transform: scale(0.95); }
            100% { opacity: 1; filter: blur(0) brightness(1); transform: scale(1); }
        }

        /* Neural loader */
        .neural-link-loader {
            display: inline-block;
            font-family: 'IBM Plex Mono', monospace;
            color: #ccff00;
            font-size: 1.2rem;
            letter-spacing: 0.1em;
            text-shadow: 0 0 10px #ccff00;
            animation: blinker 1.5s linear infinite;
        }
        @keyframes blinker { 50% { opacity: 0.3; text-shadow: none; } }
        
        /* Floating Overlay Hack */
        div[data-testid="stVerticalBlock"]:has(#glass-overlay) {
            position: absolute !important;
            top: 20px !important;
            right: 20px !important;
            width: 380px !important;
            z-index: 9999 !important;
            background: transparent !important;
            pointer-events: none; /* Let clicks pass through empty space */
        }
        
        div[data-testid="stVerticalBlock"]:has(#glass-overlay) > * {
            pointer-events: auto; /* Re-enable clicks for cards */
        }
        
        div[data-testid="stVerticalBlock"]:has(#floating-heading) {
            position: absolute !important;
            top: 20px !important;
            left: 20px !important;
            width: 500px !important;
            z-index: 9999 !important;
            background: transparent !important;
            pointer-events: none;
        }
        div[data-testid="stVerticalBlock"]:has(#floating-heading) > * {
            pointer-events: auto;
        }

        /* Map Fullscreen */
        .full-map-wrapper iframe {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 1 !important;
        }

        /* No Red Errors */
        .custom-alert {
            background: rgba(2, 6, 23, 0.8);
            border: 1px solid #ccff00;
            padding: 1rem;
            border-radius: 8px;
            color: #ccff00;
            font-family: 'IBM Plex Mono', monospace;
            box-shadow: 0 0 15px rgba(204, 255, 0, 0.2);
            margin-bottom: 1rem;
        }
    </style>
    """)
    st.markdown(css, unsafe_allow_html=True)

def login_page():
    st.markdown(textwrap.dedent("""
    <style>
        [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="column"]:nth-child(1) { max-width: 420px !important; margin: 0 auto !important; }
    </style>
    """), unsafe_allow_html=True)
    
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    
    col_form, col_space, col_hero = st.columns([1, 0.1, 1.2])
    
    with col_form:
        st.markdown(textwrap.dedent("""
            <div class="system-boot" style="margin-bottom: 2rem;">
                <p class="mono-text" style="color: #00ffff; font-size: 0.8rem; margin-bottom: 0.2rem; letter-spacing: 0.1em;">// SECURE.AUTH</p>
                <h2 style="font-size: 2.5rem; color: #ffffff; line-height: 1.1; margin-bottom: 0.5rem; font-family: 'Syne', sans-serif;">SYSTEM<br><span style="color: #ccff00;">ACCESS</span></h2>
            </div>
        """), unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='system-boot' style='animation-delay: 0.2s;'>", unsafe_allow_html=True)
            email = st.text_input("IDENTIFIER [EMAIL]", placeholder="sysadmin@eco-shift.ai")
            password = st.text_input("SECURITY KEY [PASS]", type="password", placeholder="••••••••")
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            if st.button("INITIATE UPLINK", type="primary", use_container_width=True):
                st.session_state["logged_in"] = True
                st.session_state["run"] = False
                st.rerun()
                
            st.markdown(textwrap.dedent("""
                <div style="display: flex; align-items: center; margin: 2rem 0;">
                    <div style="flex-grow: 1; height: 1px; background: rgba(0,255,255,0.1);"></div>
                    <span class="mono-text" style="padding: 0 1rem; color: #00ffff; font-size: 0.7rem; opacity: 0.6;">SECONDARY PROTOCOL</span>
                    <div style="flex-grow: 1; height: 1px; background: rgba(0,255,255,0.1);"></div>
                </div>
            """), unsafe_allow_html=True)
            
            if st.button("OVERRIDE VIA GOOGLE", type="secondary", use_container_width=True):
                st.session_state["logged_in"] = True
                st.session_state["run"] = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    with col_hero:
        st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
        st.markdown(textwrap.dedent("""
            <div class="system-boot" style="text-align: right; animation-delay: 0.4s;">
                <h1 class="heading-dynamic" style="font-size: 5rem; text-align: right;">ECO<br>SHIFT</h1>
                <p class="mono-text" style="font-size: 1rem; color: #00ffff; opacity: 0.8; margin-top: -10px; margin-bottom: 2rem;">MASTERPIECE // EDITION</p>
                
                <div style="display: inline-flex; flex-direction: column; align-items: flex-end; gap: 10px;">
                    <div class="glass-card" style="padding: 10px 20px; border-radius: 8px; border-color: rgba(204,255,0,0.3);">
                        <span class="mono-text" style="color:#ccff00; font-size: 0.8rem;">[SYS] CORE_ONLINE</span>
                    </div>
                </div>
            </div>
        """), unsafe_allow_html=True)

def create_gauge(value, title, max_val, color_hex, suffix=""):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {'suffix': suffix, 'font': {'color': color_hex, 'family': 'IBM Plex Mono', 'size': 32}},
        title = {'text': title, 'font': {'color': '#ffffff', 'family': 'IBM Plex Mono', 'size': 11}},
        gauge = {
            'axis': {'range': [0, max_val], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.1)", 'showticklabels': False},
            'bar': {'color': color_hex},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, max_val], 'color': "rgba(0,255,255,0.05)"}
            ],
            'threshold': {
                'line': {'color': color_hex, 'width': 2},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#fff"},
        height=140,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    return fig

def dashboard_page():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h2 style='font-size: 1.8rem; color: #ffffff; font-family: \"Syne\", sans-serif;'>ECO<span style='color: #00ffff;'>SHIFT</span></h2>", unsafe_allow_html=True)
        st.markdown("<p class='mono-text' style='font-size: 0.75rem; color: #ccff00; margin-bottom: 2rem;'>// NEURAL TERMINAL</p>", unsafe_allow_html=True)
        
        start_loc = st.text_input("ORIGIN_NODE", "Amman Citadel")
        end_loc = st.text_input("TARGET_NODE", "Abdali Boulevard")
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        vehicle_type = st.selectbox("CHASSIS_CONFIG", ["ELECTRIC", "HYBRID", "COMBUSTION"])
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        if st.button("EXECUTE DIRECTIVE", type="primary", use_container_width=True):
            st.session_state["initializing"] = True
            st.session_state["run"] = False
            st.session_state["data"] = None

    origin_lat, origin_lng = get_coords(start_loc)
    dest_lat, dest_lng = get_coords(end_loc)

    # --- Fullscreen Bio-Map Base Layer ---
    # We render the map first so it acts as the background.
    st.markdown("<div class='full-map-wrapper'>", unsafe_allow_html=True)
    m = folium.Map(location=[origin_lat, origin_lng], zoom_start=14, tiles="CartoDB dark_matter", zoom_control=False)
    
    # If we have route data, draw it
    data = st.session_state.get("data")
    routes = data.get("routes", []) if data else []
    
    if st.session_state.get("run") and routes:
        idx = st.session_state.get("selected_route_index", 0)
        if idx < len(routes):
            route = routes[idx]
            path_points = polyline.decode(route.get('polyline', ''))
            is_eco = "ECO" in route.get("type", "").upper()
            accent_color = "#ccff00" if is_eco else "#00ffff"
            if path_points:
                folium.PolyLine(path_points, color=accent_color, weight=5, opacity=0.9).add_to(m)
            folium.CircleMarker([origin_lat, origin_lng], radius=6, color="#00ffff", fill=True, fill_opacity=1).add_to(m)
            folium.CircleMarker([dest_lat, dest_lng], radius=6, color=accent_color, fill=True, fill_opacity=1).add_to(m)

    st_folium(m, width="100%", height=1200) # large height to fill screen
    st.markdown("</div>", unsafe_allow_html=True)

    # Add a cyan tint over the map
    st.markdown("<div style='position: fixed; top:0; left:0; width:100vw; height:100vh; background: rgba(0, 255, 255, 0.03); pointer-events:none; z-index:2;'></div>", unsafe_allow_html=True)

    # --- Boot-up / Init State Overlay ---
    if st.session_state.get("initializing"):
        with st.container():
            st.markdown("<span id='floating-heading'></span>", unsafe_allow_html=True)
            st.markdown(textwrap.dedent("""
                <div class='glass-card system-boot'>
                    <div class='neural-link-loader'>ESTABLISHING_NEURAL_UPLINK...</div>
                    <p class='mono-text' style='color: #00ffff; font-size: 0.8rem; margin-top: 10px; opacity: 0.8;'>Analyzing Bio-Map Telemetry</p>
                </div>
            """), unsafe_allow_html=True)
        time.sleep(1.5)
        
        # Simulated Backend
        st.session_state["data"] = {
            "routes": [
                {
                    "type": "ECO_OPTIMIZED",
                    "polyline": polyline.encode([(origin_lat, origin_lng), (31.96, 35.92), (dest_lat, dest_lng)]),
                    "money_saved_jod": 2.45,
                    "co2_savings_grams": 1200,
                    "terrain_metrics": {"ascent": 45},
                    "master_tip": "Regen braking optimal on sector 2 descents.",
                    "eco_zones": [{"advice": "High traffic bypassed via low-elevation routing."}]
                },
                {
                    "type": "BALANCED_DRIVE",
                    "polyline": polyline.encode([(origin_lat, origin_lng), (31.958, 35.91), (dest_lat, dest_lng)]),
                    "money_saved_jod": 1.20,
                    "co2_savings_grams": 600,
                    "terrain_metrics": {"ascent": 65},
                    "master_tip": "Standard protocol. Optimal blend of speed and efficiency.",
                    "eco_zones": [{"advice": "Moderate elevation change detected."}]
                }
            ]
        }
        st.session_state["run"] = True
        st.session_state["initializing"] = False
        st.rerun()

    # --- Overlays ---
    if not st.session_state.get("run"):
        # Awaiting Telemetry Floating Heading
        with st.container():
            st.markdown("<span id='floating-heading'></span>", unsafe_allow_html=True)
            st.markdown(textwrap.dedent("""
                <div class="system-boot">
                    <p class="mono-text" style="color: #00ffff; letter-spacing: 0.1em; margin-bottom: 0;">// STANDBY</p>
                    <h1 class="heading-dynamic" style="font-size: 3rem;">AWAITING<br>TELEMETRY</h1>
                </div>
            """), unsafe_allow_html=True)

    else:
        # Floating Dynamic Heading
        routes = st.session_state.get("data", {}).get("routes", [])
        if not routes:
            with st.container():
                st.markdown("<span id='floating-heading'></span>", unsafe_allow_html=True)
                st.markdown("<div class='custom-alert'>[ERROR] NO_TRAJECTORIES_FOUND</div>", unsafe_allow_html=True)
                if st.button("REBOOT"):
                    st.session_state["run"] = False
                    st.rerun()
            return

        route_options = [r.get("type", f"ROUTE_{i}") for i, r in enumerate(routes)]
        
        with st.container():
            st.markdown("<span id='floating-heading'></span>", unsafe_allow_html=True)
            selected_type = st.radio("STRATEGY", route_options, horizontal=True, label_visibility="collapsed")
            st.session_state["selected_route_index"] = route_options.index(selected_type)
            
            is_eco = "ECO" in selected_type.upper()
            accent_color = "#ccff00" if is_eco else "#00ffff"
            
            st.markdown(textwrap.dedent(f"""
                <div class="system-boot">
                    <p class="mono-text" style="color: {accent_color}; letter-spacing: 0.1em; margin-bottom: 0; font-size: 0.8rem;">// ACTIVE_TRAJECTORY</p>
                    <h1 class="heading-dynamic" style="font-size: 2.5rem; background: linear-gradient(90deg, {accent_color} 0%, #ffffff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        {selected_type}
                    </h1>
                </div>
            """), unsafe_allow_html=True)

        # Floating Glass Cards overlay (Right Side)
        with st.container():
            st.markdown("<span id='glass-overlay'></span>", unsafe_allow_html=True)
            
            route = routes[st.session_state["selected_route_index"]]
            money_saved = float(route.get('money_saved_jod', 0))
            co2_grams = float(route.get('co2_savings_grams', 0))
            ascent = route.get('terrain_metrics', {}).get('ascent', 0)
            strain_val = min(100, int((ascent / 100) * 20))
            
            st.markdown("<div class='glass-card system-boot' style='padding: 1rem;'>", unsafe_allow_html=True)
            fig_money = create_gauge(money_saved, "FINANCIAL_IMPACT [JOD]", 5, accent_color)
            st.plotly_chart(fig_money, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card system-boot' style='padding: 1rem; animation-delay: 0.1s;'>", unsafe_allow_html=True)
            fig_co2 = create_gauge(co2_grams/1000, "EMISSION_OFFSET [KG]", 5, accent_color)
            st.plotly_chart(fig_co2, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(textwrap.dedent(f"""
                <div class='glass-card system-boot' style='padding: 1rem; animation-delay: 0.2s;'>
                    <p class='mono-text' style='color: {accent_color}; font-size: 0.8rem; margin-bottom: 0;'>[SYS] ENGINE_STRAIN</p>
                    <h2 style='color: #fff; margin-top: 0;'>{strain_val}% <span style='font-size: 0.8rem; color: #00ffff;'>Load</span></h2>
                </div>
            """), unsafe_allow_html=True)

def main() -> None:
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "run" not in st.session_state:
        st.session_state["run"] = False
    if "data" not in st.session_state:
        st.session_state["data"] = None
    if "initializing" not in st.session_state:
        st.session_state["initializing"] = False
    if "selected_route_index" not in st.session_state:
        st.session_state["selected_route_index"] = 0

    st.set_page_config(
        page_title="Eco-Shift AI | Masterpiece",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed" if not st.session_state["logged_in"] else "expanded"
    )

    inject_global_css()

    if not st.session_state["logged_in"]:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
