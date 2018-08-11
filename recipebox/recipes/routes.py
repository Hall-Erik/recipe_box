from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from recipebox import db
from recipebox.recipes.forms import CreateRecipeForm
from recipebox.models import Recipe, Ingredient, Direction

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes/new', methods=['POST', 'GET'])
@login_required
def create_recipe():
	form = CreateRecipeForm()
	if form.validate_on_submit():
		recipe = Recipe(title=form.title.data, description=form.description.data, user_id=current_user.id)
		db.session.add(recipe)
		db.session.commit()
		
		for ingredient in form.ingredients:
			i = Ingredient(content=ingredient.data, recipe=recipe)
			db.session.add(i)
			db.session.commit()

		for direction in form.directions:
			d = Direction(content=direction.data, recipe=recipe)
			db.session.add(d)
			db.session.commit()
		
		flash('Your recipe has been added!', 'success')
		return redirect(url_for('main.home'))
	print(form.errors)
	return render_template('recipes/create_recipe.html', title="Create Recipe", form=form)
