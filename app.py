import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

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

# --- 4. SAFE SESSION INITIALIZATION (RE-STRUCTURED) ---
# AttributeError വരാതിരിക്കാൻ 'get' മെത്തേഡ് ഉപയോഗിച്ച് വേരിയബിളുകൾ ഉറപ്പാക്കുന്നു.
def get_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

# പേജ് വിവരങ്ങൾ ഇനിഷ്യലൈസ് ചെയ്യുന്നു
current_page = get_state('page', 'home')
exam_name = get_state('current_exam', 'Research Officer')
subject_name = get_state('current_subject', 'Statistics')

# --- 5. COMPLETE SYLLABUS DATA (NO SKIPPING) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling methods, Simple random sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF, Characteristic function.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Geometric, Negative Binomial, Exponential, Normal.",
            "MODULE 4: SAMPLING DISTRIBUTIONS (2 marks)": "Distribution of the mean and variance of a random sample from normal population, Chi-square, t, and F distributions.",
            "MODULE 5: ESTIMATION (3 marks)": "Point estimation, Sufficiency, Completeness. Rao-Blackwell, Lehman-Scheffe, Cramer- Rao inequality.",
            "MODULE 6: TESTING OF HYPOTHESIS (3 marks)": "Normal, t, chi-square, F tests, Parametric and Non-parametric tests.",
            "MODULE 7: LINEAR REGRESSION (2 marks)": "Simple linear regression models, least square estimators, Coefficient of determination.",
            "MODULE 8: TIME SERIES (2 marks)": "Trend and seasonal fluctuations, ACF, PACF, ARMA, ARIMA models.",
            "MODULE 9: INDEX NUMBERS (1 mark)": "Laspeyre's, Paache's and Fisher's index numbers.",
            "MODULE 10: VITAL STATISTICS (1 mark)": "Fertility (CBR, GFR, TFR) and Mortality (CDR, ASDR) measurements."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Economic Theory (4 marks)": "Indifference Curve and Revealed Preference Approach- Consumer's Surplus- Production Function.",
            "Module II-VII": "Macro Economics, Economic Growth, Fiscal Federalism, Indian Economy, Kerala Economy, Basic Econometrics."
        }
    }
}

# --- 6. COMPLETE QUIZ BANK ---
QUIZ_BANK = {
    "Economics": {
        "Module I: Micro Economic Theory (4 marks)": {
            "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 7. NAVIGATION RENDERER ---

if current_page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", key="main_ro", use_container_width=True):
        st.session_state.page = "exam_detail"
        st.session_state.current_exam = "Research Officer"
        st.rerun()

elif current_page == "exam_detail":
    if st.button("⬅ Back Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown(f"<div class='welcome-banner'><h3>📍 {exam_name}</h3></div>", unsafe_allow_html=True)
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"nav_{s}", use_container_width=True):
            st.session_state.page = "subject_options"
            st.session_state.current_subject = s
            st.rerun()

elif current_page == "subject_options":
    if st.button("⬅ Back"):
        st.session_state.page = "exam_detail"
        st.rerun()
    st.markdown(f"<div class='welcome-banner'><h3>📚 {subject_name}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True):
        st.session_state.page = "syllabus_view"
        st.rerun()
    if st.button("🎯 Test Practice", use_container_width=True):
        st.session_state.page = "quiz_setup"
        st.rerun()

elif current_page == "syllabus_view":
    if st.button("⬅ Back"):
        st.session_state.page = "subject_options"
        st.rerun()
    st.markdown(f"<div class='welcome-banner'><h3>📖 {subject_name} Syllabus</h3></div>", unsafe_allow_html=True)
    data = FULL_SYLLABUS.get(subject_name, {"Modules": {}})
    for section, detail in data['Modules'].items():
        with st.expander(section):
            st.write(detail)

elif current_page == "quiz_setup":
    if st.button("⬅ Exit Quiz"):
        st.session_state.page = "subject_options"
        st.rerun()
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World Hub</p>", unsafe_allow_html=True)