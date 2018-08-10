from flask import render_template, Blueprint
from recipebox.models import Recipe

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	recipes = Recipe.query.all()
	return render_template("home.html", recipes=recipes)

@main.route('/about')
def about():
	return render_template("about.html", title="About")