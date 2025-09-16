from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .forms import LoginForm, SignupForm
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging

# Define a blueprint for the website
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and check_password_hash(user.password, form.password.data):
                if not user.is_active:
                    flash('Account is deactivated. Please contact support.', category='error')
                    return render_template("login.html", form=form, user=current_user)
                
                # Update last login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                login_user(user, remember=form.remember_me.data)
                flash('Logged in successfully!', category='success')
                
                # Redirect to next page if specified
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash('Invalid email or password.', category='error')
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', category='error')
    
    return render_template("login.html", form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = SignupForm()
    
    if form.validate_on_submit():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already exists. Please use a different email.', category='error')
                return render_template("sign_up.html", form=form, user=current_user)
            
            # Create new user
            new_user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=generate_password_hash(form.password.data, method='pbkdf2:sha256')
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', category='success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            logging.error(f"Signup error: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', category='error')
    
    return render_template("sign_up.html", form=form, user=current_user)