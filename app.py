from flask import Flask, render_template, redirect, session, request,url_for, flash, abort, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager,  login_user, login_required, current_user, UserMixin, logout_user
import os, json
from datetime import date, datetime
import pandas as pd
import numpy as np
from zoneinfo import ZoneInfo

# Fetch the exact time specifically for India
local_time = datetime.now(ZoneInfo("Asia/Kolkata"))

app  = Flask(__name__)

app.config['SECRET_KEY'] = 'pro_secret_key_99' 

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'pro_secret_key_99')

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
login_manager.login_view = 'home'


#Migrate Procedure
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Stack Holder Details 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))



@login_manager.user_loader
def load_user(user_id):
    # Flask-Login sessions store IDs as strings, so we convert to int
    uid = int(user_id)
    
    user = User.query.get(uid)
    if user:
        return user
    
    return None


@app.route('/')
def home() :
    logout_user()
    return render_template('home.html')






# Logout Process
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='user').first():
        db.session.add(User(username='user', password='user123'))
        db.session.commit()
    
if __name__ == '__main__' :
    app.run(debug=True)