import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. JAVASCRIPT MEMORY LOCK (THE SECRET FIX) ---
# ഈ കോഡ് ബ്രൗസറിന്റെ ഉള്ളിൽ പേജ് വിവരങ്ങൾ സേവ് ചെയ്യും. 
# അതിനാൽ ഫോൺ റൊട്ടേറ്റ് ചെയ്താലും ആപ്പ് എവിടെയാണെന്ന് ബ്രൗസർ ഓർക്കും.
st.markdown("""
    <script>
    const saveState = (page, sub) => {
        localStorage.setItem('last_page', page);
        localStorage.setItem('last_sub', sub);
    };

    // പേജ് ലോഡ് ചെയ്യുമ്പോൾ പഴയ വിവരങ്ങൾ ഉണ്ടോ എന്ന് നോക്കുന്നു
    window.onload = () => {
        const p = localStorage.getItem('last_page');
        if (p && p !== 'home') {
            // ബ്രൗസർ ലിങ്കിൽ മാറ്റം വരുത്താൻ പ്രേരിപ്പിക്കുന്നു
            const url = new URL(window.location);
            if(!url.searchParams.has('p')) {
                url.searchParams.set('p', p);
                window.location.href = url.href;
            }
        }
    };
    </script>
    """, unsafe_allow_html=True)

# --- 3. URL-BASED PERSISTENCE ---
if 'page' not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("p", "home")
    st.session_state.current_sub = params.get("s", "Statistics")

def navigate(p, s="Statistics"):
    st.session_state.page = p
    st.session_state.current_sub = s
    st.query_params["p"] = p
    st.query_params["s"] = s
    # JavaScript വഴി ബ്രൗസർ മെമ്മറിയിലും സേവ് ചെയ്യുന്നു
    st.markdown(f"<script>saveState('{p}', '{s}');</script>", unsafe_allow_html=True)
    st.rerun()

# --- 4. CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #f0f2f6; }
    div.stButton > button {
        height: 70px !important; border-radius: 12px !important; 
        font-weight: bold; border: 2px solid #28a745 !important;
        background-color: white !important;
    }
    .banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DATA ---
FULL_SYLLABUS = {
    "Statistics": {"Modules": {"MODULE 1-10": "Sampling, Probability, Distributions, Estimation, Testing, Regression, Time Series, Index Numbers, Vital Stats."}},
    "Economics": {"Modules": {"Module I: Micro Theory": "Indifference Curve, Consumer's Surplus, Production Function.", "Module II-VII": "Macro, Fiscal, Indian & Kerala Economy, Econometrics."}}
}

# --- 6. UI LOGIC ---
page = st.session_state.get('page', 'home')
sub = st.session_state.get('current_sub', 'Statistics')

if page == "home":
    st.markdown("<div class='banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate("exam_detail")

elif page == "exam_detail":
    if st.button("⬅ Back Home"): navigate("home")
    st.markdown("### 📍 Select Subject")
    for s in FULL_SYLLABUS.keys():
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            navigate("sub_options", s)

elif page == "sub_options":
    if st.button("⬅ Back"): navigate("exam_detail")
    st.markdown(f"### 📚 {sub}")
    if st.button("📖 Syllabus", use_container_width=True): navigate("syllabus_view", sub)
    if st.button("🎯 Test Practice", use_container_width=True): navigate("quiz_setup", sub)

elif page == "syllabus_view":
    if st.button("⬅ Back"): navigate("sub_options", sub)
    st.write(FULL_SYLLABUS.get(sub, {}).get("Modules", {}))

elif page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate("sub_options", sub)
    st.info("ക്വിസ് തയ്യാറാകുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Shakeelurahman OP</p>", unsafe_allow_html=True)