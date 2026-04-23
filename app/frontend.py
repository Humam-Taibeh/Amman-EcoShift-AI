import streamlit as st

st.set_page_config(
    page_title="Amman OS | Login",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# STRICT CSS INJECTION - Placed at module level, zero indentation
STYLE_CODE = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
    color: #FFFFFF;
}

.stApp {
    background-color: #0a0a0a;
}

/* Hide Default Streamlit Clutter */
header, footer { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Google Button */
.google-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 12px;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 20px;
    color: white;
    font-weight: 600;
    transition: all 0.3s;
}
.google-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: #00FFFF;
}

/* Showcase Column */
.showcase-bg {
    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(0,255,255,0.05));
    border-left: 1px solid rgba(255,255,255,0.05);
    border-radius: 40px 0 0 40px;
    padding: 60px;
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-header {
    font-size: 4.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 40px;
    background: linear-gradient(135deg, #FFFFFF, #888888);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -2px;
}

/* Metric Cards */
.card-container {
    display: flex;
    gap: 20px;
}
.metric-card {
    flex: 1;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    padding: 25px;
    transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
}
.metric-card:hover {
    transform: translateY(-8px);
    border-color: rgba(0, 255, 255, 0.5);
    box-shadow: 0 10px 20px rgba(0, 255, 255, 0.1);
}
.metric-val {
    font-size: 2.2rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 10px 0;
}
.metric-label {
    font-size: 0.8rem;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Streamlit Inputs Customization */
div[data-baseweb="input"] {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #00FFFF !important;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
}
div[data-baseweb="input"] input {
    color: #FFF !important;
}

/* Streamlit Button Customization */
.stButton > button {
    background: linear-gradient(90deg, #00FFFF, #0088FF) !important;
    color: #000 !important;
    font-weight: 800 !important;
    border: none !important;
    padding: 12px !important;
    border-radius: 8px !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    margin-top: 20px !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
    transform: translateY(-2px) !important;
}
"""

def main():
    # STRICT CSS INJECTION
    st.markdown(f'<style>{STYLE_CODE}</style>', unsafe_allow_html=True)

    # Session State
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        render_login()
    else:
        render_dashboard()

def render_login():
    col1, col2 = st.columns([1, 1.4])
    
    with col1:
        st.markdown("<div style='padding: 60px 40px;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-weight:900; font-size:2.5rem; margin-bottom:5px;'>Amman OS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; margin-bottom:40px;'>Welcome to Eco-Shift. Please authenticate.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='google-btn'>
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="18px" height="18px" viewBox="0 0 48 48">
                <g><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path><path fill="none" d="M0 0h48v48H0z"></path></g>
            </svg>
            Continue with Google
        </div>
        <p style='text-align:center; color:#555; font-size:0.8rem; margin: 20px 0;'>OR PROCEED WITH CREDENTIALS</p>
        """, unsafe_allow_html=True)
        
        st.text_input("EMAIL", placeholder="operative@nexus.jo")
        st.text_input("PASSWORD", type="password", placeholder="••••••••")
        
        if st.button("ACCESS TERMINAL"):
            st.session_state.logged_in = True
            st.rerun()
            
        st.markdown("""
        <div style='display:flex; justify-content:space-between; margin-top:20px; font-size:0.8rem; color:#888;'>
            <span style='cursor:pointer;'>Forgot Password?</span>
            <span style='cursor:pointer;'>Create Account</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="showcase-bg">
            <div class="hero-header">Sustainable Mobility<br>Re-imagined.</div>
            
            <div class="card-container">
                <div class="metric-card">
                    <i class="fas fa-wallet" style="color: #00FFFF; font-size: 2rem;"></i>
                    <div class="metric-val">2.4k</div>
                    <div class="metric-label">JOD Saved</div>
                </div>
                <div class="metric-card">
                    <i class="fas fa-leaf" style="color: #00FF00; font-size: 2rem;"></i>
                    <div class="metric-val">92%</div>
                    <div class="metric-label">Efficiency</div>
                </div>
                <div class="metric-card">
                    <i class="fas fa-users" style="color: #8A2BE2; font-size: 2rem;"></i>
                    <div class="metric-val">14k+</div>
                    <div class="metric-label">Active Users</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_dashboard():
    # Placeholder for Dashboard logic so the app is complete and functional
    st.markdown("<h1 style='text-align:center; margin-top: 100px; color:#00FFFF;'>ACCESS GRANTED</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Welcome to the Main Terminal.</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
