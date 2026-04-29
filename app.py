import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .custom-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-top: 5px solid #28a745;
        transition: transform 0.3s ease;
        margin-bottom: 20px;
        text-align: center;
    }
    .custom-card:hover { transform: translateY(-5px); }
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
    }
    div.stButton > button:first-child {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        border: none;
        height: 3.5em;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(40, 167, 69, 0.2);
    }
    div.stButton > button:hover { background-color: #218838; border: none; }
    .result-card {
        background: white;
        border: 2px solid #28a745;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 25px;
    }
    h1, h2, h3 { color: #1e3c72; }
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
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = None
if 'current_subject' not in st.session_state: st.session_state.current_subject = None
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False
if 'last_selected_set' not in st.session_state: st.session_state.last_selected_set = ""

# --- 4. FULL SYLLABUS DATA (STRICTLY PRESERVED) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Total Marks": 25,
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling methods. Simple random sampling with and without replacement. Stratified sampling. Ratio estimator and regression estimator.",
            "MODULE 2: PROBABILITY AND RANDOM VARIABLES (3 marks)": "Probability measure, probability space. Independence of events, conditional probability and Bayes theorem. CDF, PDF, PGF, MGF, Characteristic function. Sequences of random variables, convergence.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Applications of standard discrete distributions- Uniform, Bernoulli, Binomial, Poisson, Geometric, Negative Binomial, Hypergeometric. Standard continuous distributions: Uniform, Exponential, Weibull, Gamma and normal.",
            "MODULE 4: SAMPLING DISTRIBUTIONS (2 marks)": "Distribution of the mean and variance of a random sample from normal population, Chi-square, t, and F distributions (both central and non-central).",
            "MODULE 5: ESTIMATION (3 marks)": "Point estimation, Minimal Sufficient Statistic, Completeness. Rao-Blackwell theorem, Lehman-Scheffe theorem, Fisher's information measure, Cramer- Rao inequality. Maximum likelihood, method of moments.",
            "MODULE 6: TESTING OF HYPOTHESIS (3 marks)": "Fundamental concepts, tests based on Normal, t, chi-square and F distributions, Kolmogorov-Smirnov, Wald Wolfowitz run test, Mann-Whitney Wilcoxon, Kruskal-Wallis, Friedman test.",
            "MODULE 7: LINEAR REGRESSION (2 marks)": "Inference on simple linear regression models. Properties of least square estimators. Significance test and confidence intervals. Coefficient of determination. Multiple linear regression models, Problem of multicollinearity. Simple, partial and multiple correlation.",
            "MODULE 8: TIME SERIES (2 marks)": "Components of Time series, trend and seasonal fluctuations, ACF and PACF, Moving Average (MA) and Auto Regressive (AR), ARMA and ARIMA models.",
            "MODULE 9: INDEX NUMBERS (1 mark)": "Laspeyre's, Paache's and Fisher's index numbers. Consumer price index number. Base shifting, splicing and deflating index numbers.",
            "MODULE 10: VITAL STATISTICS (1 mark)": "Measurement of Fertility: CBR, GFR, ASBR, TFR, GRR, NRR. Measurement of Mortality: CDR, Standardized death rates, ASDR."
        }
    },
    "Economics": {
        "Total Marks": 25,
        "Modules": {
            "Module I: Micro Economic Theory (4 marks)": "Indifference Curve and Revealed Preference Approach to Consumer Behaviour- Consumer's Surplus- Production Function- Cobb-Douglas and CES Production Functions- Traditional and Modern Cost Theories- Price and Output determination in perfect and imperfect market models- Basic Concepts in Welfare Economics and Parato Optimality Conditions.",
            "Module II: Macro Economic Principles (4 marks)": "National Income Accounting- Methods of Measuring National Income- Indian Statistical System of National Income Accounting- Inflation and Deflation- Inflation Targeting- Monetary and Fiscal Policies. Balance of Payments and exchange rates.",
            "Module III: Economic Growth and Development (4 marks)": "Concepts of Economic Growth and Development- Alternative measures of Development: PQLI, HDI, HPI - Measures of Poverty: Absolute and Relative, Head-Count Ratio, Poverty Gap Indices, MPI, Sen's Capability theorem- Harrod- Domar and Mahalanobis model of Growth - The Big Push Theory-Balanced and Unbalanced Growth strategies.",
            "Module IV: Fiscal Federalism and Budgeting (4 marks)": "Vertical and horizontal imbalances in India's federal finance- Central, State and Local finance in India- Central and State Finance Commissions- Challenges and recommendations of fifteenth Central Finance Commission. Budgetary procedure in India Public Account- Consolidated and Contingency Fund of India- Form of GST introduced in India- Fiscal Responsibility and Budget Management Act.",
            "Module V: Development Issues of India (3 marks)": "Trends in the sectoral composition of national income- Role of planning- Demographic features- Major interventions in the Agricultural, Industrial and Service Sectors.",
            "Module VI: Economy of Kerala (3 marks)": "Development experience of Kerala- Remittance economy- Decentralized Planning- Role and Relevance of KIIFB- MSME sector- Care Economy.",
            "Module VII: Basic Econometrics (3 marks)": "Population and Sample Regression Functions- Goodness of Fit- Basic assumptions of CLRM- Gauss Markov's Theorem- Dummy Variable Model."
        }
    },
    "Mathematics": {
        "Total Marks": 25,
        "Modules": {
            "Unit I-VII": "Linear Algebra, Functional Analysis, Abstract Algebra, Real Analysis, Topology, Complex Analysis, Differential Equation."
        }
    },
    "Commerce": {
        "Total Marks": 25,
        "Modules": {
            "Module 1-10": "Financial Accounting, Partnership, Cost Accounting, Direct Taxation, GST, Managerial Economics, Legal Framework."
        }
    }
}

