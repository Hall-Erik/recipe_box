from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for, render_template
from flask_mail import Message
from flask_login import UserMixin
from recipebox import db, login_manager, bcrypt, mail

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

made_recipes = db.Table('made_recipes',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(100), nullable=False, default='default_profile.jpg')
	password = db.Column(db.String(60), nullable=False)
	
	recipes = db.relationship('Recipe', backref='author', lazy=True)
	comments = db.relationship('Comment', backref='author', lazy=True)

	made_recipes = db.relationship('Recipe', secondary=made_recipes, backref='users')

	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password).decode('utf-8')

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)

	def made_this(self, recipe):
		return True if recipe in self.made_recipes else False

	def get_image_url(self):
		if self.image_file == 'default_profile.jpg':
			return url_for('static', filename='img/' + self.image_file)
		else:
			return self.image_file

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def send_reset_email(self):
		token = self.get_reset_token()
		msg = Message('Password Reset Request Do Not Reply',
			sender='noreply@recipebox.com',
			recipients=[self.email])
		msg.body = render_template(
			'email/reset_password.txt',
			user=self,
			token=token
		)
		mail.send(msg)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Recipe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text)
	cook_time = db.Column(db.String(4))
	servings = db.Column(db.String(10))
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	image_file = db.Column(db.String(100), nullable=False, default='default.png')
	directions = db.Column(db.Text)
	ingredients = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	comments = db.relationship('Comment', backref='recipe', lazy=True)

	def get_image_url(self):
		if self.image_file == 'default.png':
			return url_for('static', filename='img/' + self.image_file)
		else:
			return self.image_file

	def __repr__(self):
		return f"Recipe('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'body': self.body,
			'date_posted': self.date_posted.strftime('%b %e, %Y'),
			'author': {
				'name':	self.author.username,
				'image': self.author.get_image_url()
			}
		}

	def __repr__(self):
		return f"Comment('{self.body}', '{self.date_posted}')"