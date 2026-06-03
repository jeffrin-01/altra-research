"""
╔══════════════════════════════════════════════════════════════╗
║           ALTRA RESEARCH - Job Application Portal           ║
║              Location: Eruthoorkadai, Tamil Nadu            ║
║              Contact: altraresearch@gmail.com               ║
║              Phone: +91 98765 43210                         ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import sqlite3
import re
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import requests
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
# ULTIMATE CSS - MAXIMUM VISIBILITY & DESIGN
# ═══════════════════════════════════════════════
def load_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800;900&display=swap');
    
    /* ── GLOBAL RESET ── */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* ── APP BACKGROUND ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d1230 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* ── MAIN SCROLLBAR ── */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f3a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4f46e5, #7c3aed);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
    }
    
    /* ── MAIN CONTAINER ── */
    .main-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.1);
        margin: 25px 0;
        animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(60px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.3); }
        50% { box-shadow: 0 0 40px rgba(124, 58, 237, 0.5); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    @keyframes borderGlow {
        0%, 100% { border-color: #4f46e5; box-shadow: 0 0 15px rgba(79, 70, 229, 0.3); }
        50% { border-color: #7c3aed; box-shadow: 0 0 30px rgba(124, 58, 237, 0.5); }
    }
    
    /* ── HERO SECTION ── */
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: #ffffff;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    
    .hero-title {
        font-size: 56px !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        line-height: 1.1 !important;
        margin-bottom: 20px !important;
    }
    
    .hero-title-gradient {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 20px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        line-height: 1.6 !important;
    }
    
    /* ── STAT CARDS ── */
    .stat-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #a855f7);
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(79, 70, 229, 0.2);
        border-color: #4f46e5;
        animation: borderGlow 2s infinite;
    }
    
    .stat-number {
        font-size: 48px !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        margin: 10px 0 !important;
    }
    
    .stat-label {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* ── FEATURE CARDS ── */
    .feature-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 35px 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 60px rgba(79, 70, 229, 0.25);
        border-color: #4f46e5;
    }
    
    .feature-icon {
        font-size: 60px;
        margin-bottom: 20px;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-bottom: 12px !important;
    }
    
    .feature-desc {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #64748b !important;
        line-height: 1.7 !important;
    }
    
    /* ── JOB CARDS ── */
    .job-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        border-left: 6px solid #4f46e5;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .job-card::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, rgba(79,70,229,0.05), rgba(124,58,237,0.05));
        border-radius: 0 0 0 100%;
    }
    
    .job-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 60px rgba(79, 70, 229, 0.25);
        border-left: 6px solid #7c3aed;
        border-color: #4f46e5;
    }
    
    .job-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-bottom: 10px !important;
    }
    
    .job-company {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #4f46e5 !important;
        margin-bottom: 12px !important;
    }
    
    .job-desc {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        line-height: 1.8 !important;
        margin: 15px 0 !important;
    }
    
    /* ── BADGES ── */
    .badge {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 700;
        margin: 5px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: #ffffff;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #059669, #10b981);
        color: #ffffff;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #d97706, #f59e0b);
        color: #ffffff;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #0284c7, #38bdf8);
        color: #ffffff;
    }
    
    .badge-purple {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: #ffffff;
    }
    
    /* ── BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 16px 35px !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
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
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.5) !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    }
    
    .stButton > button:hover::before {
        width: 400px;
        height: 400px;
    }
    
    /* ── FORM INPUTS ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: 12px !important;
        border: 2.5px solid #cbd5e1 !important;
        padding: 14px 18px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #0f172a !important;
        background-color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #4f46e5 !important;
        border-width: 3px !important;
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1) !important;
        outline: none !important;
    }
    
    /* ── LABELS ── */
    .stTextInput label, 
    .stTextArea label, 
    .stSelectbox label, 
    .stNumberInput label {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #1e293b !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    
    /* ── SUCCESS MESSAGE ── */
    .success-box {
        background: linear-gradient(135deg, #059669, #10b981);
        color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #047857;
        margin: 20px 0;
        box-shadow: 0 15px 40px rgba(5, 150, 105, 0.3);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .success-box h2 {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        margin-bottom: 15px !important;
    }
    
    .success-box p {
        color: #ecfdf5 !important;
        font-size: 17px !important;
        font-weight: 500 !important;
    }
    
    /* ── ERROR MESSAGE ── */
    .error-box {
        background: #dc2626;
        color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #991b1b;
        margin: 15px 0;
        font-size: 16px;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
        animation: shake 0.5s ease-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-15px); }
        40% { transform: translateX(15px); }
        60% { transform: translateX(-10px); }
        80% { transform: translateX(10px); }
    }
    
    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1040 50%, #0d1230 100%) !important;
        border-right: 2px solid rgba(255,255,255,0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 28px !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        font-size: 14px !important;
        color: #cbd5e1 !important;
    }
    
    /* ── PROGRESS BAR ── */
    .stProgress > div {
        background: #e2e8f0 !important;
        border-radius: 20px !important;
        height: 10px !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #a855f7) !important;
        border-radius: 20px !important;
        height: 10px !important;
        animation: shimmer 2s linear infinite;
        background-size: 200% auto;
    }
    
    /* ── SECTION DIVIDERS ── */
    .section-divider {
        height: 4px;
        background: linear-gradient(90deg, transparent, #4f46e5, #7c3aed, #a855f7, transparent);
        border-radius: 2px;
        margin: 40px 0;
    }
    
    /* ── GLOW CARD ── */
    .glow-card {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border-radius: 20px;
        padding: 40px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        animation: glow 3s infinite;
    }
    
    /* ── TIMELINE ── */
    .timeline-item {
        display: flex;
        align-items: center;
        margin: 25px 0;
        padding: 20px;
        background: #ffffff;
        border-radius: 15px;
        border-left: 5px solid #4f46e5;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .timeline-item:hover {
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.15);
    }
    
    .timeline-year {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: #ffffff;
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 18px;
        min-width: 100px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.3);
    }
    
    .timeline-text {
        margin-left: 25px;
        font-size: 18px;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* ── CONTACT INFO CARD ── */
    .contact-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .contact-card:hover {
        border-color: #4f46e5;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.15);
        transform: translateX(5px);
    }
    
    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 36px !important;
        }
        
        .hero-subtitle {
            font-size: 16px !important;
        }
        
        .main-container {
            padding: 20px;
            margin: 10px;
        }
        
        .stat-number {
            font-size: 32px !important;
        }
        
        .job-card {
            padding: 20px;
        }
        
        .stButton > button {
            width: 100%;
            padding: 14px 25px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════
def init_database():
    conn = sqlite3.connect('altra_research.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  full_name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  position TEXT NOT NULL,
                  experience INTEGER,
                  education TEXT,
                  skills TEXT,
                  cover_letter TEXT,
                  applied_date TIMESTAMP,
                  status TEXT DEFAULT 'Pending')''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  subject TEXT,
                  message TEXT,
                  date TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def save_application(data):
    conn = sqlite3.connect('altra_research.db')
    c = conn.cursor()
    c.execute('''INSERT INTO applications 
                 (full_name, email, phone, position, experience, education, skills, cover_letter, applied_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['full_name'], data['email'], data['phone'], data['position'],
               data['experience'], data['education'], data['skills'], data['cover_letter'],
               datetime.now()))
    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
def main():
    load_css()
    init_database()
    
    # SIDEBAR
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 30px 15px;'>
            <div style='font-size: 60px; margin-bottom: 15px;'>🔬</div>
            <h1 style='font-size: 26px; font-weight: 900; margin-bottom: 5px; letter-spacing: 2px;'>
                ALTRA RESEARCH
            </h1>
            <p style='font-size: 13px; color: #94a3b8; font-weight: 500; letter-spacing: 3px; text-transform: uppercase;'>
                Innovation Meets Excellence
            </p>
            <div style='height: 3px; background: linear-gradient(90deg, #4f46e5, #7c3aed, #a855f7); 
                        margin: 25px 0; border-radius: 3px;'></div>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["🏠 HOME", "💼 OPEN POSITIONS", "📝 APPLY NOW", "ℹ️ ABOUT US", "📧 CONTACT"],
            icons=["house-fill", "briefcase-fill", "pencil-square", "info-circle-fill", "envelope-fill"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"font-size": "18px", "color": "#ffffff"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "8px 0",
                    "padding": "14px 18px",
                    "border-radius": "12px",
                    "color": "#ffffff",
                    "font-weight": "600",
                    "letter-spacing": "0.5px"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(79,70,229,0.4), rgba(124,58,237,0.4))",
                    "font-weight": "800",
                    "border": "1px solid rgba(255,255,255,0.2)"
                },
            }
        )
        
        st.markdown("""
        <div style='margin-top: 40px; padding-top: 25px; border-top: 2px solid rgba(255,255,255,0.15);'>
            <div style='display: flex; align-items: center; margin: 15px 0;'>
                <span style='font-size: 20px; margin-right: 10px;'>📍</span>
                <span style='font-size: 13px; font-weight: 500; color: #cbd5e1;'>Eruthoorkadai, Tamil Nadu</span>
            </div>
            <div style='display: flex; align-items: center; margin: 15px 0;'>
                <span style='font-size: 20px; margin-right: 10px;'>📧</span>
                <span style='font-size: 13px; font-weight: 500; color: #cbd5e1;'>altraresearch@gmail.com</span>
            </div>
            <div style='display: flex; align-items: center; margin: 15px 0;'>
                <span style='font-size: 20px; margin-right: 10px;'>📞</span>
                <span style='font-size: 13px; font-weight: 500; color: #cbd5e1;'>+91 98765 43210</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # PAGE ROUTING
    if selected == "🏠 HOME":
        home_page()
    elif selected == "💼 OPEN POSITIONS":
        jobs_page()
    elif selected == "📝 APPLY NOW":
        apply_page()
    elif selected == "ℹ️ ABOUT US":
        about_page()
    elif selected == "📧 CONTACT":
        contact_page()

# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
def home_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<span class="hero-badge">🚀 We Are Hiring!</span>', unsafe_allow_html=True)
        st.markdown("""
        <h1 class='hero-title'>
            Build The Future<br>
            With <span class='hero-title-gradient'>Altra Research</span>
        </h1>
        <p class='hero-subtitle'>
            Join a team of passionate innovators shaping tomorrow's technology. 
            Located in the heart of Eruthoorkadai, we're revolutionizing research 
            and development through cutting-edge innovation.
        </p>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 EXPLORE CAREERS", use_container_width=True, key="home_explore"):
                st.session_state.selected = "💼 OPEN POSITIONS"
                st.rerun()
        with col_b:
            if st.button("📝 APPLY NOW", use_container_width=True, key="home_apply"):
                st.session_state.selected = "📝 APPLY NOW"
                st.rerun()
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(79,70,229,0.05), rgba(124,58,237,0.05)); 
                    border-radius: 24px; border: 2px solid rgba(79,70,229,0.1);'>
            <div style='font-size: 150px; animation: float 4s ease-in-out infinite;'>🏢</div>
            <h3 style='font-size: 22px; font-weight: 700; color: #1e293b; margin-top: 20px;'>Your Dream Career Awaits</h3>
            <p style='font-size: 16px; color: #64748b; font-weight: 500;'>500+ Projects | 150+ Team Members | 50+ Open Roles</p>
        </div>
        """, unsafe_allow_html=True)
    
    # STATS
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>500+</div>
            <div class='stat-label'>Projects Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>150+</div>
            <div class='stat-label'>Team Members</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>50+</div>
            <div class='stat-label'>Open Positions</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>20+</div>
            <div class='stat-label'>Countries</div>
        </div>
        """, unsafe_allow_html=True)
    
    # FEATURES
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 36px; font-weight: 900; color: #0f172a; margin: 40px 0;'>Why Choose Altra Research?</h2>", unsafe_allow_html=True)
    
    features = [
        {"icon": "🚀", "title": "Innovation First", "desc": "Push boundaries with cutting-edge projects that redefine technology and science."},
        {"icon": "📈", "title": "Career Growth", "desc": "Clear advancement paths, mentorship programs, and continuous learning opportunities."},
        {"icon": "🤝", "title": "Amazing Culture", "desc": "Inclusive, diverse, and collaborative environment where every voice matters."},
        {"icon": "💎", "title": "Top Benefits", "desc": "Competitive salary, health insurance, stock options, and performance bonuses."},
        {"icon": "🌍", "title": "Global Impact", "desc": "Your work will impact millions of users across 20+ countries worldwide."},
        {"icon": "⚖️", "title": "Work-Life Balance", "desc": "Flexible hours, remote options, and generous PTO to keep you at your best."}
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='feature-card' style='animation-delay: {idx * 0.1}s;'>
                <span class='feature-icon'>{feature['icon']}</span>
                <h3 class='feature-title'>{feature['title']}</h3>
                <p class='feature-desc'>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style='text-align: center; margin: 50px 0; padding: 60px 40px; 
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
                border-radius: 24px; box-shadow: 0 25px 60px rgba(79,70,229,0.3);'>
        <h2 style='font-size: 36px; font-weight: 900; color: #ffffff; margin-bottom: 15px;'>
            Ready to Make History?
        </h2>
        <p style='font-size: 20px; font-weight: 500; color: #e0e7ff; margin-bottom: 30px;'>
            Join us and be part of something extraordinary
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🔥 VIEW ALL OPEN POSITIONS", use_container_width=True, key="cta_explore"):
            st.session_state.selected = "💼 OPEN POSITIONS"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# JOBS PAGE
# ═══════════════════════════════════════════════
def jobs_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <span class='hero-badge'>💼 Career Opportunities</span>
        <h1 style='font-size: 40px; font-weight: 900; color: #0f172a; margin: 20px 0 10px;'>
            Find Your Perfect Role
        </h1>
        <p style='font-size: 18px; color: #64748b; font-weight: 500;'>
            Discover opportunities that match your skills and passion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 SEARCH POSITIONS", placeholder="Job title, skill, or keyword...")
    with col2:
        department = st.selectbox("📂 DEPARTMENT", ["All", "Research", "Development", "Design", "Marketing", "HR"])
    with col3:
        job_type = st.selectbox("⏰ JOB TYPE", ["All", "Full-Time", "Part-Time", "Remote", "Contract"])
    
    jobs = [
        {
            "title": "Senior Research Scientist",
            "dept": "Research",
            "type": "Full-Time",
            "exp": "5-8 Years",
            "desc": "Lead groundbreaking research initiatives in Artificial Intelligence and Machine Learning. Develop innovative algorithms that solve real-world problems.",
            "skills": ["Python", "TensorFlow", "PyTorch", "Deep Learning"],
            "salary": "₹15-25 LPA"
        },
        {
            "title": "Full Stack Developer",
            "dept": "Development",
            "type": "Full-Time",
            "exp": "3-5 Years",
            "desc": "Design and build scalable web applications using cutting-edge technologies. Work across the entire stack from database to user interface.",
            "skills": ["React", "Node.js", "Python", "AWS", "Docker"],
            "salary": "₹12-20 LPA"
        },
        {
            "title": "UI/UX Designer",
            "dept": "Design",
            "type": "Remote",
            "exp": "2-4 Years",
            "desc": "Create stunning, intuitive interfaces that delight users. Conduct research, prototyping, and testing to deliver exceptional experiences.",
            "skills": ["Figma", "Adobe XD", "Prototyping", "User Research"],
            "salary": "₹8-15 LPA"
        },
        {
            "title": "Data Analyst",
            "dept": "Research",
            "type": "Full-Time",
            "exp": "2-5 Years",
            "desc": "Transform raw data into actionable insights. Build dashboards and reports that drive strategic business decisions.",
            "skills": ["SQL", "Python", "Power BI", "Statistics", "Excel"],
            "salary": "₹10-18 LPA"
        },
        {
            "title": "Marketing Lead",
            "dept": "Marketing",
            "type": "Full-Time",
            "exp": "4-7 Years",
            "desc": "Spearhead marketing campaigns that amplify our brand. Drive growth through digital strategies and creative storytelling.",
            "skills": ["Digital Marketing", "SEO/SEM", "Content Strategy", "Analytics"],
            "salary": "₹12-22 LPA"
        },
        {
            "title": "HR Business Partner",
            "dept": "HR",
            "type": "Full-Time",
            "exp": "3-6 Years",
            "desc": "Shape our company culture and drive talent strategy. Partner with leadership to build high-performing teams.",
            "skills": ["Talent Acquisition", "Employee Relations", "HR Analytics"],
            "salary": "₹8-14 LPA"
        }
    ]
    
    filtered = jobs
    if search:
        filtered = [j for j in filtered if search.lower() in j['title'].lower() 
                    or search.lower() in j['desc'].lower()
                    or any(search.lower() in s.lower() for s in j['skills'])]
    if department != "All":
        filtered = [j for j in filtered if j['dept'] == department]
    if job_type != "All":
        filtered = [j for j in filtered if j['type'] == job_type]
    
    if not filtered:
        st.warning("😔 No positions match your criteria. Try adjusting your filters!")
    
    for idx, job in enumerate(filtered):
        st.markdown(f"""
        <div class='job-card' style='animation-delay: {idx * 0.1}s;'>
            <div style='display: flex; justify-content: space-between; flex-wrap: wrap; gap: 20px;'>
                <div style='flex: 2; min-width: 300px;'>
                    <h3 class='job-title'>{job['title']}</h3>
                    <p class='job-company'>Altra Research • Eruthoorkadai</p>
                    <p class='job-desc'>{job['desc']}</p>
                    <div style='margin: 15px 0;'>
                        <span class='badge badge-primary'>📍 {job['dept']}</span>
                        <span class='badge badge-success'>⏰ {job['type']}</span>
                        <span class='badge badge-warning'>💼 {job['exp']}</span>
                        <span class='badge badge-purple'>💰 {job['salary']}</span>
                    </div>
                </div>
                <div style='flex: 1; min-width: 220px; background: #f8fafc; padding: 20px; 
                            border-radius: 15px; border: 1px solid #e2e8f0;'>
                    <p style='font-size: 14px; font-weight: 700; color: #4f46e5; margin-bottom: 10px;'>
                        🎯 REQUIRED SKILLS
                    </p>
                    <div style='line-height: 2.2;'>
                        {''.join([f'<span class="badge badge-info" style="margin:3px;">{skill}</span>' for skill in job['skills']])}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"⚡ APPLY FOR {job['title'].upper()}", key=f"apply_btn_{idx}", use_container_width=True):
            st.session_state['apply_position'] = job['title']
            st.session_state.selected = "📝 APPLY NOW"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# APPLY PAGE
