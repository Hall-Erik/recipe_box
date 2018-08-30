from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from recipebox import db, login_manager
from flask_login import UserMixin

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

	made_recipes = db.relationship('Recipe', secondary=made_recipes, backref='users')

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

	def get_image_url(self):
		if self.image_file == 'default.png':
			return url_for('static', filename='img/' + self.image_file)
		else:
			return self.image_file

	def __repr__(self):
		return f"Recipe('{self.title}', '{self.date_posted}')"
