import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. GLOBAL MOBILE ZOOM ENABLE (CRITICAL FIX) ---
# ഈ സ്ക്രിപ്റ്റ് ആപ്പിലെ എല്ലാ പേജുകളിലും വിരലുകൾ കൊണ്ടുള്ള സൂമിംഗ് (Pinch-to-zoom) നിർബന്ധമായും അനുവദിക്കും.
st.markdown("""
    <script>
    const addZoom = () => {
        var meta = document.querySelector('meta[name="viewport"]');
        if (meta) {
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
        } else {
            meta = document.createElement('meta');
            meta.name = 'viewport';
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
            document.getElementsByTagName('head')[0].appendChild(meta);
        }
    };
    // ആപ്പ് ലോഡ് ചെയ്യുമ്പോഴും പേജ് മാറുമ്പോഴും സൂം ആക്റ്റീവ് ആക്കാൻ
    addZoom();
    document.addEventListener('DOMContentLoaded', addZoom);
    </script>
    """, unsafe_allow_html=True)

# --- 3. ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    /* ഹെഡർ ഐക്കണുകൾ ഒഴിവാക്കുന്നു */
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

    /* വലിയ ബട്ടൺ കാർഡുകൾ */
    div.stButton > button {
        height: 75px !important;
        background-color: white !important;
        color: #1e3c72 !important;
        border: 2px solid #28a745 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 0.9em !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
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
    }

    .result-card {
        background: white;
        border: 2px solid #28a745;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* എല്ലാ ഇമേജുകൾക്കും ബോർഡർ */
    .stImage img {
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = None
if 'current_subject' not in st.session_state: st.session_state.current_subject = None
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False
if 'last_selected_set' not in st.session_state: st.session_state.last_selected_set = ""

# --- 5. FULL SYLLABUS DATA ---
FULL_SYLLABUS = {
    "Statistics": {
        "Total Marks": 25,
        "Modules": {
            "MODULE 1-10": "Sampling, Probability, Standard Distributions, Estimation, Testing, Regression, Time Series, Index Numbers, Vital Statistics."
        }
    },
    "Economics": {
        "Total Marks": 25,
        "Modules": {
            "Module I-VII": "Micro, Macro, Growth, Fiscal, Development Issues, Kerala Economy, Econometrics."
        }
    },
    "Mathematics": { "Total Marks": 25, "Modules": { "Unit I-VII": "Linear Algebra, Real Analysis, Topology, etc." } },
    "Commerce": { "Total Marks": 25, "Modules": { "Module 1-10": "Accounting, Taxation, GST, etc." } }
}

# --- 6. QUIZ BANK ---
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
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2><p>Professor Shakeelurahman OP</p></div>", unsafe_allow_html=True)
    exams = ["Research Officer", "HSST Stat", "CSIR NET", "HSST Maths", "HSA Maths"]
    cols = st.columns(2)
    for i, ex in enumerate(exams):
        with cols[i % 2]:
            if st.button(f"{ex}", key=ex, use_container_width=True):
                st.session_state.current_exam = ex
                st.session_state.page = "exam_detail" if ex == "Research Officer" else "other_exams"
                st.rerun()

elif st.session_state.page == "exam_detail":
    if st.button("⬅ Back Home"): st.session_state.page = "home"; st.rerun()
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
    if st.button("⬅ Back"): st.session_state.page = "exam_detail"; st.rerun()
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
    if st.button("⬅ Back"): st.session_state.page = "subject_options"; st.rerun()
    data = FULL_SYLLABUS[st.session_state.current_subject]
    for section, detail in data['Modules'].items():
        with st.expander(section): st.write(detail)

elif st.session_state.page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): 
        st.session_state.page = "subject_options"
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.rerun()
    
    mod_opts = list(FULL_SYLLABUS[st.session_state.current_subject]["Modules"].keys())
    c1, c2 = st.columns([2, 1])
    with c1: sel_mod = st.selectbox("Select Module:", mod_opts)
    with c2: sel_set = st.radio("Set:", ["Set 1", "Set 2", "Set 3"], horizontal=True)
        
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
                    st.image(q_img, use_container_width=True)
                
                ans_key = f"quiz_radio_{curr_id}_{i}"
                saved_val = st.session_state.user_answers.get(i)
                choice = st.radio(f"Answer Q{i+1}:", ["A", "B", "C", "D"], 
                                  index=["A","B","C","D"].index(saved_val) if saved_val in ["A","B","C","D"] else None,
                                  key=ans_key, horizontal=True)
                if choice: st.session_state.user_answers[i] = choice
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

            if st.button("🏆 Submit Final Answers", type="primary", use_container_width=True):
                st.session_state.quiz_submitted = True; st.rerun()
        else:
            score = sum(1 for i, (_, c, _) in enumerate(active_data) if st.session_state.user_answers.get(i) == c)
            st.markdown(f"<div class='result-card'><h1>Score: {score} / {len(active_data)}</h1></div>", unsafe_allow_html=True)
            for i, (q_img, cor, e_img) in enumerate(active_data):
                u_ans = st.session_state.user_answers.get(i, "N/A")
                with st.expander(f"Question {i+1}: {'✅' if u_ans == cor else '❌'}"):
                    if os.path.exists(q_img): st.image(q_img, use_container_width=True)
                    st.success(f"Correct: {cor} | Yours: {u_ans}")
                    if os.path.exists(e_img): st.image(e_img, use_container_width=True)
            if st.button("🔄 Restart Practice", use_container_width=True): 
                st.session_state.quiz_submitted = False; st.session_state.user_answers = {}; st.rerun()
    else:
        st.warning(f"Materials coming soon!")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>Professor Shakeelurahman OP | © 2026</p>", unsafe_allow_html=True)