"""
╔══════════════════════════════════════════════════════════════╗
║           ALTRA RESEARCH - Complete Job Portal              ║
║           Location: Eruthoorkadai, Tamil Nadu               ║
║           Contact: altraresearch@gmail.com                  ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import sqlite3
import re
import time
import random
from datetime import datetime

# ═══════════════════════════════════════════════
# PAGE CONFIGURATION - Dynamic & Responsive
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="Altra Research | Careers",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed" if st.session_state.get('mobile_view', False) else "expanded"
)

# ═══════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'show_details' not in st.session_state:
    st.session_state.show_details = False
if 'show_apply' not in st.session_state:
    st.session_state.show_apply = False
if 'applied_jobs' not in st.session_state:
    st.session_state.applied_jobs = []
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []
if 'history' not in st.session_state:
    st.session_state.history = ["home"]

# ═══════════════════════════════════════════════
# CSS - Fixed HTML rendering, Touch & Dynamic support
# ═══════════════════════════════════════════════
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { 
        font-family: 'Inter', sans-serif;
        -webkit-tap-highlight-color: transparent;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1040 30%, #0d1230 60%, #0a0a1a 100%);
        background-attachment: fixed;
    }
    
    /* Force all text to be visible - white/light colors */
    .stMarkdown p, .stMarkdown li, .stMarkdown div, 
    .element-container p, .element-container li,
    .row-widget p, .row-widget li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #e2e8f0 !important;
        line-height: 1.7 !important;
    }
    
    h1, h2, h3, h4 {
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 900 !important;
    }
    
    h1 { font-size: clamp(28px, 5vw, 48px) !important; }
    h2 { font-size: clamp(22px, 4vw, 36px) !important; }
    h3 { font-size: clamp(18px, 3vw, 28px) !important; }
    
    /* CARDS */
    .job-card {
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: clamp(15px, 3vw, 25px);
        margin: 15px 0;
        transition: all 0.3s ease;
        cursor: pointer;
        -webkit-tap-highlight-color: rgba(79,70,229,0.3);
    }
    
    .job-card:active {
        transform: scale(0.98);
        background: rgba(79,70,229,0.15);
        border-color: #4f46e5;
    }
    
    @media (hover: hover) {
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(79,70,229,0.3);
            border-color: #4f46e5;
            background: rgba(255,255,255,0.08);
        }
    }
    
    /* BUTTONS - Touch friendly */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        padding: clamp(12px, 2vw, 16px) clamp(20px, 3vw, 35px) !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: clamp(13px, 2vw, 16px) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        min-height: 48px !important;
        -webkit-tap-highlight-color: transparent !important;
        touch-action: manipulation !important;
    }
    
    .stButton > button:active {
        transform: scale(0.95) !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    }
    
    @media (hover: hover) {
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 30px rgba(79,70,229,0.5) !important;
        }
    }
    
    /* INPUTS - Touch friendly */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: clamp(12px, 2vw, 16px) !important;
        font-size: clamp(14px, 2vw, 16px) !important;
        min-height: 48px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 20px rgba(79,70,229,0.3) !important;
        outline: none !important;
    }
    
    /* LABELS */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: clamp(12px, 1.5vw, 14px) !important;
        letter-spacing: 0.5px !important;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a, #1a1040) !important;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* ALERTS */
    .stSuccess { background: #059669 !important; color: #ffffff !important; border-radius: 12px !important; padding: 20px !important; }
    .stSuccess p, .stSuccess div { color: #d1fae5 !important; }
    .stError { background: #dc2626 !important; color: #ffffff !important; border-radius: 12px !important; padding: 15px !important; }
    .stError p, .stError div { color: #fecaca !important; }
    .stWarning { background: rgba(245,158,11,0.2) !important; border: 2px solid #f59e0b !important; border-radius: 12px !important; }
    .stWarning p, .stWarning div { color: #fbbf24 !important; }
    .stInfo { background: rgba(59,130,246,0.15) !important; border: 2px solid #3b82f6 !important; border-radius: 12px !important; }
    .stInfo p, .stInfo div { color: #93c5fd !important; }
    
    /* BADGES */
    .badge {
        display: inline-block !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        margin: 3px !important;
        letter-spacing: 0.5px !important;
        color: #ffffff !important;
    }
    
    /* METRICS */
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: clamp(24px, 4vw, 36px) !important; font-weight: 900 !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: clamp(12px, 1.5vw, 14px) !important; }
    [data-testid="stMetricDelta"] { color: #34d399 !important; }
    
    /* DIVIDER */
    hr { border: none; height: 2px; background: linear-gradient(90deg, transparent, #4f46e5, transparent); margin: 25px 0; }
    
    /* BACK BUTTON */
    .back-btn {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: #ffffff;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .back-btn:hover {
        background: rgba(255,255,255,0.2);
        border-color: #4f46e5;
    }
    
    /* SCROLLBAR */
    ::-webkit-scrollbar { width: clamp(6px, 1vw, 10px); }
    ::-webkit-scrollbar-track { background: #0a0a1a; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #4f46e5, #7c3aed); border-radius: 10px; }
    
    /* ANIMATIONS */
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    .float { animation: float 3s ease-in-out infinite; }
    
    /* TOUCH FRIENDLY SPACING */
    .stRadio > div { gap: 8px !important; }
    .stRadio label { padding: 12px !important; min-height: 48px !important; display: flex !important; align-items: center !important; }
    
    /* DYNAMIC CONTAINER */
    .content-container {
        padding: clamp(10px, 2vw, 30px);
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* RESPONSIVE GRID */
    @media (max-width: 768px) {
        .stColumns { flex-direction: column !important; }
        .stColumn { width: 100% !important; }
        [data-testid="column"] { width: 100% !important; flex: none !important; }
    }
    
    /* TOUCH RIPPLE EFFECT */
    .stButton > button, .job-card {
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::after {
        width: 300px;
        height: 300px;
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect('altra.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT, phone TEXT, position TEXT,
                  experience INTEGER, education TEXT, skills TEXT,
                  cover TEXT, date TIMESTAMP, status TEXT DEFAULT 'Pending')''')
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT, subject TEXT, message TEXT, date TIMESTAMP)''')
    conn.commit()
    conn.close()

def valid_email(e):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', e) is not None

def valid_phone(p):
    return re.match(r'^\+?\d{10,15}$', p) is not None

def save_app(data):
    conn = sqlite3.connect('altra.db')
    c = conn.cursor()
    c.execute('INSERT INTO applications (name,email,phone,position,experience,education,skills,cover,date) VALUES (?,?,?,?,?,?,?,?,?)',
              (data['name'],data['email'],data['phone'],data['position'],data['exp'],data['edu'],data['skills'],data['cover'],datetime.now()))
    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════
# JOB DATA
# ═══════════════════════════════════════════════
JOBS = [
    {
        "id": 1, "title": "Senior Research Scientist", "dept": "Research", "type": "Full-Time",
        "exp": "5-8 Years", "salary": "₹15-25 LPA", "location": "Eruthoorkadai",
        "desc": "Lead cutting-edge AI and Machine Learning research initiatives. Develop innovative algorithms that solve complex real-world problems and publish groundbreaking papers.",
        "reqs": "PhD/Masters in CS/AI, 5+ years research experience, Published papers, Python expertise",
        "skills": "Python, TensorFlow, PyTorch, Deep Learning, Research",
        "benefits": "Health Insurance, Stock Options, Research Budget, Conference Travel",
        "openings": 3
    },
    {
        "id": 2, "title": "Full Stack Developer", "dept": "Development", "type": "Full-Time",
        "exp": "3-5 Years", "salary": "₹12-20 LPA", "location": "Eruthoorkadai / Remote",
        "desc": "Design and build scalable web applications using modern technologies. Work across the entire stack from database design to user interface implementation with a focus on performance.",
        "reqs": "Bachelor's in CS, 3+ years web dev, React/Node experience, AWS knowledge",
        "skills": "React, Node.js, Python, AWS, Docker, PostgreSQL",
        "benefits": "Flexible Hours, Remote Option, Health Insurance, Learning Budget",
        "openings": 5
    },
    {
        "id": 3, "title": "UI/UX Designer", "dept": "Design", "type": "Remote",
        "exp": "2-4 Years", "salary": "₹8-15 LPA", "location": "Remote",
        "desc": "Create stunning, intuitive interfaces that delight users. Conduct user research, create wireframes and prototypes, and deliver pixel-perfect designs that enhance user experience.",
        "reqs": "Design degree/certification, Strong portfolio, Figma expertise, User research experience",
        "skills": "Figma, Adobe XD, Prototyping, User Research, Design Systems",
        "benefits": "Remote Work, Design Tools, Creative Freedom, Health Insurance",
        "openings": 2
    },
    {
        "id": 4, "title": "Data Analyst", "dept": "Research", "type": "Full-Time",
        "exp": "2-5 Years", "salary": "₹10-18 LPA", "location": "Eruthoorkadai",
        "desc": "Transform raw data into actionable business insights. Build comprehensive dashboards and automated reporting systems that drive strategic decision-making.",
        "reqs": "Statistics/Math background, SQL expertise, Python proficiency, BI tool experience",
        "skills": "SQL, Python, Power BI, Statistics, Excel, Tableau",
        "benefits": "Health Insurance, Learning Budget, Performance Bonus, Gym Membership",
        "openings": 4
    },
    {
        "id": 5, "title": "Marketing Lead", "dept": "Marketing", "type": "Full-Time",
        "exp": "4-7 Years", "salary": "₹12-22 LPA", "location": "Eruthoorkadai",
        "desc": "Spearhead marketing campaigns that amplify our brand presence. Drive growth through innovative digital strategies and lead a creative team to success.",
        "reqs": "Marketing degree, 4+ years experience, Digital marketing expertise, Team leadership",
        "skills": "Digital Marketing, SEO/SEM, Content Strategy, Analytics, Team Management",
        "benefits": "Leadership Role, Marketing Budget, Health Insurance, Travel Allowance",
        "openings": 1
    },
    {
        "id": 6, "title": "HR Business Partner", "dept": "HR", "type": "Full-Time",
        "exp": "3-6 Years", "salary": "₹8-14 LPA", "location": "Eruthoorkadai",
        "desc": "Shape our company culture and drive talent strategy. Partner with leadership to build high-performing, diverse teams and foster an inclusive workplace.",
        "reqs": "HR degree/certification, 3+ years HR experience, Recruitment expertise, Labor law knowledge",
        "skills": "Talent Acquisition, Employee Relations, HR Analytics, Performance Management",
        "benefits": "Health Insurance, Professional Development, Flexible Hours, Team Events",
        "openings": 2
    }
]

# ═══════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════
def go_back():
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()
        st.session_state.page = st.session_state.history[-1]
        st.session_state.show_details = False
        st.session_state.show_apply = False
        st.rerun()

def navigate_to(page):
    st.session_state.page = page
    st.session_state.history.append(page)
    st.rerun()

def get_job_by_id(job_id):
    for job in JOBS:
        if job['id'] == job_id:
            return job
    return None

# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
def main():
    load_css()
    init_db()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:20px 10px;'>
            <div class='float' style='font-size:clamp(40px,8vw,60px);'>🔬</div>
            <h3 style='font-size:clamp(18px,3vw,24px);'>ALTRA RESEARCH</h3>
            <p style='color:#94a3b8;font-size:clamp(10px,1.5vw,12px);letter-spacing:2px;'>INNOVATION MEETS EXCELLENCE</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Back button at top
        if len(st.session_state.history) > 1:
            if st.button("⬅️ BACK", key="sidebar_back", use_container_width=True):
                go_back()
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation
        pages = ["🏠 Home", "💼 All Positions", "📊 Dashboard", "📝 My Applications", "📧 Contact"]
        current_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
        
        menu = st.radio("NAVIGATION", pages, index=current_index, label_visibility="collapsed")
        
        if menu != st.session_state.page:
            navigate_to(menu)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:rgba(255,255,255,0.05);padding:15px;border-radius:12px;'>
            <p style='font-size:clamp(11px,1.5vw,13px);color:#94a3b8;margin:5px 0;'>📍 Eruthoorkadai</p>
            <p style='font-size:clamp(11px,1.5vw,13px);color:#94a3b8;margin:5px 0;'>📧 altraresearch@gmail.com</p>
            <p style='font-size:clamp(11px,1.5vw,13px);color:#94a3b8;margin:5px 0;'>📞 +91 98765 43210</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content with back button
    if len(st.session_state.history) > 1 and st.session_state.page != "home":
        col_back, col_title = st.columns([1, 11])
        with col_back:
            if st.button("⬅️", key="main_back", help="Go back", use_container_width=True):
                go_back()
    
    # Page routing
    if st.session_state.page == "🏠 Home":
        home()
    elif st.session_state.page == "💼 All Positions":
        all_positions()
    elif st.session_state.page == "📊 Dashboard":
        dashboard()
    elif st.session_state.page == "📝 My Applications":
        my_applications()
    elif st.session_state.page == "📧 Contact":
        contact()

# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
def home():
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 🚀 WE ARE HIRING!")
        st.markdown("# Build The Future With Altra Research")
        st.markdown("Join 150+ innovators in Eruthoorkadai shaping tomorrow's technology through cutting-edge research and development.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("💼 VIEW JOBS", use_container_width=True, key="home_jobs"):
                navigate_to("💼 All Positions")
        with c2:
            if st.button("📝 APPLY NOW", use_container_width=True, key="home_apply"):
                navigate_to("💼 All Positions")
        with c3:
            if st.button("📊 DASHBOARD", use_container_width=True, key="home_dash"):
                navigate_to("📊 Dashboard")
    
    with col2:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.05);border-radius:20px;padding:clamp(20px,4vw,40px);text-align:center;border:1px solid rgba(255,255,255,0.1);'>
            <div class='float' style='font-size:clamp(60px,12vw,100px);'>🏢</div>
            <h3>Your Career Starts Here</h3>
            <p style='color:#94a3b8;'>500+ Projects | 150+ Team | 50+ Openings</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Open Positions", "6", "Active")
    with c2: st.metric("Departments", "4", "")
    with c3: st.metric("Team Size", "150+", "Growing")
    with c4: st.metric("Countries", "20+", "Global")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Featured Jobs
    st.markdown("## ⭐ Featured Positions")
    
    featured = random.sample(JOBS, min(3, len(JOBS)))
    cols = st.columns(3)
    
    for idx, job in enumerate(featured):
        with cols[idx]:
            st.markdown(f"""
            <div class='job-card'>
                <h3 style='font-size:clamp(16px,2vw,20px);'>{job['title']}</h3>
                <p style='margin:10px 0;'>
                    <span class='badge' style='background:#3b82f6;'>{job['dept']}</span>
                    <span class='badge' style='background:#10b981;'>{job['type']}</span>
                </p>
                <p style='color:#cbd5e1;font-size:clamp(13px,1.5vw,15px);'>{job['desc'][:100]}...</p>
                <p style='color:#fbbf24;font-weight:700;font-size:clamp(14px,2vw,18px);'>{job['salary']}</p>
                <p style='color:#94a3b8;font-size:12px;'>📍 {job['location']} | 🎯 {job['openings']} openings</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 View Details", key=f"feat_{idx}", use_container_width=True):
                st.session_state.selected_job = job['id']
                st.session_state.show_details = True
                navigate_to("💼 All Positions")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Why Join Us
    st.markdown("## Why Join Altra Research?")
    
    benefits = [
        {"icon": "🚀", "title": "Innovation", "desc": "Work on cutting-edge projects"},
        {"icon": "📈", "title": "Growth", "desc": "Clear career advancement paths"},
        {"icon": "🤝", "title": "Culture", "desc": "Inclusive, collaborative team"},
        {"icon": "💎", "title": "Benefits", "desc": "Top salary and perks"}
    ]
    
    bcols = st.columns(4)
    for idx, b in enumerate(benefits):
        with bcols[idx]:
            st.markdown(f"""
            <div style='text-align:center;padding:20px;background:rgba(255,255,255,0.05);border-radius:15px;'>
                <div style='font-size:clamp(30px,5vw,40px);'>{b['icon']}</div>
                <h4 style='color:#a78bfa;'>{b['title']}</h4>
                <p style='color:#cbd5e1;font-size:13px;'>{b['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style='text-align:center;padding:clamp(30px,5vw,50px);background:linear-gradient(135deg,rgba(79,70,229,0.2),rgba(124,58,237,0.2));border-radius:20px;'>
        <h2>Ready to Make History?</h2>
        <p style='font-size:clamp(16px,2vw,18px);color:#cbd5e1;'>Join us and be part of something extraordinary</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔥 BROWSE ALL OPEN POSITIONS", use_container_width=True, key="home_cta"):
        navigate_to("💼 All Positions")

# ═══════════════════════════════════════════════
# ALL POSITIONS PAGE
# ═══════════════════════════════════════════════
def all_positions():
    # Show job details if selected
    if st.session_state.show_details and st.session_state.selected_job:
        job = get_job_by_id(st.session_state.selected_job)
        if job:
            show_job_details(job)
            return
    
    # Show apply form if selected
    if st.session_state.show_apply and st.session_state.selected_job:
        job = get_job_by_id(st.session_state.selected_job)
        if job:
            show_apply_form(job)
            return
    
    # Main positions page
    st.markdown("## 💼 Open Positions")
    st.markdown("Find your perfect role at Altra Research")
    
    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Job title, skill, or keyword...", key="job_search")
    with col2:
        dept_filter = st.selectbox("Department", ["All", "Research", "Development", "Design", "Marketing", "HR"], key="dept_filter")
    with col3:
        type_filter = st.selectbox("Type", ["All", "Full-Time", "Part-Time", "Remote", "Contract"], key="type_filter")
    
    # Filter jobs
    filtered = JOBS.copy()
    if search:
        s = search.lower()
        filtered = [j for j in filtered if s in j['title'].lower() or s in j['skills'].lower() or s in j['desc'].lower()]
    if dept_filter != "All":
        filtered = [j for j in filtered if j['dept'] == dept_filter]
    if type_filter != "All":
        filtered = [j for j in filtered if j['type'] == type_filter]
    
    st.markdown(f"Showing **{len(filtered)}** position(s)")
    
    if not filtered:
        st.warning("No positions match your criteria. Try different filters.")
        return
    
    # Display jobs
    for job in filtered:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class='job-card'>
                    <h3 style='font-size:clamp(16px,2.5vw,22px);'>{job['title']}</h3>
                    <p style='margin:10px 0;'>
                        <span class='badge' style='background:#3b82f6;'>{job['dept']}</span>
                        <span class='badge' style='background:#10b981;'>{job['type']}</span>
                        <span class='badge' style='background:#8b5cf6;'>{job['exp']}</span>
                        <span class='badge' style='background:#f59e0b;color:#000;'>💰 {job['salary']}</span>
                    </p>
                    <p style='color:#cbd5e1;font-size:clamp(13px,1.5vw,15px);'>{job['desc'][:150]}...</p>
                    <p style='color:#94a3b8;font-size:12px;'>📍 {job['location']} | 🎯 {job['openings']} opening(s)</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("📋 DETAILS", key=f"det_{job['id']}", use_container_width=True):
                    st.session_state.selected_job = job['id']
                    st.session_state.show_details = True
                    st.rerun()
                
                if st.button("⚡ APPLY", key=f"apl_{job['id']}", use_container_width=True):
                    st.session_state.selected_job = job['id']
                    st.session_state.show_apply = True
                    st.rerun()
                
                # Save/Unsave
                if job['id'] in st.session_state.saved_jobs:
                    if st.button("❤️ SAVED", key=f"sav_{job['id']}", use_container_width=True):
                        st.session_state.saved_jobs.remove(job['id'])
                        st.success("Removed from saved")
                        time.sleep(0.3)
                        st.rerun()
                else:
                    if st.button("🤍 SAVE", key=f"sav_{job['id']}", use_container_width=True):
                        st.session_state.saved_jobs.append(job['id'])
                        st.success("Job saved!")
                        time.sleep(0.3)
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)


def show_job_details(job):
    """Show detailed job view"""
    if st.button("⬅️ Back to Positions", key="back_from_details", use_container_width=True):
        st.session_state.show_details = False
        st.session_state.selected_job = None
        st.rerun()
    
    st.markdown(f"## 📋 {job['title']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Job Description")
        st.markdown(job['desc'])
        
        st.markdown("### Requirements")
        reqs_list = [r.strip() for r in job['reqs'].split(',')]
        for req in reqs_list:
            st.markdown(f"- {req}")
        
        st.markdown("### Required Skills")
        skills_list = [s.strip() for s in job['skills'].split(',')]
        for skill in skills_list:
            st.markdown(f"<span class='badge' style='background:#3b82f6;'>{skill}</span>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quick Info")
        st.markdown(f"**📍 Location:** {job['location']}")
        st.markdown(f"**💼 Type:** {job['type']}")
        st.markdown(f"**⏰ Experience:** {job['exp']}")
        st.markdown(f"**💰 Salary:** {job['salary']}")
        st.markdown(f"**🎯 Openings:** {job['openings']}")
        st.markdown(f"**📂 Department:** {job['dept']}")
        
        st.markdown("### Benefits")
        benefits_list = [b.strip() for b in job['benefits'].split(',')]
        for benefit in benefits_list:
            st.markdown(f"✅ {benefit}")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("⚡ APPLY NOW", use_container_width=True, key="detail_apply"):
            st.session_state.show_apply = True
            st.rerun()
    with col_b2:
        if st.button("❌ CLOSE", use_container_width=True, key="detail_close"):
            st.session_state.show_details = False
            st.session_state.selected_job = None
            st.rerun()


def show_apply_form(job):
    """Show application form"""
    if st.button("⬅️ Back to Positions", key="back_from_apply", use_container_width=True):
        st.session_state.show_apply = False
        st.rerun()
    
    st.markdown(f"## 📝 Apply for {job['title']}")
    st.info(f"Applying for: **{job['title']}** at Altra Research, Eruthoorkadai")
    
    st.markdown("**📊 Application Progress**")
    progress_bar = st.progress(0)
    
    with st.form("apply_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name *", placeholder="Your full name", key="app_name")
            email = st.text_input("📧 Email *", placeholder="your@email.com", key="app_email")
            phone = st.text_input("📞 Phone *", placeholder="+919876543210", key="app_phone")
        
        with col2:
            position = st.text_input("💼 Position", value=job['title'], disabled=True, key="app_pos")
            exp = st.number_input("⏳ Experience (Years) *", 0, 30, 0, key="app_exp")
            edu = st.selectbox("🎓 Education *", ["Select", "High School", "Diploma", "Bachelor's", "Master's", "PhD", "Other"], key="app_edu")
        
        skills = st.text_input("🎯 Key Skills *", placeholder="Python, React, SQL...", key="app_skills")
        cover = st.text_area("✍️ Cover Letter", placeholder="Why are you the perfect fit for this role?", height=120, key="app_cover")
        resume = st.file_uploader("📄 Resume (PDF/DOC)", type=['pdf','doc','docx'], key="app_resume")
        
        # Progress
        fields = sum([bool(name), bool(email), bool(phone), edu != "Select", bool(skills)])
        progress_bar.progress(fields / 5)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            submitted = st.form_submit_button("🚀 SUBMIT", use_container_width=True)
        with col_s2:
            cancel = st.form_submit_button("❌ CANCEL", use_container_width=True)
        
        if cancel:
            st.session_state.show_apply = False
            st.rerun()
        
        if submitted:
            errors = []
            if not name: errors.append("Name required")
            if not email or not valid_email(email): errors.append("Valid email required")
            if not phone or not valid_phone(phone): errors.append("Valid phone required")
            if edu == "Select": errors.append("Education required")
            if not skills: errors.append("Skills required")
            
            if errors:
                for e in errors:
                    st.error(e)
            else:
                save_app({
                    'name': name, 'email': email, 'phone': phone,
                    'position': position, 'exp': exp, 'edu': edu,
                    'skills': skills, 'cover': cover
                })
                
                st.session_state.applied_jobs.append(job['id'])
                st.session_state.show_apply = False
                
                st.success("✅ APPLICATION SUBMITTED SUCCESSFULLY!")
                st.markdown(f"Applied for **{position}** at Altra Research")
                st.markdown("We'll review your application and respond within 5-7 business days.")
                st.markdown("📧 Contact: altraresearch@gmail.com")
                st.balloons()
                time.sleep(0.3)
                st.snow()

# ═══════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════
def dashboard():
    st.markdown("## 📊 Dashboard")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Positions", len(JOBS), "")
    with c2: st.metric("Departments", "4", "")
    with c3: st.metric("Applied", len(st.session_state.applied_jobs), "")
    with c4: st.metric("Saved", len(st.session_state.saved_jobs), "")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### 📂 Positions by Department")
    depts = {}
    for job in JOBS:
        depts[job['dept']] = depts.get(job['dept'], 0) + 1
    
    cols = st.columns(len(depts))
    for idx, (dept, count) in enumerate(depts.items()):
        with cols[idx]:
            st.metric(dept, count, "positions")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### 💰 Salary Overview")
    for job in JOBS:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05);padding:15px;border-radius:10px;margin:5px 0;display:flex;justify-content:space-between;align-items:center;'>
            <strong style='color:#e2e8f0;'>{job['title']}</strong>
            <span style='color:#34d399;font-weight:700;'>{job['salary']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### 💡 Career Tips")
    tips = [
        "Keep your resume updated with latest skills and achievements",
        "Apply to positions that match 70% or more of your skills",
        "Customize your cover letter for each application",
        "Follow up within a week after submitting applications",
        "Research the company thoroughly before interviews"
    ]
    for tip in tips:
        st.info(tip)

# ═══════════════════════════════════════════════
# MY APPLICATIONS
# ═══════════════════════════════════════════════
def my_applications():
    st.markdown("## 📝 My Applications")
    
    if not st.session_state.applied_jobs and not st.session_state.saved_jobs:
        st.info("You haven't applied to or saved any positions yet.")
        if st.button("💼 BROWSE POSITIONS", use_container_width=True):
            navigate_to("💼 All Positions")
        return
    
    # Applied jobs
    if st.session_state.applied_jobs:
        st.markdown("### ✅ Applied Positions")
        for job_id in st.session_state.applied_jobs:
            job = get_job_by_id(job_id)
            if job:
                st.markdown(f"""
                <div class='job-card'>
                    <h4 style='color:#a78bfa;'>{job['title']}</h4>
                    <p><span class='badge' style='background:#3b82f6;'>{job['dept']}</span> <span class='badge' style='background:#10b981;'>Applied</span></p>
                    <p style='color:#34d399;'><strong>Status: Under Review</strong></p>
                    <p style='color:#94a3b8;font-size:13px;'>We'll respond within 5-7 business days</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Saved jobs
    if st.session_state.saved_jobs:
        st.markdown("### ❤️ Saved Positions")
        for job_id in st.session_state.saved_jobs:
            job = get_job_by_id(job_id)
            if job and job['id'] not in st.session_state.applied_jobs:
                st.markdown(f"""
                <div class='job-card'>
                    <h4 style='color:#a78bfa;'>{job['title']}</h4>
                    <p><span class='badge' style='background:#3b82f6;'>{job['dept']}</span> <span class='badge' style='background:#f59e0b;color:#000;'>{job['salary']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⚡ Apply Now", key=f"saved_apply_{job_id}", use_container_width=True):
                    st.session_state.selected_job = job['id']
                    st.session_state.show_apply = True
                    navigate_to("💼 All Positions")

# ═══════════════════════════════════════════════
# CONTACT PAGE
# ═══════════════════════════════════════════════
def contact():
    st.markdown("## 📧 Contact Us")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Our Office")
        st.markdown("""
        **📍 Address:** 123 Research Park, Eruthoorkadai, Tamil Nadu - 627001
        
        **📧 Email:** altraresearch@gmail.com
        
        **📞 Phone:** +91 98765 43210
        
        **🕐 Hours:** Monday - Friday, 9:00 AM - 6:00 PM
        """)
    
    with col2:
        st.markdown("### 💬 Send Message")
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Name *", key="con_name")
            email = st.text_input("Email *", key="con_email")
            subject = st.text_input("Subject", key="con_subject")
            msg = st.text_area("Message *", height=120, key="con_msg")
            
            if st.form_submit_button("📨 SEND MESSAGE", use_container_width=True):
                if name and email and msg:
                    if valid_email(email):
                        conn = sqlite3.connect('altra.db')
                        c = conn.cursor()
                        c.execute('INSERT INTO contacts (name,email,subject,message,date) VALUES (?,?,?,?,?)',
                                 (name, email, subject, msg, datetime.now()))
                        conn.commit()
                        conn.close()
                        st.success("✅ Message sent successfully! We'll respond within 24 hours.")
                        st.balloons()
                    else:
                        st.error("Please enter a valid email address")
                else:
                    st.error("Please fill in all required fields (Name, Email, Message)")

# ═══════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    main()