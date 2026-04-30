import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. GLOBAL MOBILE ZOOM & ROTATION FIX ---
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
        height: 75px !important;
        background-color: white !important;
        color: #1e3c72 !important;
        border: 2px solid #28a745 !important;
        border-radius: 12px !important;
        font-weight: bold;
    }
    .q-header {
        background-color: #1e3c72;
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE INITIALIZATION ---
# AttributeError ഒഴിവാക്കാൻ എല്ലാ വേരിയബിളുകളും ഇവിടെ ലോക്ക് ചെയ്യുന്നു.
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = "Research Officer"
if 'current_subject' not in st.session_state: st.session_state.current_subject = ""
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False

# --- 5. COMPLETE SYLLABUS DATA (MODULES 1-10) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Exponential, Normal.",
            "MODULE 4-10": "Sampling Distributions, Estimation, Testing, Regression, Time Series, Index Numbers, Vital Statistics."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory (4 marks)": "Indifference Curve, Consumer's Surplus, Production Function (Cobb-Douglas, CES), Welfare Economics.",
            "Module II: Macro Economics (4 marks)": "National Income Accounting, Inflation, Monetary and Fiscal Policies.",
            "Module III: Growth and Development (4 marks)": "PQLI, HDI, HPI, Poverty Measures, Harrod-Domar models.",
            "Module IV: Fiscal Federalism (4 marks)": "GST, Finance Commissions, Budgetary procedure, FRBM Act.",
            "Module V-VII": "Indian Economy, Economy of Kerala, Basic Econometrics."
        }
    }
}

# --- 6. COMPLETE QUIZ BANK (SET 1 & 2) ---
QUIZ_BANK = {
    "Economics": {
        "Module I: Micro Theory (4 marks)": {
            "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 7. NAVIGATION RENDERER ---

# HOME PAGE
if st.session_state.page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        st.session_state.current_exam = "Research Officer"
        st.session_state.page = "exam_detail"
        st.rerun()

# EXAM DETAIL PAGE
elif st.session_state.page == "exam_detail":
    if st.button("⬅ Back Home"):
        st.session_state.page = "home"
        st.rerun()
    
    # current_exam ഉണ്ടോ എന്ന് ഉറപ്പുവരുത്തുന്നു (AttributeError തടയാൻ)
    exam_name = st.session_state.get('current_exam', 'Research Officer')
    st.markdown(f"<div class='welcome-banner'><h3>📍 {exam_name}</h3></div>", unsafe_allow_html=True)
    
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"sub_{s}", use_container_width=True):
            st.session_state.current_subject = s
            st.session_state.page = "subject_options"
            st.rerun()

# SUBJECT OPTIONS PAGE
elif st.session_state.page == "subject_options":
    if st.button("⬅ Back"):
        st.session_state.page = "exam_detail"
        st.rerun()
    
    sub_name = st.session_state.get('current_subject', 'Selected Subject')
    st.markdown(f"<div class='welcome-banner'><h3>📚 {sub_name}</h3></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Syllabus", use_container_width=True):
            st.session_state.page = "syllabus_view"
            st.rerun()
    with col2:
        if st.button("🎯 Test Practice", use_container_width=True):
            st.session_state.page = "quiz_setup"
            st.rerun()

# SYLLABUS VIEW PAGE
elif st.session_state.page == "syllabus_view":
    if st.button("⬅ Back"):
        st.session_state.page = "subject_options"
        st.rerun()
    
    sub_name = st.session_state.get('current_subject', 'Statistics')
    st.markdown(f"<div class='welcome-banner'><h3>📖 {sub_name} Syllabus</h3></div>", unsafe_allow_html=True)
    
    data = FULL_SYLLABUS.get(sub_name, {"Modules": {}})
    for section, detail in data['Modules'].items():
        with st.expander(section):
            st.write(detail)

# QUIZ SETUP PAGE
elif st.session_state.page == "quiz_setup":
    if st.button("⬅ Exit Quiz"):
        st.session_state.page = "subject_options"
        st.rerun()
    st.info("ക്വിസ് സെക്ഷൻ തയ്യാറാകുന്നു...")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>© 2026 Maths-Stat World Hub</p>", unsafe_allow_html=True)