# ═══════════════════════════════════════════════
def apply_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <span class='hero-badge'>📝 Join Our Team</span>
        <h1 style='font-size: 38px; font-weight: 900; color: #0f172a; margin: 20px 0 10px;'>
            Application Form
        </h1>
        <p style='font-size: 18px; color: #64748b; font-weight: 500;'>
            Take the first step towards an amazing career
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 10px;'>📊 APPLICATION PROGRESS</p>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    
    with st.form("application_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("👤 FULL NAME *", placeholder="John Doe")
            email = st.text_input("📧 EMAIL ADDRESS *", placeholder="john@example.com")
            phone = st.text_input("📞 PHONE NUMBER *", placeholder="+91 9876543210")
            
        with col2:
            positions_list = ["Select Position", "Senior Research Scientist", "Full Stack Developer",
                            "UI/UX Designer", "Data Analyst", "Marketing Lead", "HR Business Partner"]
            default_pos = st.session_state.get('apply_position', 'Select Position')
            default_idx = positions_list.index(default_pos) if default_pos in positions_list else 0
            
            position = st.selectbox("💼 POSITION *", positions_list, index=default_idx)
            experience = st.number_input("⏳ YEARS OF EXPERIENCE *", 0, 30, 0)
            education = st.selectbox("🎓 HIGHEST EDUCATION *", 
                                    ["Select", "High School", "Bachelor's", "Master's", "PhD", "Other"])
        
        skills = st.text_input("🎯 KEY SKILLS * (comma separated)", placeholder="Python, Machine Learning, React, SQL...")
        cover_letter = st.text_area("✍️ COVER LETTER", placeholder="Tell us why you'd be perfect for this role...", height=150)
        resume = st.file_uploader("📄 UPLOAD RESUME (PDF/DOC)", type=['pdf', 'doc', 'docx'])
        
        fields_done = sum([bool(full_name), bool(email), bool(phone), 
                          position != "Select Position", experience >= 0, 
                          education != "Select", bool(skills)])
        progress_bar.progress(fields_done / 7)
        
        submitted = st.form_submit_button("🚀 SUBMIT APPLICATION")
        
        if submitted:
            errors = []
            if not full_name: errors.append("Full name is required")
            if not email or not is_valid_email(email): errors.append("Valid email is required")
            if not phone or not is_valid_phone(phone): errors.append("Valid phone number is required")
            if position == "Select Position": errors.append("Select a position")
            if education == "Select": errors.append("Select education level")
            if not skills: errors.append("Skills are required")
            
            if errors:
                for error in errors:
                    st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
            else:
                save_application({
                    'full_name': full_name, 'email': email, 'phone': phone,
                    'position': position, 'experience': experience,
                    'education': education, 'skills': skills,
                    'cover_letter': cover_letter
                })
                
                st.markdown("""
                <div class='success-box'>
                    <h2>🎉 Application Submitted Successfully!</h2>
                    <p style='margin: 12px 0;'>Thank you for your interest in joining <strong>Altra Research</strong>.</p>
                    <p style='margin: 8px 0;'>⏰ We'll review your application and respond within <strong>5-7 business days</strong>.</p>
                    <p style='margin: 8px 0;'>📧 Questions? Contact us at <strong>altraresearch@gmail.com</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                time.sleep(0.3)
                st.snow()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# ABOUT PAGE
# ═══════════════════════════════════════════════
def about_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <span class='hero-badge'>ℹ️ Our Story</span>
        <h1 style='font-size: 38px; font-weight: 900; color: #0f172a; margin: 20px 0 10px;'>
            About Altra Research
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 10px;'>
            <h2 style='font-size: 28px; font-weight: 800; color: #4f46e5; margin-bottom: 20px;'>🚀 Our Journey</h2>
            <p style='font-size: 17px; font-weight: 500; color: #334155; line-height: 1.9;'>
                Founded in <strong>2015</strong> in the innovation hub of 
                <strong style='color: #4f46e5; background: #eef2ff; padding: 3px 10px; border-radius: 6px;'>
                Eruthoorkadai</strong>, Altra Research began as a small team with a big vision. 
                Today, we're a leading research and development powerhouse with 150+ brilliant minds 
                working on technologies that shape the future.
            </p>
            
            <h3 style='font-size: 22px; font-weight: 800; color: #0f172a; margin-top: 35px;'>💎 Our Core Values</h3>
            <div style='margin-top: 20px;'>
                <div style='margin: 15px 0; font-size: 17px; font-weight: 500; color: #334155;'>
                    <span style='font-size: 24px; margin-right: 10px;'>🎯</span>
                    <strong style='color: #4f46e5;'>Innovation</strong> — We challenge conventions and think differently
                </div>
                <div style='margin: 15px 0; font-size: 17px; font-weight: 500; color: #334155;'>
                    <span style='font-size: 24px; margin-right: 10px;'>🤝</span>
                    <strong style='color: #4f46e5;'>Integrity</strong> — We do what's right, always
                </div>
                <div style='margin: 15px 0; font-size: 17px; font-weight: 500; color: #334155;'>
                    <span style='font-size: 24px; margin-right: 10px;'>👥</span>
                    <strong style='color: #4f46e5;'>Collaboration</strong> — Together we achieve the impossible
                </div>
                <div style='margin: 15px 0; font-size: 17px; font-weight: 500; color: #334155;'>
                    <span style='font-size: 24px; margin-right: 10px;'>⭐</span>
                    <strong style='color: #4f46e5;'>Excellence</strong> — We strive for greatness in everything
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4f46e5, #7c3aed); padding: 35px; 
                    border-radius: 20px; color: #ffffff; box-shadow: 0 20px 50px rgba(79,70,229,0.3);'>
            <h2 style='font-size: 26px; font-weight: 800; color: #ffffff; margin-bottom: 30px;'>📊 Quick Facts</h2>
            
            <div style='margin: 25px 0; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 12px;'>
                <h3 style='font-size: 16px; font-weight: 700; color: #e0e7ff;'>📍 Location</h3>
                <p style='font-size: 18px; font-weight: 600; color: #ffffff;'>Eruthoorkadai, Tamil Nadu</p>
            </div>
            <div style='margin: 25px 0; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 12px;'>
                <h3 style='font-size: 16px; font-weight: 700; color: #e0e7ff;'>👥 Team Size</h3>
                <p style='font-size: 18px; font-weight: 600; color: #ffffff;'>150+ Employees</p>
            </div>
            <div style='margin: 25px 0; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 12px;'>
                <h3 style='font-size: 16px; font-weight: 700; color: #e0e7ff;'>🏆 Achievements</h3>
                <p style='font-size: 18px; font-weight: 600; color: #ffffff;'>Multiple Industry Awards</p>
            </div>
            <div style='margin: 25px 0; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 12px;'>
                <h3 style='font-size: 16px; font-weight: 700; color: #e0e7ff;'>🌍 Global Reach</h3>
                <p style='font-size: 18px; font-weight: 600; color: #ffffff;'>Clients in 20+ Countries</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; font-size: 30px; font-weight: 900; color: #0f172a; margin: 50px 0 30px;'>📅 Our Timeline</h2>", unsafe_allow_html=True)
    
    timeline = [
        ("2015", "Founded in Eruthoorkadai with a vision to revolutionize research"),
        ("2017", "Grew to 50+ team members and secured first major contract"),
        ("2019", "Expanded operations to international markets"),
        ("2021", "Launched cutting-edge AI Research Division"),
        ("2023", "Celebrated 500+ successful project deliveries"),
        ("2025", "Continuing to innovate with 150+ employees and growing")
    ]
    
    for year, event in timeline:
        st.markdown(f"""
        <div class='timeline-item'>
            <div class='timeline-year'>{year}</div>
            <div class='timeline-text'>{event}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# CONTACT PAGE
# ═══════════════════════════════════════════════
def contact_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <span class='hero-badge'>📧 Get In Touch</span>
        <h1 style='font-size: 38px; font-weight: 900; color: #0f172a; margin: 20px 0 10px;'>
            Contact Us
        </h1>
        <p style='font-size: 18px; color: #64748b; font-weight: 500;'>
            We'd love to hear from you
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h2 style='font-size: 26px; font-weight: 800; color: #4f46e5; margin-bottom: 25px;'>📍 Reach Us</h2>
        
        <div class='contact-card'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 35px; margin-right: 20px;'>📍</span>
                <div>
                    <strong style='font-size: 18px; color: #0f172a;'>Our Office</strong>
                    <p style='font-size: 16px; color: #475569; margin: 5px 0 0 0; font-weight: 500;'>
                        123 Research Park,<br>Eruthoorkadai, Tamil Nadu - 627001
                    </p>
                </div>
            </div>
        </div>
        
        <div class='contact-card'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 35px; margin-right: 20px;'>📧</span>
                <div>
                    <strong style='font-size: 18px; color: #0f172a;'>Email</strong>
                    <p style='font-size: 16px; color: #4f46e5; margin: 5px 0 0 0; font-weight: 600;'>
                        altraresearch@gmail.com
                    </p>
                </div>
            </div>
        </div>
        
        <div class='contact-card'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 35px; margin-right: 20px;'>📞</span>
                <div>
                    <strong style='font-size: 18px; color: #0f172a;'>Phone</strong>
                    <p style='font-size: 16px; color: #475569; margin: 5px 0 0 0; font-weight: 500;'>
                        +91 98765 43210
                    </p>
                </div>
            </div>
        </div>
        
        <div class='contact-card'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 35px; margin-right: 20px;'>🕐</span>
                <div>
                    <strong style='font-size: 18px; color: #0f172a;'>Working Hours</strong>
                    <p style='font-size: 16px; color: #475569; margin: 5px 0 0 0; font-weight: 500;'>
                        Monday - Friday<br>9:00 AM - 6:00 PM
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("contact_form"):
            st.markdown("<h3 style='font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 20px;'>💬 Send Message</h3>", unsafe_allow_html=True)
            
            name = st.text_input("YOUR NAME *", placeholder="John Doe")
            email = st.text_input("YOUR EMAIL *", placeholder="john@example.com")
            subject = st.text_input("SUBJECT", placeholder="How can we help?")
            message = st.text_area("YOUR MESSAGE *", placeholder="Type your message here...", height=150)
            
            submitted = st.form_submit_button("📨 SEND MESSAGE")
            
            if submitted:
                if name and email and message:
                    if is_valid_email(email):
                        conn = sqlite3.connect('altra_research.db')
                        c = conn.cursor()
                        c.execute('INSERT INTO messages (name, email, subject, message, date) VALUES (?, ?, ?, ?, ?)',
                                 (name, email, subject, message, datetime.now()))
                        conn.commit()
                        conn.close()
                        
                        st.markdown("""
                        <div class='success-box'>
                            <h3>✅ Message Sent!</h3>
                            <p>We'll respond within 24 hours.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.markdown('<div class="error-box">❌ Invalid email address</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">❌ Fill all required fields</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# RUN APP
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    main()