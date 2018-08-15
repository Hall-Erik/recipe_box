from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from recipebox.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(max=20)])
	email = StringField('Email',
							validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username already exists. Please try another.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('There is already a user associated with that email. Please try again.')

class LoginForm(FlaskForm):
	email = StringField('Email',
							validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign Up')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', 
							validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update Account')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user and user != current_user:
			raise ValidationError('That username already exists. Please try another.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user and user != current_user:
			raise ValidationError('There is already a user associated with that email. Please try again.')

class UpdatePasswordForm(FlaskForm):
	old_password = PasswordField('Current Password', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Change Password')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no email associated with that email.')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Change Password')