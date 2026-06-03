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
# CSS STYLING
# ═══════════════════════════════════════════════
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Poppins:wght@600;700;800;900&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    }
    
    /* All text in main area */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #1e293b !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: #0f172a !important;
    }
    
    /* Cards and containers */
    .stContainer {
        background: #ffffff;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 14px 30px !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(79,70,229,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(79,70,229,0.5) !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 2px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 12px 15px !important;
        font-size: 16px !important;
        color: #0f172a !important;
        background: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
    }
    
    /* Labels */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        font-weight: 700 !important;
        color: #334155 !important;
        font-size: 15px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a, #1a1040) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
    }
    
    /* Success messages */
    .stSuccess {
        background: #059669 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    /* Error messages */
    .stError {
        background: #dc2626 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    /* Info messages */
    .stInfo {
        background: #f8fafc !important;
        border-left: 4px solid #4f46e5 !important;
    }
    
    /* Expander */
    .stExpander {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
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
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔬 ALTRA RESEARCH")
        st.markdown("*Innovation Meets Excellence*")
        st.divider()
        
        selected = option_menu(
            menu_title=None,
            options=["🏠 Home", "💼 Jobs", "📝 Apply Now", "ℹ️ About Us", "📧 Contact"],
            icons=["house", "briefcase", "pencil-square", "info-circle", "envelope"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background": "transparent"},
                "icon": {"font-size": "16px"},
                "nav-link": {"font-size": "15px", "padding": "12px", "border-radius": "10px", "margin": "5px 0"},
                "nav-link-selected": {"background": "rgba(79,70,229,0.5)", "font-weight": "700"},
            }
        )
        
        st.divider()
        st.markdown("📍 **Eruthoorkadai**")
        st.markdown("📧 altraresearch@gmail.com")
        st.markdown("📞 +91 98765 43210")
    
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

# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
def home_page():
    # Hero Section
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 🚀 WE ARE HIRING!")
        st.markdown("# Build The Future With Altra Research")
        st.markdown("Join a team of passionate innovators shaping tomorrow's technology in Eruthoorkadai.")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 EXPLORE CAREERS", use_container_width=True, key="home_careers"):
                st.session_state.selected = "💼 Jobs"
                st.rerun()
        with c2:
            if st.button("📝 APPLY NOW", use_container_width=True, key="home_apply"):
                st.session_state.selected = "📝 Apply Now"
                st.rerun()
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f8fafc, #e0e7ff); 
                    border-radius: 20px; padding: 40px 20px; text-align: center; 
                    border: 2px solid #e2e8f0;'>
            <div style='font-size: 100px;'>🏢</div>
            <h3 style='color: #0f172a !important;'>Your Dream Career Awaits</h3>
            <p style='color: #475569 !important;'>500+ Projects | 150+ Team | 50+ Roles</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Stats
    st.markdown("## Our Impact")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        with st.container():
            st.metric("Projects", "500+", "Completed")
    with c2:
        with st.container():
            st.metric("Team", "150+", "Members")
    with c3:
        with st.container():
            st.metric("Positions", "50+", "Open")
    with c4:
        with st.container():
            st.metric("Countries", "20+", "Global")
    
    st.divider()
    
    # Features
    st.markdown("## Why Join Altra Research?")
    
    features = [
        {"icon": "🚀", "title": "Innovation First", "desc": "Work on cutting-edge projects that push technology boundaries."},
        {"icon": "📈", "title": "Career Growth", "desc": "Clear advancement paths with mentorship and learning."},
        {"icon": "🤝", "title": "Great Culture", "desc": "Inclusive, collaborative environment where you belong."},
        {"icon": "💎", "title": "Top Benefits", "desc": "Competitive salary, insurance, and performance bonuses."},
        {"icon": "🌍", "title": "Global Impact", "desc": "Your work impacts users across 20+ countries."},
        {"icon": "⚖️", "title": "Work Balance", "desc": "Flexible hours and remote options for your lifestyle."}
    ]
    
    cols = st.columns(3)
    for idx, f in enumerate(features):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"### {f['icon']}")
                st.markdown(f"**{f['title']}**")
                st.markdown(f"{f['desc']}")
    
    st.divider()
    
    # CTA
    st.markdown("## Ready to Make History?")
    st.markdown("Join us and be part of something extraordinary.")
    if st.button("🔥 VIEW ALL OPEN POSITIONS", use_container_width=True, key="cta"):
        st.session_state.selected = "💼 Jobs"
        st.rerun()

# ═══════════════════════════════════════════════
# JOBS PAGE
# ═══════════════════════════════════════════════
def jobs_page():
    st.markdown("## 💼 Open Positions")
    st.markdown("Find your perfect role at Altra Research")
    
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
        with st.container():
            st.markdown(f"### {job['title']}")
            st.markdown(f"**Altra Research • Eruthoorkadai**")
            st.markdown(job['desc'])
            
            st.markdown(f"📍 {job['dept']} | ⏰ {job['type']} | 💼 {job['exp']} | 💰 {job['salary']}")
            st.markdown(f"**Skills:** {job['skills']}")
            
            if st.button(f"Apply for {job['title']}", key=f"apply_{idx}"):
                st.session_state['apply_position'] = job['title']
                st.session_state.selected = "📝 Apply Now"
                st.rerun()
            
            st.divider()

# ═══════════════════════════════════════════════
# APPLY PAGE
# ═══════════════════════════════════════════════
def apply_page():
    st.markdown("## 📝 Job Application")
    st.markdown("Take the first step toward an amazing career")
    
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
        
        skills = st.text_input("Key Skills * (comma separated)", placeholder="Python, React, SQL...")
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
                st.markdown("Thank you for applying to **Altra Research**. We'll respond within 5-7 business days.")
                st.markdown("📧 Contact: altraresearch@gmail.com")
                st.balloons()

# ═══════════════════════════════════════════════
# ABOUT PAGE
# ═══════════════════════════════════════════════
def about_page():
    st.markdown("## ℹ️ About Altra Research")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Our Journey")
        st.markdown("""
        Founded in **2015** in **Eruthoorkadai**, Altra Research has grown from a small startup 
        to a leading research and development company with 150+ brilliant minds.
        """)
        
        st.markdown("### 💎 Our Values")
        st.markdown("🎯 **Innovation** — We challenge conventions")
        st.markdown("🤝 **Integrity** — We do what's right")
        st.markdown("👥 **Collaboration** — Together we achieve more")
        st.markdown("⭐ **Excellence** — We strive for greatness")
    
    with col2:
        st.markdown("### 📊 Quick Facts")
        st.info("📍 **Location:** Eruthoorkadai, Tamil Nadu")
        st.info("👥 **Team:** 150+ Employees")
        st.info("🏆 **Awards:** Multiple Industry Awards")
        st.info("🌍 **Reach:** 20+ Countries")
    
    st.markdown("### 📅 Our Timeline")
    
    timeline = [
        ("2015", "Founded in Eruthoorkadai"),
        ("2017", "Grew to 50+ employees"),
        ("2019", "Expanded internationally"),
        ("2021", "Launched AI Research Division"),
        ("2023", "500+ projects delivered"),
        ("2025", "150+ employees and growing")
    ]
    
    for year, event in timeline:
        st.markdown(f"**{year}** — {event}")

# ═══════════════════════════════════════════════
# CONTACT PAGE
# ═══════════════════════════════════════════════
def contact_page():
    st.markdown("## 📧 Contact Us")
    st.markdown("We'd love to hear from you!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Reach Us")
        st.markdown("📍 **Address:** 123 Research Park, Eruthoorkadai, Tamil Nadu - 627001")
        st.markdown("📧 **Email:** altraresearch@gmail.com")
        st.markdown("📞 **Phone:** +91 98765 43210")
        st.markdown("🕐 **Hours:** Mon-Fri, 9 AM - 6 PM")
    
    with col2:
        st.markdown("### 💬 Send Message")
        with st.form("contact"):
            name = st.text_input("Name *")
            email = st.text_input("Email *")
            subject = st.text_input("Subject")
            message = st.text_area("Message *", height=150)
            
            if st.form_submit_button("📨 Send"):
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
                        st.error("❌ Invalid email")
                else:
                    st.error("❌ Fill all required fields")

# ═══════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    main()