# --- 5. QUIZ BANK (OLDER FORMAT - MANUAL ENTRY) ---
QUIZ_BANK = {
    "Statistics": {
        "MODULE 2: PROBABILITY AND RANDOM VARIABLES (3 marks)": {
            "Set 1": [
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "1.png"), "C", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E1.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "2.png"), "A", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E2.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "3.png"), "C", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E3.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "4.png"), "D", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E4.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "5.png"), "B", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E5.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "6.png"), "C", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E6.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "7.png"), "A", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E7.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "8.png"), "B", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E8.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "9.png"), "A", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E9.png")),
                (os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", "10.png"), "A", os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Explanation", "E10.png")),
            ]
        }
    },
    "Economics": {
        "Module I: Micro Economic Theory (4 marks)": {
            "Set 1": [
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "1.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E1.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "2.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E2.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "3.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E3.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "4.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E4.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "5.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E5.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "6.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E6.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "7.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E7.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", "8.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Explanation", "E8.png")),              
            ],
            "Set 2": [
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "10.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E10.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "11.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E11.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "12.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E12.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "13.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E13.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "14.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E14.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "15.png"), "C", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E15.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "16.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E16.png")),
                (os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", "17.png"), "B", os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Explanation", "E17.png")),
            ]
        }
    }
}

# ==========================================
# PAGE LOGIC
# ==========================================

