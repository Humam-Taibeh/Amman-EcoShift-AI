"""
Eco-Shift AI Precision Navigator Dashboard.
Handles UI layout, map rendering, and backend interaction.
"""

import time
import requests
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
    """Return coordinates for a given location string."""
    return LOCATIONS.get(location_name, LOCATIONS["Default"])

def main() -> None:
    """Main execution function for the Streamlit dashboard."""
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Eco-Shift AI | Precision Navigator",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- Initialize Session State ---
    if "run" not in st.session_state:
        st.session_state["run"] = False
    if "data" not in st.session_state:
        st.session_state["data"] = None
    if "initializing" not in st.session_state:
        st.session_state["initializing"] = False
    if "selected_route_index" not in st.session_state:
        st.session_state["selected_route_index"] = 0

    # --- Premium SaaS Design System ---
    css_styles = """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Syne:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        /* Hide all standard Streamlit elements */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        
        /* Global Reset & Background */
        .stApp {
            background: radial-gradient(circle at center, #0B1120 0%, #020617 100%) !important;
            background-attachment: fixed !important;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
            z-index: 1;
        }

        /* Bokeh/Particle Effects */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(59, 130, 246, 0.06) 0%, transparent 40%);
            z-index: -1;
            pointer-events: none;
            animation: pulseBg 8s infinite alternate ease-in-out;
        }

        @keyframes pulseBg {
            0% { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Syne', sans-serif !important;
            letter-spacing: -0.02em;
        }
        
        p, span, div {
            font-family: 'Inter', sans-serif !important;
        }

        .gradient-heading {
            font-family: 'Syne', sans-serif !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #FFFFFF 0%, #60A5FA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.6) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        /* Input Fields (Sleek & Glowing) */
        .stTextInput input, .stSelectbox > div > div {
            background-color: rgba(255,255,255,0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            padding: 10px 16px !important;
            font-size: 0.9rem !important;
            font-weight: 300 !important;
            transition: all 0.3s ease !important;
            box-shadow: none !important;
        }
        
        .stTextInput input:focus, .stSelectbox > div > div:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
            background-color: rgba(59, 130, 246, 0.05) !important;
        }

        .stTextInput label, .stSelectbox label {
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: rgba(255, 255, 255, 0.6) !important;
            margin-bottom: 0.25rem !important;
        }

        /* Buttons (High-Contrast Action) */
        .stButton > button {
            background: #2563EB !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-family: 'Syne', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: 0.03em !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            width: 100% !important;
            text-transform: none !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6) !important;
            border: none !important;
        }

        /* Status Pills */
        .status-pill-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 1.5rem;
            margin-bottom: 2rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            padding: 8px 20px;
            border-radius: 9999px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 0.8rem;
            font-weight: 500;
            color: #94a3b8;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .status-pill:hover, .status-pill.active {
            border-color: rgba(59, 130, 246, 0.4);
            color: #ffffff;
            background: rgba(59, 130, 246, 0.1);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
        }

        /* Elegant Containers / Cards */
        .premium-card {
            background: rgba(2, 6, 23, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(12px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .premium-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        /* Map & Visualization */
        .visual-wrapper {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        }

        /* Animations */
        .animate-fade-in {
            animation: fadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        .animate-slide-up {
            animation: slideUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(30px);
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideUp {
            to { opacity: 1; transform: translateY(0); }
        }

        /* Neural Link Glow (Main View) */
        .neural-glow {
            position: relative;
        }
        .neural-glow::before {
            content: '';
            position: absolute;
            top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 105%; height: 105%;
            background: radial-gradient(ellipse at center, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
            z-index: -1;
            pointer-events: none;
            animation: neuralPulse 4s infinite alternate;
        }
        @keyframes neuralPulse {
            0% { opacity: 0.5; transform: translate(-50%, -50%) scale(0.95); }
            100% { opacity: 1; transform: translate(-50%, -50%) scale(1.05); }
        }
        
        .loading-pulse {
            text-align: center;
            font-family: 'Syne', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #3B82F6, #FFFFFF, #3B82F6);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: loadingGlow 2s linear infinite;
            margin-top: 20vh;
        }
        
        @keyframes loadingGlow {
            to { background-position: 200% center; }
        }
    </style>
    """
    st.markdown(css_styles, unsafe_allow_html=True)

    # --- Sidebar: Navigation Inputs ---
    with st.sidebar:
        st.markdown("<h2 class='gradient-heading' style='font-size: 1.8rem;'>Eco-Shift AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 2rem; font-weight: 300;'>Precision Navigation Engine</p>", unsafe_allow_html=True)
        
        # Dual-Input Navigation
        start_loc = st.text_input("📍 ORIGIN", "Amman Citadel", placeholder="Search origin...")
        end_loc = st.text_input("🏁 DESTINATION", "Abdali Boulevard", placeholder="Search destination...")
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        vehicle_type = st.selectbox("VEHICLE TYPE", ["GASOLINE", "HYBRID", "ELECTRIC"], index=2)
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        if st.button("INITIALIZE MISSION", use_container_width=True):
            st.session_state["initializing"] = True
            st.session_state["run"] = False
            st.session_state["data"] = None

    # Resolve coordinates
    origin_lat, origin_lng = get_coords(start_loc)
    dest_lat, dest_lng = get_coords(end_loc)

    # --- Application State: Initialization ---
    if st.session_state["initializing"]:
        st.markdown("<div class='loading-pulse animate-fade-in'>ESTABLISHING_NEURAL_UPLINK...</div>", unsafe_allow_html=True)
        time.sleep(1.5)
        
        try:
            payload = {
                "origin": {"lat": origin_lat, "lng": origin_lng},
                "destination": {"lat": dest_lat, "lng": dest_lng},
                "vehicle_type": vehicle_type
            }
            response = requests.post("http://127.0.0.1:8000/optimize", json=payload, timeout=10)
            if response.status_code == 200:
                st.session_state["data"] = response.json()
                st.session_state["run"] = True
            else:
                st.error("UPLINK_FAILURE: Backend error.")
        except requests.RequestException:
            st.error("SYSTEM_OFFLINE: Could not reach backend.")
        
        st.session_state["initializing"] = False
        st.rerun()

    # --- Main Dashboard ---
    if not st.session_state["run"]:
        # Landing View: Mission Briefing
        st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="animate-slide-up" style="text-align: center; max-width: 800px; margin: 0 auto;">
                <h1 class="gradient-heading" style="font-size: 4.5rem; margin-bottom: 1.5rem; line-height: 1.1;">Ready to Shift?</h1>
                <p style="font-size: 1.2rem; color: #94a3b8; font-weight: 300; margin-bottom: 2rem; max-width: 600px; margin-inline: auto;">
                    Experience the next generation of terrain-aware navigation. 
                    Optimized for Amman's unique topography to maximize efficiency and performance.
                </p>
                
                <div class="status-pill-container animate-fade-in" style="animation-delay: 0.3s;">
                    <div class="status-pill active">✓ Terrain Aware</div>
                    <div class="status-pill active">⚡ Live Traffic</div>
                    <div class="status-pill active">🧠 AI Core v4</div>
                </div>
                
                <div style="height: 4rem;"></div>
                <p class="animate-fade-in" style="animation-delay: 0.6s; font-size: 0.85rem; color: rgba(255,255,255,0.4); letter-spacing: 0.15em; text-transform: uppercase; font-weight: 600;">
                    Configure your mission in the sidebar to begin
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        # Mission Command Center
        data = st.session_state["data"]
        routes = data.get("routes", []) if data else []
        
        if not routes:
            st.error("NO_VALID_TRAJECTORIES_FOUND.")
            if st.button("RETRY_UPLINK"):
                st.session_state["run"] = False
                st.rerun()
        else:
            # --- Route Selection ---
            st.markdown("<h3 class='gradient-heading animate-fade-in' style='font-size: 1.8rem; margin-bottom: 0.5rem;'>Mission Strategy</h3>", unsafe_allow_html=True)
            
            # Determine available route types
            route_options = []
            for i, r in enumerate(routes):
                label = r.get("type", f"ROUTE_{i+1}")
                route_options.append(label)
            
            selected_type = st.radio("SELECT STRATEGY", route_options, horizontal=True, label_visibility="collapsed")
            st.session_state["selected_route_index"] = route_options.index(selected_type)
            
            route = routes[st.session_state["selected_route_index"]]
            
            # Extract metrics safely for formatting
            terrain_metrics = route.get('terrain_metrics', {})
            ascent = terrain_metrics.get('ascent', 0)
            
            # Status Badges for the selected route
            st.markdown(f"""
                <div class="animate-fade-in status-pill-container" style="justify-content: flex-start; margin-top: 0; margin-bottom: 2rem;">
                    <div class="status-pill active">⛰️ Terrain: {ascent}m Ascent</div>
                    <div class="status-pill active">🚦 Traffic: Optimized</div>
                    <div class="status-pill active">🎯 AI Confidence: 98%</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Wrap the main visualization in the neural glow
            st.markdown("<div class='neural-glow animate-slide-up'>", unsafe_allow_html=True)
            
            # --- Top Layout: Map & Profile ---
            col_map, col_profile = st.columns([1.2, 0.8])
            
            with col_map:
                st.markdown("<div class='visual-wrapper'>", unsafe_allow_html=True)
                # Folium Map
                m = folium.Map(location=[origin_lat, origin_lng], zoom_start=14, tiles="CartoDB dark_matter")
                
                # Decode and draw polyline
                path_points = polyline.decode(route.get('polyline', ''))
                if path_points:
                    folium.PolyLine(path_points, color="#3b82f6", weight=5, opacity=0.8).add_to(m)
                
                # Markers
                folium.Marker([origin_lat, origin_lng], tooltip="START", icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
                folium.Marker([dest_lat, dest_lng], tooltip="END", icon=folium.Icon(color='red', icon='flag')).add_to(m)
                
                st_folium(m, width="100%", height=400)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_profile:
                st.markdown("<p style='font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.5rem; font-weight: 600; text-transform: uppercase;'>ELEVATION PROFILE</p>", unsafe_allow_html=True)
                elev_data = route.get("elevation_profile", [])
                if elev_data:
                    df_elev = pd.DataFrame({"Elevation": elev_data})
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        y=df_elev["Elevation"], 
                        fill='tozeroy', 
                        line={"color": '#3b82f6', "width": 2},
                        fillcolor='rgba(59, 130, 246, 0.1)'
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin={"l": 0, "r": 0, "t": 0, "b": 0},
                        height=200,
                        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
                        yaxis={"showgrid": False, "zeroline": False, "color": 'rgba(255,255,255,0.4)'}
                    )
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("ELEVATION_DATA_UNAVAILABLE")

            st.markdown("</div>", unsafe_allow_html=True) # End neural glow wrapper

            # --- Impact Metrics ---
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                money_saved = route.get('money_saved_jod', 0)
                st.markdown(f"""
                    <div class="premium-card animate-slide-up" style="animation-delay: 0.1s;">
                        <p style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Financial Saving</p>
                        <h2 style="margin: 0; font-family: 'Syne', sans-serif; font-weight: 700; color: #ffffff; font-size: 2rem;">{money_saved} <span style="font-size: 1rem; color: #94a3b8; font-family: 'Inter', sans-serif;">JOD</span></h2>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_m2:
                co2_grams = float(route.get('co2_savings_grams', 0))
                co2_kg = co2_grams / 1000
                st.markdown(f"""
                    <div class="premium-card animate-slide-up" style="animation-delay: 0.2s;">
                        <p style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">CO2 Reduction</p>
                        <h2 style="margin: 0; font-family: 'Syne', sans-serif; font-weight: 700; color: #ffffff; font-size: 2rem;">{co2_kg:.2f} <span style="font-size: 1rem; color: #94a3b8; font-family: 'Inter', sans-serif;">kg</span></h2>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_m3:
                strain_val = min(100, int((ascent / 100) * 20))
                strain_color = "#3b82f6" if strain_val < 30 else "#f59e0b" if strain_val < 70 else "#ef4444"
                st.markdown(f"""
                    <div class="premium-card animate-slide-up" style="animation-delay: 0.3s;">
                        <p style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Engine Strain</p>
                        <h2 style="margin: 0; font-family: 'Syne', sans-serif; font-weight: 700; color: {strain_color}; font-size: 2rem;">{strain_val}%</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            # --- AI Insights ---
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            col_adv_1, col_adv_2 = st.columns([1, 1])
            with col_adv_1:
                st.markdown("<p style='font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>AI Strategy Recommendation</p>", unsafe_allow_html=True)
                master_tip = route.get('master_tip', 'Maintain steady speeds for optimal efficiency.')
                st.markdown(f"""<div class="premium-card animate-slide-up" style="border-left: 4px solid #3b82f6; animation-delay: 0.4s;">
                    <p style="font-size: 1rem; color: #ffffff; font-weight: 300;">{master_tip}</p>
                </div>""", unsafe_allow_html=True)
            with col_adv_2:
                st.markdown("<p style='font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Eco-Sector Alerts</p>", unsafe_allow_html=True)
                for zone in route.get("eco_zones", [])[:2]:
                    advice = zone.get('advice', '')
                    st.markdown(f"<div class='premium-card animate-slide-up' style='padding: 1rem; margin-bottom: 0.5rem; animation-delay: 0.5s;'><p style='font-size:0.9rem; margin: 0; color: #cbd5e1; font-weight: 300;'><span style='color:#ef4444; font-weight: 600; margin-right: 8px;'>[Alert]</span> {advice}</p></div>", unsafe_allow_html=True)

            if data and data.get("cached"):
                st.toast("⚡ INSTANT_UPLINK_SUCCESS", icon="⚡")

if __name__ == "__main__":
    main()
