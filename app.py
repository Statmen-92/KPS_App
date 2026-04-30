import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide")

# --- 2. GLOBAL MOBILE ZOOM & ORIENTATION FIX ---
st.markdown("""
    <script>
    const fixViewport = () => {
        var meta = document.querySelector('meta[name="viewport"]');
        if (!meta) {
            meta = document.createElement('meta');
            meta.name = 'viewport';
            document.getElementsByTagName('head')[0].appendChild(meta);
        }
        meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
    };
    fixViewport();
    window.addEventListener('orientationchange', () => { setTimeout(fixViewport, 500); });
    </script>
    """, unsafe_allow_html=True)

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 1rem; }
    .stApp { background-color: #f0f2f6; }
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    div.stButton > button {
        height: 70px !important;
        border-radius: 12px !important;
        font-weight: bold;
        border: 2px solid #28a745 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SAFE STATE INITIALIZATION ---
# 'AttributeError' വരാതിരിക്കാൻ ഈ ലോജിക് ഓരോ തവണയും വേരിയബിളുകൾ ഉറപ്പാക്കുന്നു
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = "Research Officer"
if 'current_sub' not in st.session_state: st.session_state.current_sub = "Statistics"

# --- 5. DATA (NO SKIPPING) ---
SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1-3": "Sampling, Probability, Standard Distributions.",
            "MODULE 4-10": "Sampling Distributions, Estimation, Hypothesis, Regression, Time Series, Index Numbers, Vital Stats."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory": "Indifference Curve, Consumer's Surplus, Production Function.",
            "Module II-VII": "Macro, Fiscal, Development, Indian & Kerala Economy, Econometrics."
        }
    }
}

QUIZ_BANK = {
    "Economics": {
        "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
        "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
    }
}

# --- 6. NAVIGATION FUNCTIONS ---
def set_page(page_name, exam=None, sub=None):
    st.session_state.page = page_name
    if exam: st.session_state.current_exam = exam
    if sub: st.session_state.current_sub = sub
    st.rerun()

# --- 7. UI RENDERER ---
page = st.session_state.page

if page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        set_page("exam_detail", exam="Research Officer")

elif page == "exam_detail":
    if st.button("⬅ Back Home"): set_page("home")
    # AttributeError തടയാൻ get() ഉപയോഗിക്കുന്നു
    exam = st.session_state.get('current_exam', 'Research Officer')
    st.markdown(f"<div class='welcome-banner'><h3>📍 {exam}</h3></div>", unsafe_allow_html=True)
    for s in SYLLABUS.keys():
        if st.button(s, key=f"nav_{s}", use_container_width=True):
            set_page("sub_menu", sub=s)

elif page == "sub_menu":
    if st.button("⬅ Back"): set_page("exam_detail")
    sub = st.session_state.get('current_sub', 'Statistics')
    st.markdown(f"<div class='welcome-banner'><h3>📚 {sub}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True): set_page("syllabus_view")
    if st.button("🎯 Test Practice", use_container_width=True): set_page("practice")

elif page == "syllabus_view":
    if st.button("⬅ Back"): set_page("sub_menu")
    sub = st.session_state.get('current_sub', 'Statistics')
    data = SYLLABUS.get(sub, {"Modules": {}})
    for mod, detail in data["Modules"].items():
        with st.expander(mod): st.write(detail)

elif page == "practice":
    if st.button("⬅ Exit Quiz"): set_page("sub_menu")
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World</p>", unsafe_allow_html=True)