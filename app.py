import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. GLOBAL MOBILE ZOOM & ROTATION SCRIPT ---
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

# --- 4. PERSISTENT SESSION STATE (THE FIX) ---
# AttributeError ഒഴിവാക്കാൻ എല്ലാ കീകളും ഇവിടെ ഡിഫോൾട്ട് ആയി നൽകുന്നു.
if 'page' not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("p", "home")
    st.session_state.current_exam = params.get("ex", "Research Officer")
    st.session_state.current_subject = params.get("sub", "Statistics")
    st.session_state.user_answers = {}
    st.session_state.quiz_submitted = False

def navigate_to(page, exam=None, subject=None):
    st.session_state.page = page
    st.query_params["p"] = page
    if exam: 
        st.session_state.current_exam = exam
        st.query_params["ex"] = exam
    if subject: 
        st.session_state.current_subject = subject
        st.query_params["sub"] = subject
    st.rerun()

# --- 5. COMPLETE SYLLABUS DATA (NO SKIPPING) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling methods, Simple random sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF, Characteristic function.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Geometric, Negative Binomial, Exponential, Normal.",
            "MODULE 4: SAMPLING DISTRIBUTIONS (2 marks)": "Normal population, Chi-square, t, and F distributions.",
            "MODULE 5: ESTIMATION (3 marks)": "Point estimation, Sufficiency, Completeness, Rao-Blackwell, Lehman-Scheffe.",
            "MODULE 6: TESTING OF HYPOTHESIS (3 marks)": "Normal, t, chi-square, F tests, Parametric and Non-parametric tests.",
            "MODULE 7: LINEAR REGRESSION (2 marks)": "Simple linear regression, least square estimators, Coefficient of determination.",
            "MODULE 8: TIME SERIES (2 marks)": "Trend and seasonal fluctuations, ACF, PACF, ARMA, ARIMA models.",
            "MODULE 9: INDEX NUMBERS (1 mark)": "Laspeyre's, Paache's and Fisher's index numbers.",
            "MODULE 10: VITAL STATISTICS (1 mark)": "Fertility (CBR, GFR, TFR) and Mortality (CDR, ASDR) measurements."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory (4 marks)": "Indifference Curve, Consumer's Surplus, Production Function (Cobb-Douglas, CES), Welfare Economics.",
            "Module II: Macro Principles (4 marks)": "National Income Accounting, Inflation, Monetary and Fiscal Policies.",
            "Module III: Growth and Development (4 marks)": "PQLI, HDI, HPI, Poverty Measures, Harrod-Domar models.",
            "Module IV: Fiscal Federalism (4 marks)": "GST, Finance Commissions, Budgetary procedure, FRBM Act.",
            "Module V: Indian Economy (3 marks)": "Sectoral composition, Planning, Demographic features.",
            "Module VI: Economy of Kerala (3 marks)": "Remittance economy, KIIFB, MSME sector, Care Economy.",
            "Module VII: Basic Econometrics (3 marks)": "Regression Functions, Gauss Markov's Theorem."
        }
    }
}

# --- 6. COMPLETE QUIZ BANK ---
QUIZ_BANK = {
    "Economics": {
        "Module I: Micro Theory (4 marks)": {
            "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 7. NAVIGATION RENDERER ---
page = st.session_state.page

if page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate_to("exam_detail", exam="Research Officer")

elif page == "exam_detail":
    if st.button("⬅ Back Home"): navigate_to("home")
    exam = st.session_state.get('current_exam', 'Research Officer')
    st.markdown(f"<div class='welcome-banner'><h3>📍 {exam}</h3></div>", unsafe_allow_html=True)
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            navigate_to("subject_options", subject=s)

elif page == "subject_options":
    if st.button("⬅ Back"): navigate_to("exam_detail")
    subject = st.session_state.get('current_subject', 'Statistics')
    st.markdown(f"<div class='welcome-banner'><h3>📚 {subject}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True): navigate_to("syllabus_view")
    if st.button("🎯 Test Practice", use_container_width=True): navigate_to("quiz_setup")

elif page == "syllabus_view":
    if st.button("⬅ Back"): navigate_to("subject_options")
    subject = st.session_state.get('current_subject', 'Statistics')
    st.markdown(f"<div class='welcome-banner'><h3>📖 Syllabus</h3></div>", unsafe_allow_html=True)
    data = FULL_SYLLABUS.get(subject, {"Modules": {}})
    for section, detail in data['Modules'].items():
        with st.expander(section): st.write(detail)

elif page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate_to("subject_options")
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World</p>", unsafe_allow_html=True)