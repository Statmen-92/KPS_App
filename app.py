import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. SESSION STATE & URL SYNC ---
# ഫോൺ തിരിക്കുമ്പോൾ ഹോം പേജിലേക്ക് പോകുന്നത് തടയാൻ URL ഉപയോഗിക്കുന്നു
if 'page' not in st.session_state:
    # ബ്രൗസർ URL-ൽ നിന്ന് നിലവിലെ പേജ് വിവരങ്ങൾ എടുക്കുന്നു
    params = st.query_params
    st.session_state.page = params.get("p", "home")
    st.session_state.current_exam = params.get("ex", "Research Officer")
    st.session_state.current_subject = params.get("sub", "Statistics")

def navigate_to(page, exam=None, subject=None):
    st.session_state.page = page
    st.query_params["p"] = page # URL-ൽ പേജ് സേവ് ചെയ്യുന്നു
    if exam: 
        st.session_state.current_exam = exam
        st.query_params["ex"] = exam
    if subject: 
        st.session_state.current_subject = subject
        st.query_params["sub"] = subject
    st.rerun()

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #f0f2f6; }
    div.stButton > button {
        height: 70px !important; border-radius: 12px !important; 
        font-weight: bold; border: 2px solid #28a745 !important;
        background-color: white !important;
    }
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA (SYLLABUS & QUIZ) ---
FULL_SYLLABUS = {
    "Statistics": {"Modules": {"MODULE 1-10": "Sampling, Probability, Distributions, Estimation, Testing, Regression, Time Series, Index Numbers, Vital Stats."}},
    "Economics": {"Modules": {"Module I: Micro Theory": "Indifference Curve, Consumer's Surplus, Production Function.", "Module II-VII": "Macro, Fiscal, Indian & Kerala Economy, Econometrics."}}
}

QUIZ_BANK = {
    "Economics": {
        "Set 1": [("Q1.png", "B"), ("Q2.png", "B")], 
        "Set 2": [("Q10.png", "C"), ("Q11.png", "B")]
    }
}

# --- 5. APP UI LOGIC ---
# AttributeError ഒഴിവാക്കാൻ സുരക്ഷിതമായി വിവരങ്ങൾ എടുക്കുന്നു
page = st.session_state.get('page', 'home')
exam = st.session_state.get('current_exam', 'Research Officer')
subject = st.session_state.get('current_subject', 'Statistics')

if page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate_to("exam_detail", exam="Research Officer")

elif page == "exam_detail":
    if st.button("⬅ Back Home"): navigate_to("home")
    st.markdown(f"### 📍 {exam}")
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            navigate_to("subject_options", subject=s)

elif page == "subject_options":
    if st.button("⬅ Back"): navigate_to("exam_detail")
    st.markdown(f"### 📚 {subject}")
    if st.button("📖 Syllabus", use_container_width=True): navigate_to("syllabus_view")
    if st.button("🎯 Test Practice", use_container_width=True): navigate_to("quiz_setup")

elif page == "syllabus_view":
    if st.button("⬅ Back"): navigate_to("subject_options")
    st.write(FULL_SYLLABUS.get(subject, {}).get("Modules", {}))

elif page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate_to("subject_options")
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Shakeelurahman OP</p>", unsafe_allow_html=True)