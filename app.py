from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

app = Flask(__name__)

# Configuration
import os as os_module
app.config['SECRET_KEY'] = os_module.environ.get('SECRET_KEY', 'altra-research-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///altra_research.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('JobApplication', backref='applicant', lazy=True)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    resume_filename = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)
    portfolio_link = db.Column(db.String(200))
    linkedin_profile = db.Column(db.String(200))
    github_profile = db.Column(db.String(200))
    additional_docs = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', company_name='Altra Research')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            phone=phone
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', company_name='Altra Research')

@app.route('/dashboard')
@login_required
def dashboard():
    positions = [
        {'title': 'Senior Research Scientist', 'department': 'R&D', 'location': 'Hybrid'},
        {'title': 'Data Analyst', 'department': 'Analytics', 'location': 'Remote'},
        {'title': 'Software Engineer', 'department': 'IT', 'location': 'On-site'},
        {'title': 'Project Manager', 'department': 'Operations', 'location': 'Hybrid'},
        {'title': 'Lab Technician', 'department': 'Research', 'location': 'On-site'},
    ]
    return render_template('dashboard.html', company_name='Altra Research', positions=positions)

@app.route('/apply/<position>', methods=['GET', 'POST'])
@login_required
def apply(position):
    if request.method == 'POST':
        resume = request.files.get('resume')
        additional_docs = request.files.get('additional_docs')
        
        resume_filename = None
        additional_docs_filename = None
        
        if resume:
            resume_filename = secure_filename(f"{uuid.uuid4()}_{resume.filename}")
            resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))
        
        if additional_docs:
            additional_docs_filename = secure_filename(f"{uuid.uuid4()}_{additional_docs.filename}")
            additional_docs.save(os.path.join(app.config['UPLOAD_FOLDER'], additional_docs_filename))
        
        application = JobApplication(
            position=position,
            resume_filename=resume_filename,
            cover_letter=request.form.get('cover_letter'),
            portfolio_link=request.form.get('portfolio_link'),
            linkedin_profile=request.form.get('linkedin_profile'),
            github_profile=request.form.get('github_profile'),
            additional_docs=additional_docs_filename,
            user_id=current_user.id
        )
        db.session.add(application)
        db.session.commit()
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('apply.html', company_name='Altra Research', position=position)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = ContactMessage(
            name=request.form.get('name'),
            email=request.form.get('email'),
            subject=request.form.get('subject'),
            message=request.form.get('message')
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', company_name='Altra Research')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)