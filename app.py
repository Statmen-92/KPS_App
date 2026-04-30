import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .stApp { background-color: #f0f2f6; }
    
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
    }

    div.stButton > button {
        height: 75px !important;
        background-color: white !important;
        color: #1e3c72 !important;
        border: 2px solid #28a745 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 0.85em !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        transition: 0.3s !important;
        white-space: normal !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 5px !important;
    }
    
    div.stButton > button:hover {
        background-color: #28a745 !important;
        color: white !important;
    }

    .q-header {
        background-color: #1e3c72;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-weight: bold;
        text-align: center;
        font-size: 1.1em;
    }

    .result-card {
        background: white;
        border: 2px solid #28a745;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = None
if 'current_subject' not in st.session_state: st.session_state.current_subject = None
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False
if 'last_selected_set' not in st.session_state: st.session_state.last_selected_set = ""

# --- 4. FULL SYLLABUS DATA ---
FULL_SYLLABUS = {
    "Statistics": {
        "Total Marks": 25,
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling methods. Simple random sampling with and without replacement. Stratified sampling. Ratio estimator and regression estimator.",
            "MODULE 2: PROBABILITY AND RANDOM VARIABLES (3 marks)": "Probability measure, probability space. Independence of events, conditional probability and Bayes theorem. CDF, PDF, PGF, MGF, Characteristic function. Sequences of random variables, convergence.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Applications of standard discrete distributions.",
            "MODULE 4: SAMPLING DISTRIBUTIONS (2 marks)": "Distribution of the mean and variance.",
            "MODULE 5: ESTIMATION (3 marks)": "Point estimation, Minimal Sufficient Statistic, Completeness.",
            "MODULE 6: TESTING OF HYPOTHESIS (3 marks)": "Fundamental concepts, Parametric and Non-parametric tests.",
            "MODULE 7: LINEAR REGRESSION (2 marks)": "Properties of least square estimators. Significance tests.",
            "MODULE 8: TIME SERIES (2 marks)": "Components of Time series, ARMA and ARIMA models.",
            "MODULE 9: INDEX NUMBERS (1 mark)": "Laspeyre's, Paache's and Fisher's index numbers.",
            "MODULE 10: VITAL STATISTICS (1 mark)": "Measurement of Fertility and Mortality."
        }
    },
    "Economics": {
        "Total Marks": 25,
        "Modules": {
            "Module I: Micro Economic Theory (4 marks)": "Consumer Behaviour, Production Function, Welfare Economics.",
            "Module II: Macro Economic Principles (4 marks)": "National Income Accounting, Inflation, Fiscal Policies.",
            "Module III: Economic Growth and Development (4 marks)": "HDI, Poverty measures, Growth strategies.",
            "Module IV: Fiscal Federalism and Budgeting (4 marks)": "GST, Finance Commissions, Budgetary procedure.",
            "Module V: Development Issues of India (3 marks)": "Sectoral composition, Demographic features.",
            "Module VI: Economy of Kerala (3 marks)": "Remittance economy, MSME sector.",
            "Module VII: Basic Econometrics (3 marks)": "CLRM, Gauss Markov's Theorem."
        }
    },
    "Mathematics": { "Total Marks": 25, "Modules": { "Unit I-VII": "Linear Algebra, Real Analysis, Abstract Algebra, Topology, etc." } },
    "Commerce": { "Total Marks": 25, "Modules": { "Module 1-10": "Accounting, Taxation, GST, Managerial Economics." } }
}

# --- 5. QUIZ BANK ---
QUIZ_BANK = {
    "Statistics": {
        "MODULE 2: PROBABILITY AND RANDOM VARIABLES (3 marks)": {
            "Set 1": [
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", f"{i}.png"), ans, os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", f"E{i}.png"))
                for i, ans in zip(range(1, 11), ["C", "A", "C", "D", "B", "C", "A", "B", "A", "A"])
            ]
        }
    },
    "Economics": {
        "Module I: Micro Economic Theory (4 marks)": {
            "Set 1": [
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", f"{i}.png"), ans, os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", f"E{i}.png"))
                for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])
            ],
            "Set 2": [
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", f"{i}.png"), ans, os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", f"E{i}.png"))
                for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])
            ]
        }
    }
}

# --- PAGE LOGIC ---

if st.session_state.page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2><p style='font-size:0.8em;'>Research Officer Hub</p></div>", unsafe_allow_html=True)
    exams = ["Research Officer", "HSST Stat", "CSIR NET", "HSST Maths", "HSA Maths"]
    cols = st.columns(2)
    for i, ex in enumerate(exams):
        with cols[i % 2]:
            if st.button(f"{ex}", key=ex, use_container_width=True):
                st.session_state.current_exam = ex
                st.session_state.page = "exam_detail" if ex == "Research Officer" else "other_exams"
                st.rerun()

