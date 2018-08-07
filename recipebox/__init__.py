from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from recipebox.config import Config

# db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	# db.init_app(app)

	# from recipebox.users.routes import users
	# from recipebox.recipes.routes import recipes
	from recipebox.main.routes import main
	# from recipebox.errors.handlers import errors

	# app.register_blueprint(users)
	# app.register_blueprint(recipes)
	app.register_blueprint(main)
	# app.register_blueprint(errors)

	return app
