"""
╔══════════════════════════════════════════════════════════════╗
║           ALTRA RESEARCH - Premium Job Portal               ║
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
from streamlit_option_menu import option_menu
import os

# ═══════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="Altra Research | Careers",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════
# COMPLETE CSS - ALL TEXT VISIBLE
# ═══════════════════════════════════════════════
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800;900&display=swap');
    
    /* ═══ GLOBAL TEXT COLORS - WHITE TEXT ═══ */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1040 30%, #0d1230 60%, #0a0a1a 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Force ALL main content text to WHITE */
    .stMarkdown p,
    .stMarkdown span,
    .stMarkdown li,
    .stMarkdown div,
    .element-container p,
    .element-container span,
    .element-container li,
    .element-container div,
    .row-widget,
    .stText,
    p, span, li {
        color: #ffffff !important;
    }
    
    /* Headers - Bright gradient */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 800 !important;
    }
    
    h1 { font-size: 42px !important; }
    h2 { font-size: 32px !important; }
    h3 { font-size: 24px !important; }
    
    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 36px !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #34d399 !important;
        font-weight: 700 !important;
    }
    
    /* ═══ GLASS CARDS ═══ */
    .glass-card {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 20px 50px rgba(99, 102, 241, 0.3) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* ═══ NEON GLOW EFFECTS ═══ */
    .neon-card {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid #4f46e5 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.3), 
                    inset 0 0 20px rgba(79, 70, 229, 0.1) !important;
        transition: all 0.3s ease !important;
        animation: neonPulse 2s infinite !important;
    }
    
    @keyframes neonPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.3), inset 0 0 20px rgba(79, 70, 229, 0.1); }
        50% { box-shadow: 0 0 40px rgba(79, 70, 229, 0.6), inset 0 0 30px rgba(79, 70, 229, 0.2); }
    }
    
    /* ═══ FLOATING ANIMATION ═══ */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite !important;
    }
    
    /* ═══ SHIMMER EFFECT ═══ */
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .shimmer-text {
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6, #60a5fa) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: shimmer 3s linear infinite !important;
    }
    
    /* ═══ PULSE RING ═══ */
    @keyframes pulseRing {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(1.5); opacity: 0; }
    }
    
    .pulse-ring {
        animation: pulseRing 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite !important;
    }
    
    /* ═══ SPIN ANIMATION ═══ */
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .spin-slow {
        animation: spin 8s linear infinite !important;
    }
    
    /* ═══ BUTTONS ═══ */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #a855f7) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 16px 35px !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s, height 0.6s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(79, 70, 229, 0.6) !important;
    }
    
    .stButton > button:hover::before {
        width: 400px !important;
        height: 400px !important;
    }
    
    /* ═══ INPUT FIELDS ═══ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Labels */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    /* ═══ SIDEBAR ═══ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a, #1a1040, #0d1230) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h3 {
        background: linear-gradient(135deg, #60a5fa, #a78bfa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    /* ═══ PROGRESS BAR ═══ */
    .stProgress > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        height: 10px !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #a855f7) !important;
        border-radius: 20px !important;
        animation: shimmer 2s linear infinite !important;
        background-size: 200% auto !important;
    }
    
    /* ═══ SUCCESS / ERROR ═══ */
    .stSuccess {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: #ffffff !important;
        border-radius: 16px !important;
        padding: 25px !important;
        border: 2px solid #34d399 !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stError {
        background: #dc2626 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: 2px solid #f87171 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.2) !important;
        color: #fbbf24 !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #93c5fd !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    /* ═══ EXPANDER ═══ */
    .stExpander {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    .stExpander p, .stExpander span {
        color: #e2e8f0 !important;
    }
    
    /* ═══ TABS ═══ */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        box-shadow: 0 5px 20px rgba(79, 70, 229, 0.4) !important;
    }
    
    /* ═══ MINI-GAME STYLES ═══ */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-30px); }
    }
    
    .game-emoji {
        font-size: 80px;
        animation: bounce 0.5s ease infinite;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .game-emoji:hover {
        transform: scale(1.3);
        filter: drop-shadow(0 0 20px rgba(167, 139, 250, 0.8));
    }
    
    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4f46e5, #7c3aed);
        border-radius: 10px;
    }
    
    /* ═══ DIVIDER ═══ */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #4f46e5, #7c3aed, #a855f7, transparent) !important;
        margin: 30px 0 !important;
    }
    
    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 768px) {
        h1 { font-size: 28px !important; }
        h2 { font-size: 22px !important; }
        .stButton > button { padding: 12px 25px !important; font-size: 14px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════
def init_database():
    conn = sqlite3.connect('altra_research.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  full_name TEXT, email TEXT, phone TEXT, position TEXT,
                  experience INTEGER, education TEXT, skills TEXT,
                  cover_letter TEXT, applied_date TIMESTAMP, status TEXT DEFAULT 'Pending')''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT, subject TEXT, message TEXT, date TIMESTAMP)''')
    conn.commit()
    conn.close()

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def is_valid_phone(phone):
    return re.match(r'^\+?1?\d{9,15}$', phone) is not None

def save_application(data):
    conn = sqlite3.connect('altra_research.db')
    c = conn.cursor()
    c.execute('''INSERT INTO applications 
                 (full_name, email, phone, position, experience, education, skills, cover_letter, applied_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['full_name'], data['email'], data['phone'], data['position'],
               data['experience'], data['education'], data['skills'], data['cover_letter'], datetime.now()))
    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════
# TIPS GENERATOR
# ═══════════════════════════════════════════════
def get_daily_tip():
    tips = [
        "💡 Tip: Tailor your resume for each job application to highlight relevant skills.",
        "🚀 Tip: Research the company before your interview - it shows initiative!",
        "📝 Tip: Use action verbs like 'developed', 'led', 'achieved' in your resume.",
        "🎯 Tip: Network on LinkedIn - 85% of jobs are filled through networking.",
        "⭐ Tip: Prepare 3-5 questions to ask your interviewer - it demonstrates interest.",
        "💪 Tip: Update your skills regularly - the tech industry evolves fast!",
        "🎨 Tip: Keep your resume clean and professional - use consistent formatting.",
        "🔥 Tip: Follow up after interviews with a thank-you email within 24 hours.",
        "📊 Tip: Quantify achievements - use numbers and percentages when possible.",
        "🌟 Tip: Build a portfolio website to showcase your projects and skills.",
        "🎓 Tip: Continuous learning is key - take online courses to stay competitive.",
        "💼 Tip: Dress professionally for interviews, even virtual ones.",
        "🗣️ Tip: Practice your elevator pitch - you have 30 seconds to make an impression.",
        "📅 Tip: Arrive 10-15 minutes early for interviews - punctuality matters.",
        "🤝 Tip: Connect with current employees to learn about company culture."
    ]
    return random.choice(tips)

# ═══════════════════════════════════════════════
# MINI GAME
# ═══════════════════════════════════════════════
def mini_game():
    st.markdown("## 🎮 Speed Click Challenge")
    st.markdown("*Click the emoji as fast as you can in 5 seconds!*")
    
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 5
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.game_started:
            if st.button("🎮 START GAME", use_container_width=True):
                st.session_state.game_started = True
                st.session_state.score = 0
                st.session_state.time_left = 5
                st.session_state.game_over = False
                st.rerun()
        else:
            if not st.session_state.game_over:
                st.markdown(f"### ⏱️ Time: {st.session_state.time_left}s | 🏆 Score: {st.session_state.score}")
                
                emojis = ["🚀", "⭐", "💎", "🔥", "🎯", "🌟", "💪", "🏆"]
                target = random.choice(emojis)
                
                st.markdown(f"""
                <div style='text-align: center; padding: 30px;'>
                    <div class='game-emoji'>{target}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"CLICK {target}!", key=f"game_{st.session_state.score}", use_container_width=True):
                    st.session_state.score += 1
                    st.rerun()
                
                # Timer logic
                if st.session_state.time_left > 0:
                    time.sleep(1)
                    st.session_state.time_left -= 1
                    if st.session_state.time_left == 0:
                        st.session_state.game_over = True
                    st.rerun()
            else:
                st.markdown(f"## 🎉 Game Over!")
                st.markdown(f"### Your Score: **{st.session_state.score}** clicks!")
                
                if st.session_state.score >= 15:
                    st.success("🏆 LEGENDARY! You're a speed demon!")
                    st.balloons()
                elif st.session_state.score >= 10:
                    st.success("⭐ AMAZING! Great reflexes!")
                elif st.session_state.score >= 5:
                    st.info("👍 GOOD JOB! Keep practicing!")
                else:
                    st.warning("💪 Keep trying! You can do better!")
                
                if st.button("🔄 PLAY AGAIN", use_container_width=True):
                    st.session_state.game_started = False
                    st.session_state.score = 0
                    st.session_state.time_left = 5
                    st.session_state.game_over = False
                    st.rerun()

# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
def main():
    load_css()
    init_database()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px 10px;'>
            <div class='float-animation' style='font-size: 70px;'>🔬</div>
            <h3 style='font-size: 24px; font-weight: 900; margin: 15px 0;'>ALTRA RESEARCH</h3>
            <p style='font-size: 12px; color: #94a3b8; letter-spacing: 3px; text-transform: uppercase;'>Innovation Meets Excellence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["🏠 Home", "💼 Jobs", "📝 Apply", "ℹ️ About", "📧 Contact", "🎮 Fun Zone"],
            icons=["house-fill", "briefcase-fill", "pencil-square", "info-circle-fill", "envelope-fill", "controller"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background": "transparent"},
                "icon": {"font-size": "18px"},
                "nav-link": {
                    "font-size": "15px", "padding": "14px", "border-radius": "12px",
                    "margin": "6px 0", "font-weight": "600", "letter-spacing": "0.5px"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(79,70,229,0.6), rgba(124,58,237,0.6))",
                    "font-weight": "800", "box-shadow": "0 5px 20px rgba(79,70,229,0.3)"
                },
            }
        )
        
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);'>
            <p style='font-size: 13px; color: #94a3b8; margin: 5px 0;'>📍 Eruthoorkadai</p>
            <p style='font-size: 13px; color: #94a3b8; margin: 5px 0;'>📧 altraresearch@gmail.com</p>
            <p style='font-size: 13px; color: #94a3b8; margin: 5px 0;'>📞 +91 98765 43210</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Page routing
    if selected == "🏠 Home":
        home_page()
    elif selected == "💼 Jobs":
        jobs_page()
    elif selected == "📝 Apply":
        apply_page()
    elif selected == "ℹ️ About":
        about_page()
    elif selected == "📧 Contact":
        contact_page()
    elif selected == "🎮 Fun Zone":
        fun_zone_page()

# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
def home_page():
    # Hero Section
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 🚀 WE ARE HIRING!")
        st.markdown("<h1 style='font-size: 48px;'>Build The Future<br>With <span class='shimmer-text'>Altra Research</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px; color: #cbd5e1;'>Join a team of passionate innovators shaping tomorrow's technology in Eruthoorkadai.</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 EXPLORE CAREERS", use_container_width=True, key="h_careers"):
                st.session_state.selected = "💼 Jobs"
                st.rerun()
        with c2:
            if st.button("📝 APPLY NOW", use_container_width=True, key="h_apply"):
                st.session_state.selected = "📝 Apply"
                st.rerun()
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); border-radius: 24px; padding: 40px 20px; 
                    text-align: center; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(20px);'>
            <div class='float-animation' style='font-size: 120px;'>🏢</div>
            <h3 style='font-size: 22px; margin: 20px 0 10px;'>Your Dream Career</h3>
            <p style='color: #94a3b8;'>500+ Projects | 150+ Team | 50+ Roles</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Daily Tip
    tip = get_daily_tip()
    st.info(tip)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Stats
    st.markdown("<h2 style='text-align: center;'>Our Impact</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Projects", "500+", "Completed")
    with c2:
        st.metric("Team", "150+", "Members")
    with c3:
        st.metric("Positions", "50+", "Open")
    with c4:
        st.metric("Countries", "20+", "Global")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Features with hover effect
    st.markdown("<h2 style='text-align: center;'>Why Join Us?</h2>", unsafe_allow_html=True)
    
    features = [
        {"icon": "🚀", "title": "Innovation First", "desc": "Cutting-edge projects pushing tech boundaries."},
        {"icon": "📈", "title": "Career Growth", "desc": "Clear paths with mentorship and learning."},
        {"icon": "🤝", "title": "Great Culture", "desc": "Inclusive, collaborative environment."},
        {"icon": "💎", "title": "Top Benefits", "desc": "Competitive salary, insurance, bonuses."},
        {"icon": "🌍", "title": "Global Impact", "desc": "Impact users across 20+ countries."},
        {"icon": "⚖️", "title": "Work Balance", "desc": "Flexible hours and remote options."}
    ]
    
    cols = st.columns(3)
    for idx, f in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='glass-card' style='margin: 10px 0;'>
                <div style='font-size: 50px; text-align: center; margin-bottom: 15px;'>{f['icon']}</div>
                <h3 style='text-align: center; font-size: 20px;'>{f['title']}</h3>
                <p style='text-align: center; color: #cbd5e1;'>{f['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, rgba(79,70,229,0.2), rgba(124,58,237,0.2)); 
                border-radius: 24px; border: 1px solid rgba(255,255,255,0.1);'>
        <h2>Ready to Make History?</h2>
        <p style='color: #cbd5e1; font-size: 18px;'>Join us and be part of something extraordinary</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔥 VIEW ALL POSITIONS", use_container_width=True, key="cta"):
        st.session_state.selected = "💼 Jobs"
        st.rerun()

# ═══════════════════════════════════════════════
# JOBS PAGE
# ═══════════════════════════════════════════════
def jobs_page():
    st.markdown("<h2 style='text-align: center;'>💼 Open Positions</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Find your perfect role at Altra Research</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Job title or skill...")
    with col2:
        dept = st.selectbox("Department", ["All", "Research", "Development", "Design", "Marketing", "HR"])
    with col3:
        jtype = st.selectbox("Type", ["All", "Full-Time", "Part-Time", "Remote", "Contract"])
    
    jobs = [
        {"title": "Senior Research Scientist", "dept": "Research", "type": "Full-Time", "exp": "5-8 Years",
         "desc": "Lead AI and ML research initiatives. Develop innovative algorithms.", "skills": "Python, TensorFlow, PyTorch", "salary": "₹15-25 LPA"},
        {"title": "Full Stack Developer", "dept": "Development", "type": "Full-Time", "exp": "3-5 Years",
         "desc": "Build scalable web applications with modern tech stack.", "skills": "React, Node.js, Python, AWS", "salary": "₹12-20 LPA"},
        {"title": "UI/UX Designer", "dept": "Design", "type": "Remote", "exp": "2-4 Years",
         "desc": "Create beautiful, intuitive interfaces. Conduct user research.", "skills": "Figma, Adobe XD, Prototyping", "salary": "₹8-15 LPA"},
        {"title": "Data Analyst", "dept": "Research", "type": "Full-Time", "exp": "2-5 Years",
         "desc": "Transform data into insights. Build dashboards and reports.", "skills": "SQL, Python, Power BI", "salary": "₹10-18 LPA"},
        {"title": "Marketing Lead", "dept": "Marketing", "type": "Full-Time", "exp": "4-7 Years",
         "desc": "Drive marketing campaigns and brand growth strategies.", "skills": "Digital Marketing, SEO, Analytics", "salary": "₹12-22 LPA"},
        {"title": "HR Business Partner", "dept": "HR", "type": "Full-Time", "exp": "3-6 Years",
         "desc": "Shape culture and drive talent strategy across the organization.", "skills": "Recruitment, HR Analytics", "salary": "₹8-14 LPA"}
    ]
    
    filtered = jobs
    if search:
        filtered = [j for j in filtered if search.lower() in j['title'].lower() or search.lower() in j['skills'].lower()]
    if dept != "All":
        filtered = [j for j in filtered if j['dept'] == dept]
    if jtype != "All":
        filtered = [j for j in filtered if j['type'] == jtype]
    
    if not filtered:
        st.warning("No positions found. Try different filters.")
    
    for idx, job in enumerate(filtered):
        st.markdown(f"""
        <div class='neon-card' style='margin: 15px 0; animation-delay: {idx * 0.1}s;'>
            <h3>{job['title']}</h3>
            <p style='color: #a78bfa;'>Altra Research • Eruthoorkadai</p>
            <p style='color: #cbd5e1;'>{job['desc']}</p>
            <p style='color: #94a3b8;'>
                📍 {job['dept']} | ⏰ {job['type']} | 💼 {job['exp']} | 💰 {job['salary']}
            </p>
            <p style='color: #60a5fa;'><strong>Skills:</strong> {job['skills']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"⚡ Apply for {job['title']}", key=f"apply_{idx}"):
            st.session_state['apply_position'] = job['title']
            st.session_state.selected = "📝 Apply"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# APPLY PAGE
# ═══════════════════════════════════════════════
def apply_page():
    st.markdown("<h2 style='text-align: center;'>📝 Job Application</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Take the first step toward an amazing career</p>", unsafe_allow_html=True)
    
    st.markdown("**Application Progress**")
    progress_bar = st.progress(0)
    
    with st.form("app_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email *", placeholder="your@email.com")
            phone = st.text_input("Phone *", placeholder="+91 9876543210")
        
        with col2:
            positions = ["Select", "Senior Research Scientist", "Full Stack Developer",
                        "UI/UX Designer", "Data Analyst", "Marketing Lead", "HR Business Partner"]
            default_pos = st.session_state.get('apply_position', 'Select')
            default_idx = positions.index(default_pos) if default_pos in positions else 0
            
            position = st.selectbox("Position *", positions, index=default_idx)
            experience = st.number_input("Experience (Years) *", 0, 30, 0)
            education = st.selectbox("Education *", ["Select", "High School", "Bachelor's", "Master's", "PhD", "Other"])
        
        skills = st.text_input("Key Skills *", placeholder="Python, React, SQL...")
        cover_letter = st.text_area("Cover Letter", placeholder="Tell us about yourself...", height=150)
        resume = st.file_uploader("Upload Resume", type=['pdf', 'doc', 'docx'])
        
        fields = sum([bool(full_name), bool(email), bool(phone), position != "Select",
                     experience >= 0, education != "Select", bool(skills)])
        progress_bar.progress(fields / 7)
        
        submitted = st.form_submit_button("🚀 SUBMIT APPLICATION")
        
        if submitted:
            errors = []
            if not full_name: errors.append("Name required")
            if not email or not is_valid_email(email): errors.append("Valid email required")
            if not phone or not is_valid_phone(phone): errors.append("Valid phone required")
            if position == "Select": errors.append("Position required")
            if education == "Select": errors.append("Education required")
            if not skills: errors.append("Skills required")
            
            if errors:
                for e in errors:
                    st.error(f"❌ {e}")
            else:
                save_application({
                    'full_name': full_name, 'email': email, 'phone': phone,
                    'position': position, 'experience': experience,
                    'education': education, 'skills': skills, 'cover_letter': cover_letter
                })
                st.success("✅ Application Submitted Successfully!")
                st.markdown("<p style='color: #d1fae5;'>Thank you for applying to <strong>Altra Research</strong>. We'll respond within 5-7 business days.</p>", unsafe_allow_html=True)
                st.markdown("<p style='color: #a7f3d0;'>📧 Contact: altraresearch@gmail.com</p>", unsafe_allow_html=True)
                st.balloons()
                time.sleep(0.5)
                st.snow()

# ═══════════════════════════════════════════════
# ABOUT PAGE
# ═══════════════════════════════════════════════
def about_page():
    st.markdown("<h2 style='text-align: center;'>ℹ️ About Altra Research</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs(["📖 Our Story", "💎 Values", "📅 Timeline", "🌟 Achievements"])
    
    with tabs[0]:
        st.markdown("### Our Journey")
        st.markdown("""
        <p style='color: #e2e8f0; font-size: 17px; line-height: 1.8;'>
        Founded in <strong style='color: #a78bfa;'>2015</strong> in the innovation hub of 
        <strong style='color: #60a5fa;'>Eruthoorkadai</strong>, Altra Research began as a small team 
        with a big vision. Today, we're a leading research and development powerhouse with 
        <strong style='color: #f472b6;'>150+ brilliant minds</strong> working on technologies 
        that shape the future.
        </p>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("### Our Values")
        values = [
            ("🎯", "Innovation", "We challenge conventions and think differently"),
            ("🤝", "Integrity", "We do what's right, always"),
            ("👥", "Collaboration", "Together we achieve the impossible"),
            ("⭐", "Excellence", "We strive for greatness in everything")
        ]
        for icon, title, desc in values:
            st.markdown(f"""
            <div class='glass-card' style='margin: 10px 0; padding: 20px;'>
                <span style='font-size: 30px;'>{icon}</span>
                <strong style='color: #a78bfa; font-size: 18px;'> {title}</strong>
                <p style='color: #cbd5e1; margin-top: 5px;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("### Our Timeline")
        timeline = [
            ("2015", "Founded in Eruthoorkadai"),
            ("2017", "Grew to 50+ employees"),
            ("2019", "Expanded internationally"),
            ("2021", "Launched AI Research Division"),
            ("2023", "500+ projects delivered"),
            ("2025", "150+ employees and growing")
        ]
        for year, event in timeline:
            st.markdown(f"""
            <div style='display: flex; align-items: center; margin: 15px 0;'>
                <div style='background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #fff; 
                            padding: 10px 20px; border-radius: 50px; font-weight: 800; min-width: 80px; text-align: center;'>
                    {year}
                </div>
                <p style='margin-left: 20px; color: #e2e8f0; font-size: 16px;'>{event}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("### Our Achievements")
        achievements = [
            "🏆 Best Research Company 2023",
            "🌟 Innovation Excellence Award 2022",
            "👥 Great Place to Work Certified",
            "🌍 Top 50 Global Research Firms",
            "💡 500+ Successful Projects",
            "📈 98% Client Satisfaction Rate"
        ]
        for ach in achievements:
            st.markdown(f"""
            <div class='neon-card' style='margin: 10px 0; padding: 15px;'>
                <p style='color: #fbbf24; font-size: 18px; font-weight: 600;'>{ach}</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# CONTACT PAGE
# ═══════════════════════════════════════════════
def contact_page():
    st.markdown("<h2 style='text-align: center;'>📧 Contact Us</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>We'd love to hear from you!</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Reach Us")
        
        contacts = [
            ("📍", "Address", "123 Research Park, Eruthoorkadai, Tamil Nadu - 627001"),
            ("📧", "Email", "altraresearch@gmail.com"),
            ("📞", "Phone", "+91 98765 43210"),
            ("🕐", "Hours", "Mon-Fri, 9 AM - 6 PM")
        ]
        
        for icon, label, value in contacts:
            st.markdown(f"""
            <div class='glass-card' style='margin: 10px 0; padding: 15px;'>
                <span style='font-size: 30px;'>{icon}</span>
                <strong style='color: #a78bfa; font-size: 16px;'> {label}</strong>
                <p style='color: #e2e8f0; margin: 5px 0 0 40px;'>{value}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💬 Send Message")
        with st.form("contact"):
            name = st.text_input("Name *")
            email = st.text_input("Email *")
            subject = st.text_input("Subject")
            message = st.text_area("Message *", height=150)
            
            if st.form_submit_button("📨 SEND MESSAGE"):
                if name and email and message:
                    if is_valid_email(email):
                        conn = sqlite3.connect('altra_research.db')
                        c = conn.cursor()
                        c.execute('INSERT INTO messages (name, email, subject, message, date) VALUES (?, ?, ?, ?, ?)',
                                 (name, email, subject, message, datetime.now()))
                        conn.commit()
                        conn.close()
                        st.success("✅ Message sent! We'll respond within 24 hours.")
                        st.balloons()
                    else:
                        st.error("❌ Invalid email address")
                else:
                    st.error("❌ Please fill all required fields")

# ═══════════════════════════════════════════════
# FUN ZONE PAGE
# ═══════════════════════════════════════════════
def fun_zone_page():
    st.markdown("<h2 style='text-align: center;'>🎮 Fun Zone</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Take a break and have some fun!</p>", unsafe_allow_html=True)
    
    tabs = st.tabs(["🎯 Click Game", "💡 Career Tips", "🎨 Inspirations", "🔮 Fortune"])
    
    with tabs[0]:
        mini_game()
    
    with tabs[1]:
        st.markdown("### 💡 Career Tips & Tricks")
        for i in range(5):
            st.markdown(f"""
            <div class='glass-card' style='margin: 10px 0; padding: 20px;'>
                <p style='color: #fbbf24; font-size: 17px;'>{get_daily_tip()}</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("🔄 Refresh Tips", use_container_width=True):
            st.rerun()
    
    with tabs[2]:
        st.markdown("### 🎨 Daily Inspiration")
        quotes = [
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
            ("Your work is going to fill a large part of your life.", "Steve Jobs"),
        ]
        quote, author = random.choice(quotes)
        st.markdown(f"""
        <div class='neon-card' style='text-align: center; padding: 40px;'>
            <p style='font-size: 24px; color: #fbbf24; font-style: italic;'>"{quote}"</p>
            <p style='color: #a78bfa; font-size: 18px; margin-top: 20px;'>— {author}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 New Quote", use_container_width=True):
            st.rerun()
    
    with tabs[3]:
        st.markdown("### 🔮 Career Fortune Cookie")
        fortunes = [
            "🌟 A great opportunity is heading your way!",
            "💎 Your skills will open unexpected doors.",
            "🚀 This month brings career advancement.",
            "⭐ A mentor will appear in your life soon.",
            "🎯 Your dream job is closer than you think.",
            "💪 Hard work will pay off in amazing ways.",
            "🌈 A positive change is coming to your career.",
            "🔥 Your passion will lead to success."
        ]
        
        if st.button("🥠 OPEN FORTUNE COOKIE", use_container_width=True):
            fortune = random.choice(fortunes)
            st.markdown(f"""
            <div class='neon-card' style='text-align: center; padding: 40px; margin-top: 20px;'>
                <div style='font-size: 80px; animation: float 2s ease-in-out infinite;'>🥠</div>
                <p style='font-size: 22px; color: #fbbf24; margin-top: 20px;'>{fortune}</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()

# ═══════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    main()