elif st.session_state.page == "exam_detail":
    if st.button("⬅ Back Home", key="back_home"): st.session_state.page = "home"; st.rerun()
    st.markdown(f"<div class='welcome-banner'><h3>📍 {st.session_state.current_exam}</h3></div>", unsafe_allow_html=True)
    subs = list(FULL_SYLLABUS.keys())
    cols = st.columns(2)
    for i, s in enumerate(subs):
        with cols[i % 2]:
            if st.button(f"{s}", key=f"sub_{s}", use_container_width=True):
                st.session_state.current_subject = s
                st.session_state.page = "subject_options"
                st.rerun()

elif st.session_state.page == "subject_options":
    if st.button("⬅ Back", key="back_exam"): st.session_state.page = "exam_detail"; st.rerun()
    st.markdown(f"<div class='welcome-banner'><h3>📚 {st.session_state.current_subject}</h3></div>", unsafe_allow_html=True)
    feats = {"Syllabus": "📖", "Notes": "📝", "Test Practice": "🎯", "Model Exam": "📝", "Video Class": "🎥"}
    cols = st.columns(2)
    for i, (name, icon) in enumerate(feats.items()):
        with cols[i % 2]:
            if st.button(f"{icon} {name}", key=f"opt_{name}", use_container_width=True):
                if name == "Syllabus": st.session_state.page = "syllabus_view"
                elif name == "Test Practice": st.session_state.page = "quiz_setup"
                else: st.info(f"{name} Coming Soon!")
                st.rerun()

elif st.session_state.page == "syllabus_view":
    if st.button("⬅ Back", key="back_opt"): st.session_state.page = "subject_options"; st.rerun()
    data = FULL_SYLLABUS[st.session_state.current_subject]
    st.markdown(f"<div class='welcome-banner'><h3>📖 Syllabus: {st.session_state.current_subject}</h3></div>", unsafe_allow_html=True)
    for section, detail in data['Modules'].items():
        with st.expander(section): st.write(detail)

elif st.session_state.page == "quiz_setup":
    if st.button("⬅ Exit Quiz", key="exit_quiz"): 
        st.session_state.page = "subject_options"
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.rerun()
    
    st.markdown(f"<div class='welcome-banner'><h3>🎯 {st.session_state.current_subject} Practice</h3></div>", unsafe_allow_html=True)
    
    mod_opts = list(FULL_SYLLABUS[st.session_state.current_subject]["Modules"].keys())
    c1, c2 = st.columns([2, 1])
    with c1: sel_mod = st.selectbox("Select Module:", mod_opts)
    with c2: sel_set = st.radio("Choose Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)
        
    curr_id = f"{st.session_state.current_subject}_{sel_mod}_{sel_set}"
    if st.session_state.last_selected_set != curr_id:
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.session_state.last_selected_set = curr_id
        st.rerun()

    active_data = QUIZ_BANK.get(st.session_state.current_subject, {}).get(sel_mod, {}).get(sel_set)

    if active_data:
        if not st.session_state.quiz_submitted:
            for i, (q_img, cor, e_img) in enumerate(active_data):
                st.markdown(f"<div class='q-header'>Question No: {i + 1}</div>", unsafe_allow_html=True)
                
                if os.path.exists(q_img):
                    # --- ZOOM FACILITY ---
                    with st.expander(f"🔍 View/Zoom Question {i+1}"):
                        st.image(q_img, use_container_width=True)
                    st.image(q_img, use_container_width=True)
                
                ans_key = f"quiz_radio_{curr_id}_{i}"
                saved_val = st.session_state.user_answers.get(i)
                choice = st.radio(f"Select Answer Q{i+1}:", ["A", "B", "C", "D"], 
                                  index=["A","B","C","D"].index(saved_val) if saved_val in ["A","B","C","D"] else None,
                                  key=ans_key, horizontal=True)
                if choice: st.session_state.user_answers[i] = choice
                st.markdown("<br><hr style='border: 0.5px solid #ddd;'><br>", unsafe_allow_html=True)

            if st.button("🏆 Submit Final Answers", type="primary", use_container_width=True):
                st.session_state.quiz_submitted = True; st.rerun()
        else:
            score = sum(1 for i, (_, c, _) in enumerate(active_data) if st.session_state.user_answers.get(i) == c)
            st.markdown(f"<div class='result-card'><h1>Score: {score} / {len(active_data)}</h1></div>", unsafe_allow_html=True)
            for i, (q_img, cor, e_img) in enumerate(active_data):
                u_ans = st.session_state.user_answers.get(i, "N/A")
                with st.expander(f"Question {i+1}: {'✅ Correct' if u_ans == cor else '❌ Incorrect'}"):
                    if os.path.exists(q_img): st.image(q_img, use_container_width=True)
                    st.success(f"Correct Answer: {cor} | Your Answer: {u_ans}")
                    if os.path.exists(e_img):
                        st.write("#### Explanation:")
                        st.image(e_img, use_container_width=True)
            if st.button("🔄 Restart Practice", use_container_width=True): 
                st.session_state.quiz_submitted = False; st.session_state.user_answers = {}; st.rerun()
    else:
        st.warning(f"Materials for '{sel_mod}' coming soon!")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>Professor Shakeelurahman OP | © 2026</p>", unsafe_allow_html=True)