if st.session_state.page == "home":
    # ബാനറിന്റെ സൈസ് അല്പം കുറച്ചു
    st.markdown("<div class='welcome-banner' style='padding:20px;'><h1 style='font-size:1.8em;'>🎓 MATHS-STAT WORLD</h1><p>Research Officer Hub</p></div>", unsafe_allow_html=True)
    
    exams = ["Research Officer", "CSIR NET", "HSA Maths", "HSST Stat", "HSST Maths"]
    
    # ലാപ്ടോപ്പിൽ 3 കോളവും മൊബൈലിൽ 2 കോളവും വരാൻ (Small trick with columns)
    # ഇത് മൊബൈൽ സ്ക്രീനിൽ ഫുൾ ആയി ഒതുങ്ങാൻ സഹായിക്കും
    cols = st.columns(2) # മൊബൈലിനായി 2 കോളങ്ങൾ മാത്രം ഉപയോഗിക്കുന്നു
    
    for i, ex in enumerate(exams):
        # വരികൾ മാറി മാറി വരാൻ i % 2 ഉപയോഗിക്കുന്നു
        with cols[i % 2]:
            st.markdown(f"""
                <div class='custom-card' style='padding: 15px; margin-bottom: 10px;'>
                    <h4 style='font-size: 1em;'>{ex}</h4>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Start {ex.split()[-1]}", key=ex, use_container_width=True):
                st.session_state.current_exam = ex
                st.session_state.page = "exam_detail" if ex == "Research Officer" else "other_exams"
                st.rerun()

# --- ബാക്കിയുള്ള കോഡുകൾ (exam_detail, subject_options, etc.) മാറ്റമില്ലാതെ തുടരുക ---

elif st.session_state.page == "exam_detail":
    st.title(f"📍 {st.session_state.current_exam}")
    if st.button("⬅️ Back Home"): st.session_state.page = "home"; st.rerun()
    subs = list(FULL_SYLLABUS.keys())
    cols = st.columns(2)
    for i, s in enumerate(subs):
        with cols[i % 2]:
            st.markdown(f"<div class='custom-card'><h2>{s}</h2></div>", unsafe_allow_html=True)
            if st.button(f"Explore {s}", key=f"sub_{s}"):
                st.session_state.current_subject = s
                st.session_state.page = "subject_options"
                st.rerun()

elif st.session_state.page == "subject_options":
    st.title(f"📚 {st.session_state.current_subject}")
    if st.button("⬅️ Back"): st.session_state.page = "exam_detail"; st.rerun()
    feats = {"Syllabus": "📖", "Notes": "📝", "Test Practice": "🎯", "Model Exam": "📝", "Video Class": "🎥"}
    cols = st.columns(3)
    for i, (name, icon) in enumerate(feats.items()):
        with cols[i % 3]:
            st.markdown(f"<div class='custom-card'><h1>{icon}</h1><h4>{name}</h4></div>", unsafe_allow_html=True)
            if st.button(f"Open {name}", key=f"opt_{name}"):
                if name == "Syllabus": st.session_state.page = "syllabus_view"
                elif name == "Test Practice": st.session_state.page = "quiz_setup"
                else: st.info(f"{name} Coming Soon!")
                st.rerun()

elif st.session_state.page == "syllabus_view":
    st.title(f"📖 Syllabus: {st.session_state.current_subject}")
    if st.button("⬅️ Back"): st.session_state.page = "subject_options"; st.rerun()
    data = FULL_SYLLABUS[st.session_state.current_subject]
    st.header(f"Total: {data['Total Marks']} Marks")
    for section, detail in data['Modules'].items():
        with st.expander(section): st.write(detail)

elif st.session_state.page == "quiz_setup":
    with st.sidebar:
        st.markdown(f"### 📍 {st.session_state.current_exam}")
        mod_opts = list(FULL_SYLLABUS[st.session_state.current_subject]["Modules"].keys())
        sel_mod = st.selectbox("Select Module:", mod_opts)
        sel_set = st.radio("Choose Set:", ["Set 1", "Set 2", "Set 3"])
        
        curr_id = f"{st.session_state.current_subject}_{sel_mod}_{sel_set}"
        if st.session_state.last_selected_set != curr_id:
            st.session_state.quiz_submitted = False
            st.session_state.user_answers = {}
            st.session_state.current_q = 0
            st.session_state.last_selected_set = curr_id
            st.rerun()
        if st.button("🏁 Exit"): st.session_state.page = "subject_options"; st.rerun()

    st.title(f"🎯 {sel_mod}")
    active_data = QUIZ_BANK.get(st.session_state.current_subject, {}).get(sel_mod, {}).get(sel_set)

    if active_data:
        if not st.session_state.quiz_submitted:
            p_cols = st.columns(10)
            for i in range(len(active_data)):
                with p_cols[i]:
                    if st.button(f"{i+1}", key=f"btn_{i}", type="primary" if i == st.session_state.current_q else "secondary"):
                        st.session_state.current_q = i; st.rerun()
            st.markdown("---")
            q_idx = st.session_state.current_q
            q_img, cor, e_img = active_data[q_idx]
            
            # --- ഇമേജിന് മുകളിൽ ക്വസ്റ്റ്യൻ നമ്പർ കാണിക്കുന്നു ---
            st.markdown(f"<div class='q-header'>Question No: {q_idx + 1}</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([3, 1])
            with c1:
                if os.path.exists(q_img): st.image(q_img, use_container_width=True)
                else: st.error(f"Image not found: {q_img}")
            with c2:
                ans_key = f"radio_{curr_id}_{q_idx}"
                saved = st.session_state.user_answers.get(q_idx)
                choice = st.radio("Answer:", ["A", "B", "C", "D"], index=["A","B","C","D"].index(saved) if saved else None, key=ans_key)
                if st.button("Save & Next"):
                    if choice: st.session_state.user_answers[q_idx] = choice
                    st.session_state.current_q = min(q_idx + 1, len(active_data)-1); st.rerun()
                if q_idx == len(active_data)-1 and st.button("🏆 Submit"):
                    st.session_state.quiz_submitted = True; st.rerun()
        else:
            score = sum(1 for i, (_, c, _) in enumerate(active_data) if st.session_state.user_answers.get(i) == c)
            st.markdown(f"<div class='result-card'><h1>Score: {score} / {len(active_data)}</h1></div>", unsafe_allow_html=True)
            for i, (q_img, cor, e_img) in enumerate(active_data):
                u_ans = st.session_state.user_answers.get(i, "N/A")
                is_right = u_ans == cor
                with st.expander(f"Question {i+1}: {'✅ Correct' if is_right else '❌ Incorrect'}"):
                    r1, r2 = st.columns([2, 1])
                    with r1:
                        if os.path.exists(q_img): st.image(q_img, use_container_width=True)
                    with r2:
                        st.success(f"Correct Answer: {cor}")
                        st.write(f"Your Answer: {u_ans}")
                    st.markdown("---")
                    st.write("#### 💡 Explanation:")
                    if os.path.exists(e_img): st.image(e_img, use_container_width=True)
                    else: st.warning("Explanation image missing.")
            if st.button("🔄 Restart Quiz"): st.session_state.quiz_submitted = False; st.rerun()
    else:
        st.warning(f"Materials for '{sel_mod}' coming soon!")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>Professor Shakeelurahman OP | © 2026</p>", unsafe_allow_html=True)