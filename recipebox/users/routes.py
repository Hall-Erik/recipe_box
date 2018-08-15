from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from recipebox import db, bcrypt
from recipebox.models import User
from recipebox.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
									RequestResetForm, ResetPasswordForm)
from recipebox.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created. You can now login.', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/register.html', title="Register", form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		flash('Login unsuccessful. Please check email and password.', 'danger')
	return render_template('users/login.html', title="Login", form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture = save_picture(form.picture.data)
			current_user.image_file = picture
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your account has been updated!", 'success')
		return redirect(url_for('users.account'))
	form.username.data = current_user.username
	form.email.data = current_user.email
	profile_pic = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('users/account.html', title='Account', form=form, profile_pic=profile_pic)

@users.route('/users/<int:user_id>/recipes')
def user_recipes(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('home.html', title=f"{user.username}'s recipes", recipes=user.recipes)

@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('users/reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('This is an invalid token.', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pw
		db.session.commit()
		flash('Your password has been updated!', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/reset_token.html', title='Reset Password', form=form)