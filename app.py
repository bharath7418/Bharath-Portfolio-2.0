import os
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, render_template, redirect, session, request, url_for, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'pro_secret_key_99_bharath')

# Database configuration (handles Postgres for production & SQLite for Vercel/Local)
raw_db_url = os.getenv('DATABASE_URL')
use_tmp_sqlite = os.getenv('VERCEL') == '1'

if raw_db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url.replace("postgres://", "postgresql://", 1)
elif use_tmp_sqlite:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message_category = 'info'

# --- DATABASE MODELS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Hashed password storage

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    title = db.Column(db.String(150), nullable=False)
    problem_statement = db.Column(db.String(400), default=None)
    description = db.Column(db.Text, nullable=False)
    tools = db.Column(db.String(100))
    filename1 = db.Column(db.String(100))
    filename2 = db.Column(db.String(100))
    filename3 = db.Column(db.String(100))
    filename4 = db.Column(db.String(100))
    solution = db.Column(db.String(200))
    project_link = db.Column(db.String(200),default=None)
    project_report = db.Column(db.String(200),default=None)
    insta_link = db.Column(db.String(200),default=None)
    youtube_link = db.Column(db.String(200),default=None)
    feedback = db.Column(db.String(200),default=None)

    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False, default='code')

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- PUBLIC ROUTING ---

@app.route('/')
def home():
    # Pass major projects to display in the hero/featured section
    major_projects = Project.query.filter_by(project_type='Major').limit(3).all()
    return render_template('home.html', projects=major_projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    major_projects = Project.query.filter_by(project_type='Major').all()
    return render_template('projects.html', projects=major_projects)

@app.route('/miniprojects')
def miniprojects():
    mini_projects = Project.query.filter_by(project_type='Mini').all()
    return render_template('miniprojects.html', projects=mini_projects)

@app.route('/services')
def services():
    all_services = Service.query.all()
    return render_template('services.html', services=all_services)

@app.route('/blogs')
def blogs():
    all_blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('blogs.html', blogs=all_blogs)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for reaching out, Bharath will respond shortly!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# --- AUTHENTICATION & ADMIN PATHS ---

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Admin authentication successful.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid administrative credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out cleanly.', 'info')
    return redirect(url_for('home'))

# --- CRUD OPERATIONS FOR PROJECTS ---

@app.route('/admin')
@login_required
def admin_dashboard():
    all_projects = Project.query.all()
    return render_template('admin.html', projects=all_projects)

@app.route('/admin/project/add', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    tech_stack = request.form.get('tech_stack')
    project_type = request.form.get('project_type', 'Major')
    link = request.form.get('link')
    
    new_project = Project(title=title, description=description, tech_stack=tech_stack, project_type=project_type, link=link)
    db.session.add(new_project)
    db.session.commit()
    flash('Project added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/project/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/service/add', methods=['POST'])
@login_required
def add_service():
    title = request.form.get('title')
    description = request.form.get('description')
    icon = request.form.get('icon', 'code')
    
    new_service = Service(title=title, description=description, icon=icon)
    db.session.add(new_service)
    db.session.commit()
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/blog/add', methods=['POST'])
@login_required
def add_blog():
    title = request.form.get('title')
    content = request.form.get('content')
    
    new_blog = Blog(title=title, content=content, date_posted=datetime.utcnow())
    db.session.add(new_blog)
    db.session.commit()
    flash('Blog posted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# --- DATABASE SEEDING ---
with app.app_context():
    db.create_all()
    # Check if admin configuration exists; if not, provision default securely.
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('user123')
        db.session.add(User(username='admin', password=hashed_password))
        db.session.commit()
        
    # Check if Project table is empty; if so, populate with user's projects
    if not Project.query.first():
        project = Project(
            name="COPACK",
            title="Student Compiler & Placement Platform",
            tools="Flask, HTML, CSS, JS",
            problem_statement="Lorem100 Lorem ipsum dolor sit amet consectetur adipisicing elit...",
            description="Developed a scalable platform to manage coding tests and automate performance tracking for 700+ users. Engineered secure anti-cheating features and streamlined the evaluation workflow to eliminate manual code sharing.",
            filename1=r"D:\Projects\Bharath Portfolio 2.0\uploads\filename (1).jpg",
            filename2=r"D:\Projects\Bharath Portfolio 2.0\uploads\filename (2).jpg",
            filename3=r"D:\Projects\Bharath Portfolio 2.0\uploads\filename (3).jpg",
            filename4=r"D:\Projects\Bharath Portfolio 2.0\uploads\filename (4).jpg",
            solution="Lorem ipsum dolor sit amet consectetur adipisicing elit...",
            project_link="Lorem ipsum dolor sit amet consectetur adipisicing elit.",
            project_report="Lorem aksjdfkjfkjdskfjk fjfklsdjfkdjfk dfkjdkfjkjfak fjdkfjakjfkdfkas kfjkdf ajfkjd",
            insta_link="aksjdfkjkdsjfkf fkajskdf",
            youtube_link="sjakfjkjfksajdfkljffasf",
            feedback="akjdk kdj akjsdaf ksjafkj jaksdjf"
        )
        db.session.add(project)
        db.session.commit()

    # Check if Service table is empty; if so, populate with default services
    if not Service.query.first():
        seeded_services = [
            Service(
                title="Full Stack Core Deployments",
                description="Responsive Python/Flask backends engineered against custom relational database schemes.",
                icon="layer-group"
            ),
            Service(
                title="AI & Data Pipeline Processing",
                description="Implementing structural analytics maps with NumPy, Pandas, and structured ML patterns.",
                icon="chart-line"
            ),
            Service(
                title="Graphic Design & Print Workflows",
                description="Leveraging digital assets creation with Photoshop and CorelDRAW for high-quality production deliverables.",
                icon="print"
            )
        ]
        db.session.bulk_save_objects(seeded_services)
        db.session.commit()

    # Check if Blog table is empty; if so, populate with default blogs
    if not Blog.query.first():
        seeded_blogs = [
            Blog(
                title="Welcome to My Engineering Portfolio",
                content="This digital portfolio is built utilizing Python, Flask, SQLite, and SQLAlchemy. It showcases my professional experience, key engineering projects, academic background, and leadership achievements. You can log into the administrative control panel to add, edit, or delete items in real-time.",
                date_posted=datetime.utcnow()
            )
        ]
        db.session.bulk_save_objects(seeded_blogs)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)