"""
Altra Research - Job Application Portal
Location: Eruthoorkadai
Framework: Streamlit (Free Deployment)
Contact: altraresearch@gmail.com
"""

import streamlit as st
import sqlite3
import re
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import os

# Page configuration
st.set_page_config(
    page_title="Altra Research - Careers",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - MAXIMUM VISIBILITY
def load_css():
    st.markdown("""
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Global Reset - All Text Black by Default */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main App Background - Light Gray */
    .stApp {
        background: #e8eaed;
    }
    
    /* Force ALL text to be dark */
    p, span, div, li, label, h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }
    
    /* Main Container - White */
    .main-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        margin: 20px 0;
        border: 2px solid #d1d5db;
    }
    
    /* Card Styling - High Contrast */
    .job-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        border: 2px solid #9ca3af;
        border-left: 6px solid #000000;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        border-left: 6px solid #1d4ed8;
        border-color: #1d4ed8;
    }
    
    .job-card h3 {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #000000 !important;
    }
    
    .job-card p {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        line-height: 1.8 !important;
    }
    
    .feature-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 30px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        border: 2px solid #9ca3af;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
        border-color: #1d4ed8;
    }
    
    .feature-card h2 {
        font-size: 38px !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }
    
    .feature-card h3 {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }
    
    .feature-card p {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    
    /* Button Styling - High Contrast */
    .stButton > button {
        background: #000000 !important;
        color: #ffffff !important;
        border: 3px solid #000000 !important;
        padding: 16px 35px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: #ffffff !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
    }
    
    /* Form Inputs - Clear & Visible */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 3px solid #6b7280 !important;
        padding: 14px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #000000 !important;
        background-color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #000000 !important;
        border-width: 3px !important;
        box-shadow: 0 0 0 4px rgba(0,0,0,0.1) !important;
        background-color: #f9fafb !important;
    }
    
    /* Form Labels - Big & Bold */
    .stTextInput label, 
    .stTextArea label, 
    .stSelectbox label, 
    .stNumberInput label {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        margin-bottom: 8px !important;
    }
    
    /* Placeholder Text */
    ::placeholder {
        color: #6b7280 !important;
        font-weight: 500 !important;
        font-size: 15px !important;
    }
    
    /* Success Message */
    .success-message {
        background: #000000 !important;
        color: #ffffff !important;
        padding: 25px !important;
        border-radius: 12px !important;
        border: 3px solid #000000 !important;
        margin: 20px 0 !important;
    }
    
    .success-message h2 {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
    }
    
    .success-message p {
        font-size: 17px !important;
        font-weight: 600 !important;
        color: #e5e7eb !important;
        margin: 12px 0 !important;
    }
    
    /* Error Message */
    .error-message {
        background: #dc2626 !important;
        color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 3px solid #991b1b !important;
        margin: 15px 0 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    
    /* Badge Styling */
    .badge {
        background: #000000 !important;
        color: #ffffff !important;
        padding: 8px 18px !important;
        border-radius: 25px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        display: inline-block !important;
        margin: 6px !important;
        border: 2px solid #000000 !important;
    }
    
    /* Sidebar - Dark with White Text */
    [data-testid="stSidebar"] {
        background: #000000 !important;
        border-right: 4px solid #374151 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 28px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] p {
        font-size: 15px !important;
        color: #d1d5db !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: #000000 !important;
        height: 8px !important;
        border-radius: 10px !important;
    }
    
    .stProgress > div {
        background: #d1d5db !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    
    /* Headers - Extra Bold & Large */
    h1 {
        font-size: 40px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        margin-bottom: 20px !important;
    }
    
    h2 {
        font-size: 30px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        margin-bottom: 15px !important;
    }
    
    h3 {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }
    
    /* Info Box */
    .stAlert {
        font-size: 16px !important;
        font-weight: 600 !important;
        border: 3px solid #000000 !important;
        border-radius: 10px !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        border: 3px dashed #6b7280 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #000000 !important;
        background: #f9fafb !important;
    }
    
    /* Select Box Options */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 3px solid #6b7280 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Timeline */
    .timeline-year {
        background: #000000 !important;
        color: #ffffff !important;
        padding: 12px 25px !important;
        border-radius: 25px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        min-width: 90px !important;
        text-align: center !important;
        display: inline-block !important;
    }
    
    /* Animation Keyframes */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main-container {
        animation: slideIn 0.6s ease-out;
    }
    
    /* Pulse Animation */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.4);
        }
        70% {
            transform: scale(1.03);
            box-shadow: 0 0 0 15px rgba(0, 0, 0, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
        }
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-container {
            padding: 20px;
            margin: 10px;
        }
        
        h1 {
            font-size: 28px !important;
        }
        
        h2 {
            font-size: 22px !important;
        }
        
        .stButton > button {
            width: 100%;
            padding: 14px 25px !important;
            font-size: 16px !important;
        }
        
        .job-card, .feature-card {
            padding: 15px;
            margin: 10px 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
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
                  resume TEXT,
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

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Phone validation
def is_valid_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

# Save application
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

# Main app
def main():
    load_css()
    init_database()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 30px 10px;'>
            <h1 style='font-size: 30px !important; font-weight: 900 !important; 
                       color: #ffffff !important; margin-bottom: 10px !important;'>
                🔬 ALTRA RESEARCH
            </h1>
            <p style='font-size: 16px !important; color: #d1d5db !important; 
                      font-weight: 600 !important; margin-bottom: 5px !important;'>
                Innovation Meets Excellence
            </p>
            <div style='height: 4px; background: #ffffff; margin: 25px 0; border-radius: 2px;'></div>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["🏠 Home", "💼 Jobs", "📝 Apply Now", "ℹ️ About Us", "📧 Contact"],
            icons=["house", "briefcase", "pencil-square", "info-circle", "envelope"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"font-size": "18px", "color": "#ffffff"}, 
                "nav-link": {
                    "font-size": "17px", 
                    "text-align": "left", 
                    "margin": "8px 0", 
                    "padding": "14px",
                    "border-radius": "10px",
                    "color": "#ffffff",
                    "font-weight": "600"
                },
                "nav-link-selected": {
                    "background": "rgba(255,255,255,0.25)",
                    "font-weight": "800",
                    "color": "#ffffff"
                },
            }
        )
        
        st.markdown("""
        <div style='margin-top: 30px; padding-top: 25px; border-top: 2px solid rgba(255,255,255,0.3);'>
            <p style='margin: 10px 0; font-size: 15px !important; color: #ffffff !important; font-weight: 600;'>
                📍 Eruthoorkadai
            </p>
            <p style='margin: 10px 0; font-size: 15px !important; color: #ffffff !important; font-weight: 600;'>
                📧 altraresearch@gmail.com
            </p>
            <p style='margin: 10px 0; font-size: 15px !important; color: #ffffff !important; font-weight: 600;'>
                📞 +91 98765 43210
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Page routing
    if selected == "🏠 Home":
        home_page()
    elif selected == "💼 Jobs":
        jobs_page()
    elif selected == "📝 Apply Now":
        apply_page()
    elif selected == "ℹ️ About Us":
        about_page()
    elif selected == "📧 Contact":
        contact_page()

# Home Page
def home_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h1 style='font-size: 44px !important; font-weight: 900 !important; 
                   color: #000000 !important; margin-bottom: 15px !important;'>
            Welcome to <span style='color: #1d4ed8 !important; 
            text-decoration: underline; text-underline-offset: 8px;'>Altra Research</span>
        </h1>
        <p style='font-size: 22px !important; font-weight: 700 !important; 
                  color: #374151 !important; margin: 25px 0 !important;'>
            Shaping the Future Through Innovation and Research
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='margin: 35px 0; background: #f3f4f6; padding: 25px; 
                    border-radius: 12px; border-left: 5px solid #000000;'>
            <p style='font-size: 18px !important; line-height: 1.9 !important; 
                      color: #111827 !important; font-weight: 500 !important;'>
                At Altra Research, we're not just building technology — we're building the future. 
                Located in the heart of <strong style='color: #000000 !important; 
                font-size: 19px !important;'>Eruthoorkadai</strong>, we're on a mission to 
                revolutionize research and development through cutting-edge innovation.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
            <div class='feature-card pulse'>
                <h2 style='font-size: 42px !important; font-weight: 900 !important; 
                           color: #000000 !important; margin: 0 !important;'>500+</h2>
                <p style='font-size: 17px !important; font-weight: 600 !important; 
                          color: #374151 !important; margin-top: 10px !important;'>
                    Projects Completed
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown("""
            <div class='feature-card pulse' style='animation-delay: 0.3s;'>
                <h2 style='font-size: 42px !important; font-weight: 900 !important; 
                           color: #000000 !important; margin: 0 !important;'>150+</h2>
                <p style='font-size: 17px !important; font-weight: 600 !important; 
                          color: #374151 !important; margin-top: 10px !important;'>
                    Happy Employees
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown("""
            <div class='feature-card pulse' style='animation-delay: 0.6s;'>
                <h2 style='font-size: 42px !important; font-weight: 900 !important; 
                           color: #000000 !important; margin: 0 !important;'>50+</h2>
                <p style='font-size: 17px !important; font-weight: 600 !important; 
                          color: #374151 !important; margin-top: 10px !important;'>
                    Open Positions
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 50px 20px; background: #f3f4f6; 
                    border-radius: 15px; border: 3px solid #d1d5db;'>
            <div style='font-size: 120px;'>🏢</div>
            <h3 style='font-size: 24px !important; font-weight: 800 !important; 
                       color: #000000 !important; margin-top: 25px !important;'>
                Join Our Team
            </h3>
            <p style='font-size: 17px !important; font-weight: 600 !important; 
                      color: #374151 !important;'>
                Build your career with us
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("<h2 style='text-align: center; margin: 50px 0 35px; font-size: 34px !important; font-weight: 900 !important; color: #000000 !important;'>Why Join Altra Research?</h2>", unsafe_allow_html=True)
    
    features = [
        {"icon": "🚀", "title": "Innovation First", "description": "Work on cutting-edge projects that push the boundaries of technology and science"},
        {"icon": "🌱", "title": "Growth Opportunities", "description": "Continuous learning programs, mentorship, and clear career advancement paths"},
        {"icon": "🤝", "title": "Collaborative Culture", "description": "Be part of a supportive, diverse team that values your unique ideas and contributions"},
        {"icon": "💼", "title": "Work-Life Balance", "description": "Flexible working hours, remote options, and generous paid time off policies"},
        {"icon": "🏆", "title": "Competitive Benefits", "description": "Top-tier salary packages, comprehensive health insurance, and performance bonuses"},
        {"icon": "🌍", "title": "Global Impact", "description": "Your innovations will impact millions of users and industries worldwide"}
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='feature-card' style='animation-delay: {idx * 0.1}s;'>
                <div style='font-size: 50px; margin-bottom: 15px;'>{feature['icon']}</div>
                <h3 style='font-size: 20px !important; font-weight: 800 !important; 
                           color: #000000 !important; margin-bottom: 12px !important;'>
                    {feature['title']}
                </h3>
                <p style='font-size: 16px !important; font-weight: 500 !important; 
                          color: #374151 !important; line-height: 1.7 !important;'>
                    {feature['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div style='text-align: center; margin: 50px 0; padding: 55px 30px; 
                background: #000000; border-radius: 20px; border: 3px solid #000000;'>
        <h2 style='font-size: 34px !important; font-weight: 900 !important; 
                   color: #ffffff !important; margin-bottom: 15px !important;'>
            Ready to Make an Impact?
        </h2>
        <p style='font-size: 20px !important; font-weight: 600 !important; 
                  color: #d1d5db !important; margin-bottom: 35px !important;'>
            Join our team of innovators and shape the future together
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 EXPLORE OPEN POSITIONS", key="explore_btn", use_container_width=True):
            st.session_state.selected = "💼 Jobs"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Jobs Page
def jobs_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 38px !important; font-weight: 900 !important; color: #000000 !important; margin-bottom: 35px;'>OPEN POSITIONS</h1>", unsafe_allow_html=True)
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 SEARCH POSITIONS", key="job_search", placeholder="Type job title or skill...")
    with col2:
        department = st.selectbox("DEPARTMENT", ["All", "Research", "Development", "Design", "Marketing", "HR"])
    with col3:
        job_type = st.selectbox("JOB TYPE", ["All", "Full-Time", "Part-Time", "Remote", "Contract"])
    
    jobs = [
        {
            "title": "Senior Research Scientist",
            "department": "Research",
            "type": "Full-Time",
            "experience": "5-8 years",
            "description": "Lead research initiatives in AI and machine learning. Develop innovative solutions for complex problems.",
            "skills": ["Python", "TensorFlow", "PyTorch", "Research"],
            "salary": "₹15-25 LPA"
        },
        {
            "title": "Full Stack Developer",
            "department": "Development",
            "type": "Full-Time",
            "experience": "3-5 years",
            "description": "Build scalable web applications using modern technologies. Work on both frontend and backend.",
            "skills": ["React", "Node.js", "Python", "AWS"],
            "salary": "₹12-20 LPA"
        },
        {
            "title": "UI/UX Designer",
            "department": "Design",
            "type": "Remote",
            "experience": "2-4 years",
            "description": "Create intuitive and beautiful user interfaces. Conduct user research and testing.",
            "skills": ["Figma", "Adobe XD", "User Research", "Prototyping"],
            "salary": "₹8-15 LPA"
        },
        {
            "title": "Data Analyst",
            "department": "Research",
            "type": "Full-Time",
            "experience": "2-5 years",
            "description": "Analyze complex data sets to drive business decisions. Create insightful dashboards and reports.",
            "skills": ["SQL", "Python", "Power BI", "Statistics"],
            "salary": "₹10-18 LPA"
        },
        {
            "title": "Marketing Manager",
            "department": "Marketing",
            "type": "Full-Time",
            "experience": "4-7 years",
            "description": "Develop and execute marketing strategies. Lead brand awareness and growth campaigns.",
            "skills": ["Digital Marketing", "SEO", "Content Strategy", "Analytics"],
            "salary": "₹12-20 LPA"
        },
        {
            "title": "HR Coordinator",
            "department": "HR",
            "type": "Part-Time",
            "experience": "1-3 years",
            "description": "Support HR operations and employee engagement. Manage end-to-end recruitment processes.",
            "skills": ["Recruitment", "Employee Relations", "HRIS"],
            "salary": "₹5-8 LPA"
        }
    ]
    
    # Filter jobs
    filtered_jobs = jobs
    if search:
        filtered_jobs = [j for j in filtered_jobs if search.lower() in j['title'].lower() 
                        or search.lower() in j['description'].lower() 
                        or search.lower() in ' '.join(j['skills']).lower()]
    if department != "All":
        filtered_jobs = [j for j in filtered_jobs if j['department'] == department]
    if job_type != "All":
        filtered_jobs = [j for j in filtered_jobs if j['type'] == job_type]
    
    if len(filtered_jobs) == 0:
        st.warning("⚠️ No jobs found matching your criteria. Try adjusting your filters.")
    
    # Display jobs
    for idx, job in enumerate(filtered_jobs):
        with st.container():
            st.markdown(f"""
            <div class='job-card'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 25px;'>
                    <div style='flex: 2; min-width: 280px;'>
                        <h3 style='font-size: 22px !important; font-weight: 800 !important; 
                                   color: #000000 !important; margin: 0 0 12px 0 !important;'>
                            {job['title']}
                        </h3>
                        <p style='font-size: 16px !important; font-weight: 500 !important; 
                                  color: #374151 !important; margin: 15px 0 !important; line-height: 1.8 !important;'>
                            {job['description']}
                        </p>
                        <div style='margin: 20px 0;'>
                            <span class='badge'>📍 {job['department']}</span>
                            <span class='badge'>⏰ {job['type']}</span>
                            <span class='badge'>💼 {job['experience']}</span>
                            <span class='badge'>💰 {job['salary']}</span>
                        </div>
                    </div>
                    <div style='flex: 1; min-width: 220px; background: #f3f4f6; padding: 20px; 
                                border-radius: 12px; border: 2px solid #d1d5db;'>
                        <p style='font-size: 16px !important; font-weight: 700 !important; 
                                  color: #000000 !important; margin-bottom: 12px !important;'>
                            REQUIRED SKILLS:
                        </p>
                        <p style='font-size: 16px !important; font-weight: 500 !important; 
                                  color: #374151 !important; line-height: 2 !important;'>
                            {'<br>• '.join([''] + job['skills'])}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"APPLY FOR {job['title'].upper()}", key=f"apply_{idx}"):
                st.session_state['apply_position'] = job['title']
                st.session_state.selected = "📝 Apply Now"
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Apply Page
def apply_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 38px !important; font-weight: 900 !important; color: #000000 !important;'>JOB APPLICATION FORM</h1>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 18px !important; font-weight: 700 !important; color: #000000 !important; margin: 20px 0;'>APPLICATION PROGRESS</p>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    
    with st.form("job_application", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("FULL NAME *", placeholder="Enter your full name")
            email = st.text_input("EMAIL ADDRESS *", placeholder="your.email@example.com")
            phone = st.text_input("PHONE NUMBER *", placeholder="+91 98765 43210")
            
        with col2:
            default_position = st.session_state.get('apply_position', 'Select Position')
            positions = ["Select Position", "Senior Research Scientist", "Full Stack Developer",
                        "UI/UX Designer", "Data Analyst", "Marketing Manager", "HR Coordinator"]
            
            default_index = positions.index(default_position) if default_position in positions else 0
                
            position = st.selectbox("POSITION APPLIED FOR *", positions, index=default_index)
            experience = st.number_input("YEARS OF EXPERIENCE *", min_value=0, max_value=30, value=0)
            education = st.selectbox("HIGHEST EDUCATION *", 
                                    ["Select Education", "High School", "Bachelor's Degree", 
                                     "Master's Degree", "PhD", "Other"])
        
        skills = st.text_input("KEY SKILLS * (comma separated)", placeholder="Python, Machine Learning, Data Analysis")
        cover_letter = st.text_area("COVER LETTER", placeholder="Tell us why you're perfect for this role...", height=150)
        
        uploaded_file = st.file_uploader("UPLOAD RESUME (PDF/DOC)", type=['pdf', 'doc', 'docx'])
        
        # Update progress
        fields_completed = sum([bool(full_name), bool(email), bool(phone), 
                               position != "Select Position", experience >= 0, 
                               education != "Select Education", bool(skills)])
        progress = fields_completed / 7
        progress_bar.progress(progress)
        
        submitted = st.form_submit_button("SUBMIT APPLICATION 🚀")
        
        if submitted:
            errors = []
            if not full_name:
                errors.append("FULL NAME is required")
            if not email or not is_valid_email(email):
                errors.append("VALID EMAIL is required")
            if not phone or not is_valid_phone(phone):
                errors.append("VALID PHONE NUMBER is required")
            if position == "Select Position":
                errors.append("Please SELECT A POSITION")
            if education == "Select Education":
                errors.append("Please select EDUCATION LEVEL")
            if not skills:
                errors.append("SKILLS are required")
            
            if errors:
                for error in errors:
                    st.markdown(f"""
                    <div class='error-message'>
                        <strong>❌ {error}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                application_data = {
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'position': position,
                    'experience': experience,
                    'education': education,
                    'skills': skills,
                    'cover_letter': cover_letter
                }
                save_application(application_data)
                
                st.markdown("""
                <div class='success-message'>
                    <h2 style='font-size: 26px !important; font-weight: 800 !important; 
                               color: #ffffff !important; margin: 0 0 15px 0 !important;'>
                        ✅ APPLICATION SUBMITTED SUCCESSFULLY!
                    </h2>
                    <p style='font-size: 18px !important; font-weight: 600 !important; 
                              color: #e5e7eb !important; margin: 12px 0 !important;'>
                        Thank you for your interest in joining Altra Research.
                    </p>
                    <p style='font-size: 17px !important; font-weight: 500 !important; 
                              color: #d1d5db !important; margin: 8px 0 !important;'>
                        We'll review your application and get back to you within 5-7 business days.
                    </p>
                    <p style='font-size: 16px !important; font-weight: 600 !important; 
                              color: #ffffff !important; margin: 8px 0 !important;'>
                        📧 Contact: altraresearch@gmail.com
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                time.sleep(0.5)
                st.snow()
    
    st.markdown("</div>", unsafe_allow_html=True)

# About Page
def about_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 38px !important; font-weight: 900 !important; color: #000000 !important;'>ABOUT ALTRA RESEARCH</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 25px;'>
            <h2 style='font-size: 28px !important; font-weight: 800 !important; 
                       color: #000000 !important;'>OUR STORY</h2>
            <p style='font-size: 18px !important; line-height: 1.9 !important; 
                      color: #111827 !important; font-weight: 500 !important;'>
                Founded in 2015, Altra Research has grown from a small startup in 
                <strong style='color: #000000 !important; font-size: 19px !important; 
                background: #fef08a; padding: 2px 8px; border-radius: 4px;'>
                Eruthoorkadai</strong> to a leading research and development company. 
                Our mission is to push the boundaries of technology and create solutions 
                that make a real difference in people's lives.
            </p>
            
            <h3 style='font-size: 24px !important; font-weight: 800 !important; 
                       color: #000000 !important; margin-top: 35px !important;'>OUR VALUES</h3>
            <ul style='list-style-type: none; padding: 0;'>
                <li style='margin: 18px 0; font-size: 18px !important; font-weight: 600 !important; color: #111827 !important;'>
                    <span style='font-size: 24px;'>🎯</span> 
                    <strong style='color: #000000 !important; font-size: 19px !important;'>INNOVATION</strong> 
                    <span style='color: #374151 !important;'>- We dare to think differently</span>
                </li>
                <li style='margin: 18px 0; font-size: 18px !important; font-weight: 600 !important; color: #111827 !important;'>
                    <span style='font-size: 24px;'>🤝</span> 
                    <strong style='color: #000000 !important; font-size: 19px !important;'>INTEGRITY</strong> 
                    <span style='color: #374151 !important;'>- We do the right thing, always</span>
                </li>
                <li style='margin: 18px 0; font-size: 18px !important; font-weight: 600 !important; color: #111827 !important;'>
                    <span style='font-size: 24px;'>👥</span> 
                    <strong style='color: #000000 !important; font-size: 19px !important;'>COLLABORATION</strong> 
                    <span style='color: #374151 !important;'>- Together we achieve more</span>
                </li>
                <li style='margin: 18px 0; font-size: 18px !important; font-weight: 600 !important; color: #111827 !important;'>
                    <span style='font-size: 24px;'>📈</span> 
                    <strong style='color: #000000 !important; font-size: 19px !important;'>EXCELLENCE</strong> 
                    <span style='color: #374151 !important;'>- We strive for the best in everything</span>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #000000; padding: 35px; border-radius: 15px; 
                    border: 3px solid #000000; margin-top: 20px;'>
            <h2 style='font-size: 28px !important; font-weight: 800 !important; 
                       color: #ffffff !important; margin-bottom: 30px !important;'>
                QUICK FACTS
            </h2>
            <div style='margin: 25px 0;'>
                <h3 style='font-size: 18px !important; font-weight: 700 !important; 
                           color: #ffffff !important;'>📍 LOCATION</h3>
                <p style='font-size: 17px !important; font-weight: 500 !important; 
                          color: #d1d5db !important;'>Eruthoorkadai, Tamil Nadu</p>
            </div>
            <div style='margin: 25px 0;'>
                <h3 style='font-size: 18px !important; font-weight: 700 !important; 
                           color: #ffffff !important;'>👥 TEAM SIZE</h3>
                <p style='font-size: 17px !important; font-weight: 500 !important; 
                          color: #d1d5db !important;'>150+ Employees</p>
            </div>
            <div style='margin: 25px 0;'>
                <h3 style='font-size: 18px !important; font-weight: 700 !important; 
                           color: #ffffff !important;'>🏆 ACHIEVEMENTS</h3>
                <p style='font-size: 17px !important; font-weight: 500 !important; 
                          color: #d1d5db !important;'>Multiple Industry Awards</p>
            </div>
            <div style='margin: 25px 0;'>
                <h3 style='font-size: 18px !important; font-weight: 700 !important; 
                           color: #ffffff !important;'>🌍 GLOBAL PRESENCE</h3>
                <p style='font-size: 17px !important; font-weight: 500 !important; 
                          color: #d1d5db !important;'>Clients in 20+ Countries</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Timeline
    st.markdown("<h2 style='text-align: center; font-size: 30px !important; font-weight: 900 !important; color: #000000 !important; margin: 50px 0 35px;'>OUR JOURNEY</h2>", unsafe_allow_html=True)
    
    timeline = [
        {"year": "2015", "event": "Company Founded in Eruthoorkadai"},
        {"year": "2017", "event": "Reached 50 Employees"},
        {"year": "2019", "event": "Expanded to International Markets"},
        {"year": "2021", "event": "Launched AI Research Division"},
        {"year": "2023", "event": "500+ Projects Completed"},
        {"year": "2024", "event": "Continuing to Innovate and Grow"}
    ]
    
    for item in timeline:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin: 25px 0; padding: 15px; 
                    background: #f9fafb; border-radius: 12px; border-left: 5px solid #000000;'>
            <div class='timeline-year'>
                {item['year']}
            </div>
            <div style='margin-left: 25px; font-size: 18px !important; font-weight: 600 !important; 
                        color: #111827 !important;'>
                {item['event']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Contact Page
def contact_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 38px !important; font-weight: 900 !important; color: #000000 !important;'>CONTACT US</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 25px;'>
            <h2 style='font-size: 28px !important; font-weight: 800 !important; 
                       color: #000000 !important;'>GET IN TOUCH</h2>
            <p style='font-size: 18px !important; line-height: 1.8 !important; 
                      color: #374151 !important; font-weight: 500 !important;'>
                Have questions? We'd love to hear from you. Send us a message 
                and we'll respond as soon as possible.
            </p>
            
            <div style='margin: 35px 0;'>
                <div style='margin: 22px 0; padding: 15px; background: #f3f4f6; 
                            border-radius: 10px; border-left: 4px solid #000000;'>
                    <span style='font-size: 28px;'>📍</span>
                    <strong style='margin-left: 12px; font-size: 18px !important; color: #000000 !important;'>ADDRESS:</strong>
                    <p style='margin-left: 45px; font-size: 17px !important; font-weight: 500 !important; color: #374151 !important;'>
                        123 Research Park, Eruthoorkadai, Tamil Nadu - 627001
                    </p>
                </div>
                <div style='margin: 22px 0; padding: 15px; background: #f3f4f6; 
                            border-radius: 10px; border-left: 4px solid #000000;'>
                    <span style='font-size: 28px;'>📧</span>
                    <strong style='margin-left: 12px; font-size: 18px !important; color: #000000 !important;'>EMAIL:</strong>
                    <p style='margin-left: 45px; font-size: 17px !important; font-weight: 600 !important; color: #1d4ed8 !important;'>
                        altraresearch@gmail.com
                    </p>
                </div>
                <div style='margin: 22px 0; padding: 15px; background: #f3f4f6; 
                            border-radius: 10px; border-left: 4px solid #000000;'>
                    <span style='font-size: 28px;'>📞</span>
                    <strong style='margin-left: 12px; font-size: 18px !important; color: #000000 !important;'>PHONE:</strong>
                    <p style='margin-left: 45px; font-size: 17px !important; font-weight: 500 !important; color: #374151 !important;'>
                        +91 98765 43210
                    </p>
                </div>
                <div style='margin: 22px 0; padding: 15px; background: #f3f4f6; 
                            border-radius: 10px; border-left: 4px solid #000000;'>
                    <span style='font-size: 28px;'>🕐</span>
                    <strong style='margin-left: 12px; font-size: 18px !important; color: #000000 !important;'>WORKING HOURS:</strong>
                    <p style='margin-left: 45px; font-size: 17px !important; font-weight: 500 !important; color: #374151 !important;'>
                        Monday - Friday: 9:00 AM - 6:00 PM
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("contact_form"):
            st.markdown("<h3 style='font-size: 24px !important; font-weight: 800 !important; color: #000000 !important;'>SEND US A MESSAGE</h3>", unsafe_allow_html=True)
            
            name = st.text_input("YOUR NAME *", placeholder="Enter your name")
            email = st.text_input("YOUR EMAIL *", placeholder="your.email@example.com")
            subject = st.text_input("SUBJECT", placeholder="What's this about?")
            message = st.text_area("YOUR MESSAGE *", height=150, placeholder="Type your message here...")
            
            submitted = st.form_submit_button("SEND MESSAGE 📨")
            
            if submitted:
                if name and email and message:
                    if is_valid_email(email):
                        conn = sqlite3.connect('altra_research.db')
                        c = conn.cursor()
                        c.execute('''INSERT INTO messages (name, email, subject, message, date)
                                    VALUES (?, ?, ?, ?, ?)''',
                                 (name, email, subject, message, datetime.now()))
                        conn.commit()
                        conn.close()
                        
                        st.markdown("""
                        <div class='success-message'>
                            <h3 style='font-size: 22px !important; font-weight: 800 !important; 
                                       color: #ffffff !important;'>✅ MESSAGE SENT SUCCESSFULLY!</h3>
                            <p style='font-size: 17px !important; font-weight: 600 !important; 
                                      color: #e5e7eb !important;'>
                                Thank you for reaching out. We'll get back to you within 24 hours.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.markdown("""
                        <div class='error-message'>
                            <strong>❌ Please enter a VALID EMAIL address.</strong>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='error-message'>
                        <strong>❌ Please fill in ALL REQUIRED FIELDS.</strong>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Map
    st.markdown("""
    <div style='text-align: center; margin: 35px 0; padding: 45px; 
                background: #f3f4f6; border-radius: 15px; border: 3px dashed #6b7280;'>
        <h3 style='font-size: 22px !important; font-weight: 800 !important; color: #000000 !important;'>
            📍 OUR LOCATION
        </h3>
        <p style='font-size: 19px !important; font-weight: 600 !important; color: #374151 !important;'>
            <strong>Eruthoorkadai, Tamil Nadu</strong>
        </p>
        <p style='font-size: 16px !important; font-weight: 500 !important; color: #6b7280 !important;'>
            [Interactive Map Coming Soon]
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()